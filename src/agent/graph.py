from langgraph.graph import StateGraph, END
from agent.models.state import State
from agent.nodes.load_pdf import load_pdf_as_single_text
from agent.nodes.extract_llm import extract_with_llm_whole_doc
from agent.nodes.finalize import finalize_json
from agent.nodes.check_sheet import check_against_sheet
from agent.nodes.dummy import dummy_node_for_missing


def build_graph():
    builder = StateGraph(State)
    builder.add_node("load_pdf_as_single_text", load_pdf_as_single_text)
    builder.add_node("extract_with_llm_whole_doc", extract_with_llm_whole_doc)
    builder.add_node("finalize_json", finalize_json)
    builder.add_node("check_against_sheet", check_against_sheet)
    builder.add_node("dummy_node_for_missing", dummy_node_for_missing)

    builder.set_entry_point("load_pdf_as_single_text")
    builder.add_edge("load_pdf_as_single_text", "extract_with_llm_whole_doc")
    builder.add_edge("extract_with_llm_whole_doc", "finalize_json")
    builder.add_edge("finalize_json", "check_against_sheet")

    def _route_after_check(state: State) -> str:
        return "missing" if state.get("missing_invoices") else "done"

    builder.add_conditional_edges(
        "check_against_sheet",
        _route_after_check,
        {"missing": "dummy_node_for_missing", "done": END},
    )
    builder.add_edge("dummy_node_for_missing", END)
    return builder.compile()


graph = build_graph()
