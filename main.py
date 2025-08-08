from mcp.server.fastmcp import FastMCP, Image
# from PIL import Image as PILImage

# Create an MCP server for managing a simple in-memory to-do list
mcp = FastMCP("MCP Outils LaPresse")

# In-memory storage for to-do items
todo_list = []

@mcp.tool()
def add_todo(item: str) -> str:
    """
    Add a new to-do item to the in-memory list.

    Args:
        item (str): The task to be added to the list.

    Returns:
        str: Confirmation message indicating the task was added.
    """
    todo_list.append(item)
    return f"Added to-do: '{item}'"

@mcp.tool()
def list_todos() -> str:
    """
    Retrieve the full list of current to-do items.

    Returns:
        str: Formatted string of all to-do items.
    """
    if not todo_list:
        return "Your to-do list is empty."
    return "\n".join(f"{idx+1}. {task}" for idx, task in enumerate(todo_list))

@mcp.tool()
def update_todo(index: int, new_item: str) -> str:
    """
    Update a to-do item by its index (1-based).

    Args:
        index (int): 1-based index of the item to update.
        new_item (str): The new content for the task.

    Returns:
        str: Confirmation or error message.
    """
    if 0 < index <= len(todo_list):
        old_item = todo_list[index - 1]
        todo_list[index - 1] = new_item
        return f"Updated to-do {index}: '{old_item}' -> '{new_item}'"
    return "Invalid index."

@mcp.tool()
def delete_todo(index: int) -> str:
    """
    Delete a to-do item by its index (1-based).

    Args:
        index (int): 1-based index of the task to remove.

    Returns:
        str: Confirmation or error message.
    """
    if 0 < index <= len(todo_list):
        removed = todo_list.pop(index - 1)
        return f"Deleted to-do {index}: '{removed}'"
    return "Invalid index."

@mcp.resource("todos://latest")
def get_latest_todo() -> str:
    """
    Get the most recently added to-do item.

    Returns:
        str: The latest task or a default message if list is empty.
    """
    return todo_list[-1] if todo_list else "No to-dos yet."

@mcp.prompt()
def todo_summary_prompt() -> str:
    """
    Generate a prompt asking the AI to summarize the current to-do list.

    Returns:
        str: AI-ready prompt string, or a default message if list is empty.
    """
    if not todo_list:
        return "There are no to-do items."
    return f"Summarize the following to-do items: {', '.join(todo_list)}"



@mcp.tool()
def create_plan_media(
    target_users: str = None,
    budget: str = None,
    timeline: str = None,
    preferred_section: str = None
) -> dict:
    """
    Generate a media plan including:
    - Target users
    - Budget
    - Timeline
    - Preferred section (e.g., Sports, Actuality, Politics)

    All fields are required. If any are missing, instruct the user to provide them.

    Args:
        target_users (str): The type of users to target.
        budget (str): The marketing budget. Always in Canadian dollars.
        timeline (str): The marketing timeline.
        preferred_section (str): Section de préférence(Sports, Actualité, Politique, etc.)

    Returns:
        dict: Structured media plan or instructions for missing fields.

        Always respond in french.
    """
    missing = []
    if not target_users:
        missing.append("1. Quel type d'utilisateurs souhaitez-vous cibler?")
    if not budget:
        missing.append("2. Quel est votre budget marketing?")
    if not timeline:
        missing.append("3. Quel est votre calendrier marketing?")
    if not preferred_section:
        missing.append("4. Avez-vous une section de préférence (Sports, Actualité, Politique, etc.)?")

    if missing:
        return {
            "error": "Informations requises manquantes.",
            "instruction": "Veuillez répondre aux questions suivantes :\n" + "\n".join(missing)
        }

    return {
        "media_plan": {
            "target_users": target_users,
            "budget": budget,
            "timeline": timeline,
            "preferred_section": preferred_section
        },
        "message": "Here is your structured media plan."
    }



@mcp.tool()
def list_available_tools() -> dict:
    """
    List all available MCP tools for the user.

    Returns:
        dict: Tool names and their descriptions.
    """
    return {
        tool.name: tool.__doc__ or "No description."
        for tool in mcp.tools
    }



