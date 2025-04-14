# Hugo MCP Server

A powerful MCP (Model Control Protocol) server for managing Hugo static site generator. This server provides a comprehensive set of tools for creating, managing, and deploying Hugo sites.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Tools](#tools)
  - [Environment Setup Tools](#environment-setup-tools)
  - [Site Management Tools](#site-management-tools)
  - [Theme Management Tools](#theme-management-tools)
  - [Content Management Tools](#content-management-tools)
  - [Preview and Build Tools](#preview-and-build-tools)
- [Complete Workflow Example](#complete-workflow-example)
- [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- Python 3.10+
- uv (Python package manager)
- Git (Highly recommended)

### Installing the Hugo MCP Server

1. Clone the repository:

   ```bash
   git clone https://github.com/sunnycloudyang/hugo-mcp.git
   ```

2. Add server to your config (make sure `uv` has been installed before):

   ```json
   {
        "mcpServers": {
            "hugo-mcp": {
                "command": "uv",
                "args": [
                    "--directory",
                    "/ABSOLUTE/PATH/TO/PARENT/FOLDER/hugo-mcp",
                    "run",
                    "main.py"
                ]
            }
        }
    }
   ```

   Remember to replace "/ABSOLUTE/PATH/TO/PARENT/FOLDER/hugo-mcp" to your installation path

3. Enalble this mcp server and try it!

## Usage

The Hugo MCP server provides a set of tools that can be used to manage Hugo sites. Each tool has specific parameters and returns a structured response.

### Basic Usage

1. Start the server manually (If needed):

   ```bash
   uv run main.py
   ```

2. Connect to the server using an MCP client.

3. Use the tools to manage your Hugo sites.

## Tools

### Environment Setup Tools

#### check_hugo_installation

**Description**: Check if Hugo is installed and get its version.

**Parameters**: None

**Returns**:

```json
{
  "status": "success",
  "version": "Hugo Static Site Generator v0.92.0/extended linux/amd64 BuildDate=unknown"
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Hugo is not installed or not in PATH"
}
```

**Prerequisites**: None

**Actions After Success**: None

**Actions After Failure**: Install Hugo using the `install_hugo` tool.

#### install_hugo

**Description**: Install Hugo using the appropriate method for the current OS.

**Parameters**:

- `version` (optional): The version of Hugo to install. Defaults to "latest".

**Returns**:

```json
{
  "status": "success",
  "message": "Hugo installed via Homebrew"
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Installation failed: Command 'brew install hugo' returned non-zero exit status 1."
}
```

**Prerequisites**: Appropriate package manager (Homebrew, apt, dnf, yum) must be installed.

**Actions After Success**: Hugo is installed and ready to use.

**Actions After Failure**: Manual installation may be required.

#### check_go_installation

**Description**: Check if Go is installed and get its version.

**Parameters**: None

**Returns**:

```json
{
  "status": "success",
  "version": "go version go1.17.5 darwin/amd64"
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Go is not installed or not in PATH"
}
```

**Prerequisites**: None

**Actions After Success**: None

**Actions After Failure**: Install Go using the `install_go` tool.

#### install_go

**Description**: Install Go using the appropriate method for the current OS.

**Parameters**:

- `version` (optional): The version of Go to install. Defaults to "latest".

**Returns**:

```json
{
  "status": "success",
  "message": "Go installed via Homebrew"
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Installation failed: Command 'brew install go' returned non-zero exit status 1."
}
```

**Prerequisites**: Appropriate package manager (Homebrew, apt, dnf, yum) must be installed.

**Actions After Success**: Go is installed and ready to use.

**Actions After Failure**: Manual installation may be required.

#### check_git_installation

**Description**: Check if Git is installed and get its configuration.

**Parameters**: None

**Returns**:

```json
{
  "status": "success",
  "version": "git version 2.30.1 (Apple Git-130)",
  "user": {
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "default_branch": "main"
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Git is not installed or not in PATH"
}
```

**Prerequisites**: None

**Actions After Success**: None

**Actions After Failure**: Install Git using the `install_git` tool.

#### install_git

**Description**: Install Git using the appropriate method for the current OS.

**Parameters**: None

**Returns**:

```json
{
  "status": "success",
  "message": "Git installed via Homebrew"
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Installation failed: Command 'brew install git' returned non-zero exit status 1."
}
```

**Prerequisites**: Appropriate package manager (Homebrew, apt, dnf, yum) must be installed.

**Actions After Success**: Git is installed and ready to use.

**Actions After Failure**: Manual installation may be required.

#### configure_git

**Description**: Configure Git with user name and email.

**Parameters**:

- `name`: The user name to set.
- `email`: The email address to set.

**Returns**:

```json
{
  "status": "success",
  "message": "Git configured with name 'John Doe' and email 'john.doe@example.com'"
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Failed to configure Git: Command 'git config --global user.name John Doe' returned non-zero exit status 1."
}
```

**Prerequisites**: Git must be installed.

**Actions After Success**: Git is configured with the specified user name and email.

**Actions After Failure**: Manual configuration may be required.

### Site Management Tools

#### create_site

**Description**: Create a new Hugo site.

**Parameters**:

- `site_name`: The name of the site to create.
- `theme` (optional): The theme to use for the site.
- `force` (optional): Whether to force creation if the directory already exists. Defaults to `false`.
- `use_example_site` (optional): Whether to use the example site from the theme. Defaults to `true`.

**Returns**:

```json
{
  "status": "success",
  "path": "/path/to/site",
  "theme": "paper",
  "example_site": true,
  "author": {
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Directory 'site' already exists. Use force=True to overwrite."
}
```

**Prerequisites**: Hugo must be installed.

**Actions After Success**: A new Hugo site is created with the specified theme and example content.

**Actions After Failure**: The site is not created.

### Theme Management Tools

#### list_themes

**Description**: List available Hugo themes from the official Hugo themes website.

**Parameters**: None

**Returns**:

```json
{
  "status": "success",
  "themes": [
    {
      "name": "PaperMod",
      "url": "https://github.com/gohugoio/hugoThemes/tree/master/themes/hugo-papermod",
      "image": "https://themes.gohugo.io/themes/hugo-papermod/tn-featured_hu_275191178647f5e7.png"
    },
    {
      "name": "Hugo Blox - Tailwind",
      "url": "https://github.com/gohugoio/hugoThemes/tree/master/themes/blox-tailwind",
      "image": "https://themes.gohugo.io/themes/blox-tailwind/tn-featured_hu_8c1541d303ce3b9b.png"
    }
  ],
  "count": 150
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Network error: Connection refused"
}
```

**Prerequisites**: Internet connection.

**Actions After Success**: A list of available themes is returned.

**Actions After Failure**: No themes are returned.

#### get_theme_details

**Description**: Get detailed information about a specific Hugo theme.

**Parameters**:

- `theme_name`: The name of the theme to get details for.

**Returns**:

```json
{
  "status": "success",
  "theme": {
    "name": "Paper",
    "url": "https://github.com/gohugoio/hugoThemes/tree/master/themes/paper",
    "image": "https://themes.gohugo.io/themes/paper/tn-featured.png",
    "description": "A simple, clean, and responsive Hugo theme for personal blog.",
    "features": [
      "Responsive design",
      "Clean and minimal",
      "Fast and lightweight",
      "SEO friendly"
    ],
    "tags": ["blog", "minimal", "responsive"],
    "github_url": "https://github.com/nanxiaobei/hugo-paper",
    "demo_url": "https://themes.gohugo.io/theme/paper/",
    "installation": "git submodule add https://github.com/nanxiaobei/hugo-paper themes/paper"
  }
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Theme 'NonExistentTheme' not found on the Hugo themes website"
}
```

**Prerequisites**: Internet connection.

**Actions After Success**: Detailed information about the theme is returned.

**Actions After Failure**: No theme details are returned.

#### install_theme

**Description**: Install a Hugo theme using git submodule or Hugo modules.

**Parameters**:

- `site_path`: The path to the Hugo site.
- `theme_name`: The name of the theme to install.
- `theme_url`: The URL of the theme repository.
- `use_modules` (optional): Whether to use Hugo modules instead of git submodules. Defaults to `false`.

**Returns**:

```json
{
  "status": "success",
  "theme": "paper",
  "method": "git_submodule"
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Failed to install theme: Command 'git submodule add https://github.com/nanxiaobei/hugo-paper themes/paper' returned non-zero exit status 1."
}
```

**Prerequisites**:

- Hugo must be installed.
- Git must be installed (for git submodules).
- Go must be installed (for Hugo modules).

**Actions After Success**: The theme is installed and configured in the site.

**Actions After Failure**: The theme is not installed.

#### update_theme

**Description**: Update an installed Hugo theme.

**Parameters**:

- `site_path`: The path to the Hugo site.
- `theme_name`: The name of the theme to update.
- `use_modules` (optional): Whether the theme was installed using Hugo modules. Defaults to `false`.

**Returns**:

```json
{
  "status": "success",
  "theme": "paper",
  "method": "git_submodule"
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Failed to update theme: Command 'git submodule update --remote themes/paper' returned non-zero exit status 1."
}
```

**Prerequisites**:

- Hugo must be installed.
- Git must be installed (for git submodules).
- Go must be installed (for Hugo modules).
- The theme must be already installed.

**Actions After Success**: The theme is updated to the latest version.

**Actions After Failure**: The theme is not updated.

### Content Management Tools

#### create_post

**Description**: Create a new Hugo post.

**Parameters**:

- `site_path`: The path to the Hugo site.
- `post_title`: The title of the post.
- `content_type` (optional): The content type of the post. Defaults to "posts".
- `draft` (optional): Whether the post should be a draft. Defaults to `true`.
- `date` (optional): The date of the post.

**Returns**:

```json
{
  "status": "success",
  "file": "content/posts/my-first-post.md",
  "draft": true
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Site path '/path/to/site' does not exist"
}
```

**Prerequisites**: Hugo must be installed.

**Actions After Success**: A new post is created in the specified content type directory.

**Actions After Failure**: The post is not created.

#### list_content

**Description**: List content in the Hugo site.

**Parameters**:

- `site_path`: The path to the Hugo site.
- `content_type` (optional): The content type to list. If not specified, all content is listed.

**Returns**:

```json
{
  "status": "success",
  "content": [
    "posts/my-first-post.md",
    "posts/another-post.md",
    "pages/about.md"
  ]
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Site path '/path/to/site' does not exist"
}
```

**Prerequisites**: Hugo must be installed.

**Actions After Success**: A list of content files is returned.

**Actions After Failure**: No content is returned.

### Preview and Build Tools

#### start_preview

**Description**: Start Hugo local server.

**Parameters**:

- `site_path`: The path to the Hugo site.
- `port` (optional): The port to use. Defaults to 1313.
- `bind` (optional): The address to bind to. Defaults to "127.0.0.1".
- `build_drafts` (optional): Whether to build draft content. Defaults to `false`.
- `build_future` (optional): Whether to build future content. Defaults to `false`.
- `build_expired` (optional): Whether to build expired content. Defaults to `false`.

**Returns**:

```json
{
  "status": "success",
  "url": "http://127.0.0.1:1313",
  "pid": 12345,
  "options": {
    "build_drafts": false,
    "build_future": false,
    "build_expired": false
  }
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Site path '/path/to/site' does not exist"
}
```

**Prerequisites**: Hugo must be installed.

**Actions After Success**: The Hugo server is started and accessible at the specified URL.

**Actions After Failure**: The server is not started.

#### stop_preview

**Description**: Stop a running Hugo preview server.

**Parameters**:

- `pid`: The process ID of the server to stop.

**Returns**:

```json
{
  "status": "success",
  "message": "Server with PID 12345 stopped"
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Process with PID 12345 not found"
}
```

**Prerequisites**: None.

**Actions After Success**: The Hugo server is stopped.

**Actions After Failure**: The server is not stopped.

#### build_site

**Description**: Build the Hugo site for production.

**Parameters**:

- `site_path`: The path to the Hugo site.
- `destination` (optional): The destination directory. Defaults to "public".
- `clean_destination` (optional): Whether to clean the destination directory before building. Defaults to `false`.
- `minify` (optional): Whether to minify the output. Defaults to `false`.

**Returns**:

```json
{
  "status": "success",
  "destination": "/path/to/site/public",
  "output": "Built in 123 ms"
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Site path '/path/to/site' does not exist"
}
```

**Prerequisites**: Hugo must be installed.

**Actions After Success**: The site is built and ready for deployment.

**Actions After Failure**: The site is not built.

#### deploy_site

**Description**: Deploy a Hugo site to various platforms.

**Parameters**:

- `site_path`: The path to the Hugo site.
- `platform`: Deployment platform (github-pages, netlify, vercel, custom).
- `destination` (optional): Build destination directory. Defaults to "public".
- `branch` (optional): Branch to deploy to. Defaults to "main".
- `commit_message` (optional): Commit message for the deployment. Defaults to "Update site".
- `remote_url` (optional): Remote URL for custom deployment.
- `api_key` (optional): API key for the deployment platform.
- `additional_options` (optional): Additional platform-specific options.

**Returns**:

```json
{
  "status": "success",
  "platform": "github-pages",
  "branch": "gh-pages",
  "url": "https://username.github.io"
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Deployment failed: GitHub Pages deployment failed: Command 'git push origin gh-pages --force' returned non-zero exit status 1."
}
```

**Prerequisites**:

- Hugo must be installed.
- Git must be installed.
- For GitHub Pages: Git repository must be initialized.
- For Netlify: Netlify CLI must be installed (will be installed automatically if not present).
- For Vercel: Vercel CLI must be installed (will be installed automatically if not present).

**Actions After Success**: The site is deployed to the specified platform and accessible at the returned URL.

**Actions After Failure**: The site is not deployed.

**Platform-specific notes**:

- **GitHub Pages**: Requires a Git repository and optionally an API key for authentication.
- **Netlify**: Requires Netlify CLI and optionally an API key for authentication.
- **Vercel**: Requires Vercel CLI and optionally an API key for authentication.
- **Custom**: Requires a Git repository and a remote URL.

## Complete Workflow Example

Here's a complete workflow example (in python scripts rather than mcp server tools to show the common route) for creating a new Hugo site with a theme:

1. Check if Hugo is installed:

   ```python
   result = await check_hugo_installation()
   if result["status"] != "success":
       result = await install_hugo()
   ```

2. Check if Git is installed:

   ```python
   result = await check_git_installation()
   if result["status"] != "success":
       result = await install_git()
   ```

3. Configure Git:

   ```python
   result = await configure_git("John Doe", "john.doe@example.com")
   ```

4. List available themes:

   ```python
   result = await list_themes()
   themes = result["themes"]
   ```

5. Get details for a specific theme:

   ```python
   result = await get_theme_details("Paper")
   theme_details = result["theme"]
   ```

6. Create a new site with the theme:

   ```python
   result = await create_site("my-blog", theme="nanxiaobei/hugo-paper", use_example_site=True)
   site_path = result["path"]
   ```

7. Start the preview server:

   ```python
   result = await start_preview(site_path, build_drafts=True)
   preview_url = result["url"]
   ```

8. Create a new post:

   ```python
   result = await create_post(site_path, "my-first-post", draft=False)
   post_file = result["file"]
   ```

9. Build the site for production:

   ```python
   result = await build_site(site_path, minify=True)
   ```

10. Deploy the site to GitHub Pages:
    ```python
    result = await deploy_site(
        site_path=site_path,
        platform="github-pages",
        branch="gh-pages",
        commit_message="Deploy site",
        api_key="your-github-token"
    )
    deploy_url = result["url"]
    ```

## Troubleshooting

### Common Issues

1. **Hugo is not installed**:

   - Use the `install_hugo` tool to install Hugo.

2. **Git is not installed**:

   - Use the `install_git` tool to install Git.

3. **Theme installation fails**:

   - Check if the theme URL is correct.
   - Make sure Git is installed for git submodules.
   - Make sure Go is installed for Hugo modules.
   - Read the theme's doc to check if there is sth. different

4. **Preview server fails to start**:

   - Check if the port is already in use.
   - Make sure the site path is correct.
   - Check your network

5. **Build fails**:
   - Check if the site path is correct.
   - Make sure all required dependencies are installed.

### Getting Help

If you encounter any issues not covered in this documentation, please [open an issue](https://github.com/sunnycloudyang/hugo-mcp/issues) on the GitHub repository.
