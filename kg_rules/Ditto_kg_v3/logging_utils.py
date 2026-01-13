from config import VERBOSE

def log(step: str, msg: str = ""):
    if VERBOSE:
        print(f"\n🟦 [{step}] {msg}".rstrip())

def log_ok(step: str, msg: str = ""):
    if VERBOSE:
        print(f"✅ [{step}] {msg}".rstrip())

def log_warn(step: str, msg: str = ""):
    print(f"⚠️ [{step}] {msg}".rstrip())
