from langchain_community.document_loaders import PyPDFLoader
from ..models.state import State


def load_pdf_as_single_text(state: State) -> State:
    loader = PyPDFLoader(state["pdf_path"])
    docs = loader.load()
    pages = []
    for i, d in enumerate(docs):
        pages.append(f"\n\n===== PAGE {i+1} =====\n{d.page_content or ''}")
    return {"full_text": "".join(pages).strip(), "page_count": len(docs)}
