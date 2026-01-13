from typing import Any, Dict, List, Optional, Protocol
from logging_utils import log, log_ok

class DBAdapter(Protocol):
    def fetch_user(self, user_num: int) -> Optional[Dict[str, Any]]: ...
    def fetch_user_profile(self, user_num: int) -> Optional[Dict[str, Any]]: ...
    def fetch_reco_session(self, session_id: str) -> Optional[Dict[str, Any]]: ...
    def fetch_plants_catalog(self) -> List[Dict[str, Any]]: ...
    def fetch_recommendation_items(self, session_id: str) -> List[Dict[str, Any]]: ...

class InMemoryDB(DBAdapter):
    """
    ✅ 디버깅용 데모 DB
    나중에 Postgres/SQLite로 갈아끼울 때는 이 클래스를 새 구현으로 교체하면 됨.
    """
    def __init__(self):
        self.users = {
            1: {"user_num": 1, "user_jid": "test01", "name": "홍길동", "created_at": "2026-01-09 10:00:00"}
        }
        self.user_profiles = {
            1: {
                "user_num": 1, "has_pet": 1, "has_kid": 0, "allergy_sensitive": 1,
                "skill_level": "초보", "watering_habit": "잊음",
                "profile_extra": {"pet_types": ["CAT"], "style_tags": ["MINIMAL"]},
                "created_at": "2026-01-09 10:01:00", "updated_at": "2026-01-09 10:01:30",
            }
        }
        self.sessions = {
            "sess-001": {
                "session_id": "sess-001", "user_num": 1, "photo_id2": "N/A",
                "session_kind": "plant_reco", "status": "recommended",
                "algo_version": "v0.1", "params_json": {"top_k": 5},
                "created_at": "2026-01-09 10:02:00", "updated_at": "2026-01-09 10:02:30",
                "note": "no-photo demo",
            }
        }
        self.plants = [
            {"plant_id": 101, "name_ko": "스투키", "care_difficulty": "쉬움", "pet_caution": 1, "human_allergy_caution": 0},
            {"plant_id": 102, "name_ko": "스킨답서스", "care_difficulty": "쉬움", "pet_caution": 1, "human_allergy_caution": 0},
            {"plant_id": 103, "name_ko": "라벤더", "care_difficulty": "보통", "pet_caution": 1, "human_allergy_caution": 1},
        ]
        self.reco_items = {
            "sess-001": [
                {
                    "rec_item_id": "rec-001", "session_id": "sess-001", "plant_id": 102,
                    "rank_no": 1, "score_total": 0.91, "score_style": 0.70, "score_survival": 0.95,
                    "is_best": 1,
                    "reason_json": {"why": ["초보도 키우기 쉬움", "향/알러지 주의 식물 회피"]},
                    "kg_trace_json": {"path": ["UserProfile", "Plant"]},
                    "created_at": "2026-01-09 10:02:40",
                }
            ]
        }

    def fetch_user(self, user_num: int):
        log("DB-FETCH", f"users user_num={user_num}")
        row = self.users.get(user_num)
        log_ok("DB-FETCH", f"users found={bool(row)} keys={list(row.keys()) if row else []}")
        return row

    def fetch_user_profile(self, user_num: int):
        log("DB-FETCH", f"user_profile user_num={user_num}")
        row = self.user_profiles.get(user_num)
        log_ok("DB-FETCH", f"user_profile found={bool(row)} keys={list(row.keys()) if row else []}")
        return row

    def fetch_reco_session(self, session_id: str):
        log("DB-FETCH", f"reco_sessions session_id={session_id}")
        row = self.sessions.get(session_id)
        log_ok("DB-FETCH", f"reco_session found={bool(row)} keys={list(row.keys()) if row else []}")
        return row

    def fetch_plants_catalog(self):
        log("DB-FETCH", "plants catalog")
        log_ok("DB-FETCH", f"plants count={len(self.plants)}")
        return self.plants

    def fetch_recommendation_items(self, session_id: str):
        log("DB-FETCH", f"recommendation_items session_id={session_id}")
        rows = self.reco_items.get(session_id, [])
        log_ok("DB-FETCH", f"recommendation_items count={len(rows)}")
        return rows
