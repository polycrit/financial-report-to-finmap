from typing import TypedDict, Dict, Any, List


class State(TypedDict, total=False):
    pdf_path: str
    page_count: int
    full_text: str
    llm_invoices: List[dict]
    json_out: Dict[str, Any]
    sheet_checked_invoices: List[dict]
    missing_invoices: List[dict]
