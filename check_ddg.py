try:
    import duckduckgo_search
    print(f"✅ duckduckgo_search imported. Version: {duckduckgo_search.__version__}")
except ImportError as e:
    print(f"❌ duckduckgo_search failed to import: {e}")

try:
    from duckduckgo_search import DDGS
    print("✅ DDGS imported")
except ImportError as e:
    print(f"❌ DDGS failed to import: {e}")
