
from api.ai.llms import get_openai_llm
from api.ai.schemas import EmailMessageSchema

from api.ai.tools import (
    send_me_email,
    get_unread_emails
)

EMAIL_TOOLS = {
    "send_me_email": send_me_email,
    "get_unread_emails": get_unread_emails,
}


def email_assistant(query:str):
    llm_base = get_openai_llm()
    llm = llm_base.bind_tools(list(EMAIL_TOOLS.values())) # check for TOOL MODELING in dockerhub
    messages = [

        (
            "system",
            "You are a helpful assistant for managing my email inbox."
        ),
        ("human", f"{query}."),
    ]
    response = llm.invoke(messages)
    messages.append(response)
    if hasattr(response,"tool_calls") and response.tool_calls: # Check if AI wants to use tools
        for tool_call in response.tool_calls: # Loop through each tool call
            tool_name = tool_call.get("name")   # "get_unread_emails"
            tool_func = EMAIL_TOOLS.get(tool_name) # Gets actual Python function
            tool_args = tool_call.get('args')   # {"hours_ago": 24}
            if not tool_func:
                continue # Skip if tool doesn't exist
            tool_result = tool_func.invoke(tool_args) # Execute the function
            messages.append(tool_result)    # Add result to conversation
        final_response = llm.invoke(messages)
        return final_response
    return response