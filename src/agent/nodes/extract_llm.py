from ..services.llm import get_llm_structured
from ..models.invoice import InvoiceList
from ..models.state import State

SYSTEM = (
    "Ви — система вилучення структурованих даних з фінансових документів. "
    "Повертайте відповіді ТІЛЬКИ у форматі JSON за схемою.\n"
    "- Date: YYYY-MM-DD або null\n"
    "- Sum: число (крапка як десятковий розділювач)\n"
    "- Payment Destination: повний текст\n"
    "- Transfer Type: Debit/Credit або null\n"
    "Не вигадуйте значення."
)

USER_TEMPLATE = (
    "Витягніть усі записи рахунків/платіжних документів з тексту нижче.\n"
    "Повний текст:\n<<<\n{full_text}\n>>>"
)


def extract_with_llm_whole_doc(state: State) -> State:
    full_text = (state.get("full_text") or "").strip()
    if not full_text:
        return {"llm_invoices": []}
    structured = get_llm_structured()
    result: InvoiceList = structured.invoke(
        [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": USER_TEMPLATE.format(full_text=full_text)},
        ]
    )
    return {"llm_invoices": [inv.model_dump(by_alias=True) for inv in result.invoices]}
