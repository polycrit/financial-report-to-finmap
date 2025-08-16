from langchain_openai import ChatOpenAI
from ..models.invoice import InvoiceList


def get_llm_structured() -> ChatOpenAI:
    model = ChatOpenAI(model="gpt-4o", temperature=0.3)
    return model.with_structured_output(InvoiceList)
