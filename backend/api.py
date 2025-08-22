from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pdfplumber
import io

from src.plagiarism_checker import analyze_plagiarism

app = FastAPI(title="Paper Similarity API")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


def extract_pdf_text_from_bytes(data: bytes) -> str:
	text = ""
	with pdfplumber.open(io.BytesIO(data)) as pdf:
		for page in pdf.pages:
			page_text = page.extract_text() or ""
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


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
	try:
		data = await file.read()
		full_text = extract_pdf_text_from_bytes(data)
		if not full_text.strip():
			return JSONResponse(status_code=400, content={"error": "No text extracted from PDF"})
		report = analyze_plagiarism(full_text)
		return report
	except Exception as e:
		return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/health")
async def health():
	return {"status": "ok"}
