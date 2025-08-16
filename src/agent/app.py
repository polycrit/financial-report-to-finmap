from .graph import graph


def run(state: dict) -> dict:
    return graph.invoke(state)
