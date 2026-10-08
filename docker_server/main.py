from fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
import docker as docker_server
import os
import tempfile


client = docker_server.from_env()

mcp = FastMCP(name="Docker Server")


@mcp.tool(name="docker_login", 
          description='''
    Login to a Docker registry using the provided username and password.

    Arguments:
    - username: Docker registry username.
    - password: Docker registry password.
    - registry: Docker registry URL (default is Docker Hub).

                            Example:
            ----------------------------------------------------
                        {
                            "username": "username",
                            "password": "Password",
                            "registry": "https://index.docker.io/v1/"
                        }
            ----------------------------------------------------
    '''
)
def docker_login(username: str, password: str, registry: str = "https://index.docker.io/v1/"):

    
    if not username or not password:
        return "Username and password are required"
    try:
        client.login(username=username, password=password, registry=registry)
        return "Login successful"
    except docker_server.errors.APIError as e:
        return f"Login failed: {str(e)}"
    
@mcp.tool(name="docker_logout", 
          description='''
    Logout from a Docker registry.

    Arguments:
    - registry: Docker registry URL (default is Docker Hub).

                            Example:
            ----------------------------------------------------
                        {
                            "registry": "https://index.docker.io/v1/"
                        }
            ----------------------------------------------------
    '''
)
def docker_logout(registry: str = "https://index.docker.io/v1/"):
    try:
        client.logout(registry=registry)
        return "Logout successful"
    except docker_server.errors.APIError as e:
        return f"Logout failed: {str(e)}"
    
@mcp.tool(name="list_docker_images", 
          description='''
    List all Docker images on the host.

    Returns a list of all Docker images available on the host.
    '''
)
def list_docker_images():
    '''
    List all Docker images on the host.
    '''
    try:
        images = client.images.list()
        image_list = [image.tags for image in images]
        return image_list
    except docker_server.errors.APIError as e:
        return f"Failed to list images: {str(e)}"


@mcp.tool(name="pull_docker_image_from_registry", 
          description='''
    Pull a Docker image from a registry.

    Arguments:
    - image_name: Name of the Docker image to pull.
    - tag: Tag of the Docker image (default is "latest").

                            Example:
            ----------------------------------------------------
                        {
                            "image_name": "httpd",
                            "tag": "latest"
                        }
            ----------------------------------------------------
    '''
)
def pull_docker_image_from_registry(image_name: str, tag: str = "latest"):


    # if already exists, skip
    existing_images = client.images.list(name=f"{image_name}:{tag}")
    if existing_images:
        return f"Image {image_name}:{tag} already exists"
    try:
        client.images.pull(f"{image_name}:{tag}")
        return f"Successfully pulled image: {image_name}:{tag}"
    except docker_server.errors.APIError as e:
        return f"Failed to pull image: {str(e)}"

@mcp.tool(name="run_docker_container", 
          description='''
    Run a Docker container from an image.

    Arguments:
    - image_name: Name of the Docker image to run.
    - command: Command to run in the container (optional).
    - ports: Dictionary of port mappings (optional).
    - tty: Allocate a pseudo-TTY (optional) and it is used to run the container in -t flag.
    - stdin_open: Keep STDIN open even if not attached (optional) and it is used to run the container in -i flag.

                                Example:
            ----------------------------------------------------

                    {
                        "image_name": "httpd",
                        "container_name": "my_httpd_container",
                        "command": null,
                        "ports": {
                            "80/tcp": 8001
                        },
                        "tty": true,
                        "stdin_open": true
                    }

            ----------------------------------------------------
    '''
)
def run_docker_container(image_name: str, container_name: str, command: str = None, ports: dict = None, tty: bool = False, stdin_open: bool = False):
    
    try:
        container = client.containers.run(
            image_name,
            name=container_name,
            command=command,
            detach=True,
            ports=ports,
            tty=tty,
            stdin_open=stdin_open
        )
        return f"Container started with ID: {container.id}"
    except docker_server.errors.APIError as e:
        return f"Failed to run container: {str(e)}"


@mcp.tool(name="list_running_containers",
            description='''    List all running Docker containers on the host.
    '''
)   
def list_running_containers():
    try:
        containers = client.containers.list()
        container_list = [container.name for container in containers]
        return container_list
    except docker_server.errors.APIError as e:
        return f"Failed to list containers: {str(e)}"

@mcp.tool(name="list_all_containers",
            description='''    List all Docker containers on the host.
    '''
)
def list_all_containers():
    try:
        containers = client.containers.list(all=True)
        container_list = [container.name for container in containers]
        return container_list
    except docker_server.errors.APIError as e:
        return f"Failed to list containers: {str(e)}"

@mcp.tool(name="stop_docker_container",
            description='''    Stop a running Docker container.
    '''
)
def stop_docker_container(container_id: str):

    try:
        container = client.containers.get(container_id)
        container.stop()
        return f"Container {container_id} stopped successfully"
    except docker_server.errors.APIError as e:
        return f"Failed to stop container: {str(e)}"
    except docker_server.errors.NotFound:
        return f"Container {container_id} not found"

@mcp.tool(name="remove_docker_container",
            description='''    Remove a Docker container and optionally force removal.
    ''')
def remove_docker_container(container_id: str, force: bool = False):

    try:
        container = client.containers.get(container_id)
        container.remove(force=force)
        return f"Container {container_id} removed successfully"
    except docker_server.errors.APIError as e:
        return f"Failed to remove container: {str(e)}"
    except docker_server.errors.NotFound:
        return f"Container {container_id} not found"

@mcp.tool(name="remove_docker_image",
            description='''    Remove a Docker image and optionally force removal.
    ''')
def remove_docker_image(image_name: str, force: bool = False):
    '''
    Remove a Docker image.
    '''
    try:
        client.images.remove(image=image_name, force=force)
        return f"Image {image_name} removed successfully"
    except docker_server.errors.APIError as e:
        return f"Failed to remove image: {str(e)}"
    except docker_server.errors.ImageNotFound:
        return f"Image {image_name} not found"

@mcp.tool(name="get_docker_container_id",
            description='''    Get the ID of a Docker container by name.
    ''')
def get_docker_container_id(container_name: str):
    '''
    Get the ID of a Docker container by name.
    '''
    try:
        container = client.containers.get(container_name)
        return container.id
    except docker_server.errors.APIError as e:
        return f"Failed to get container ID: {str(e)}"
    except docker_server.errors.NotFound:
        return f"Container {container_name} not found"

@mcp.tool(name="rename_docker_container_with_tag",
            description='''    Rename a Docker container with a tag for the Docker image.
    ''')
def list_all_containers():
    try:
        containers = client.containers.list(all=True)
        container_list = [container.name for container in containers]
        return container_list
    except docker_server.errors.APIError as e:
        return f"Failed to list containers: {str(e)}"

@mcp.tool(name="rename_docker_container_with_tag",
            description='''    Rename a Docker container with a tag for the Docker image. the input are the container id, new name and tag.
    Example:
            ----------------------------------------------------
                        {                            "container_id": "1234567890ab",
                            "new_name": "my_new_container",
                            "tag": "my_new_tag"
                        }
            ----------------------------------------------------
    ''')
def rename_docker_container_with_tag(container_id: str, new_name: str, tag: str):
    try:
        container = client.containers.get(container_id)
        container.rename(new_name)
        client.images.tag(container.image, tag)
        return f"Container {container_id} renamed to {new_name} and tagged with {tag}"
    except docker_server.errors.APIError as e:
        return f"Failed to rename container: {str(e)}"
    except docker_server.errors.NotFound:
        return f"Container {container_id} not found"

@mcp.tool(name="push_docker_image",
            description='''    Push a Docker image to a registry.
    Example:
            ----------------------------------------------------
                        {                            "image_name": "my_app_image",
                            "tag": "latest",
                            "registry": "myregistry.com",
                            "username": "my_username",
                            "password": "my_password"
                        }
            ----------------------------------------------------
    ''')
def push_docker_image(image_name: str, tag: str, registry: str, username: str, password: str):
    '''
    Push a Docker image to a registry.
    '''
    try:
        client.images.push(repository=f"{registry}/{image_name}", tag=tag, auth=(username, password))
        return f"Image {image_name}:{tag} pushed to {registry} successfully"
    except docker_server.errors.APIError as e:
        return f"Failed to push image: {str(e)}"

@mcp.tool(name="dockerization" , description='''    Dockerize a Python application by creating a Dockerfile and building the image.
    Example:
            ----------------------------------------------------
                        dockerization(path_to_dockerfile="/path/to/Dockerfile",
                                    name="my_app_image")
            ----------------------------------------------------
    ''')
def dockerization(path_to_dockerfile: str, name: str):
    '''
    Dockerize a Python application by creating a Dockerfile and building the image.
    '''
    if not os.path.exists(path_to_dockerfile):
        return f"Dockerfile not found at {path_to_dockerfile}"

    try:
        with open(path_to_dockerfile, 'r') as file:
            dockerfile_content = file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.Dockerfile') as temp_file:
            temp_file.write(dockerfile_content.encode('utf-8'))
            temp_file_path = temp_file.name

        client.images.build(path=os.path.dirname(temp_file_path), dockerfile=os.path.basename(temp_file_path), tag=name)
        os.remove(temp_file_path)
        return f"Image {name} built successfully"
    except docker_server.errors.APIError as e:
        return f"Failed to build image: {str(e)}"
    

@mcp.tool(name="get_docker_container_logs",
            description='''    Get logs from a Docker container.
    Example:
            ----------------------------------------------------
                        {                            "container_id": "1234567890ab",
                            "tail": 100
                        }
            ----------------------------------------------------
    ''')
def get_docker_container_logs(container_id: str, tail: int = 100):
    '''
    Get logs from a Docker container.
    '''
    try:
        container = client.containers.get(container_id)
        logs = container.logs(tail=tail)
        return logs.decode('utf-8')
    except docker_server.errors.APIError as e:
        return f"Failed to get logs: {str(e)}"
    except docker_server.errors.NotFound:
        return f"Container {container_id} not found"
    
@mcp.tool(name="get_docker_container_stats",
            description='''    Get stats from a Docker container.
    Example:
            ----------------------------------------------------
                        {                            "container_id": "1234567890ab"
                        }
            ----------------------------------------------------
    ''')
def get_docker_container_stats(container_id: str):
    '''
    Get stats from a Docker container.
    '''
    try:
        container = client.containers.get(container_id)
        stats = container.stats(stream=False)
        return stats
    except docker_server.errors.APIError as e:
        return f"Failed to get stats: {str(e)}"
    except docker_server.errors.NotFound:
        return f"Container {container_id} not found"
    

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
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

