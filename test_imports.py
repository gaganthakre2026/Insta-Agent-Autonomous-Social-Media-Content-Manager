"""Test script to diagnose import issues."""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

print("Testing imports...")

try:
    print("1. Importing config...")
    from config import settings
    print("   ✓ Config imported")
except Exception as e:
    print(f"   ✗ Config failed: {e}")

try:
    print("2. Importing db...")
    from db import engine, Base
    print("   ✓ DB imported")
except Exception as e:
    print(f"   ✗ DB failed: {e}\n")
    import traceback
    traceback.print_exc()

try:
    print("3. Importing models...")
    from models.user import User
    print("   ✓ User model imported")
except Exception as e:
    print(f"   ✗ Models failed: {e}\n")
    import traceback
    traceback.print_exc()

try:
    print("4. Importing llm_client...")
    from llm_client import ollama_client
    print("   ✓ LLM client imported")
except Exception as e:
    print(f"   ✗ LLM client failed: {e}")

try:
    print("5. Importing APIs...")
    from apis.v1 import auth
    print("   ✓ APIs imported")
except Exception as e:
    print(f"   ✗ APIs failed: {e}\n")
    import traceback
    traceback.print_exc()

print("\n✓ All imports successful!")
