import os
import shutil
from typing import List

import chromadb

from config import CHROMA_DB_DIR, CHROMA_COLLECTION_NAME
from logging_utils import log, log_ok, log_warn

def init_chroma_collection(reset_entire_db_dir: bool = False, reset_collection: bool = False):
    log("CHROMA-INIT", f"db_dir='{CHROMA_DB_DIR}', collection='{CHROMA_COLLECTION_NAME}'")

    if reset_entire_db_dir and os.path.exists(CHROMA_DB_DIR):
        shutil.rmtree(CHROMA_DB_DIR)
        log_ok("CHROMA-INIT", "DB 디렉토리 삭제(완전 초기화)")

    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    log_ok("CHROMA-INIT", "PersistentClient 준비 완료")

    if reset_collection:
        try:
            chroma_client.delete_collection(name=CHROMA_COLLECTION_NAME)
            log_ok("CHROMA-INIT", "컬렉션 삭제 완료")
        except Exception:
            log_warn("CHROMA-INIT", "기존 컬렉션 없음 → 삭제 생략")

    collection = chroma_client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)
    log_ok("CHROMA-INIT", "컬렉션 준비 완료")
    return collection

def upsert_documents(collection, ids: List[str], documents: List[str], embeddings: List[List[float]]):
    log("CHROMA-UPsert", f"count={len(ids)}")
    if hasattr(collection, "upsert"):
        collection.upsert(ids=ids, documents=documents, embeddings=embeddings)
        log_ok("CHROMA-UPsert", "upsert 완료")
        return
    log_warn("CHROMA-UPsert", "upsert 미지원 → delete+add fallback")
    try:
        collection.delete(ids=ids)
    except Exception:
        pass
    collection.add(ids=ids, documents=documents, embeddings=embeddings)
    log_ok("CHROMA-UPsert", "delete+add 완료")
