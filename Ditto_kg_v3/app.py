from logging_utils import log, log_ok
from memory_store import load_memory, save_memory
from chroma_store import init_chroma_collection, upsert_documents
from llm_client import build_openrouter_client
from db_adapter import InMemoryDB
from facts_pack import pack_facts_user_plant_only
from kg_builder import build_triples_user_plant_only
from models import MemoryNote, FactStore
from agent import get_embedding, extract_triples_from_text, answer_with_agent_memory

def build_vector_index(client, notes, collection):
    log("CHROMA-INDEX", f"notes 인덱싱 | notes={len(notes)}")
    if not notes or collection is None:
        return
    ids, docs, embs = [], [], []
    for n in notes:
        ids.append(n.id)
        docs.append(n.text)
        embs.append(get_embedding(client, n.text))
    upsert_documents(collection, ids, docs, embs)
    log_ok("CHROMA-INDEX", "완료")

def add_memory_note(client, collection, notes, triples, text: str):
    log("NOTE-ADD", f"메모 추가 | '{text}'")
    mem_id = f"mem-{len(notes)}"
    note = MemoryNote(id=mem_id, text=text)
    notes.append(note)

    new_triples = extract_triples_from_text(client, text, source_id=mem_id)
    triples.extend(new_triples)

    emb = get_embedding(client, note.text)
    upsert_documents(collection, [note.id], [note.text], [emb])

    log_ok("NOTE-ADD", f"완료 | new_triples={len(new_triples)}")
    return notes, triples

def rebuild_kg_from_facts(triples, facts: FactStore, source_id: str = "facts"):
    before = len(triples)
    triples[:] = [t for t in triples if t.source_id != source_id]
    removed = before - len(triples)

    rebuilt = build_triples_user_plant_only(facts, source_id=source_id)
    triples.extend(rebuilt)
    log_ok("KG-REBUILD", f"removed={removed}, added={len(rebuilt)}, total={len(triples)}")
    return triples

def main():
    log("MAIN", "시작(User+Plant only)")

    notes, facts, triples = load_memory()
    log_ok("MAIN", f"현재 상태 | notes={len(notes)}, triples={len(triples)}")

    client = build_openrouter_client()
    collection = init_chroma_collection(reset_entire_db_dir=False, reset_collection=False)
    build_vector_index(client, notes, collection)

    notes, triples = add_memory_note(client, collection, notes, triples, "나는 꽃가루 알러지가 있어")
    notes, triples = add_memory_note(client, collection, notes, triples, "나는 식물을 잘 못 키워서 쉬운 걸 원해")

    db = InMemoryDB()
    user_num = 1
    session_id = "sess-001"

    user_row = db.fetch_user(user_num)
    profile_row = db.fetch_user_profile(user_num)
    session_row = db.fetch_reco_session(session_id)
    plants_rows = db.fetch_plants_catalog()
    rec_rows = db.fetch_recommendation_items(session_id)

    facts = pack_facts_user_plant_only(
        user=user_row,
        profile=profile_row,
        session=session_row,
        plants=plants_rows,
        rec_items=rec_rows,
    )

    triples = rebuild_kg_from_facts(triples, facts, source_id="facts")

    save_memory(notes, facts, triples)

    for q in [
        "나한테 추천된 식물이 뭐야?",
        "왜 그 식물이 추천됐어?",
        "나는 알러지가 있는데 주의할 식물 있어?",
    ]:
        print("\n" + "=" * 70)
        print("Q:", q)
        ans = answer_with_agent_memory(client, q, notes, facts, triples, collection)
        print("A:", ans)
        print("=" * 70)

    log_ok("MAIN", "종료")

if __name__ == "__main__":
    main()
