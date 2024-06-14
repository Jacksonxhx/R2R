"""Base classes for knowledge graph providers."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple

from ..abstractions.llama_abstractions import (
    EntityNode,
    LabelledNode,
    Relation,
    VectorStoreQuery,
)
from .base_provider import ProviderConfig

logger = logging.getLogger(__name__)


class KGConfig(ProviderConfig):
    """A base KG config class"""

    provider: Optional[str] = None
    batch_size: int = 1
    kg_extraction_prompt: Optional[str] = "ner_kg_extraction"

    def validate(self) -> None:
        if not self.provider:
            raise ValueError("Provider must be set.")
        if self.provider and self.provider not in self.supported_providers:
            raise ValueError(f"Provider '{self.provider}' is not supported.")

    @property
    def supported_providers(self) -> list[str]:
        return ["None", "neo4j"]


class KGProvider(ABC):
    """An abstract class to provide a common interface for Knowledge Graphs."""

    def __init__(self, config: KGConfig) -> None:
        if not isinstance(config, KGConfig):
            raise ValueError(
                "KGProvider must be initialized with a `KGConfig`."
            )
        logger.info(f"Initializing KG provider with config: {config}")
        self.config = config
        self.validate_config()

    def validate_config(self) -> None:
        self.config.validate()

    @property
    @abstractmethod
    def client(self) -> Any:
        """Get client."""
        pass

    @abstractmethod
    def get(self, subj: str) -> list[list[str]]:
        """Abstract method to get triplets."""
        pass

    @abstractmethod
    def get_rel_map(
        self,
        subjs: Optional[list[str]] = None,
        depth: int = 2,
        limit: int = 30,
    ) -> dict[str, list[list[str]]]:
        """Abstract method to get depth-aware rel map."""
        pass

    @abstractmethod
    def upsert_nodes(self, nodes: list[EntityNode]) -> None:
        """Abstract method to add triplet."""
        pass

    @abstractmethod
    def upsert_relations(self, relations: list[Relation]) -> None:
        """Abstract method to add triplet."""
        pass

    @abstractmethod
    def delete(self, subj: str, rel: str, obj: str) -> None:
        """Abstract method to delete triplet."""
        pass

    @abstractmethod
    def get_schema(self, refresh: bool = False) -> str:
        """Abstract method to get the schema of the graph store."""
        pass

    @abstractmethod
    def structured_query(
        self, query: str, param_map: Optional[dict[str, Any]] = {}
    ) -> Any:
        """Abstract method to query the graph store with statement and parameters."""
        pass

    @abstractmethod
    def vector_query(
        self, query: VectorStoreQuery, **kwargs: Any
    ) -> Tuple[list[LabelledNode], list[float]]:
        """Abstract method to query the graph store with a vector store query."""

    # TODO - Type this method.
    @abstractmethod
    def update_extraction_prompt(
        self,
        prompt_provider: Any,
        entity_types: list[Any],
        relations: list[Relation],
    ):
        """Abstract method to update the KG extraction prompt."""
        pass
