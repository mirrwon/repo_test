from typing import Any, Dict, List, Optional
from logging_utils import log, log_ok, log_warn
from models import FactStore

REQUIRED_USER_KEYS = ["user_num"]
REQUIRED_SESSION_KEYS = ["session_id", "user_num"]

def _missing_keys(row: Optional[Dict[str, Any]], keys: List[str]) -> List[str]:
    if not isinstance(row, dict):
        return keys[:]  # 전부 missing 취급
    return [k for k in keys if k not in row or row.get(k) is None]

def pack_facts_user_plant_only(
    user: Optional[Dict[str, Any]],
    profile: Optional[Dict[str, Any]],
    session: Optional[Dict[str, Any]],
    plants: List[Dict[str, Any]],
    rec_items: List[Dict[str, Any]],
) -> FactStore:
    """
    ✅ DB 결과를 FactStore에 “그냥 담기 + 필수키 검사”만 함
    (여기서는 KG 만들지 않음)
    """
    log("FACTS-PACK", "DB row → FactStore")

    miss_user = _missing_keys(user, REQUIRED_USER_KEYS)
    if miss_user:
        log_warn("FACTS-PACK", f"users missing_keys={miss_user}")

    miss_sess = _missing_keys(session, REQUIRED_SESSION_KEYS)
    if miss_sess:
        log_warn("FACTS-PACK", f"reco_session missing_keys={miss_sess}")

    bad_plants = [p for p in plants if not isinstance(p, dict) or p.get("plant_id") is None]
    if bad_plants:
        log_warn("FACTS-PACK", f"plants 중 plant_id 없는 row 존재 count={len(bad_plants)}")

    bad_recs = [r for r in rec_items if not isinstance(r, dict)]
    if bad_recs:
        log_warn("FACTS-PACK", f"recommendation_items 비정상 row count={len(bad_recs)}")

    facts = FactStore(
        user=user,
        user_profile=profile,
        reco_session=session,
        plants=plants or [],
        recommendation_items=rec_items or [],
    )
    log_ok("FACTS-PACK", f"완료 | plants={len(facts.plants)}, rec_items={len(facts.recommendation_items)}")
    return facts
