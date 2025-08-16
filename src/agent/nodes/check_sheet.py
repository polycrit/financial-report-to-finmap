from typing import Dict, List
from ..models.state import State
from ..services.sheets import load_sheet_index
from ..utils.normalize import parse_date_to_iso, round_money
from ..logging import dbg
from ..utils.config import settings


def check_against_sheet(state: State) -> State:
    payload = state.get("json_out") or {}
    invoices = payload.get("invoices", [])
    if not invoices:
        dbg("No invoices to check.")
        return {"sheet_checked_invoices": [], "missing_invoices": []}

    sheet_keys, _ = load_sheet_index()

    # Near-miss helpers
    date_to_sums: Dict[str, set] = {}
    sum_to_dates: Dict[str, set] = {}
    for d, s in sheet_keys:
        date_to_sums.setdefault(d, set()).add(s)
        sum_to_dates.setdefault(s, set()).add(d)

    checked: List[dict] = []
    missing: List[dict] = []

    dbg("---- Checking invoices against sheet ----")
    for idx, inv in enumerate(invoices, start=1):
        d_iso = parse_date_to_iso(inv.get("Date"))
        s_norm = round_money(inv.get("Sum"))
        exists = (d_iso, s_norm) in sheet_keys if d_iso and s_norm else False
        dbg(
            f"Invoice {idx}: Date='{inv.get('Date')}'->'{d_iso}', Sum='{inv.get('Sum')}'->'{s_norm}', exists={exists}"
        )
        if not exists and settings.debug_sheet:
            if d_iso in date_to_sums:
                dbg(f"  Same date, other sums: {sorted(date_to_sums[d_iso])}")
            if s_norm in sum_to_dates:
                dbg(f"  Same sum, other dates: {sorted(sum_to_dates[s_norm])}")

        annotated = {
            **inv,
            "ExistsInSheet": exists,
            "MatchKey": {"Date": d_iso, "Sum": s_norm},
        }
        checked.append(annotated)
        if not exists:
            missing.append(annotated)

    dbg(f"Missing invoices: {len(missing)} / {len(invoices)}")
    return {"sheet_checked_invoices": checked, "missing_invoices": missing}
