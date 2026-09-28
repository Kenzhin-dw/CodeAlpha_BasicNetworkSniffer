# Manual GitHub Upload Guide

This guide keeps all account actions manual. It does not require any GitHub integration.

## Repository details

- **Recommended name:** `CodeAlpha_BasicNetworkSniffer`
- **Description:** `A Python and Streamlit dashboard for authorized network packet capture, protocol analysis, traffic statistics, and safe CSV metadata export.`
- **Visibility:** Public, if CodeAlpha requires an accessible repository and you are comfortable publishing the reviewed source.

## Method A — GitHub website and VS Code terminal

### A. Create an empty repository on GitHub

1. Open GitHub in your browser and sign in manually.
2. Select **New repository**.
3. Enter `CodeAlpha_BasicNetworkSniffer` as the repository name.
4. Paste the description above.
5. Select **Public** if appropriate for the internship submission.
6. Do **not** initialize the remote repository with a README, `.gitignore`, or license. The local project already has all three. Keeping the remote empty avoids an unnecessary first-push conflict.
7. Select **Create repository**.
8. Keep the resulting repository page open. You will copy its URL later.

### B. Open the correct local folder

1. Open VS Code.
2. Select **File → Open Folder**.
3. Choose the folder named `CodeAlpha_BasicNetworkSniffer` that directly contains `app.py`, `README.md`, and `requirements.txt`.
4. Select **Terminal → New Terminal**.
5. Confirm the location:

```powershell
Get-Location
```

The final folder name shown should be `CodeAlpha_BasicNetworkSniffer`. You can also list the root files:

```powershell
Get-ChildItem -Force
```

### C. Security check before Git

Read `.gitignore` before staging:

```powershell
Get-Content .gitignore
```

The repository must not contain or commit:

- `.env` or `.streamlit/secrets.toml`
- credentials, access tokens, API keys, cookies, or private keys
- `.venv/`, `venv/`, `__pycache__/`, or `.pytest_cache/`
- PCAP, PCAPNG, CAP, raw log, `eve.json`, database, or runtime export files
- real captured CSV data
- screenshots that reveal IP addresses, adapter GUIDs, usernames, tokens, or private traffic

Only the deliberately synthetic `sample/sample_packets.csv` should be committed as packet-like sample data.

If Git is already initialized, inspect the current state before doing anything else:

```powershell
git status
```

If Git reports that this is not a repository, continue to the next section.

### D. Initialize Git and stage the project

Run each command separately:

```powershell
git init
```

This creates local Git history in the current project folder. It does not upload anything.

```powershell
git status
```

This shows untracked and modified files. Confirm that you are in the correct project.

```powershell
git add .
```

This stages files that are not excluded by `.gitignore`. Staging prepares a snapshot; it does not upload it.

```powershell
git status
```

Review every staged path. Stop and unstage a sensitive file with `git restore --staged <FILE>` if anything unexpected appears.

### E. Review staged content

```powershell
git diff --cached
```

Read the staged source and documentation. Confirm that it contains no secret values, private network data, absolute user paths, raw captures, or unsanitized screenshots. For a new repository, `git diff --cached --stat` is also useful for a concise file summary.

### F. Create the first commit

```powershell
git commit -m "Initial CodeAlpha internship project"
```

A commit is a named local snapshot of the staged files. If Git requests your name and email, follow its displayed commands to configure the identity you want attached to public commits, then repeat the commit.

### G. Use the main branch

```powershell
git branch -M main
```

This names the primary branch `main`, which matches the common GitHub default.

### H. Connect the empty GitHub repository

Copy the repository URL from the GitHub page, then use it in place of the placeholder:

```powershell
git remote add origin <MY-GITHUB-REPOSITORY-URL>
```

Do not type the angle brackets. `origin` is the conventional local name for the remote repository.

Verify the saved URL:

```powershell
git remote -v
```

### I. Push manually

```powershell
git push -u origin main
```

- `origin` identifies the GitHub remote.
- `main` identifies the branch being uploaded.
- `-u` records the upstream relationship so later pushes can use only `git push`.

Complete GitHub authentication in the official browser or credential prompt if Git requests it. Never paste an access token into project files.

### J. Verify on GitHub

Refresh the repository page and confirm:

- `README.md` renders on the front page.
- `app.py`, `sniffer/`, `utils/`, `tests/`, `docs/`, and `sample/` are present.
- `.venv`, capture files, real CSV exports, logs, and secrets are absent.
- Mermaid architecture renders or at least remains readable as source.
- Documentation links open correctly.
- The repository is accessible with the visibility required by CodeAlpha.

### K. Future updates

For later changes, use:

```powershell
git status
git add .
git diff --cached
git commit -m "Update project documentation"
git push
```

You do not run `git init` or `git remote add origin` again for the same local repository.

## Copy the final GitHub link

After the push succeeds, copy the repository URL from the browser address bar. Its format is:

```text
https://github.com/<username>/<repository>
```

Submit this repository URL—not your GitHub profile URL—in the CodeAlpha field **GitHub Repository Link (Task 1)**.

## Optional alternative — GitHub Desktop

1. Open GitHub Desktop and choose **File → Add Local Repository**.
2. Select the `CodeAlpha_BasicNetworkSniffer` folder.
3. If prompted, create a repository in that folder.
4. Review all changed files and confirm sensitive artifacts are absent.
5. Enter a commit summary and select **Commit to main**.
6. Select **Publish repository**, use the recommended name, and choose the required visibility.
7. Open the published repository in the browser and perform the same safety verification above.

