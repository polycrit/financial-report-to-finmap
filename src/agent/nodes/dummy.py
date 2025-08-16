from ..models.state import State
from ..logging import dbg


def dummy_node_for_missing(state: State) -> State:
    dbg("Dummy node received missing:", state.get("missing_invoices", []))
    # placeholder for future side-effects
    return {}
