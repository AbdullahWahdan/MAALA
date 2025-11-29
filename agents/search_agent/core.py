from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
import re

class SearchAgent:
    def __init__(self, groq_api_key):
        self.llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant", temperature=0)
        
        # Initialize Tools
        self.api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
        self.wiki = WikipediaQueryRun(api_wrapper=self.api_wrapper_wiki)
        
        self.api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=500)
        self.arxiv = ArxivQueryRun(api_wrapper=self.api_wrapper_arxiv)
        
        self.search = DuckDuckGoSearchRun(name="Search")
        
        self.tools = {
            "Search": self.search,
            "Wikipedia": self.wiki,
            "Arxiv": self.arxiv
        }

    def run(self, query, callbacks=None):
        system_prompt = """You are a helpful assistant with access to the following tools:

Search: Useful for searching the internet for current events and general information.
Wikipedia: Useful for finding detailed information about historical figures, concepts, and places.
Arxiv: Useful for searching scientific papers and academic research.

To use a tool, please use the following format:
Thought: Do I need to use a tool? Yes
Action: [The name of the tool to use, e.g. Search]
Action Input: [The input to the tool]
Observation: [The result of the tool]

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
Thought: Do I need to use a tool? No
Final Answer: [your response here]

Begin!
"""
        messages = [
            ("system", system_prompt),
            ("human", query)
        ]
        
        sources = []
        max_iterations = 5
        
        for _ in range(max_iterations):
            response = self.llm.invoke(messages).content
            
            # Parse for Action
            action_match = re.search(r"Action:\s*(.*)", response)
            action_input_match = re.search(r"Action Input:\s*(.*)", response)
            
            # Capture thought
            thought_match = re.search(r"Thought:\s*(.*)", response)
            thought = thought_match.group(1).strip() if thought_match else "Thinking..."
            
            if "Final Answer:" in response:
                final_answer = response.split("Final Answer:")[-1].strip()
                return {
                    "response": final_answer, 
                    "sources": list(set(sources)),
                    "history": messages  # Return full history for debugging/display
                }
            
            if action_match and action_input_match:
                tool_name = action_match.group(1).strip()
                tool_input = action_input_match.group(1).strip()
                
                # Clean up tool name
                tool_name = tool_name.split()[0] if " " in tool_name else tool_name
                tool_name = tool_name.replace("[", "").replace("]", "")
                tool_input = tool_input.replace("[", "").replace("]", "")

                if tool_name in self.tools:
                    try:
                        observation = self.tools[tool_name].run(tool_input)
                        sources.append(f"{tool_name}: {tool_input}")
                    except Exception as e:
                        observation = f"Error executing tool: {e}"
                    
                    messages.append(("ai", response))
                    messages.append(("human", f"Observation: {observation}"))
                else:
                    observation = f"Tool '{tool_name}' not found. Please use one of {list(self.tools.keys())}."
                    messages.append(("ai", response))
                    messages.append(("human", f"Observation: {observation}"))
            else:
                # If no action/final answer found, just return response (fallback)
                return {
                    "response": response, 
                    "sources": list(set(sources)),
                    "history": messages
                }
                
        return {
            "response": "I reached the maximum number of iterations without finding a final answer.", 
            "sources": list(set(sources)),
            "history": messages
        }
