from fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware


mcp = FastMCP(
    name="Planning Server"
)

@mcp.prompt()
def setup_project_environment():
    """
    Steps to set up a new project environment:
    1. Ask the user for the project name and technology stack.
    2. Create a new directory for the project.
    3. Initialize a virtual environment or container.
    4. Install dependencies as listed in requirements.txt or package.json.
    5. Run initial setup scripts and verify configuration.
    """


@mcp.prompt()
def generate_plan(user_objective: str):
    """
    Create a detailed step-by-step plan based on the user's objective.
    Example: 'Build a weather forecasting web app.'
    """
    return f"Here’s a step-by-step plan to achieve: {user_objective}"



@mcp.prompt()
def setup_and_plan(objective: str):
    plan = generate_plan(objective)
    steps = manual_to_use_planning_tools()
    return f"{plan}\n\nNext, follow these steps:\n{steps}"




@mcp.prompt()
def manual_to_use_planning_tools():
    planning_steps = """
    1) First You need to Understand the User's Objective.
    2) Build a step-by-step plan to achieve the objective.
    3) Architect the plan into smaller manageable tasks.
    4) Check that all the required tools are available to accomplish the plan.
    5) Plan the Structure of the Directories and Files needed.
    6) Use the file and directory management tools to create the necessary files and directories.
    7) Then start Coding based on the plan.
    8) Populate the files with relevant content.
    9) Review the plan and make adjustments as necessary.
    10) Dockerize the application if needed using Docker management tools.
    11) Finally, Test the application to ensure it meets the user's objective.
    """
    return planning_steps


@mcp.prompt()
def manual_to_use_file_management_tools():
    '''
    You are a helpful assistant that provides users with a list of available file and directory management tools 
    and their descriptions. The alignment is in JSON format as a list of objects with 
    "name", "description", and "function signature" fields.

    Example:
    [
        {
            "name": "create_file",
            "description": "Creates a new file with the specified name and content.",
            "function signature": "def create_file(name: str, content: str):"
        }
    ]
    '''

    return [
        # ------------------- FILE OPERATIONS -------------------
        {
            "name": "create_file",
            "description": "Creates a new file with the specified name and content.",
            "function signature": "def create_file(name: str, content: str):"
        },
        {
            "name": "read_file",
            "description": "Reads and returns the content of a specified file.",
            "function signature": "def read_file(path: str):"
        },
        {
            "name": "clear_file",
            "description": "Clears all content from the specified file.",
            "function signature": "def clear_file(path: str):"
        },
        {
            "name": "clear_and_write_file",
            "description": "Clears existing content of a file and writes new content to it.",
            "function signature": "def clear_and_write_file(path: str, content: str):"
        },
        {
            "name": "append_to_file",
            "description": "Appends new content to the end of a specified file.",
            "function signature": "def append_to_file(path: str, content: str):"
        },
        {
            "name": "update_exact_match_of_old_and_new_content_in_the_file",
            "description": "Searches for exact old content in a file and replaces it with new content.",
            "function signature": "def update_exact_match_of_old_and_new_content_in_the_file(path: str, old_content: str, new_content: str):"
        },
        {
            "name": "delete_file",
            "description": "Deletes the specified file from the system.",
            "function signature": "def delete_file(path: str):"
        },
        {
            "name": "rename_file",
            "description": "Renames a file from an old name to a new name.",
            "function signature": "def rename_file(old_name: str, new_name: str):"
        },
        {
            "name": "list_files",
            "description": "Lists all files in the current working directory.",
            "function signature": "def list_files():"
        },
        {
            "name": "get_file_content",
            "description": "Retrieves and returns the content of a specified file.",
            "function signature": "def get_file_content(path: str):"
        },
        {
            "name": "get_file_extension",
            "description": "Returns the extension of a specified file.",
            "function signature": "def get_file_extension(path: str):"
        },
        {
            "name": "get_file_size",
            "description": "Returns the size (in bytes) of a specified file.",
            "function signature": "def get_file_size(path: str):"
        },
        {
            "name": "get_file_info",
            "description": "Provides detailed information about a file, including size and last modified time.",
            "function signature": "def get_file_info(path: str):"
        },
        {
            "name": "is_file_exists",
            "description": "Checks if a specified file exists on the server.",
            "function signature": "def is_file_exists(path: str):"
        },

        # ------------------- DIRECTORY OPERATIONS -------------------
        {
            "name": "create_directory",
            "description": "Creates a new directory with the specified name.",
            "function signature": "def create_directory(name: str):"
        },
        {
            "name": "delete_directory",
            "description": "Deletes the specified directory from the server.",
            "function signature": "def delete_directory(name: str):"
        },
        {
            "name": "list_directories",
            "description": "Lists all directories in the current working directory.",
            "function signature": "def list_directories():"
        },
        {
            "name": "get_directory_info",
            "description": "Provides size and last modified time information for a specified directory.",
            "function signature": "def get_directory_info(name: str):"
        },
        {
            "name": "rename_directory",
            "description": "Renames a directory from an old name to a new name.",
            "function signature": "def rename_directory(old_name: str, new_name: str):"
        },
        {
            "name": "get_current_working_directory",
            "description": "Returns the current working directory of the server.",
            "function signature": "def get_current_working_directory():"
        },
        {
            "name": "change_working_directory",
            "description": "Changes the server's current working directory to a specified path.",
            "function signature": "def change_working_directory(path: str):"
        },
        {
            "name": "list_files_and_folders",
            "description": "Lists all files and folders inside a specified directory.",
            "function signature": "def list_files_and_folders(directory_path: str):"
        },
        {
            "name": "is_directory",
            "description": "Checks whether a given path is a directory.",
            "function signature": "def is_directory(path: str):"
        }
    ]


@mcp.prompt()
def manual_to_use_docker_management_tools():
    '''
    You are a helpful assistant that provides users with a list of available Docker management tools 
    and their descriptions. The alignment is in JSON format as a list of objects with 
    "name", "description", and "function signature" fields.

    Example:
    [
        {
            "name": "docker_login",
            "description": "Login to a Docker registry using the provided username and password.",
            "function signature": "def docker_login(username: str, password: str, registry: str = 'https://index.docker.io/v1/'):"
        }
    ]
    '''
    return [
        {
            "name": "docker_login",
            "description": "Login to a Docker registry using the provided username and password.",
            "function signature": "def docker_login(username: str, password: str, registry: str = 'https://index.docker.io/v1/'):"
        },
        {
            "name": "docker_logout",
            "description": "Logout from a Docker registry.",
            "function signature": "def docker_logout(registry: str = 'https://index.docker.io/v1/'):"
        },
        {
            "name": "list_docker_images",
            "description": "List all Docker images on the host.",
            "function signature": "def list_docker_images():"
        },
        {
            "name": "pull_docker_image_from_registry",
            "description": "Pull a Docker image from a registry.",
            "function signature": "def pull_docker_image_from_registry(image_name: str, tag: str = 'latest'):"
        },
        {
            "name": "run_docker_container",
            "description": "Run a Docker container from an image.",
            "function signature": "def run_docker_container(image_name: str, container_name: str, command: str = None, ports: dict = None, tty: bool = False, stdin_open: bool = False):"
        },
        {
            "name": "list_running_containers",
            "description": "List all running Docker containers on the host.",
            "function signature": "def list_running_containers():"
        },
        {
            "name": "list_all_containers",
            "description": "List all Docker containers on the host, including stopped ones.",
            "function signature": "def list_all_containers():"
        },
        {
            "name": "stop_docker_container",
            "description": "Stop a running Docker container.",
            "function signature": "def stop_docker_container(container_id: str):"
        },
        {
            "name": "remove_docker_container",
            "description": "Remove a Docker container, with optional force removal.",
            "function signature": "def remove_docker_container(container_id: str, force: bool = False):"
        },
        {
            "name": "remove_docker_image",
            "description": "Remove a Docker image from the host, with optional force removal.",
            "function signature": "def remove_docker_image(image_name: str, force: bool = False):"
        },
        {
            "name": "get_docker_container_id",
            "description": "Get the ID of a Docker container by name.",
            "function signature": "def get_docker_container_id(container_name: str):"
        },
        {
            "name": "rename_docker_container_with_tag",
            "description": "Rename a Docker container and tag its image.",
            "function signature": "def rename_docker_container_with_tag(container_id: str, new_name: str, tag: str):"
        },
        {
            "name": "push_docker_image",
            "description": "Push a Docker image to a registry.",
            "function signature": "def push_docker_image(image_name: str, tag: str, registry: str, username: str, password: str):"
        },
        {
            "name": "dockerization",
            "description": "Dockerize a Python application by building an image from a Dockerfile.",
            "function signature": "def dockerization(path_to_dockerfile: str, name: str):"
        },
        {
            "name": "get_docker_container_logs",
            "description": "Get logs from a Docker container.",
            "function signature": "def get_docker_container_logs(container_id: str, tail: int = 100):"
        },
        {
            "name": "get_docker_container_stats",
            "description": "Retrieve detailed stats (CPU, memory, etc.) from a Docker container.",
            "function signature": "def get_docker_container_stats(container_id: str):"
        }
    ]


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8002,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ],
    )

