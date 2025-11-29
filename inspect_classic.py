import langchain_classic
print(f"Classic Version: {langchain_classic.__version__}")
print("dir(langchain_classic):")
print(dir(langchain_classic))
try:
    import langchain_classic.agents
    print("dir(langchain_classic.agents):")
    print(dir(langchain_classic.agents))
except ImportError:
    print("No langchain_classic.agents")
