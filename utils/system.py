import subprocess
import platform
from typing import Dict, Any


async def get_system_info() -> Dict[str, Any]:
    """Get system information using platform module."""
    system_info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }
    return {"status": "success", "system_info": system_info}


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
