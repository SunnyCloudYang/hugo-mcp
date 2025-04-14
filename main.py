from typing import Any, Dict, Optional
import subprocess
import os
import platform
import shutil
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("hugo-mcp")


# Environment setup tools
@mcp.tool(
    name="check_hugo_installation",
    description="Check if Hugo is installed and get its version",
)
async def check_hugo_installation() -> Dict[str, Any]:
    try:
        result = subprocess.run(
            ["hugo", "version"], capture_output=True, text=True, check=True
        )
        return {"status": "success", "version": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Hugo is not installed or not in PATH: {str(e)}",
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": "Hugo is not installed or not in PATH",
        }


@mcp.tool(
    name="install_hugo",
    description="Install Hugo using the appropriate method for the current OS",
)
async def install_hugo(version: str = "latest") -> Dict[str, str]:
    system = platform.system().lower()

    try:
        if system == "darwin":  # macOS
            subprocess.run(["brew", "install", "hugo"], check=True)
            return {
                "status": "success",
                "message": "Hugo installed via Homebrew",
            }
        elif system == "linux":
            # Try to detect package manager
            if shutil.which("apt"):
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "hugo"], check=True)
                return {
                    "status": "success",
                    "message": "Hugo installed via apt",
                }
            elif shutil.which("dnf"):
                subprocess.run(["sudo", "dnf", "install", "-y", "hugo"], check=True)
                return {
                    "status": "success",
                    "message": "Hugo installed via dnf",
                }
            elif shutil.which("yum"):
                subprocess.run(["sudo", "yum", "install", "-y", "hugo"], check=True)
                return {
                    "status": "success",
                    "message": "Hugo installed via yum",
                }
            else:
                return {
                    "status": "error",
                    "message": "Unsupported Linux distribution. Please install Hugo manually.",
                }
        elif system == "windows":
            return {
                "status": "error",
                "message": "Windows installation not supported via this tool. Please install Hugo manually from https://gohugo.io/installation/windows/",
            }
        else:
            return {
                "status": "error",
                "message": f"Unsupported operating system: {system}",
            }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Installation failed: {str(e)}",
        }


@mcp.tool(
    name="check_go_installation",
    description="Check if Go is installed and get its version",
)
async def check_go_installation() -> Dict[str, Any]:
    try:
        result = subprocess.run(
            ["go", "version"], capture_output=True, text=True, check=True
        )
        return {"status": "success", "version": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Go is not installed or not in PATH: {str(e)}",
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": "Go is not installed or not in PATH",
        }


@mcp.tool(
    name="install_go",
    description="Install Go using the appropriate method for the current OS",
)
async def install_go(version: str = "latest") -> Dict[str, str]:
    system = platform.system().lower()

    try:
        if system == "darwin":  # macOS
            subprocess.run(["brew", "install", "go"], check=True)
            return {"status": "success", "message": "Go installed via Homebrew"}
        elif system == "linux":
            # Try to detect package manager
            if shutil.which("apt"):
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "golang"], check=True)
                return {"status": "success", "message": "Go installed via apt"}
            elif shutil.which("dnf"):
                subprocess.run(["sudo", "dnf", "install", "-y", "golang"], check=True)
                return {"status": "success", "message": "Go installed via dnf"}
            elif shutil.which("yum"):
                subprocess.run(["sudo", "yum", "install", "-y", "golang"], check=True)
                return {"status": "success", "message": "Go installed via yum"}
            else:
                return {
                    "status": "error",
                    "message": "Unsupported Linux distribution. Please install Go manually.",
                }
        elif system == "windows":
            return {
                "status": "error",
                "message": "Windows installation not supported via this tool. Please install Go manually from https://golang.org/dl/",
            }
        else:
            return {
                "status": "error",
                "message": f"Unsupported operating system: {system}",
            }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Installation failed: {str(e)}",
        }


# Hugo commands as MCP tools
@mcp.tool(
    name="check_git_installation",
    description="Check if Git is installed and get its configuration",
)
async def check_git_installation() -> Dict[str, Any]:
    try:
        # Check if git is installed
        git_version = subprocess.run(
            ["git", "--version"], capture_output=True, text=True, check=True
        )

        # Get git user configuration
        git_user_name = subprocess.run(
            ["git", "config", "user.name"], capture_output=True, text=True
        )
        git_user_email = subprocess.run(
            ["git", "config", "user.email"], capture_output=True, text=True
        )

        # Get git default branch
        git_default_branch = subprocess.run(
            ["git", "config", "--global", "init.defaultBranch"],
            capture_output=True,
            text=True,
        )

        return {
            "status": "success",
            "version": git_version.stdout.strip(),
            "user": {
                "name": (
                    git_user_name.stdout.strip()
                    if git_user_name.returncode == 0
                    else None
                ),
                "email": (
                    git_user_email.stdout.strip()
                    if git_user_email.returncode == 0
                    else None
                ),
            },
            "default_branch": (
                git_default_branch.stdout.strip()
                if git_default_branch.returncode == 0
                else "main"
            ),
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Git is not installed or not in PATH: {str(e)}",
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": "Git is not installed or not in PATH",
        }
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool(
    name="install_git",
    description="Install Git using the appropriate method for the current OS",
)
async def install_git() -> Dict[str, str]:
    system = platform.system().lower()

    try:
        if system == "darwin":  # macOS
            subprocess.run(["brew", "install", "git"], check=True)
            return {"status": "success", "message": "Git installed via Homebrew"}
        elif system == "linux":
            # Try to detect package manager
            if shutil.which("apt"):
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "git"], check=True)
                return {"status": "success", "message": "Git installed via apt"}
            elif shutil.which("dnf"):
                subprocess.run(["sudo", "dnf", "install", "-y", "git"], check=True)
                return {"status": "success", "message": "Git installed via dnf"}
            elif shutil.which("yum"):
                subprocess.run(["sudo", "yum", "install", "-y", "git"], check=True)
                return {"status": "success", "message": "Git installed via yum"}
            else:
                return {
                    "status": "error",
                    "message": "Unsupported Linux distribution. Please install Git manually.",
                }
        elif system == "windows":
            return {
                "status": "error",
                "message": "Windows installation not supported via this tool. Please install Git manually from https://git-scm.com/download/win",
            }
        else:
            return {
                "status": "error",
                "message": f"Unsupported operating system: {system}",
            }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Installation failed: {str(e)}",
        }


@mcp.tool(name="configure_git", description="Configure Git with user name and email")
async def configure_git(name: str, email: str) -> Dict[str, str]:
    try:
        # Set git user name
        subprocess.run(["git", "config", "--global", "user.name", name], check=True)

        # Set git user email
        subprocess.run(["git", "config", "--global", "user.email", email], check=True)

        return {
            "status": "success",
            "message": f"Git configured with name '{name}' and email '{email}'",
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Failed to configure Git: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
        }


@mcp.tool(name="create_site", description="Create a new Hugo site")
async def create_site(
    site_abs_path: str,
    site_name: str,
    force: bool = False,
) -> Dict[str, Any]:
    try:
        # Check if directory already exists
        site_path = Path(site_name)
        if site_path.exists() and not force:
            return {
                "status": "error",
                "message": f"Directory '{site_name}' already exists. Use force=True to overwrite.",
            }

        # Create the site
        subprocess.run(
            ["hugo", "new", "site", site_name], cwd=site_abs_path, check=True
        )

        # Change to site directory
        os.chdir(f"{site_abs_path}/{site_name}")

        # Initialize git repository
        subprocess.run(["git", "init"], check=True)

        return {
            "status": "success",
            "message": f"Hugo site '{site_name}' created successfully at {site_abs_path}",
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Failed to create Hugo site: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
        }


@mcp.tool(name="create_post", description="Create a new Hugo post")
async def create_post(
    site_path: str,
    post_title: str,
    content_type: str = "posts",
    draft: bool = True,
    date: Optional[str] = None,
) -> Dict[str, Any]:
    try:
        # Validate site path
        if not os.path.isdir(site_path):
            return {
                "status": "error",
                "message": f"Site path '{site_path}' does not exist",
            }

        # Change to site directory
        os.chdir(site_path)

        # Create the post
        cmd = ["hugo", "new", f"{content_type}/{post_title}.md"]
        if date:
            cmd.extend(["--date", date])

        subprocess.run(cmd, check=True)

        # Update draft status if needed
        post_path = f"content/{content_type}/{post_title}.md"
        if os.path.exists(post_path):
            with open(post_path, "r") as f:
                content = f.read()

            # Update draft status
            if draft:
                content = content.replace("draft: false", "draft: true")
            else:
                content = content.replace("draft: true", "draft: false")

            with open(post_path, "w") as f:
                f.write(content)

        return {"status": "success", "file": post_path, "draft": draft}
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Failed to create post: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
        }


@mcp.tool(name="start_preview", description="Start Hugo local server")
async def start_preview(
    site_path: str,
    port: int = 1313,
    bind: str = "127.0.0.1",
    build_drafts: bool = False,
    build_future: bool = False,
    build_expired: bool = False,
) -> Dict[str, Any]:
    try:
        # Validate site path
        if not os.path.isdir(site_path):
            return {
                "status": "error",
                "message": f"Site path '{site_path}' does not exist",
            }

        # Change to site directory
        os.chdir(site_path)

        # Build command
        cmd = ["hugo", "server", "--port", str(port), "--bind", bind]

        if build_drafts:
            cmd.append("--buildDrafts")
        if build_future:
            cmd.append("--buildFuture")
        if build_expired:
            cmd.append("--buildExpired")

        # Start the server in the background
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Wait a moment to check if the server started successfully
        import time

        time.sleep(2)

        if process.poll() is not None:
            # Process has terminated
            error_output = process.stderr.read()
            return {
                "status": "error",
                "message": f"Server failed to start: {error_output}",
            }

        return {
            "status": "success",
            "url": f"http://{bind}:{port}",
            "pid": process.pid,
            "options": {
                "build_drafts": build_drafts,
                "build_future": build_future,
                "build_expired": build_expired,
            },
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
        }


@mcp.tool(name="build_site", description="Build the Hugo site for production")
async def build_site(
    site_path: str,
    destination: str = "public",
    clean_destination: bool = False,
    minify: bool = False,
) -> Dict[str, Any]:
    try:
        # Validate site path
        if not os.path.isdir(site_path):
            return {
                "status": "error",
                "message": f"Site path '{site_path}' does not exist",
            }

        # Change to site directory
        os.chdir(site_path)

        # Build command
        cmd = ["hugo", "--destination", destination]

        if clean_destination:
            cmd.append("--cleanDestinationDir")
        if minify:
            cmd.append("--minify")

        # Run the build
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        return {
            "status": "success",
            "destination": os.path.abspath(destination),
            "output": result.stdout,
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Build failed: {e.stderr}",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
        }


@mcp.tool(name="deploy_site", description="Deploy a Hugo site to various platforms")
async def deploy_site(
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
        # Validate site path
        if not os.path.isdir(site_path):
            return {
                "status": "error",
                "message": f"Site path '{site_path}' does not exist",
            }

        # Change to site directory
        os.chdir(site_path)

        # Build the site first
        build_result = await build_site(site_path, destination, clean_destination=True)
        if build_result["status"] != "success":
            return build_result

        # Deploy based on platform
        if platform.lower() == "github-pages":
            return await _deploy_to_github_pages(
                site_path, destination, branch, commit_message, api_key
            )
        elif platform.lower() == "netlify":
            return await _deploy_to_netlify(
                site_path, destination, api_key, additional_options
            )
        elif platform.lower() == "vercel":
            return await _deploy_to_vercel(
                site_path, destination, api_key, additional_options
            )
        elif platform.lower() == "custom" and remote_url:
            return await _deploy_to_custom(
                site_path, destination, remote_url, branch, commit_message
            )
        else:
            return {"status": "error", "message": f"Unsupported platform: {platform}"}

    except Exception as e:
        return {
            "status": "error",
            "message": f"Deployment failed: {str(e)}",
        }


async def _deploy_to_github_pages(
    site_path: str,
    destination: str,
    branch: str,
    commit_message: str,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Deploy to GitHub Pages"""
    try:
        # Check if git is initialized
        if not os.path.exists(os.path.join(site_path, ".git")):
            subprocess.run(["git", "init"], check=True)

        # Add the destination directory
        subprocess.run(["git", "add", destination], check=True)

        # Commit the changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Create a new branch if it doesn't exist
        try:
            subprocess.run(["git", "checkout", "-b", branch], check=True)
        except subprocess.CalledProcessError:
            # Branch might already exist
            subprocess.run(["git", "checkout", branch], check=True)

        # Push to GitHub
        if api_key:
            # Use token for authentication
            remote_url = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()

            # Replace HTTPS URL with token
            if remote_url.startswith("https://"):
                remote_url = remote_url.replace("https://", f"https://{api_key}@")
                subprocess.run(
                    ["git", "remote", "set-url", "origin", remote_url], check=True
                )

        subprocess.run(["git", "push", "origin", branch, "--force"], check=True)

        return {
            "status": "success",
            "platform": "github-pages",
            "branch": branch,
            "url": f"https://{os.path.basename(site_path)}.github.io",
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"GitHub Pages deployment failed: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"GitHub Pages deployment failed: {str(e)}",
        }


async def _deploy_to_netlify(
    site_path: str,
    destination: str,
    api_key: Optional[str] = None,
    additional_options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Deploy to Netlify"""
    try:
        # Check if Netlify CLI is installed
        try:
            subprocess.run(["netlify", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Install Netlify CLI
            subprocess.run(["npm", "install", "-g", "netlify-cli"], check=True)

        # Login to Netlify if API key is provided
        if api_key:
            subprocess.run(["netlify", "login", "--token", api_key], check=True)

        # Deploy to Netlify
        cmd = ["netlify", "deploy", "--dir", destination]

        if (
            additional_options
            and "production" in additional_options
            and additional_options["production"]
        ):
            cmd.append("--prod")

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Extract deployment URL from output
        import re

        url_match = re.search(r"https://[^\s]+", result.stdout)
        deploy_url = url_match.group(0) if url_match else "URL not found in output"

        return {"status": "success", "platform": "netlify", "url": deploy_url}
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Netlify deployment failed: {e.stderr}",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Netlify deployment failed: {str(e)}",
        }


async def _deploy_to_vercel(
    site_path: str,
    destination: str,
    api_key: Optional[str] = None,
    additional_options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Deploy to Vercel"""
    try:
        # Check if Vercel CLI is installed
        try:
            subprocess.run(["vercel", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Install Vercel CLI
            subprocess.run(["npm", "install", "-g", "vercel"], check=True)

        # Login to Vercel if API key is provided
        if api_key:
            subprocess.run(["vercel", "login", "--token", api_key], check=True)

        # Deploy to Vercel
        cmd = ["vercel", "--cwd", destination]

        if (
            additional_options
            and "production" in additional_options
            and additional_options["production"]
        ):
            cmd.append("--prod")

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Extract deployment URL from output
        import re

        url_match = re.search(r"https://[^\s]+", result.stdout)
        deploy_url = url_match.group(0) if url_match else "URL not found in output"

        return {"status": "success", "platform": "vercel", "url": deploy_url}
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Vercel deployment failed: {e.stderr}",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Vercel deployment failed: {str(e)}",
        }


async def _deploy_to_custom(
    site_path: str, destination: str, remote_url: str, branch: str, commit_message: str
) -> Dict[str, Any]:
    """Deploy to a custom remote"""
    try:
        # Check if git is initialized
        if not os.path.exists(os.path.join(site_path, ".git")):
            subprocess.run(["git", "init"], check=True)

        # Add the destination directory
        subprocess.run(["git", "add", destination], check=True)

        # Commit the changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Add remote if it doesn't exist
        try:
            subprocess.run(["git", "remote", "add", "deploy", remote_url], check=True)
        except subprocess.CalledProcessError:
            # Remote might already exist
            subprocess.run(
                ["git", "remote", "set-url", "deploy", remote_url], check=True
            )

        # Push to remote
        subprocess.run(
            ["git", "push", "deploy", f"HEAD:{branch}", "--force"], check=True
        )

        return {
            "status": "success",
            "platform": "custom",
            "remote_url": remote_url,
            "branch": branch,
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Custom deployment failed: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Custom deployment failed: {str(e)}",
        }


@mcp.tool(
    name="list_themes",
    description="List available Hugo themes from the official Hugo themes website",
)
async def list_themes() -> Dict[str, Any]:
    try:
        import requests
        from bs4 import BeautifulSoup

        # Fetch the Hugo themes website
        response = requests.get("https://themes.gohugo.io/")
        if response.status_code != 200:
            return {
                "status": "error",
                "message": f"Failed to fetch themes: HTTP {response.status_code}",
            }

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all theme items
        theme_items = soup.select('ul[role="list"] li')

        themes = []
        for item in theme_items:
            # Extract theme name
            name_elem = item.select_one("p.text-sm.font-medium")
            if not name_elem:
                continue

            theme_name = name_elem.text.strip()

            # Extract theme URL
            link_elem = item.select_one('a[href^="/themes/"]')
            if not link_elem:
                continue

            theme_path = link_elem.get("href", "")
            theme_url = (
                f"https://github.com/gohugoio/hugoThemes/tree/master/themes{theme_path}"
            )

            # Extract theme image
            img_elem = item.select_one("img")
            img_url = None
            if img_elem and img_elem.get("src"):
                img_url = f"https://themes.gohugo.io{img_elem['src']}"

            themes.append({"name": theme_name, "url": theme_url, "image": img_url})

        return {
            "status": "success",
            "themes": themes,
            "count": len(themes),
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "message": f"Network error: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list themes: {str(e)}",
        }


@mcp.tool(
    name="install_theme",
    description="Install a Hugo theme using git submodule or Hugo modules",
)
async def install_theme(
    site_path: str, theme_name: str, theme_url: str, use_modules: bool = False
) -> Dict[str, Any]:
    try:
        # Validate site path
        if not os.path.isdir(site_path):
            return {
                "status": "error",
                "message": f"Site path '{site_path}' does not exist",
            }

        # Change to site directory
        os.chdir(site_path)

        # Install the theme
        if use_modules:
            # Initialize Hugo modules if not already initialized
            if not os.path.exists("go.mod"):
                # Extract username and project from site_path
                site_name = os.path.basename(os.path.normpath(site_path))
                subprocess.run(
                    ["hugo", "mod", "init", f"github.com/{site_name}"], check=True
                )

            # Add the theme as a module
            subprocess.run(["hugo", "mod", "get", theme_url], check=True)

            # Update config to use the theme via module imports
            config_files = ["config.toml", "hugo.toml", "config.yaml", "hugo.yaml"]
            for config_file in config_files:
                if os.path.exists(config_file):
                    if config_file.endswith(".toml"):
                        with open(config_file, "r") as f:
                            content = f.read()

                        # Remove theme line if present
                        lines = content.split("\n")
                        new_lines = []
                        for line in lines:
                            if not line.strip().startswith("theme = "):
                                new_lines.append(line)

                        # Add module section if not present
                        if "[module]" not in content:
                            new_lines.append("\n[module]")
                            new_lines.append("  [[module.imports]]")
                            new_lines.append(f'    path = "{theme_url}"')

                        with open(config_file, "w") as f:
                            f.write("\n".join(new_lines))
                    elif config_file.endswith(".yaml"):
                        import yaml

                        with open(config_file, "r") as f:
                            config = yaml.safe_load(f) or {}

                        # Remove theme if present
                        if "theme" in config:
                            del config["theme"]

                        # Add module section if not present
                        if "module" not in config:
                            config["module"] = {}

                        if "imports" not in config["module"]:
                            config["module"]["imports"] = []

                        # Check if the theme is already in imports
                        theme_in_imports = False
                        for imp in config["module"]["imports"]:
                            if isinstance(imp, dict) and imp.get("path") == theme_url:
                                theme_in_imports = True
                                break

                        if not theme_in_imports:
                            config["module"]["imports"].append({"path": theme_url})

                        with open(config_file, "w") as f:
                            yaml.dump(
                                config, f, default_flow_style=False, sort_keys=False
                            )

            return {"status": "success", "theme": theme_name, "method": "hugo_modules"}
        else:
            # Create themes directory if it doesn't exist
            themes_dir = Path("themes")
            if not themes_dir.exists():
                themes_dir.mkdir()

            # Add the theme as a git submodule
            subprocess.run(
                ["git", "submodule", "add", theme_url, f"themes/{theme_name}"],
                check=True,
            )

            # Update config to use the theme
            config_files = ["config.toml", "hugo.toml", "config.yaml", "hugo.yaml"]
            for config_file in config_files:
                if os.path.exists(config_file):
                    if config_file.endswith(".toml"):
                        with open(config_file, "r") as f:
                            content = f.read()

                        # Check if theme line already exists
                        if "theme = " in content:
                            # Replace existing theme line
                            lines = content.split("\n")
                            new_lines = []
                            for line in lines:
                                if line.strip().startswith("theme = "):
                                    new_lines.append(f'theme = "{theme_name}"')
                                else:
                                    new_lines.append(line)
                            content = "\n".join(new_lines)
                        else:
                            # Add theme line
                            content += f'\ntheme = "{theme_name}"'

                        with open(config_file, "w") as f:
                            f.write(content)
                    elif config_file.endswith(".yaml"):
                        import yaml

                        with open(config_file, "r") as f:
                            config = yaml.safe_load(f) or {}

                        # Update theme
                        config["theme"] = theme_name

                        with open(config_file, "w") as f:
                            yaml.dump(
                                config, f, default_flow_style=False, sort_keys=False
                            )

            return {"status": "success", "theme": theme_name, "method": "git_submodule"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Failed to install theme: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool(name="update_theme", description="Update an installed Hugo theme")
async def update_theme(
    site_path: str, theme_name: str, use_modules: bool = False
) -> Dict[str, Any]:
    try:
        # Validate site path
        if not os.path.isdir(site_path):
            return {
                "status": "error",
                "message": f"Site path '{site_path}' does not exist",
            }

        # Change to site directory
        os.chdir(site_path)

        # Update the theme
        if use_modules:
            # Update Hugo modules
            subprocess.run(["hugo", "mod", "get", "-u"], check=True)
            return {"status": "success", "theme": theme_name, "method": "hugo_modules"}
        else:
            # Update git submodule
            subprocess.run(
                ["git", "submodule", "update", "--remote", f"themes/{theme_name}"],
                check=True,
            )
            return {"status": "success", "theme": theme_name, "method": "git_submodule"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Failed to update theme: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool(name="list_content", description="List content in the Hugo site")
async def list_content(
    site_path: str, content_type: Optional[str] = None
) -> Dict[str, Any]:
    try:
        # Validate site path
        if not os.path.isdir(site_path):
            return {
                "status": "error",
                "message": f"Site path '{site_path}' does not exist",
            }

        # Change to site directory
        os.chdir(site_path)

        # List content
        content_dir = "content"
        if content_type:
            content_dir = f"{content_dir}/{content_type}"

        if not os.path.isdir(content_dir):
            return {
                "status": "error",
                "message": f"Content directory '{content_dir}' does not exist",
            }

        # Get list of content files
        content_files = []
        for root, _, files in os.walk(content_dir):
            for file in files:
                if file.endswith((".md", ".mdx", ".html")):
                    rel_path = os.path.relpath(os.path.join(root, file), "content")
                    content_files.append(rel_path)

        return {"status": "success", "content": content_files}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool(name="stop_preview", description="Stop a running Hugo preview server")
async def stop_preview(pid: int) -> Dict[str, Any]:
    try:
        import signal

        os.kill(pid, signal.SIGTERM)
        return {"status": "success", "message": f"Server with PID {pid} stopped"}
    except ProcessLookupError:
        return {"status": "error", "message": f"Process with PID {pid} not found"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to stop server: {str(e)}"}


@mcp.tool(
    name="get_theme_details",
    description="Get detailed information about a specific Hugo theme",
)
async def get_theme_details(theme_name: str) -> Dict[str, Any]:
    try:
        import requests
        from bs4 import BeautifulSoup
        import re

        # First, get the list of themes using the list_themes function
        themes_result = await list_themes()
        if themes_result["status"] != "success":
            return {"status": "error", "message": "Failed to fetch themes list"}

        # Find the theme in the list
        theme_info = None
        for theme in themes_result["themes"]:
            if theme["name"].lower() == theme_name.lower():
                theme_info = theme
                break

        if not theme_info:
            return {
                "status": "error",
                "message": f"Theme '{theme_name}' not found on the Hugo themes website",
            }

        # Extract the theme path from the URL
        theme_path = theme_info["url"].split("/themes/")[-1]

        # Now fetch the theme's detail page
        detail_url = f"https://themes.gohugo.io/themes/{theme_path}/"
        detail_response = requests.get(detail_url)

        if detail_response.status_code != 200:
            return {
                "status": "partial",
                "message": "Could not fetch theme details page",
                "theme": theme_info,
            }

        # Parse the detail page
        detail_soup = BeautifulSoup(detail_response.text, "html.parser")

        # Extract theme description
        description = ""
        desc_elem = detail_soup.select_one("div.prose p")
        if desc_elem:
            description = desc_elem.text.strip()

        # Extract theme features
        features = []
        feature_elems = detail_soup.select("div.prose ul li")
        for elem in feature_elems:
            features.append(elem.text.strip())

        # Extract theme tags
        tags = []
        tag_elems = detail_soup.select("div.flex.flex-wrap.gap-2 a")
        for elem in tag_elems:
            tags.append(elem.text.strip())

        # Extract GitHub repository
        github_url = None
        github_links = detail_soup.select('a[href*="github.com"]')
        for link in github_links:
            href = link.get("href", "")
            if "github.com" in href and not href.endswith("github.com"):
                github_url = href
                break

        # Extract demo URL
        demo_url = None
        demo_links = detail_soup.select('a[href*="://"]')
        for link in demo_links:
            href = link.get("href", "")
            if "github.com" not in href and not href.startswith(
                "https://themes.gohugo.io"
            ):
                demo_url = href
                break

        # Extract installation instructions
        installation = ""
        install_section = detail_soup.find(
            string=re.compile(r"Installation|Install", re.IGNORECASE)
        )
        if install_section:
            install_elem = install_section.find_parent()
            if install_elem:
                next_elem = install_elem.find_next_sibling()
                if next_elem and next_elem.name in ["p", "div"]:
                    installation = next_elem.text.strip()

        # Combine basic info with detailed info
        theme_info.update(
            {
                "description": description,
                "features": features,
                "tags": tags,
                "github_url": github_url,
                "demo_url": demo_url,
                "installation": installation,
            }
        )

        return {"status": "success", "theme": theme_info}
    except requests.RequestException as e:
        return {"status": "error", "message": f"Network error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to get theme details: {str(e)}"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
