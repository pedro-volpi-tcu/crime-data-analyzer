from decimal import Decimal
from typing import Any, Iterable, TypeAlias, cast

import networkx as nx
import pandas as pd

NodeType: TypeAlias = str
NodeData: TypeAlias = dict[str, Any]
NodeWithData: TypeAlias = tuple[NodeType, NodeData]


class StressScorer:
    def __init__(self, severity_scores: pd.DataFrame, policy_budgets: dict[str, float]) -> None:
        self.severity_scores = severity_scores

    def _accumulate_severity(self, crimes: Iterable[NodeWithData]) -> float:
        severities = (crime["severity"] for crime in crimes)
        return sum(severities)

    def calculate_policy_stresses(self, graph: "PolicyGraph") -> dict[NodeType, float]:
        # TODO
        stress_scores: dict[str, float] = {}
        for policy_id, data in graph.get_all_policies():
            crimes = graph.get_crimes_for_policy(policy_id)
            total_severity = self._accumulate_severity(crimes)
            stress_scores[policy_id] = total_severity / data["budget"]
        return stress_scores


class PolicyGraph:
    def __init__(self, graph: nx.DiGraph[str]) -> None:
        self._graph = graph

    def get_all_policies(self) -> Iterable[NodeWithData]:
        nodes_with_data = cast(Iterable[NodeWithData], self._graph.nodes(data=True))
        return ((node, data) for node, data in nodes_with_data if data.get("type") == "policy")

    def get_crimes_for_policy(self, policy_id: str) -> Iterable[NodeWithData]:
        # This method hides the networkx complexity from the rest of the app
        neighbors = self._graph.neighbors(policy_id)
        return [
            (neighbor, self._graph.nodes[neighbor]["severity"])
            for neighbor in neighbors
            if self._graph.nodes[neighbor]["type"] == "crime"
        ]


class PolicyGraphBuilder:
    def __init__(self) -> None:
        self._graph: nx.DiGraph[str] = nx.DiGraph()

    def add_policy(self, policy_id: str, budget: Decimal) -> "PolicyGraphBuilder":
        self._graph.add_node(policy_id, type="policy", budget=budget)
        return self

    def add_crime(self, crime_id: str, severity: float) -> "PolicyGraphBuilder":
        self._graph.add_node(crime_id, type="crime", severity=severity)
        return self

    def link_policy_to_crime(self, policy_id: str, crime_id: str) -> "PolicyGraphBuilder":
        # TODO: add validation here, e.g., ensure nodes exist
        self._graph.add_edge(policy_id, crime_id)
        return self

    def build(self) -> "PolicyGraph":
        return PolicyGraph(self._graph)
