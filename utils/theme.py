import subprocess
import os
from typing import Dict, Any
from pathlib import Path
import yaml
import requests
from bs4 import BeautifulSoup
import re


async def list_themes() -> Dict[str, Any]:
    try:
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
            theme_url = f"https://themes.gohugo.io{theme_path}"

            themes.append({"name": theme_name, "detail_url": theme_url})

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


async def install_theme(
    site_root_path: str,
    theme_name: str,
    theme_git_url: str,
    use_go_module: bool = False,
) -> Dict[str, Any]:
    try:
        # Validate site path
        if not os.path.isdir(site_root_path):
            return {
                "status": "error",
                "message": f"Site path '{site_root_path}' does not exist",
            }

        # Change to site directory
        os.chdir(site_root_path)

        # Install the theme
        if use_go_module:
            # Initialize Hugo modules if not already initialized
            if not os.path.exists("go.mod"):
                # Extract username and project from site_path
                site_name = os.path.basename(os.path.normpath(site_root_path))
                subprocess.run(
                    ["hugo", "mod", "init", f"github.com/{site_name}"], check=True
                )

            # Add the theme as a module
            subprocess.run(["hugo", "mod", "get", theme_git_url], check=True)

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
                            new_lines.append(f'    path = "{theme_git_url}"')

                        with open(config_file, "w") as f:
                            f.write("\n".join(new_lines))
                    elif config_file.endswith(".yaml"):
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
                            if (
                                isinstance(imp, dict)
                                and imp.get("path") == theme_git_url
                            ):
                                theme_in_imports = True
                                break

                        if not theme_in_imports:
                            config["module"]["imports"].append({"path": theme_git_url})

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
                ["git", "submodule", "add", theme_git_url, f"themes/{theme_name}"],
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


async def update_theme(
    site_root_path: str, theme_name: str, use_modules: bool = False
) -> Dict[str, Any]:
    try:
        # Validate site path
        if not os.path.isdir(site_root_path):
            return {
                "status": "error",
                "message": f"Site path '{site_root_path}' does not exist",
            }

        # Change to site directory
        os.chdir(site_root_path)

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


async def get_theme_details(detail_url: str) -> Dict[str, Any]:
    try:
        # Fetch the theme's detail page
        detail_response = requests.get(detail_url)
        if detail_response.status_code != 200:
            return {
                "status": "error",
                "message": f"Could not fetch theme details: HTTP {detail_response.status_code}",
            }

        # Parse the detail page
        detail_soup = BeautifulSoup(detail_response.text, "html.parser")

        # Extract theme name
        name = ""
        name_elem = detail_soup.select_one("h1")
        if name_elem:
            name = name_elem.text.strip()

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

        theme_info = {
            "name": name,
            "detail_url": detail_url,
            "github_url": github_url,
            "demo_url": demo_url,
            "installation": installation,
        }

        return {"status": "success", "theme": theme_info}
    except requests.RequestException as e:
        return {"status": "error", "message": f"Network error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to get theme details: {str(e)}"}
