# AI-agent-based-Deep-Research

This project implements a multi-agent system for gathering information from websites and drafting a summary. The system uses LangGraph for defining the workflow of agents and Pydantic for data validation.

Key Components:
1. Research Agent: This agent crawls a list of URLs provided by the user and collects the first few paragraphs of content from each webpage. It uses the requests library to make HTTP requests and BeautifulSoup to parse and extract the relevant text.

2. Drafting Agent: Once the research agent has gathered information, the drafting agent takes over. It combines all the gathered paragraphs into one text, cleans it by removing excessive whitespace, and then drafts a summary. If the content exceeds 1000 characters, it truncates the text for brevity.

3. LangGraph Workflow: The system is built using LangGraph, a tool that allows the creation of workflows using multiple agents. The workflow consists of two nodes:
ResearchAgent: Starts the process by gathering information.
DraftingAgent: Compiles the gathered content into a summary.
END: Marks the end of the workflow.

4. Data Flow: 
The ResearchState class holds the state of the entire process, including the list of URLs, gathered information, and the final drafted summary.
The ResearchAgent collects the content and updates the state.
The DraftingAgent processes the gathered data and provides the final output, which is the summary of the gathered content.

Workflow in Action:
The user provides a list of URLs.

1. The Research Agent crawls each website and gathers the text from the first 5 paragraphs.
2. The Drafting Agent compiles all the gathered information, cleans it, and drafts a concise summary.
3. The final summary is printed as the output.
