import langchain.agents
import langchain
print(f"Version: {langchain.__version__}")
print(f"Path: {langchain.__file__}")
print(f"Has create_react_agent: {'create_react_agent' in dir(langchain.agents)}")
print(f"Has initialize_agent: {'initialize_agent' in dir(langchain.agents)}")
print(f"Has AgentExecutor: {'AgentExecutor' in dir(langchain.agents)}")
