# PDF Invoice Extractor

An AI-powered pipeline for extracting structured data from PDF invoices in Ukrainian into clean JSON. To be extended to automatically map the invoice entries as finmap entries and assign categories based on payment destination.

It processes multi-page PDFs as a single document to extract key fields:

-   **Date**
-   **Total Sum**
-   **Correspondent** (Sender/Receiver)
-   **Bank Name**
-   **Payment Destination**
-   **Transfer Type** (Debit/Credit)

---

## Getting Started

1.  **Install dependencies:**

    ```bash
    pip install -e . "langgraph-cli[inmem]"
    ```

2.  **Configure environment:**
    Copy the example file and add your OpenAI API key.

    ```bash
    cp .env.example .env
    ```

3.  **Run the local server:**
    ```bash
    langgraph dev
    ```

---

## Usage Example

Invoke the graph programmatically with a path to your PDF:

```python
from src.agent.graph import graph

state = {"pdf_path": "examples/sample.pdf"}
result = graph.invoke(state)
print(result["json_out"])
```

**Example JSON Output:**

```json
{
    "page_count": 4,
    "invoice_count": 2,
    "invoices": [
        {
            "Date": "2025-08-01",
            "Sum": 1500.0,
            "Correspondent": "Company A",
            "Bank": "BankName",
            "Payment Destination": "Payment for services",
            "Transfer Type": "Debit"
        },
        {
            "Date": "2025-08-02",
            "Sum": 2500.0,
            "Correspondent": "Company B",
            "Bank": null,
            "Payment Destination": "Prepayment for goods",
            "Transfer Type": "Credit"
        }
    ]
}
```

---

## How It Works & Customization

-   **PDF Processing**: All pages are merged into a single text input for contextual analysis.
-   **AI Extraction**: A single call to an OpenAI model uses a Pydantic schema for reliable, structured output.
-   **Normalization**: Data is cleaned and formatted, and duplicates are removed.
-   **Customization**: Modify `graph.py` to change the extraction schema (e.g., add invoice numbers) or adjust the AI prompts for different document types.
