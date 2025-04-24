import os
import subprocess
import signal
from pathlib import Path
from typing import Dict, Any, Optional


async def create_site(
    site_abs_path: str,
    site_name: str,
    force: bool = False,
    in_current_dir: bool = False,
) -> Dict[str, Any]:
    try:
        # Convert paths to Path objects
        site_abs_path = Path(site_abs_path)
        target_path = site_abs_path / site_name if not in_current_dir else site_abs_path

        # Create target directory if it doesn't exist
        target_path.mkdir(parents=True, exist_ok=True)

        # Check directory contents
        contents = list(target_path.iterdir())
        has_only_git = len(contents) == 1 and contents[0].name == ".git"
        is_empty = len(contents) == 0

        if in_current_dir:
            # Case: Initialize in current directory
            if not (is_empty or has_only_git):
                if not force:
                    return {
                        "status": "error",
                        "message": "Current directory is not empty (contains files other than .git). Use force=True to override.",
                    }

            # Change to target directory
            os.chdir(target_path)
            cmd = [
                "hugo",
                "new",
                "site",
                ".",
                "--force",
            ]  # -f for force in current directory

        else:
            # Case: Create new site in new directory
            if contents and not is_empty and not has_only_git:
                if not force:
                    return {
                        "status": "error",
                        "message": f"Directory '{site_name}' already exists and is not empty. Use force=True to override.",
                    }

            # Change to parent directory
            os.chdir(site_abs_path)
            cmd = ["hugo", "new", "site", site_name]
            if force:
                cmd.append("--force")

        # Create the site
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        return {
            "status": "success",
            "path": str(target_path),
            "message": result.stdout.strip(),
            "in_current_dir": in_current_dir,
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
        cmd = ["hugo", "server", "--port", str(port), "--bind", bind, "--openBrowser"]

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


async def stop_preview(pid: int) -> Dict[str, Any]:
    try:
        os.kill(pid, signal.SIGTERM)
        return {"status": "success", "message": f"Server with PID {pid} stopped"}
    except ProcessLookupError:
        return {"status": "error", "message": f"Process with PID {pid} not found"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to stop server: {str(e)}"}
