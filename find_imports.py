import sys

print("Checking AgentExecutor...")
try:
    from langchain.agents import AgentExecutor
    print("Found in langchain.agents")
except ImportError:
    pass

try:
    from langchain_core.agents import AgentExecutor
    print("Found in langchain_core.agents")
except ImportError:
    pass

try:
    from langchain.agent_executor import AgentExecutor
    print("Found in langchain.agent_executor")
except ImportError:
    pass

print("\nChecking create_react_agent...")
try:
    from langchain.agents import create_react_agent
    print("Found in langchain.agents")
except ImportError:
    pass

try:
    from langchain_core.agents import create_react_agent
    print("Found in langchain_core.agents")
except ImportError:
    pass

try:
    from langchain.agents.react.agent import create_react_agent
    print("Found in langchain.agents.react.agent")
except ImportError:
    pass

print("\nChecking initialize_agent...")
try:
    from langchain.agents import initialize_agent
    print("Found in langchain.agents")
except ImportError:
    pass
