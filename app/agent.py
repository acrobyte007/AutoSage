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
    answer: str = Field(
        description="Structured research report with URLs included in references."
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

    SYSTEM_PROMPT = """
You are an autonomous AI Research Agent.
Your task is to independently research the user's topic using the available search tools and generate a structured research report.
and current time is {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}.
You have access to two tools:
1. exa_search
   Use for:
   - Technical documentation
   - Research papers
   - Tutorials
   - Blogs
   - Long-form articles
2. tavily_search
   Use for:
   - General web search
   - Current information
   - Recent news
   - Public websites
Guidelines:
- Select the most appropriate tool based on the user's query.
- If needed, use BOTH tools to gather more comprehensive information.
- Compare information from multiple sources.
- Remove duplicate or redundant information.
- Ignore irrelevant content.
- Never invent or hallucinate facts.
- Base your response only on information returned by the tools.
Return your answer using the following structure.
# Summary
Provide a concise overview.
# Key Points
- Bullet point
- Bullet point
- Bullet point
# Important Findings
Summarize the most important information collected from different sources.
# References
List every URL referenced during your research as a bulleted list with the URL and a brief description.
# Actionable Insights
Provide practical recommendations if applicable.
If no actionable insight exists, write:
Not Applicable
Formatting Rules
- Use Markdown.
- Use headings.
- Use bullet points.
- Avoid repetition.
- Keep the report concise and professional.
- Include all URLs in the References section.
- The URLs field must contain all URLs mentioned in the report.
"""

    user_payload = f"""
User Query:
{query}
Conversation History:
{conversation if conversation else "No previous conversation"}
Current Time:
{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
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

    end = time.time()
    logger.info(
        f"Research Agent completed in {end - start:.2f} seconds."
    )
    return result["structured_response"]