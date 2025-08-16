import os, json, base64, gspread
from typing import Dict, Tuple, Set
from google.oauth2.service_account import Credentials
from ..utils.config import settings
from ..utils.normalize import parse_date_to_iso, clean_number_str, round_money
from ..logging import dbg


def _client() -> gspread.Client:
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    inline = settings.google_service_account_json

    if inline:
        if (inline.startswith("'") and inline.endswith("'")) or (
            inline.startswith('"') and inline.endswith('"')
        ):
            inline = inline[1:-1]
        info = json.loads(inline)
        return gspread.authorize(
            Credentials.from_service_account_info(info, scopes=scopes)
        )

    return gspread.oauth()


def load_sheet_index() -> Tuple[Set[tuple], Dict[str, int]]:
    gc = _client()
    ws = gc.open_by_key(settings.google_sheet_id).get_worksheet_by_id(
        settings.google_sheet_gid
    )
    if ws is None:
        raise RuntimeError(f"Worksheet gid={settings.google_sheet_gid} not found.")

    rows = ws.get_all_values()
    dbg(f"Total rows: {len(rows)}")
    hdr_idx = max(0, settings.sheet_header_row - 1)
    if len(rows) <= hdr_idx:
        return set(), {}

    header = rows[hdr_idx]
    name_to_idx = {name.strip(): i for i, name in enumerate(header)}
    dbg(f"Header row {settings.sheet_header_row}: {header}")
    dbg("Header->index:", name_to_idx)

    if (
        settings.sheet_date_header not in name_to_idx
        or settings.sheet_sum_header not in name_to_idx
    ):
        raise RuntimeError(
            f"Headers must include '{settings.sheet_date_header}' and '{settings.sheet_sum_header}'. Found {list(name_to_idx.keys())}"
        )

    date_idx = name_to_idx[settings.sheet_date_header]
    sum_idx = name_to_idx[settings.sheet_sum_header]

    keyset = set()
    for i, r in enumerate(rows[hdr_idx + 1 :], start=hdr_idx + 2):
        date_raw = r[date_idx] if date_idx < len(r) else ""
        sum_raw = r[sum_idx] if sum_idx < len(r) else ""
        d = parse_date_to_iso(date_raw)
        s_clean = clean_number_str(sum_raw)
        try:
            s_val = float(s_clean)
        except ValueError:
            dbg(f"Row {i}: cannot parse sum_raw='{sum_raw}' (clean='{s_clean}')")
            continue
        s = round_money(s_val)
        if d and s:
            keyset.add((d, s))
            if settings.debug_sheet and i <= hdr_idx + 6:
                dbg(f"Row {i}: '{date_raw}'->'{d}', '{sum_raw}'->'{s}'")
    dbg(f"Total keys in sheet: {len(keyset)}")
    return keyset, name_to_idx
