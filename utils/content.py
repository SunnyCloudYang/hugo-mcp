import os
import subprocess
from typing import Dict, Any, Optional


async def create_post(
    site_path: str,
    post_title: str,
    content_type: str = "posts",
    draft: bool = True,
    date: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new Hugo post with the specified parameters."""
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


async def list_content(
    site_path: str, content_type: Optional[str] = None
) -> Dict[str, Any]:
    """List content files in the Hugo site, optionally filtered by content type."""
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
