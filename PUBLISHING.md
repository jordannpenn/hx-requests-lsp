# Publishing Guide

This guide provides step-by-step instructions for publishing `hx-requests-lsp` to PyPI and the VS Code extension to the Marketplace.

## Prerequisites

Before publishing, ensure you have:

- GitHub account with repositories created (`jordannpenn/hx-requests-lsp` and `jordannpenn/hx-requests-lsp-vscode-extension`)
- Python 3.11+ installed locally
- Node.js 20+ installed locally
- Git configured with your credentials
- GitHub CLI (`gh`) installed and authenticated

## Part 1: PyPI Setup

### Step 1.1: Create PyPI Account

1. Visit [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. Complete the registration form with your email address
3. Verify your email address by clicking the confirmation link
4. Enable Two-Factor Authentication (2FA) in Account Settings → Security

### Step 1.2: Configure Trusted Publishing

Trusted publishing eliminates the need for manual API tokens by using OpenID Connect (OIDC) from GitHub Actions.

1. Log in to PyPI at [https://pypi.org](https://pypi.org)
2. Navigate to your Account Settings
3. Scroll to **Publishing** section
4. Click **Add a new pending publisher**
5. Fill in the form:
   - **PyPI Project Name**: `hx-requests-lsp`
   - **Owner**: `jordannpenn`
   - **Repository name**: `hx-requests-lsp`
   - **Workflow name**: `publish.yml`
   - **Environment name**: (leave blank)
6. Click **Add**

**Important**: The project name must match exactly what's in your `pyproject.toml`. The first publish will create the project automatically.

### Step 1.3: First Release to PyPI

Once trusted publishing is configured and your GitHub repo has the `.github/workflows/publish.yml` workflow:

1. **Ensure all tests pass locally**:
   ```bash
   cd ~/dev/hx-requests-lsp
   pytest tests/ --tb=short -q
   ```

2. **Build locally to verify**:
   ```bash
   python -m build
   # Verify dist/ contains wheel and sdist
   ls -la dist/
   ```

3. **Push your code to GitHub** (if not already):
   ```bash
   git push origin main
   ```

4. **Create a GitHub Release**:
   ```bash
   # Using GitHub CLI
   gh release create v0.1.0 \
     --title "v0.1.0" \
     --notes "Initial public release of hx-requests-lsp

   Features:
   - Django template LSP support for hx-requests
   - Go-to-definition for hx_request template tags
   - Hover documentation
   - Python and HTML/Django template parsing"
   
   # Or use the GitHub web interface at:
   # https://github.com/jordannpenn/hx-requests-lsp/releases/new
   ```

5. **Monitor the workflow**:
   ```bash
   gh run watch
   ```

6. **Verify on PyPI**: Visit [https://pypi.org/project/hx-requests-lsp/](https://pypi.org/project/hx-requests-lsp/) after the workflow completes

7. **Test installation**:
   ```bash
   pip install hx-requests-lsp
   hx-requests-lsp --help
   ```

## Part 2: VS Code Marketplace Setup

### Step 2.1: Create Publisher Account

1. **Create Microsoft Account** (if you don't have one):
   - Visit [https://account.microsoft.com](https://account.microsoft.com)
   - Complete registration

2. **Create Azure DevOps Organization**:
   - Go to [https://dev.azure.com](https://dev.azure.com)
   - Click **Start free**
   - Sign in with your Microsoft account
   - Create a new organization (e.g., `jordannpenn`)

3. **Create Publisher on Marketplace**:
   - Navigate to [https://marketplace.visualstudio.com/manage](https://marketplace.visualstudio.com/manage)
   - Click **Create publisher**
   - Fill in:
     - **ID**: `jordannpenn` (permanent, cannot be changed)
     - **Name**: Your display name
     - **Email**: Your contact email
   - Click **Create**

### Step 2.2: Generate Azure DevOps Personal Access Token (PAT)

1. Go to [https://dev.azure.com](https://dev.azure.com)
2. Click your profile icon (top right) → **Security**
3. Click **+ New Token**
4. Configure the token:
   - **Name**: `vsce-marketplace-publish`
   - **Organization**: Select your organization
   - **Expiration**: 90 days (or custom, maximum 1 year)
   - **Scopes**: Select **Marketplace** → Check **Manage**
5. Click **Create**
6. **IMPORTANT**: Copy the token immediately - you cannot view it again

### Step 2.3: Add PAT to GitHub Secrets

1. Navigate to your extension repository:
   ```
   https://github.com/jordannpenn/hx-requests-lsp-vscode-extension/settings/secrets/actions
   ```

2. Click **New repository secret**
3. Add secret:
   - **Name**: `VSCE_PAT`
   - **Value**: Paste the Personal Access Token from Step 2.2
4. Click **Add secret**

### Step 2.4: First Release to Marketplace

**Prerequisites**:
- LSP package must already be published to PyPI (see Part 1)
- GitHub secrets configured with `VSCE_PAT`

**Steps**:

1. **Verify extension builds locally**:
   ```bash
   cd ~/dev/hx-requests-lsp-vscode-extension
   npm ci
   npm run bundle-lsp  # Bundles from PyPI
   npm run compile
   npx @vscode/vsce package
   ```

2. **Push code to GitHub**:
   ```bash
   git push origin main
   ```

3. **Create GitHub Release**:
   ```bash
   gh release create v0.1.0 \
     --title "v0.1.0" \
     --notes "Initial VS Code extension release

   Features:
   - LSP support for hx-requests Django template tags
   - Bundled hx-requests-lsp server (no pip install required)
   - Auto-detects Django projects with hx-requests"
   ```

4. **Monitor workflow**:
   ```bash
   gh run watch
   ```

5. **Verify on Marketplace**: Visit:
   ```
   https://marketplace.visualstudio.com/items?itemName=jordannpenn.hx-requests-lsp
   ```

6. **Test installation in VS Code**:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search "hx-requests"
   - Click Install

## Part 3: Ongoing Releases

### Version Bumping

Both packages use semantic versioning (SemVer): `MAJOR.MINOR.PATCH`

- **PATCH** (0.1.0 → 0.1.1): Bug fixes, no new features
- **MINOR** (0.1.0 → 0.2.0): New features, backward compatible
- **MAJOR** (0.1.0 → 1.0.0): Breaking changes

**Update version in**:
- LSP: `pyproject.toml` → `version = "x.y.z"`
- Extension: `package.json` → `"version": "x.y.z"`

### Release Workflow

For **both** repositories:

1. **Update version number** in the respective config file
2. **Update CHANGELOG.md** (if you maintain one) with release notes
3. **Commit the version bump**:
   ```bash
   git add pyproject.toml  # or package.json
   git commit -m "chore: bump version to x.y.z"
   git push origin main
   ```

4. **Create and push a git tag**:
   ```bash
   git tag -a vx.y.z -m "Release vx.y.z"
   git push origin vx.y.z
   ```

5. **Create GitHub Release**:
   ```bash
   gh release create vx.y.z \
     --title "vx.y.z" \
     --notes "Release notes here"
   ```

6. **Verify CI/CD workflow runs and publishes successfully**:
   ```bash
   gh run watch
   ```

### Troubleshooting

**PyPI publish fails with "project does not exist"**:
- Ensure trusted publishing is configured correctly
- Check that PyPI project name matches `pyproject.toml`
- First release must be done through workflow (not manual upload)

**Marketplace publish fails with "401 Unauthorized"**:
- Verify `VSCE_PAT` GitHub secret is set correctly
- Check PAT hasn't expired
- Ensure PAT has "Marketplace (Manage)" scope

**Extension bundling fails**:
- Ensure LSP package is published to PyPI first
- Check network connectivity during `npm run bundle-lsp`
- Verify Python 3.11+ is available in CI environment

## Support

For issues or questions:
- LSP: [https://github.com/jordannpenn/hx-requests-lsp/issues](https://github.com/jordannpenn/hx-requests-lsp/issues)
- Extension: [https://github.com/jordannpenn/hx-requests-lsp-vscode-extension/issues](https://github.com/jordannpenn/hx-requests-lsp-vscode-extension/issues)
