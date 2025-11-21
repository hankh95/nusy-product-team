from huggingface_hub import HfApi

api = HfApi()
try:
    user = api.whoami()
    print(f"✅ Token is valid! Authenticated as: {user['name']}")
except Exception as e:
    print(f"❌ Token is invalid or expired: {e}")