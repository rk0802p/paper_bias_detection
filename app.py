import streamlit as st
import pandas as pd
import pdfplumber

from src.plagiarism_checker import analyze_plagiarism


def extract_pdf_text(uploaded_file) -> str:
	"""Extract text with fallback that reconstructs words when spacing is broken."""
	text = ""
	with pdfplumber.open(uploaded_file) as pdf:
		for page in pdf.pages:
			page_text = page.extract_text() or ""
			# Fallback: rebuild from word boxes if too sparse
			if len(page_text.strip()) < 80:
				try:
					words = page.extract_words()
					if words:
						page_text = " ".join(w.get("text", "") for w in words)
				except Exception:
					pass
			if page_text:
				text += page_text + "\n"
	return text


def main():
	st.set_page_config(layout="wide")
	st.title("Research Paper Plagiarism & Similarity Analysis")

	st.sidebar.title("Controls")
	uploaded_file = st.sidebar.file_uploader("Upload Academic Paper (PDF)", type="pdf")

	if uploaded_file:
		with st.spinner("Reading PDF..."):
			full_text = extract_pdf_text(uploaded_file)
			if not full_text.strip():
				st.error("Could not extract text from PDF. The file may be image-based.")
				return

		with st.spinner("Analyzing sections for similarity (via Semantic Scholar)..."):
			report = analyze_plagiarism(full_text)

		st.subheader("Overall Similarity")
		st.metric("Overall Similarity", f"{report['overall_percent']:.2f}%", help=report["overall_category"])
		st.caption(report["overall_category"])

		st.subheader("Section-wise Results")
		for section_name in ["Title", "Abstract", "Methodology", "Conclusions"]:
			sec = report["sections"][section_name]
			st.markdown(f"**{section_name}** — {sec['best_similarity_percent']:.2f}% ({sec['category']})")
			if sec["matches"]:
				links_df = pd.DataFrame(sec["matches"])  # columns: percent,title,url
				st.dataframe(links_df, use_container_width=True)
			else:
				st.info("No close matches found for this section.")

		st.divider()
		st.caption("Similarity is computed using TF-IDF cosine similarity between your section text and titles/abstracts returned by Semantic Scholar. This is an approximate signal and not a legal plagiarism determination.")
	else:
		st.info("Upload a PDF file to begin analysis.")


if __name__ == "__main__":
	main()
