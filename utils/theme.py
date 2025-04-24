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


async def install_theme(
    site_path: str, theme_name: str, theme_url: str, use_go_module: bool = False
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
        if use_go_module:
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


async def get_theme_details(theme_name: str) -> Dict[str, Any]:
    try:
        # First, get the list of themes
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
