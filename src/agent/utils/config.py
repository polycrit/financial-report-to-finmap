from pydantic import BaseModel
import os


class Settings(BaseModel):
    google_service_account_json: str = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_JSON", ""
    ).strip()
    google_sheet_id: str = os.getenv("GOOGLE_SHEET_ID", "").strip()
    google_sheet_gid: int = int(os.getenv("GOOGLE_SHEET_GID", "0").strip())
    sheet_date_header: str = os.getenv("SHEET_DATE_HEADER", "Дата оплати").strip()
    sheet_sum_header: str = os.getenv("SHEET_SUM_HEADER", "Сума").strip()
    sheet_header_row: int = int(os.getenv("SHEET_HEADER_ROW", "4").strip())
    debug_sheet: bool = os.getenv("DEBUG_SHEET", "0").strip() == "1"


settings = Settings()
