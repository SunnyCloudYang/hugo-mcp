import subprocess
import os
from typing import Dict, Any, Optional


async def deploy_to_github_pages(
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


async def deploy_to_netlify(
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


async def deploy_to_vercel(
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


async def deploy_to_custom(
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
