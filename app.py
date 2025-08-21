import streamlit as st
import plotly.express as px
import pandas as pd
import pdfplumber

# Import all our backend modules
from src.advanced_bias_analyzer import AdvancedBiasAnalyzer, StatisticalAnalyzer
from src.quality_assessor import QualityAssessor
from src.citation_analyzer import CitationAnalyzer

def generate_suggestions(results):
    """Generates improvement suggestions based on analysis results."""
    suggestions = []
    if results['bias_scores'][results['bias_types'].index('Confirmation Bias')] > 0:
        suggestions.append("Consider rephrasing statements that strongly confirm pre-existing beliefs to maintain objectivity.")
    if not results['quality_details']['data_availability']:
        suggestions.append("Add a data availability statement to improve transparency and reproducibility.")
    if not results['quality_details']['code_availability']:
        suggestions.append("Consider publishing your analysis code in a public repository.")
    if results['quality_details']['methodology_strength'] < 0.5:
        suggestions.append("Strengthen the methodology section by detailing the experimental design (e.g., control groups, randomization, blinding). ")
    if results['p_hacking_suspected']:
        suggestions.append("Review the statistical analysis for potential p-hacking. Ensure a clear distinction between exploratory and confirmatory analysis.")
    return suggestions

def analyze_paper(uploaded_file):
    """Main function to orchestrate the analysis of the uploaded paper."""
    # 1. Extract text from PDF
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # Debug: Check if text was extracted
        if len(text.strip()) == 0:
            st.error("No text could be extracted from the PDF. The file might be image-based or corrupted.")
            return None
            
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

    # 2. Instantiate all analyzers
    bias_analyzer = AdvancedBiasAnalyzer()
    stat_analyzer = StatisticalAnalyzer()
    quality_assessor = QualityAssessor()
    citation_analyzer = CitationAnalyzer() # Note: This will use its internal sample data

    # 3. Run all analyses
    # Bias analysis
    detected_biases = bias_analyzer.linguistic_pattern_detector(text)
    bias_scores = [1 if b in detected_biases else 0 for b in bias_analyzer.bias_patterns.keys()]
    
    # Statistical analysis
    p_values = stat_analyzer.extract_p_values(text)
    p_hacking_suspected = stat_analyzer.detect_p_hacking(p_values)
    
    # Quality score
    quality_score, quality_details = quality_assessor.calculate_unified_quality_score(text)

    # 4. Collate results
    results = {
        'text': text,
        'bias_types': list(bias_analyzer.bias_patterns.keys()),
        'bias_scores': bias_scores,
        'quality_score': quality_score * 10, # Scale to 0-10
        'quality_details': quality_details,
        'p_hacking_suspected': p_hacking_suspected,
    }

    # 5. Generate suggestions
    results['suggestions'] = generate_suggestions(results)

    return results

def main():
    st.set_page_config(layout="wide")
    st.title("AI-Powered Academic Paper Bias Detection & Quality Assessment System")

    st.sidebar.title("Controls")
    uploaded_file = st.sidebar.file_uploader("Upload Academic Paper (PDF)", type="pdf")

    if uploaded_file:
        # Process paper
        with st.spinner("Analyzing paper... This may take a moment."):
            results = analyze_paper(uploaded_file)
            
        if results:
            st.header("Analysis Dashboard")
        else:
            st.error("Analysis failed. Please check the file and try again.")
            return
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Bias Detection Results")
            bias_df = pd.DataFrame({'Bias Type': results['bias_types'], 'Detected': results['bias_scores']})
            bias_chart = px.bar(bias_df, x='Bias Type', y='Detected', title="Detected Linguistic Biases", color='Detected',
                                color_continuous_scale=px.colors.sequential.Reds)
            st.plotly_chart(bias_chart, use_container_width=True)

        with col2:
            st.subheader("Overall Quality Score")
            st.metric("Quality Score", f"{results['quality_score']:.2f}/10")
            st.progress(results['quality_score'] / 10)
            with st.expander("See Quality Details"):
                st.write(results['quality_details'])

        st.subheader("Improvement Suggestions")
        for suggestion in results['suggestions']:
            st.success(f"• {suggestion}")
        
        st.subheader("Full Paper Text")
        with st.expander("Click to view full text"):
            st.text_area("Paper Text", results['text'], height=300, label_visibility="collapsed")

    else:
        st.info("Upload a PDF file to begin analysis.")

if __name__ == "__main__":
    main()
