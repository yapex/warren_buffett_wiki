"""Buffett Wiki RAG - 段落级检索 + 概念时间线"""
from .config import (
    search_paragraphs,
    search_concept_timeline,
    search_concept_in_doc,
    get_concept_quote_timeline,
    build_paragraph_index,
    save_paragraph_index,
    load_paragraph_index,
    DOCUMENTS,
    PARAGRAPHS,
)

__version__ = "0.1.0"
__all__ = [
    "search_paragraphs",
    "search_concept_timeline",
    "search_concept_in_doc",
    "get_concept_quote_timeline",
    "build_paragraph_index",
    "save_paragraph_index",
    "load_paragraph_index",
    "DOCUMENTS",
    "PARAGRAPHS",
]
