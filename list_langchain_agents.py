import os
import langchain
path = os.path.join(os.path.dirname(langchain.__file__), "agents")
print(f"Listing {path}")
try:
    print(os.listdir(path))
    init_path = os.path.join(path, "__init__.py")
    if os.path.exists(init_path):
        print(f"\nContent of {init_path}:")
        with open(init_path, 'r') as f:
            print(f.read())
except Exception as e:
    print(e)
