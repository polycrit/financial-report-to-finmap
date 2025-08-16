from ..models.state import State
from ..utils.normalize import round_money


def finalize_json(state: State) -> State:
    invoices = state.get("llm_invoices", []) or []
    seen = set()
    unique = []
    for inv in invoices:
        key = (
            (inv.get("Date") or "").strip(),
            round_money(inv.get("Sum")),
            (inv.get("Correspondent") or "")[:80].strip(),
            (inv.get("Payment Destination") or "")[:160].strip(),
            (inv.get("Transfer Type") or "").strip().lower(),
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(inv)
    payload = {
        "page_count": state.get("page_count", 0),
        "invoice_count": len(unique),
        "invoices": unique,
    }
    return {"json_out": payload}
