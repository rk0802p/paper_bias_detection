# AI-Powered Academic Paper Bias Detection & Quality Assessment System

This project is an AI-powered system that analyzes academic papers for multiple types of bias while providing quality scores and improvement suggestions. The system combines natural language processing with rule-based analysis to provide a comprehensive assessment of academic work.

---

## Features

- **Multi-Type Bias Detection**: Identifies linguistic patterns related to confirmation bias, selection bias, and more.
- **Statistical Sanity Checks**: Scans for p-values and flags potential p-hacking.
- **Methodology Validation**: Checks for keywords related to robust experimental design (e.g., control groups, blinding).
- **RipetaScore-Inspired Quality Metrics**: Scores papers on transparency and reproducibility by checking for data and code availability statements.
- **Unified Scoring System**: Combines multiple metrics into a single, easy-to-understand quality score.
- **Interactive Web Interface**: An easy-to-use Streamlit application for uploading and analyzing papers.

---

## Project Structure

```
/paper-bias-detection
|-- app.py                    # Main Streamlit web application
|-- requirements.txt          # Project dependencies
|-- Dockerfile                # For containerized deployment
|-- /src                      # Backend source code
|   |-- bias_detector_model.py  # Deep learning model (DistilBERT)
|   |-- traditional_models.py   # TF-IDF and rule-based models
|   |-- advanced_bias_analyzer.py # Advanced pattern and statistical analysis
|   |-- citation_analyzer.py    # Citation network analysis
|   |-- quality_assessor.py     # Quality scoring engine
|   |-- ...
|-- /data
|   |-- /annotated            # Sample annotated data
|-- /docs
|   |-- annotation_guidelines.md # Guidelines for bias annotation
|-- /tests
|   |-- test_quality_assessor.py # Sample unit tests
```

---

## How to Run

1.  **Set up the Environment**:
    - Make sure you have Python 3.8+ installed.
    - Create and activate a virtual environment:
      ```bash
      python -m venv venv
      # On Windows:
      venv\Scripts\activate
      # On macOS/Linux:
      source venv/bin/activate
      ```

2.  **Install Dependencies**:
    - Install all required packages from `requirements.txt`:
      ```bash
      pip install -r requirements.txt
      ```

3.  **Run the Application**:
    - Launch the Streamlit app:
      ```bash
      streamlit run app.py
      ```
    - Your web browser should open with the application running.

4.  **Using the App**:
    - Click the "Upload Academic Paper (PDF)" button in the sidebar.
    - Select a PDF file from your local machine.
    - The system will analyze the paper and display the bias and quality dashboard.
