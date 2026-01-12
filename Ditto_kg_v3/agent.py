import json
from typing import List

from config import EMBED_MODEL, LLM_MODEL
from logging_utils import log, log_ok, log_warn
from models import MemoryNote, KGTriple, FactStore

KG_SYSTEM_PROMPT = """
너는 '실내 식물 추천 서비스'의 KG(triple) 추출기다.
입력 텍스트에서 "사용자 프로필/선호/제약"에 관련된 사실만 뽑는다.
사진/스팟/빛 정보는 지금 단계에서 제외한다.
반드시 JSON만 출력한다.

{"triples":[{"head":"...", "relation":"...", "tail":"..."}]}

prefix 권장: User:, Profile:, Session:, Plant:
"""

MEMORY_SYSTEM_PROMPT = """
당신은 사용자의 notes(원문 메모), KG(triples), facts(JSON)를 참고해 답하는 비서입니다.

규칙:
- 제공된 데이터에 기반해 답합니다.
- 없는 정보는 단정하지 말고 "기록에 없음"이라고 말하세요.
- 답변은 한국어로 자연스럽게 하세요.
"""

def get_embedding(client, text: str, model: str = EMBED_MODEL) -> List[float]:
    log("EMBED", f"임베딩 생성(len={len(text)})")
    resp = client.embeddings.create(model=model, input=text)
    log_ok("EMBED", "완료")
    return resp.data[0].embedding

def extract_triples_from_text(client, text: str, source_id: str, model: str = LLM_MODEL) -> List[KGTriple]:
    log("LLM-KG", f"notes에서 KG 추출 | source={source_id}")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": KG_SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0.1,
    )
    content = resp.choices[0].message.content
    try:
        data = json.loads(content)
        raw = data.get("triples", []) or []
    except json.JSONDecodeError:
        log_warn("LLM-KG", "JSON 파싱 실패 → 생략")
        return []

    out: List[KGTriple] = []
    for t in raw:
        if not isinstance(t, dict):
            continue
        h = (t.get("head") or "").strip()
        r = (t.get("relation") or "").strip()
        ta = (t.get("tail") or "").strip()
        if h and r and ta:
            out.append(KGTriple(head=h, relation=r, tail=ta, source_id=source_id))

    log_ok("LLM-KG", f"추출 완료 | triples={len(out)}")
    return out

def tokenize_ko_simple(text: str) -> List[str]:
    for ch in [",", ".", "?", "!", ":", ";", "(", ")", "[", "]", "{", "}", "'", '"']:
        text = text.replace(ch, " ")
    return [t for t in text.split() if t]

def find_kg_by_question(question: str, triples: List[KGTriple], top_k: int = 12) -> List[KGTriple]:
    log("KG-FIND", f"질문 기반 triples 검색 | top_k={top_k}")
    toks = list(set(tokenize_ko_simple(question)))
    scored = []
    for t in triples:
        s = 0
        for tok in toks:
            if tok and (tok in t.head or tok in t.relation or tok in t.tail):
                s += 1
        if s > 0:
            scored.append((s, t))
    scored.sort(key=lambda x: x[0], reverse=True)
    out = [t for _, t in scored[:top_k]]
    log_ok("KG-FIND", f"찾음 | count={len(out)}")
    return out

def format_kg_content(triples: List[KGTriple]) -> str:
    if not triples:
        return "(관련 KG 없음)"
    return "\n".join([f"- ({t.head}, {t.relation}, {t.tail})  // from {t.source_id}" for t in triples])

def format_memory_context(notes: List[MemoryNote]) -> str:
    if not notes:
        return "(관련 텍스트 메모 없음)"
    return "\n".join([f"[{n.id}] {n.text}" for n in notes])

def search_memory(client, collection, query: str, top_k: int = 5) -> List[MemoryNote]:
    log("CHROMA-SEARCH", f"top_k={top_k} | query='{query}'")
    if collection is None:
        log_warn("CHROMA-SEARCH", "collection 없음 → 생략")
        return []
    q_emb = get_embedding(client, query)
    result = collection.query(query_embeddings=[q_emb], n_results=top_k)
    ids = result.get("ids", [[]])[0]
    docs = result.get("documents", [[]])[0]
    log_ok("CHROMA-SEARCH", f"hits={len(ids)}")
    return [MemoryNote(id=_id, text=doc) for _id, doc in zip(ids, docs)]

def answer_with_agent_memory(
    client,
    question: str,
    notes: List[MemoryNote],
    facts: FactStore,
    triples: List[KGTriple],
    collection,
    top_k_text: int = 5,
    top_k_kg: int = 12,
) -> str:
    log("AGENT", f"답변 생성 | question='{question}'")
    text_hist = search_memory(client, collection, question, top_k=top_k_text)
    kg_hist = find_kg_by_question(question, triples, top_k=top_k_kg)

    facts_brief = {
        "user_num": (facts.user or {}).get("user_num"),
        "session_id": (facts.reco_session or {}).get("session_id"),
        "plants_count": len(facts.plants),
        "recommendation_items_count": len(facts.recommendation_items),
        "profile": facts.user_profile,
    }

    user_content = f"""
[질문]
{question}

[관련 메모(notes)]
{format_memory_context(text_hist)}

[관련 KG(triples)]
{format_kg_content(kg_hist)}

[facts 요약]
{json.dumps(facts_brief, ensure_ascii=False, indent=2)}
"""

    log("AGENT", "LLM 호출 중…")
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": MEMORY_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        temperature=0.3,
    )
    log_ok("AGENT", "답변 생성 완료")
    return resp.choices[0].message.content
