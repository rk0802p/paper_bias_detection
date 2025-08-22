import re
import math
import requests
from typing import Dict, List, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SEMANTIC_SCHOLAR_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
OPENALEX_SEARCH = "https://api.openalex.org/works"


def _normalize_whitespace(text: str) -> str:
	"""Collapse multiple spaces/newlines and strip."""
	if not text:
		return ""
	text = re.sub(r"[\u00A0\t]+", " ", text)
	text = re.sub(r"\s+", " ", text)
	return text.strip()


def extract_sections(full_text: str) -> Dict[str, str]:
	"""Extract Title, Abstract, Methodology, Conclusions using simple heuristics.
	- Title: first non-empty line (<= 200 chars)
	- Abstract/Methodology/Conclusions: by heading regex variants
	"""
	text = full_text or ""
	lines = [l.strip() for l in text.splitlines()]
	title = next((l for l in lines if l and len(l) <= 200), "Untitled")

	# Build a case-insensitive marker-based split
	markers = [
		("abstract", "Abstract"),
		("methodology|methods|materials and methods|experimental setup|approach", "Methodology"),
		("conclusion|conclusions|discussion and conclusion|summary", "Conclusions"),
	]
	sections: Dict[str, str] = {"Title": title, "Abstract": "", "Methodology": "", "Conclusions": ""}

	lower = text.lower()
	indices: Dict[str, int] = {}
	for pattern, key in markers:
		m = re.search(rf"\n\s*(?:\d+\.?\s*)?(?:{pattern})\s*\n", lower, re.IGNORECASE)
		if m:
			indices[key] = m.start()

	# Determine spans between markers
	ordered = sorted(indices.items(), key=lambda kv: kv[1])
	spans: List[Tuple[str, int, int]] = []
	for i, (name, start) in enumerate(ordered):
		end = ordered[i + 1][1] if i + 1 < len(ordered) else len(text)
		spans.append((name, start, end))

	for name, start, end in spans:
		content = _normalize_whitespace(text[start:end])
		# Remove the heading itself (first line)
		content = re.sub(r"^.{0,120}?\b(?i:" + name.lower() + r")\b[:\s-]*", "", content, flags=re.IGNORECASE)
		sections[name] = content.strip()

	# Fallbacks: if markers not found, approximate by paragraphs
	if not sections["Abstract"]:
		sections["Abstract"] = _normalize_whitespace(" ".join(lines[:200]))[:1500]
	if not sections["Methodology"]:
		sections["Methodology"] = _normalize_whitespace(" ".join(lines[200:800]))[:3000]
	if not sections["Conclusions"]:
		sections["Conclusions"] = _normalize_whitespace(" ".join(lines[-400:]))[:2000]

	return sections


def _semantic_scholar_search(qt: str, max_results: int) -> List[Dict[str, str]]:
	params = {"query": qt, "limit": max_results, "fields": "title,url,abstract"}
	resp = requests.get(SEMANTIC_SCHOLAR_SEARCH, params=params, timeout=12)
	resp.raise_for_status()
	data = resp.json() or {}
	results = []
	for item in data.get("data", []):
		results.append({
			"title": item.get("title") or "Untitled",
			"url": item.get("url") or "",
			"abstract": item.get("abstract") or ""
		})
	return results


def _openalex_search(qt: str, max_results: int) -> List[Dict[str, str]]:
	params = {"search": qt, "per_page": max_results}
	resp = requests.get(OPENALEX_SEARCH, params=params, timeout=12)
	resp.raise_for_status()
	data = resp.json() or {}
	results = []
	for item in data.get("results", []):
		results.append({
			"title": (item.get("title") or "Untitled"),
			"url": (item.get("id") or ""),
			"abstract": (item.get("abstract_inverted_index") and " ".join(sorted(item["abstract_inverted_index"].keys()))) or ""
		})
	return results


def _build_queries(section_text: str) -> List[str]:
	# Build progressively shorter/cleaner queries to improve hit rate
	s = _normalize_whitespace(section_text)
	queries: List[str] = []
	if len(s) > 400:
		queries.append(s[:400])
	if len(s) > 200:
		queries.append(s[:200])
	if len(s) > 30:
		words = [w for w in re.findall(r"[A-Za-z]{3,}", s)][:25]
		queries.append(" ".join(words))
	return [q for q in queries if q]


def search_related_papers(query_text: str, max_results: int = 8) -> List[Dict[str, str]]:
	"""Search multiple scholarly APIs with robust query fallback."""
	queries = _build_queries(query_text)
	seen = set()
	out: List[Dict[str, str]] = []
	for q in queries:
		for provider in ("ss", "oa"):
			try:
				results = _semantic_scholar_search(q, max_results) if provider == "ss" else _openalex_search(q, max_results)
				for r in results:
					key = (r.get("title"), r.get("url"))
					if key not in seen and r.get("url"):
						seen.add(key)
						out.append(r)
				if len(out) >= max_results:
					return out[:max_results]
			except Exception:
				continue
	return out[:max_results]


def similarity_percent(a: str, b: str) -> float:
	"""TF-IDF cosine similarity converted to percent 0-100."""
	texts = [a or "", b or ""]
	vectorizer = TfidfVectorizer(stop_words="english")
	try:
		X = vectorizer.fit_transform(texts)
		sim = cosine_similarity(X[0:1], X[1:2]).ravel()[0]
	except ValueError:
		sim = 0.0
	return max(0.0, min(1.0, float(sim))) * 100.0


def categorize_similarity(pct: float) -> str:
	if pct <= 25:
		return "1–25%: Low similarity (mostly original ideas)"
	if pct <= 50:
		return "25–50%: Moderate similarity"
	return ">50%: High similarity (heavily copied)"


def analyze_section(section_text: str, top_k: int = 5) -> Dict[str, object]:
	"""Search for related papers and score similarity against each. Return top matches."""
	candidates = search_related_papers(section_text, max_results=12)
	scored: List[Tuple[float, Dict[str, str]]] = []
	for paper in candidates:
		content = f"{paper.get('title','')}\n{paper.get('abstract','')}"
		pct = similarity_percent(section_text, content)
		scored.append((pct, paper))
	# Sort high to low
	scored.sort(key=lambda x: x[0], reverse=True)
	top = scored[:top_k]
	best_pct = top[0][0] if top else 0.0
	return {
		"best_similarity_percent": round(best_pct, 2),
		"category": categorize_similarity(best_pct),
		"matches": [
			{
				"percent": round(p, 2),
				"title": d.get("title", "Untitled"),
				"url": d.get("url", ""),
			}
			for p, d in top if d.get("url")
		]
	}


def analyze_plagiarism(full_text: str) -> Dict[str, object]:
	"""Analyze Title, Abstract, Methodology, Conclusions for similarity and provide links."""
	sections = extract_sections(full_text)
	report: Dict[str, object] = {"sections": {}, "overall_percent": 0.0}
	percents: List[float] = []
	for name in ["Title", "Abstract", "Methodology", "Conclusions"]:
		result = analyze_section(sections.get(name, ""))
		report["sections"][name] = result
		percents.append(result["best_similarity_percent"])  # simple aggregation: max per section
	# Overall as weighted average favoring Abstract and Methodology
	weights = np.array([0.1, 0.4, 0.4, 0.1])
	values = np.array([
		report["sections"]["Title"]["best_similarity_percent"],
		report["sections"]["Abstract"]["best_similarity_percent"],
		report["sections"]["Methodology"]["best_similarity_percent"],
		report["sections"]["Conclusions"]["best_similarity_percent"],
	])
	report["overall_percent"] = float(np.round(np.dot(weights, values), 2))
	report["overall_category"] = categorize_similarity(report["overall_percent"])
	return report
