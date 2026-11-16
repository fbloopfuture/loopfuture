# Publishing the two repositories on GitHub

Two repositories, side by side:

| Repository | Visibility | Who has access | Content |
|------------|------------|----------------|---------|
| `loopfuture-databricks-training-trainer` | **Private** | trainers only (Francisco, Samantha, Neha, Daniel, Afonso) | everything, with 🎤 notes and solutions |
| `loopfuture-databricks-training` | Private (or Public) | trainers + trainees (Lara, Rodrigo B., Rodrigo M.) | clean notebooks + data dictionary |

> Recommended: create them under a **LoopFuture GitHub organization** (if it exists) instead of a personal account,
> so the material stays with the company.

## Option A — GitHub Desktop (easiest, no command line)

1. Install GitHub Desktop and sign in.
2. **File → Add local repository** → choose the folder `loopfuture-databricks-training-trainer` → *create a repository* → **Publish repository** → tick **Keep this code private**.
3. Same for `loopfuture-databricks-training`.
4. On github.com → each repo → **Settings → Collaborators** → invite the people in the table above.

## Option B — command line

```bash
cd loopfuture-databricks-training-trainer
git init -b main
git add .
git commit -m "Week 1 trainer material"
git remote add origin https://github.com/<org-or-user>/loopfuture-databricks-training-trainer.git
git push -u origin main

cd ../loopfuture-databricks-training
git init -b main
git add .
git commit -m "Week 1 notebooks"
git remote add origin https://github.com/<org-or-user>/loopfuture-databricks-training.git
git push -u origin main
```
(Create the two **empty** repositories on github.com first, without README, so the push does not conflict.)

## Option C — upload on the website

github.com → **New repository** → create → **uploading an existing file** → drag the folder contents.
Works, but folders with many files are slower and you lose the easy update workflow.

## How trainees use the shared repo

- **Recommended:** each trainee creates **their own** repo (notebook `00a`) and imports the notebooks of the week into it.
  Their solutions stay in their repo; the shared repo stays clean.
- Alternative: trainees add the shared repo as a second Git folder (read-only use) and **Pull** each morning to get new material.

## Updating during the training

```bash
python tools/build_trainee_version.py          # regenerate trainee repo
# then commit & push both repos (GitHub Desktop or git CLI)
```
