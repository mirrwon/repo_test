import json
from typing import Any, Dict, List, Optional, Union

from logging_utils import log, log_ok
from models import FactStore, KGTriple

def _as_scalar(v: Any) -> Optional[str]:
    if v is None:
        return None
    if isinstance(v, (str, int, float, bool)):
        return str(v)
    try:
        return json.dumps(v, ensure_ascii=False)
    except Exception:
        return str(v)

def add_attr_triples(triples: List[KGTriple], node: str, data: Dict[str, Any], source_id: str):
    for k, v in (data or {}).items():
        sval = _as_scalar(v)
        if sval is not None:
            triples.append(KGTriple(node, f"ATTR_{str(k).upper()}", sval, source_id))

def build_triples_user_plant_only(facts: FactStore, source_id: str = "facts") -> List[KGTriple]:
    """
    ✅ 매핑 규칙에 따라 facts를 KG(triples)로 “변환”만 한다.
    """
    log("KG-BUILD", "facts → triples 생성(User+Plant ONLY)")
    triples: List[KGTriple] = []

    user_num = (facts.user or {}).get("user_num") or "U_UNKNOWN"
    session_id = (facts.reco_session or {}).get("session_id") or "S_UNKNOWN"

    U = f"User:{user_num}"
    PR = f"Profile:{user_num}"
    S = f"Session:{session_id}"

    if isinstance(facts.user, dict):
        triples.append(KGTriple(U, "IS_A", "User", source_id))
        add_attr_triples(triples, U, facts.user, source_id)
        log_ok("KG-BUILD", f"users → {U}")

    if isinstance(facts.user_profile, dict):
        triples.append(KGTriple(U, "HAS_PROFILE", PR, source_id))
        triples.append(KGTriple(PR, "IS_A", "UserProfile", source_id))
        add_attr_triples(triples, PR, facts.user_profile, source_id)
        log_ok("KG-BUILD", f"user_profile → {PR}")

    if isinstance(facts.reco_session, dict):
        triples.append(KGTriple(U, "STARTED_SESSION", S, source_id))
        triples.append(KGTriple(S, "IS_A", "RecoSession", source_id))
        add_attr_triples(triples, S, facts.reco_session, source_id)
        log_ok("KG-BUILD", f"reco_session → {S}")

    plant_nodes: Dict[Union[str, int], str] = {}
    for plant in facts.plants or []:
        if not isinstance(plant, dict):
            continue
        plant_id = plant.get("plant_id")
        if plant_id is None:
            continue
        PL = f"Plant:{plant_id}"
        plant_nodes[plant_id] = PL
        triples.append(KGTriple(PL, "IS_A", "Plant", source_id))
        add_attr_triples(triples, PL, plant, source_id)
    log_ok("KG-BUILD", f"plants count={len(plant_nodes)}")

    rec_count = 0
    for rec in facts.recommendation_items or []:
        if not isinstance(rec, dict):
            continue
        rec_item_id = rec.get("rec_item_id") or f"REC_{session_id}_{rec_count+1}"
        RI = f"RecItem:{rec_item_id}"

        triples.append(KGTriple(S, "HAS_RECOMMENDATION_ITEM", RI, source_id))
        triples.append(KGTriple(RI, "IS_A", "RecommendationItem", source_id))
        add_attr_triples(triples, RI, rec, source_id)

        plant_id = rec.get("plant_id")
        if plant_id is not None:
            PL = plant_nodes.get(plant_id, f"Plant:{plant_id}")
            triples.append(KGTriple(RI, "RECOMMENDS_PLANT", PL, source_id))
        rec_count += 1

    log_ok("KG-BUILD", f"rec_items count={rec_count} | total_triples={len(triples)}")
    return triples
