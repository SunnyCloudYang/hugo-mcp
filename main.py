from typing import Any, Dict, Optional
from mcp.server.fastmcp import FastMCP
from utils import (
    get_system_info,
    check_hugo_installation,
    check_go_installation,
    check_git_installation,
    create_site,
    create_post,
    list_content,
    start_preview,
    stop_preview,
    build_site,
    list_themes,
    install_theme,
    update_theme,
    get_theme_details,
    deploy_to_github_pages,
    deploy_to_netlify,
    deploy_to_vercel,
    deploy_to_custom,
)

# Initialize MCP server
mcp = FastMCP("hugo-mcp")


# System information tools
@mcp.tool(
    name="get_system_info",
    description="Get system information",
)
async def get_system_info_tool() -> dict:
    return await get_system_info()


@mcp.tool(
    name="check_hugo_installation",
    description="Check if Hugo is installed and get its version",
)
async def check_hugo_installation_tool() -> Dict[str, Any]:
    return await check_hugo_installation()


@mcp.tool(
    name="check_go_installation",
    description="Check if Go is installed and get its version",
)
async def check_go_installation_tool() -> Dict[str, Any]:
    return await check_go_installation()


@mcp.tool(
    name="check_git_installation",
    description="Check if Git is installed and get its configuration",
)
async def check_git_installation_tool() -> Dict[str, Any]:
    return await check_git_installation()


# Hugo site management tools
@mcp.tool(name="create_site", description="Create a new Hugo site")
async def create_site_tool(
    site_abs_path: str,
    site_name: str,
    force: bool = False,
    in_current_dir: bool = False,
) -> Dict[str, Any]:
    return await create_site(site_abs_path, site_name, force, in_current_dir)


@mcp.tool(name="create_post", description="Create a new Hugo post")
async def create_post_tool(
    site_path: str,
    post_title: str,
    content_type: str = "posts",
    draft: bool = True,
    date: Optional[str] = None,
) -> Dict[str, Any]:
    return await create_post(site_path, post_title, content_type, draft, date)


@mcp.tool(name="list_content", description="List content in the Hugo site")
async def list_content_tool(
    site_path: str, content_type: Optional[str] = None
) -> Dict[str, Any]:
    return await list_content(site_path, content_type)


@mcp.tool(name="start_preview", description="Start Hugo local server for preview")
async def start_preview_tool(
    site_path: str,
    port: int = 1313,
    bind: str = "127.0.0.1",
    build_drafts: bool = False,
    build_future: bool = False,
    build_expired: bool = False,
) -> Dict[str, Any]:
    return await start_preview(
        site_path, port, bind, build_drafts, build_future, build_expired
    )


@mcp.tool(name="stop_preview", description="Stop a running Hugo preview server")
async def stop_preview_tool(pid: int) -> Dict[str, Any]:
    return await stop_preview(pid)


@mcp.tool(name="build_site", description="Build the Hugo site for production")
async def build_site_tool(
    site_path: str,
    destination: str = "public",
    clean_destination: bool = False,
    minify: bool = False,
) -> Dict[str, Any]:
    return await build_site(site_path, destination, clean_destination, minify)


# Theme management tools
@mcp.tool(
    name="list_themes",
    description="List available Hugo themes from the official Hugo themes website",
)
async def list_themes_tool() -> Dict[str, Any]:
    return await list_themes()


@mcp.tool(name="install_theme", description="Install a Hugo theme")
async def install_theme_tool(
    site_path: str, theme_name: str, theme_url: str, use_go_module: bool = False
) -> Dict[str, Any]:
    return await install_theme(site_path, theme_name, theme_url, use_go_module)


@mcp.tool(name="update_theme", description="Update an installed Hugo theme")
async def update_theme_tool(
    site_path: str, theme_name: str, use_modules: bool = False
) -> Dict[str, Any]:
    return await update_theme(site_path, theme_name, use_modules)


@mcp.tool(
    name="get_theme_details",
    description="Get detailed information about a specific Hugo theme",
)
async def get_theme_details_tool(theme_name: str) -> Dict[str, Any]:
    return await get_theme_details(theme_name)


# Deployment tools
@mcp.tool(name="deploy_site", description="Deploy a Hugo site to various platforms")
async def deploy_site_tool(
    site_path: str,
    platform: str,
    destination: str = "public",
    branch: str = "main",
    commit_message: str = "Update site",
    remote_url: Optional[str] = None,
    api_key: Optional[str] = None,
    additional_options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Deploy a Hugo site to various platforms.

    Args:
        site_path: Path to the Hugo site
        platform: Deployment platform (github-pages, netlify, vercel, custom)
        destination: Build destination directory (default: "public")
        branch: Branch to deploy to (default: "main")
        commit_message: Commit message for the deployment (default: "Update site")
        remote_url: Remote URL for custom deployment
        api_key: API key for the deployment platform
        additional_options: Additional platform-specific options

    Returns:
        Dict with deployment status and information
    """
    try:
        # Build the site first
        build_result = await build_site(site_path, destination, clean_destination=True)
        if build_result["status"] != "success":
            return build_result

        # Deploy based on platform
        if platform.lower() == "github-pages":
            return await deploy_to_github_pages(
                site_path, destination, branch, commit_message, api_key
            )
        elif platform.lower() == "netlify":
            return await deploy_to_netlify(
                site_path, destination, api_key, additional_options
            )
        elif platform.lower() == "vercel":
            return await deploy_to_vercel(
                site_path, destination, api_key, additional_options
            )
        elif platform.lower() == "custom" and remote_url:
            return await deploy_to_custom(
                site_path, destination, remote_url, branch, commit_message
            )
        else:
            return {"status": "error", "message": f"Unsupported platform: {platform}"}

    except Exception as e:
        return {
            "status": "error",
            "message": f"Deployment failed: {str(e)}",
        }


if __name__ == "__main__":
    mcp.run(transport="stdio")
