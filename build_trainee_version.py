"""
Builds the TRAINEE repository from this TRAINER repository.

Removes everything marked with 🎤 (trainer notes, trainer answers, exam answers,
solutions headers) and code cells starting with "# SOLUTION".

Expected layout (both repos cloned side by side):
    <parent>/loopfuture-databricks-training-trainer/   <- this repo
    <parent>/loopfuture-databricks-training/           <- trainee repo (created/updated)

Usage (from anywhere):
    python tools/build_trainee_version.py                    # all weekN folders
    python tools/build_trainee_version.py week1              # only week1
    python tools/build_trainee_version.py week1 --with-solutions   # keep exercise solutions
"""
import os
import re
import shutil
import sys

TRAINER_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAINEE_ROOT = os.path.join(os.path.dirname(TRAINER_ROOT), "loopfuture-databricks-training")
TEMPLATES = os.path.join(TRAINER_ROOT, "tools", "templates")
SEP_IN = "\n# COMMAND ----------\n"
SEP_OUT = "\n\n# COMMAND ----------\n\n"

args = [a for a in sys.argv[1:] if not a.startswith("--")]
KEEP_SOLUTIONS = "--with-solutions" in sys.argv


def first_content_line(cell: str) -> str:
    for line in cell.strip().splitlines():
        text = line.replace("# MAGIC", "", 1).strip()
        if text and text != "%md":
            return text
    return ""


def clean_notebook(text: str) -> str:
    out = []
    for cell in text.split(SEP_IN):
        stripped = cell.strip()
        if stripped.startswith("# SOLUTION") and not KEEP_SOLUTIONS:
            continue
        first = first_content_line(cell)
        if "🎤" in first and not (KEEP_SOLUTIONS and "Solutions" in first):
            continue
        lines = cell.splitlines()
        # cut a "---" + "### 🎤 Trainer notes" block until the end of the cell
        for i, line in enumerate(lines):
            if "### 🎤" in line:
                start = i - 1 if i > 0 and lines[i - 1].strip() == "# MAGIC ---" else i
                if start > 0 and lines[start - 1].strip() == "# MAGIC":
                    start -= 1
                lines = lines[:start]
                break
        # remove "> 🎤 ..." quote blocks (and their continuation lines)
        cleaned, skipping = [], False
        for line in lines:
            if line.startswith("# MAGIC > 🎤"):
                skipping = True
                if cleaned and cleaned[-1].strip() == "# MAGIC":
                    cleaned.pop()
                continue
            if skipping and line.startswith("# MAGIC >"):
                continue
            skipping = False
            cleaned.append(line)
        new_cell = "\n".join(cleaned).strip("\n")
        if new_cell.strip() in ("", "# MAGIC %md"):
            continue
        out.append(new_cell)
    return SEP_OUT.join(out) + "\n"


def clean_sql(text: str) -> str:
    return re.sub(r"--\n-- TRAINER NOTES.*?(?=-- =====)", "", text, flags=re.S)


def build_week(week: str) -> None:
    src = os.path.join(TRAINER_ROOT, week)
    dst = os.path.join(TRAINEE_ROOT, week)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    for name in sorted(os.listdir(src)):
        path = os.path.join(src, name)
        if not os.path.isfile(path) or name == "README.md":
            continue
        text = open(path, encoding="utf-8").read()
        if name.endswith(".py"):
            text = clean_notebook(text)
        elif name.endswith(".sql"):
            text = clean_sql(text)
        open(os.path.join(dst, name), "w", encoding="utf-8").write(text)
        assert "🎤" not in text and "TRAINER NOTES" not in text, f"trainer content leaked in {name}"
    template = os.path.join(TEMPLATES, f"README_{week}_trainees.md")
    if os.path.exists(template):
        shutil.copy(template, os.path.join(dst, "README.md"))
    print(f"built {week} -> {dst}")


if __name__ == "__main__":
    os.makedirs(TRAINEE_ROOT, exist_ok=True)
    weeks = args or sorted(d for d in os.listdir(TRAINER_ROOT) if d.startswith("week"))
    for week in weeks:
        build_week(week)
    # shared files
    os.makedirs(os.path.join(TRAINEE_ROOT, "docs"), exist_ok=True)
    shutil.copy(os.path.join(TRAINER_ROOT, "docs", "data_dictionary.md"),
                os.path.join(TRAINEE_ROOT, "docs", "data_dictionary.md"))
    shutil.copy(os.path.join(TEMPLATES, "README_root_trainees.md"), os.path.join(TRAINEE_ROOT, "README.md"))
    shutil.copy(os.path.join(TRAINER_ROOT, ".gitignore"), os.path.join(TRAINEE_ROOT, ".gitignore"))
    shutil.copy(os.path.join(TEMPLATES, "GETTING_STARTED.md"), os.path.join(TRAINEE_ROOT, "GETTING_STARTED.md"))
    print("done")
