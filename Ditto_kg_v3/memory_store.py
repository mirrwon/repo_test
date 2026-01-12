import json
import os
from dataclasses import asdict
from typing import List, Tuple

from logging_utils import log, log_ok, log_warn
from config import MEMORY_PATH
from models import MemoryNote, KGTriple, FactStore

def save_memory(
    notes: List[MemoryNote],
    facts: FactStore,
    triples: List[KGTriple],
    path: str = MEMORY_PATH
):
    log("MEMORY-SAVE", f"저장 시작 → {path}")
    data = {
        "notes": [asdict(n) for n in notes],
        "facts": asdict(facts),
        "triples": [asdict(t) for t in triples],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log_ok("MEMORY-SAVE", f"저장 완료 | notes={len(notes)}, triples={len(triples)}")

def load_memory(path: str = MEMORY_PATH) -> Tuple[List[MemoryNote], FactStore, List[KGTriple]]:
    log("MEMORY-LOAD", f"로딩 시도 → {path}")

    if not os.path.exists(path):
        log_warn("MEMORY-LOAD", "메모리 파일 없음 → 새로 시작")
        return [], FactStore(), []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 구버전(list) 호환
    if isinstance(data, list):
        log_warn("MEMORY-LOAD", "구버전 포맷(list) 감지 → 변환")
        notes = []
        for idx, item in enumerate(data):
            if isinstance(item, dict):
                notes.append(MemoryNote(id=item.get("id", f"mem-{idx}"), text=item.get("text", str(item))))
            else:
                notes.append(MemoryNote(id=f"mem-{idx}", text=str(item)))
        facts = FactStore()
        triples = []
        save_memory(notes, facts, triples, path)
        return notes, facts, triples

    if not isinstance(data, dict):
        log_warn("MEMORY-LOAD", "포맷 이상 → 초기화")
        return [], FactStore(), []

    # notes
    notes_data = data.get("notes", []) or []
    notes: List[MemoryNote] = []
    for idx, n in enumerate(notes_data):
        if isinstance(n, dict):
            notes.append(MemoryNote(id=n.get("id", f"mem-{idx}"), text=n.get("text", "")))
        else:
            notes.append(MemoryNote(id=f"mem-{idx}", text=str(n)))

    # facts
    facts_data = data.get("facts", {}) or {}
    facts = FactStore(
        user=facts_data.get("user"),
        user_profile=facts_data.get("user_profile"),
        reco_session=facts_data.get("reco_session"),
        plants=facts_data.get("plants") or [],
        recommendation_items=facts_data.get("recommendation_items") or [],
        extra=facts_data.get("extra") or {},
    )

    # triples
    triples_data = data.get("triples", []) or []
    triples: List[KGTriple] = []
    for t in triples_data:
        if isinstance(t, dict):
            h = (t.get("head") or "").strip()
            r = (t.get("relation") or "").strip()
            ta = (t.get("tail") or "").strip()
            sid = (t.get("source_id") or "").strip()
            if h and r and ta:
                triples.append(KGTriple(head=h, relation=r, tail=ta, source_id=sid))

    log_ok("MEMORY-LOAD", f"로딩 완료 | notes={len(notes)}, triples={len(triples)}")
    return notes, facts, triples
