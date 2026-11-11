# Linux MCP Automation Toolkit

This project provides a set of Model Context Protocol (MCP) servers that let an AI assistant interact with a Linux development environment through structured tools, prompts, and resources. The servers expose HTTP endpoints implemented with FastMCP and can be connected to an MCP-compatible client.

## Resume-ready project points

- Built a modular MCP-based automation toolkit in Python that enables AI assistants to perform Linux file-system, project-planning, and Docker operations through structured tools.
- Developed an HTTP-based file-management server with tools for creating, reading, updating, deleting, renaming, and inspecting files and directories.
- Integrated the Docker SDK to expose container and image lifecycle operations, including login, pull, run, stop, remove, logs, statistics, build, and push workflows.
- Created reusable planning prompts that convert user objectives into step-by-step implementation plans and coordinate file-management and Docker workflows.
- Implemented MCP resources for serving reusable instructions and tool usage guidance to improve assistant context and interaction consistency.
- Configured FastMCP, Starlette CORS middleware, and Python 3.12 project environments for local HTTP-based service integration.

## Components

| Component                | Purpose                                        | Default port |
| ------------------------ | ---------------------------------------------- | -----------: |
| `file_management_server` | File and directory operations                  |         8001 |
| `docker_server`          | Docker image and container management          |         8000 |
| `planing_server`         | Project-planning prompts and tool guidance     |         8002 |
| `Resources/resources`    | Example tool, resource, and instruction server |         8000 |

## Technology stack

- Python 3.12+
- FastMCP / MCP
- Docker SDK for Python
- Starlette CORS middleware
- HTTP transport for MCP client connections

## Running a server

Each component is an independent Python project. From a component directory, install its dependencies with the project tooling and run its entry point:

```bash
cd file_management_server
uv sync
uv run python main.py
```

Use the same pattern with `docker_server`, `planing_server`, or `Resources/resources`. The Docker server requires access to a running Docker daemon. The default ports are listed above; do not run both services configured for port `8000` at the same time.

## Repository layout

```text
docker_server/              Docker MCP tools
file_management_server/     Linux file and directory MCP tools
planing_server/             Planning prompts and workflow guidance
Resources/resources/        MCP resource and instruction example
Demo/                       Experimental/demo projects
```

## Project scope

The project is designed as a local automation layer for an AI assistant. Operations are performed with the permissions of the user running each server, so deployments should add authentication, restrict CORS origins, validate paths, and apply least-privilege controls before exposing the services beyond a trusted local environment.
