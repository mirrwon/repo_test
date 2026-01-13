from openai import OpenAI
from config import OPENROUTER_API_KEY, APP_URL, APP_NAME
from logging_utils import log_ok, log_warn

def build_openrouter_client() -> OpenAI:
    if not OPENROUTER_API_KEY:
        log_warn("BOOT", "OPENROUTER_API_KEY 없음 → LLM/임베딩 호출은 실패할 수 있음")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        default_headers={
            "HTTP-Referer": APP_URL,
            "X-Title": APP_NAME,
        },
    )
    log_ok("BOOT", "OpenRouter(OpenAI SDK) 클라이언트 준비 완료")
    return client
