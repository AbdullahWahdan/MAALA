from langchain.agents import create_agent
try:
    print(help(create_agent))
except Exception as e:
    print(e)

print("\nChecking langchain_community.agents...")
try:
    import langchain_community.agents
    print(dir(langchain_community.agents))
except ImportError:
    print("No langchain_community.agents")
