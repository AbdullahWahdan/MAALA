import langchain_classic
print(dir(langchain_classic))
try:
    import langchain_classic.chains
    print("Found chains")
except:
    print("No chains")
