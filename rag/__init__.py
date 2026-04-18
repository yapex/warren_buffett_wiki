"""Buffett Wiki RAG - Meilisearch-based search"""
from .meilisearch_search import (
    search_paragraphs,
    search_concept_timeline,
    search_concept_in_doc,
    get_concept_quote_timeline,
    search_with_filters,
    get_facets,
    benchmark,
)

__version__ = "0.2.0"
__all__ = [
    "search_paragraphs",
    "search_concept_timeline",
    "search_concept_in_doc",
    "get_concept_quote_timeline",
    "search_with_filters",
    "get_facets",
    "benchmark",
]
