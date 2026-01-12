from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

@dataclass
class MemoryNote:
    id: str
    text: str

@dataclass
class KGTriple:
    head: str
    relation: str
    tail: str
    source_id: str

@dataclass
class FactStore:
    # ✅ User + Plant only
    user: Optional[Dict[str, Any]] = None
    user_profile: Optional[Dict[str, Any]] = None
    reco_session: Optional[Dict[str, Any]] = None

    plants: List[Dict[str, Any]] = field(default_factory=list)
    recommendation_items: List[Dict[str, Any]] = field(default_factory=list)

    extra: Dict[str, Any] = field(default_factory=dict)

JsonScalar = Union[str, int, float, bool, None]
