from .utils.config import settings


def dbg(*args):
    if settings.debug_sheet:
        print("[SHEET-DEBUG]", *args)
