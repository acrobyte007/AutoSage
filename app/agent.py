from logger.logger import get_logger
logger = get_logger(__name__)
import time
from typing import List
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from app.tools.teveli import search_and_extract_tavily
from app.tools.exa import search_and_extract

load_dotenv()

@tool
def exa_search(query: str) -> str:
    """
    Search the web using Exa.

    Best suited for:
    - Technical documentation
    - Research papers
    - Blogs
    - Tutorials
    - Long-form articles
    """

    logger.info(f"Searching Exa for: {query}")

    try:
        results = search_and_extract(query)

        if not results:
            return "No relevant results found from Exa."

        output = []

        for idx, item in enumerate(results, start=1):
            output.append(
                f"""
Result {idx}

URL:
{item['url']}

Highlights:
{item['highlights']}
"""
            )

        return "\n".join(output)

    except Exception as e:
        logger.exception(e)
        return f"Exa Search Error: {str(e)}"

@tool
def tavily_search(query: str) -> str:
    """
    Search the web using Tavily.
    Best suited for:
    - General web search
    - Current information
    - News
    - Recent events
    """
    logger.info(f"Searching Tavily for: {query}")
    try:
        results = search_and_extract_tavily(query)
        if not results:
            return "No relevant results found from Tavily."
        output = []
        for idx, item in enumerate(results, start=1):
            output.append(
                f"""
Result {idx}
URL:
{item['url']}
Content:
{item['content']}
""")

        return "\n".join(output)
    except Exception as e:
        logger.exception(e)
        return f"Tavily Search Error: {str(e)}"

mistral_primary = ChatMistralAI(
    model="ministral-8b-latest",
    temperature=0,
    max_retries=1,
)

class ResearchAgentResponse(BaseModel):
    summary: str = Field(
        description="A concise summary of the research topic, including the main points and findings."
    )
    keypoints: str = Field(
        description="A list of the most important points derived from the research, formatted as bullet points."
    )
    important_findings: str = Field(
        description="Summary of the most important information collected from different sources."
    )
    actionable_insights: str = Field(
        description="Practical recommendations based on the research findings."
    )
    urls: List[str] = Field(
        description="List of all URLs referenced in the research report."
    )

tools = [exa_search, tavily_search]
agent = create_agent(
    mistral_primary,
    tools,
    response_format=ResearchAgentResponse,
)

async def get_research_answer(
    query: str,
    conversation: List = None,
) -> str:

    SYSTEM_PROMPT = f"""
You are an autonomous AI Research Agent.
Current time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
Your job is to research the user's query using the available search tools and return a structured research report.
Available tools:
1. exa_search
Use for:
- Technical documentation
- Research papers
- Blogs
- Tutorials
- Long-form articles

2. tavily_search
Use for:
- General web search
- Current information
- News
- Recent events
- Public websites

Instructions:

- Select the most appropriate search tool.
- Use both tools whenever it improves coverage.
- Compare information from multiple sources.
- Remove duplicate or redundant information.
- Ignore irrelevant results.
- Never hallucinate or invent facts.
- Base every statement only on information returned by the tools.
- If the available information is insufficient, clearly mention the limitation.
- Extract every referenced URL from the tool outputs.

Return ONLY a response matching the ResearchAgentResponse schema.

Field requirements:
summary:
- Provide a concise summary of the research topic, including the main points and findings.
- Keep it brief and to the point.
keypoints:
- Return markdown bullet points.
- Include the most important facts only.
- Keep them concise.

important_findings:
- Write a concise summary combining information from all relevant sources.
- Do not repeat the key points verbatim.

actionable_insights:
- Provide practical recommendations or next steps when applicable.
- If no recommendation exists, return exactly:
  Not Applicable

urls:
- Return a list of every unique URL referenced during the research.
- Do not include duplicates.
- Include only valid URLs.

Do not return markdown headings such as:
# Summary
# Key Points
# References

Return only the structured fields required by the schema.
"""

    user_payload = f"""
User Query:
{query}
Conversation History:
{conversation if conversation else "No previous conversation"}
"""

    start = time.time()

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_payload,
                },
            ]
        }
    )
    logger.info(f"Research Agent raw response: {result['structured_response']}")
    end = time.time()
    logger.info(
        f"Research Agent completed in {end - start:.2f} seconds."
    )
    return result["structured_response"]