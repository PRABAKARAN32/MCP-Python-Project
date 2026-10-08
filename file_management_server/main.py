import os
from fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

mcp = FastMCP(name="File Management Server")

# File Operations
@mcp.tool(name="create_file", description='''
 Create a file with the specified name and content.
 This tool allows you to create a file on the server with the given name and content.
 The file will be created in the current working directory of the server.
 Example usage:
    create_file(name="example.txt", content="Hello, World!")
''')
async def create_file(name: str, content: str):
    with open(name, "w") as f:
        f.write(content)
    return {"message": "File created successfully."}

@mcp.tool(name="read_file", description='''
    Read the content of a file with the specified name.
    This tool allows you to read the content of a file on the server.
    Example usage:
        read_file(path="/path/to/file.txt")
''')
async def read_file(path: str):
    if not os.path.exists(path):
        return {"error": "File does not exist."}
    with open(path, "r") as f:
        content = f.read()
    return {"content": content}

@mcp.tool(name="clear_file", description='''
    Clear the content of a file with the specified name.
    This tool allows you to clear the content of a file on the server.
    Example usage:
        clear_file(path="/path/to/file.txt")
''')
async def clear_file(path: str):
    if not os.path.exists(path):
        return {"error": "File does not exist."}
    with open(path, "w") as f:
        f.write("")  # Clear the content by writing an empty string
    return {"message": "File cleared successfully."}

@mcp.tool(name="clear_and_write_file", description='''
          Clear the content of a file and write new content to it.
          This tool allows you to clear the content of a file and then write new content to it.
          Example usage:
              clear_and_write_file(path="/path/to/file.txt", content="New content")
          ''')
async def clear_and_write_file(path: str, content: str):
    if not os.path.exists(path):
        return {"error": "File does not exist."}
    with open(path, "w") as f:
        f.write(content)  # Clear the content and write new content
    return {"message": "File cleared and new content written successfully."}

@mcp.tool(name="append_to_file", description='''
          Append content to a file with the specified name.
          This tool allows you to append content to a file on the server.
          Example usage:
              append_to_file(path="/path/to/file.txt", content="Additional text")
''')
async def append_to_file(path: str, content: str):
    if not os.path.exists(path):
        return {"error": "File does not exist."}
    with open(path, "a") as f:  # Open the file in append mode
        f.write(content + "\n")  # Append content with a newline
    return {"message": "Content appended successfully."}

@mcp.tool(name="update_exact_match_of_old_and_new_content_in_the_file", description='''
    Update the content of a file by replacing old content with new content.
    This tool allows you to search for old content in a file and replace it with new content.
    Example usage:
        update_exact_match_of_old_and_new_content_in_the_file(path="/path/to/file.txt", old_content="old text", new_content="new text")
''')
async def update_exact_match_of_old_and_new_content_in_the_file(path: str, old_content: str, new_content: str):
    if not os.path.exists(path):
        return {"error": "File does not exist."}
    with open(path, "r") as f:
        content = f.read()
    if old_content not in content:
        return {"error": "Old content not found in the file."}
    content = content.replace(old_content, new_content)
    with open(path, "w") as f:
        f.write(content)
    return {"message": "File content updated successfully."}

@mcp.tool(name="delete_file", description='''
    Delete a file with the specified name.
    This tool allows you to delete a file on the server.
    Example usage:
        delete_file(path="/path/to/file.txt")
''')
async def delete_file(path: str):
    if not os.path.exists(path):
        return {"error": "File does not exist."}
    os.remove(path)
    return {"message": "File deleted successfully."}

@mcp.tool(name="rename_file", description='''
          Rename a file from old name to new name.
          This tool allows you to rename a file on the server.
          Example usage:
              rename_file(old_name="old_file.txt", new_name="new_file.txt")
          ''')
async def rename_file(old_name: str, new_name: str):
    if not os.path.exists(old_name):
        return {"error": "Old file does not exist."}
    if os.path.exists(new_name):
        return {"error": "New file name already exists."}
    os.rename(old_name, new_name)
    return {"message": "File renamed successfully."}

@mcp.tool(name="list_files", description='''
    List all files in the current working directory.
    This tool allows you to list all files in the current working directory of the server.
    Example usage:
        list_files()
''')
async def list_files():
    files = os.listdir(".")
    return {"files": files}


@mcp.tool(name="get_file_content", description='''    Get the content of a file with the specified name.
    This tool allows you to get the content of a file on the server.
    Example usage:
        get_file_content(path="/path/to/file.txt")
''')
async def get_file_content(path: str):
    if not os.path.exists(path):
        return {"error": "File does not exist."}
    with open(path, "r") as f:
        content = f.read()
    return {"content": content}

@mcp.tool(name="get_file_extension", description='''
            Get the extension of a file with the specified name.
          This tool allows you to get the extension of a file on the server.
          Example usage:
              get_file_extension(path="/path/to/file.txt")
''')
async def get_file_extension(path: str):
    if not os.path.exists(path):
        return {"error": "File does not exist."}
    _, extension = os.path.splitext(path)
    return {"extension": extension if extension else "No extension found."}

@mcp.tool(name="get_file_size", description='''
    Get the size of a file with the specified name.
    This tool allows you to get the size of a file on the server.
    Example usage:
        get_file_size(path="/path/to/file.txt")
''')
async def get_file_size(path: str):
    if not os.path.exists(path):
        return {"error": "File does not exist."}
    size = os.path.getsize(path)
    return {"size": size}


@mcp.tool(name="get_file_info", description='''    Get information about a file with the specified name.
    This tool allows you to get information about a file on the server, including its size and last modified time.
    Example usage:
        get_file_info(path="/path/to/file.txt") 
''')
async def get_file_info(path: str):
    if not os.path.exists(path):
        return {"error": "File does not exist."}
    size = os.path.getsize(path)
    last_modified = os.path.getmtime(path)
    return {
        "size": size,
        "last_modified": last_modified,
        "message": "File information retrieved successfully."
    }

@mcp.tool(name="is_file_exists", description='''
          Check if a file with the specified name exists.
          This tool allows you to check if a file exists on the server.
          Example usage:
              is_file_exists(path="/path/to/file.txt")
''')
async def is_file_exists(path: str):
    if os.path.exists(path):
        return {"exists": True, "message": "File exists."}
    else:
        return {"exists": False, "message": "File does not exist."}

#Directory Operations
@mcp.tool(name="create_directory", description='''
    Create a directory with the specified name.
    This tool allows you to create a directory on the server with the given name.
    Example usage:
        create_directory(name="example_directory")
''')
async def create_directory(name: str):
    if not os.path.exists(name):
        os.makedirs(name)
        return {"message": "Directory created successfully."}
    return {"error": "Directory already exists."}

@mcp.tool(name="delete_directory", description='''
    Delete a directory with the specified name.
    This tool allows you to delete a directory on the server.
    Example usage:
        delete_directory(name="example_directory")
''')
async def delete_directory(name: str):
    if os.path.exists(name):
        os.rmdir(name)
        return {"message": "Directory deleted successfully."}
    return {"error": "Directory does not exist."}

@mcp.tool(name="list_directories", description='''
    List all directories in the current working directory.
    This tool allows you to list all directories in the current working directory of the server.
    Example usage:
        list_directories()
''')
async def list_directories():
    directories = [d for d in os.listdir(".") if os.path.isdir(d)]
    return {"directories": directories}

@mcp.tool(name="get_directory_info", description='''
    Get information about a directory with the specified name.
    This tool allows you to get information about a directory on the server, including its size and last modified time.
    Example usage:
        get_directory_info(name="example_directory")
''')
async def get_directory_info(name: str):
    if not os.path.exists(name):
        return {"error": "Directory does not exist."}
    size = sum(os.path.getsize(os.path.join(name, f)) for f in os.listdir(name) if os.path.isfile(os.path.join(name, f)))
    last_modified = os.path.getmtime(name)
    return {
        "size": size,
        "last_modified": last_modified,
        "message": "Directory information retrieved successfully."
    }


@mcp.tool(name="rename_directory", description='''
          Rename a directory from old name to new name.
    This tool allows you to rename a directory on the server.
    Example usage:
        rename_directory(old_name="old_directory", new_name="new_directory")
''')
async def rename_directory(old_name: str, new_name: str):
    if not os.path.exists(old_name):
        return {"error": "Old directory does not exist."}
    if os.path.exists(new_name):
        return {"error": "New directory name already exists."}
    os.rename(old_name, new_name)
    return {"message": "Directory renamed successfully."}

@mcp.tool(name="get_current_working_directory", description='''
          Get the current working directory of the server.
    This tool allows you to get the current working directory of the server.
    Example usage:
        get_current_working_directory()
''')
async def get_current_working_directory():
    cwd = os.getcwd()
    return {"current_working_directory": cwd}

@mcp.tool(name="change_working_directory", description='''
    Change the current working directory of the server to the specified path.
    This tool allows you to change the current working directory of the server.
    Example usage:
        change_working_directory(path="/path/to/new/directory")
''')
async def change_working_directory(path: str):
    if not os.path.exists(path):
        return {"error": "Directory does not exist."}
    os.chdir(path)
    return {"message": "Current working directory changed successfully.", "new_directory": os.getcwd()}

@mcp.tool(name="list_files_and_folders", description='''
    List all files and folders in the specified directory.
    This tool allows you to list all files and folders in a specified directory.
    Example usage:
        list_files_and_folders(directory_path="/path/to/directory")
''')
async def list_files_and_folders(directory_path: str):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        items = os.listdir(directory_path)
        print(f"Files and folders in directory {directory_path}: {items}")
        return items
    else:
        print(f"Directory does not exist at: {directory_path}")
        return []


@mcp.tool(name="is_directory", description='''
    Check if the specified path is a directory.
    This tool allows you to check if a given path is a directory.
    Example usage:
        is_directory(path="/path/to/directory")
''')
async def is_directory(path: str):
    is_dir = os.path.isdir(path)
    return {"is_directory": is_dir, "message": f"Is path a directory {path}: {is_dir}"}


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8001,
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


