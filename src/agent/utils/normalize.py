from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Optional

NBSPs = ("\u00a0", "\u202f", "\u2009")


def clean_number_str(s: Any) -> str:
    s = str(s).strip()
    for ch in NBSPs:
        s = s.replace(ch, "")
    s = s.replace(" ", "").replace(",", ".")
    if s.startswith("'"):
        s = s[1:]
    return s


def round_money(x: Optional[float]) -> str:
    if x is None:
        return ""
    d = Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{d:.2f}"


def parse_date_to_iso(s: Optional[str]) -> str:
    if not s:
        return ""
    s = str(s).strip().split()[0]
    if s.startswith("'"):
        s = s[1:]
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    try:
        if s.replace(".", "", 1).isdigit():
            base = datetime(1899, 12, 30)
            return (base + timedelta(days=float(s))).date().isoformat()
    except Exception:
        pass
    return s
