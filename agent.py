import os
from langchain.agents import create_react_agent
from langchain.chat_models import init_chat_model
from langchain.agents import AgentExecutor
from langchain.hub import pull
from pydantic_models.required_pydantic import ToolSpec
from langchain.tools import StructuredTool
from Apis.tools_api import create_api_tool
from Database.db import add_tool, get_tool
import asyncio

agent_tools = []


async def create_tool_endpoint(tool_details: ToolSpec):
    await add_tool(tool_details)
    return {"success": "tool added and created successfully"}


async def get_tooldb():
    tools = await get_tool()
    print("calling tools ", tools, "\n")
    tool_for_agent = []
    for tool in tools:
        tool_for_agent.append(create_api_tool(spec=tool))
    print(tool_for_agent, "\n\n")
    return tool_for_agent


agent_tools = asyncio.run(get_tooldb())
print("ai wale tools", agent_tools)

llm = init_chat_model("gpt-4o")
instructions = """you are a helpful ai agent that answers query very preciously
                  you are having tools that would help you to process users query 
                """

prompt = pull("langchain-ai/react-agent-template")
print(agent_tools, "\n\n")
agent = create_react_agent(prompt=prompt, llm=llm, tools=agent_tools)
agent_executor = AgentExecutor(
    agent=agent, tools=agent_tools, handle_parsing_errors=True, max_iterations=3
)

input = "create a user whose name is kk and his email is kk@gmail.com and password is 5247423092490 role will be user"
res = agent_executor.invoke(input={"input": input, "instructions": instructions})
print(res)
