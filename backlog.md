# Backlog — open work and ideas

Status: ⬜ to do · 🟨 in progress · ✅ done

## Before Monday 16 Nov (blocking)

- ⬜ **Run every week 1 notebook in a Free Edition account** (not a trial) and fix what fails: volume file writes from Python, `CREATE TABLE` without columns before `COPY INTO`, `samples.nyctaxi.trips`, SDP pipeline.
- ⬜ Confirm with Daniel: Academy Labs subscription (USD 200/person/year) yes or no — changes how much custom lab material is needed.
- ⬜ Pre-work message to trainees: create Free Edition + GitHub accounts **before** Monday, bring laptop.
- ⬜ Publish both repos on GitHub (`docs/github_setup.md`).
- ⬜ Fix 4 items in the planning Excel: 7 Dec labelled "Week 3" (is week 4); Exam Mapping section 6 missing 25 Nov, section 1 missing 23 Nov; week 3 owners empty.

## Week 1 content still missing

- ⬜ **Day 3 (18 Nov) – Spark & PySpark:** `Spark_Architecture` (driver/executors/stages/tasks, `explain`, Query Profile), `Joins_and_Unions` (inner, left, broadcast, multi-key, cross, union vs unionByName), `Transformations` (explode on review tags, dedup, aggregations, `approx_count_distinct`, `summary`).
- ⬜ **Day 4 (19 Nov) – Ingestion I:** `Auto_Loader_vs_COPY_INTO`, `Schema_Evolution_and_Rescued_Data` (the `language` field appearing in reviews batch 3), `Ingest_JSON_Nested` (reviewer struct, tags array).
- ⬜ **Day 5 (20 Nov) – Ingestion II:** `MERGE_INTO_Upserts` (late status updates: shipped → delivered / returned), `Choosing_an_Ingestion_Method` (Lakeflow Connect standard vs managed, JDBC/REST — demo/discussion only on Free Edition), `Mini_Project_Bronze_3_Sources` (orders CSV + reviews JSON + products), `Week1_Checkpoint_Quiz`.
- ⬜ Add a generator for **order status updates** (corrections file) to feed the MERGE exercise.

## Nice to have

- ⬜ Day 1 **theory slides**: lakehouse vs warehouse, medallion, control vs compute plane, compute types and cost, Unity Catalog object model.
- ⬜ One-page **PySpark ↔ SQL cheat sheet** for trainees.
- ⬜ **Mini-project brief + evaluation rubric** (what "done" means, how it is scored).
- ⬜ **Troubleshooting page**: common errors on Free Edition (quota reached, Git push errors, `%run` path, ANSI cast errors) and fixes.
- ⬜ **Databricks CLI + VS Code** setup guide (day 2 in the plan: authentication profiles).
- ⬜ **Progress tracker**: who finished each notebook / pushed to GitHub / exam-question score.
- ⬜ End-of-week **feedback form** for trainees.
- ⬜ **Hand-off note to Samantha** (week 2): what was covered, what each trainee struggled with, state of the ShopLoop tables (week 2 starts from the week 1 bronze tables).
- ⬜ Reuse the **ShopLoop** dataset in weeks 2–3 (SDP + AUTO CDC on status updates, Jobs, bundles, Unity Catalog masks on customer e-mail) so the whole program tells one story.
- ⬜ Build the trainee repo automatically with a **GitHub Action** on every push to the trainer repo (week 2 CI/CD example!).

## Done

- ✅ Teams team + private trainers channel, welcome message, useful links
- ✅ Week 1 notebooks 00–06 with trainer notes, Check yourself, exam-style questions
- ✅ ShopLoop dataset (customers, products, daily orders, nested JSON reviews)
- ✅ Trainer / trainee split + build tool
