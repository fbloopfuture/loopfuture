# Databricks notebook source
# MAGIC %md
# MAGIC # 01 · Python & PySpark Basics
# MAGIC
# MAGIC A warm-up before the labs. Everything here is "obvious" once you've seen it, so we go fast and try things.
# MAGIC
# MAGIC | Block | Topic | Time |
# MAGIC |---|---|---|
# MAGIC | 0 | Notebook basics | 10 min |
# MAGIC | 1 | Python essentials | 25 min |
# MAGIC | 2 | From Python to Spark | 15 min |
# MAGIC | 3 | Your first DataFrame | 15 min |
# MAGIC | 4 | Everyday operations (PySpark ↔ SQL) | 30 min |
# MAGIC | 5 | Exercises | 20 min |
# MAGIC
# MAGIC **How to run a cell:** `Shift + Enter`. **Run everything:** *Run all* at the top.
# MAGIC
# MAGIC ---
# MAGIC ### 🎤 Trainer notes
# MAGIC - **Goal:** everyone leaves able to read and write simple PySpark. No AI assistant, no Genie today: we type the code ourselves so we understand it. The Assistant comes later, once the basics are solid.
# MAGIC - **Pace:** ask *"Who has programmed in Python before?"* at the start. If most say yes, go through Block 1 in 10 minutes as a review.
# MAGIC - **Method:** run each cell live, then ask a trainee to change one thing (a value, a column, a filter) and run it again. Small changes = fast learning.
# MAGIC - **Key message of the day:** *PySpark and SQL are two ways of saying the same thing to the same engine.* Repeat it in Block 4.
# MAGIC - **Common mistakes to watch for:** forgetting quotes around column names, mixing `=` and `==`, expecting a transformation to "do something" without an action.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Block 0 · Notebook basics
# MAGIC
# MAGIC - A notebook is a list of **cells**. Each cell has a language: Python (default here), SQL, or Markdown.
# MAGIC - Change the language of one cell with a **magic command** on the first line: `%sql`, `%md`, `%python`.
# MAGIC - `display(...)` shows tables and charts nicely. `print(...)` shows plain text.
# MAGIC - Variables created in one Python cell are available in the next ones (same **session**).

# COMMAND ----------

print("Hello, Databricks!")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- This cell is SQL because of the %sql magic on the first line
# MAGIC SELECT 'Hello from SQL' AS greeting, current_date() AS today, current_user() AS me

# COMMAND ----------

# MAGIC %md
# MAGIC This cell is **Markdown** (`%md`): use it to document your notebook — titles, lists, `code`, links.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Block 1 · Python essentials
# MAGIC Only what we will actually use with PySpark.
# MAGIC
# MAGIC | Concept | Why it matters in PySpark |
# MAGIC |---|---|
# MAGIC | variables & types | column values have types too (string, int, double, date…) |
# MAGIC | lists | lists of column names: `df.select(["a", "b"])` |
# MAGIC | dictionaries | rows, configs, options: `{"header": "true"}` |
# MAGIC | functions | reusable transformations in pipelines |
# MAGIC | f-strings | building table names and paths: `f"{catalog}.{schema}.orders"` |
# MAGIC
# MAGIC > 🎤 *Trainer:* in Python, **indentation is syntax** (4 spaces define a block). Show what happens when you remove it.

# COMMAND ----------

# Variables and basic types
name = "Lara"            # str
orders = 3               # int
price = 19.9             # float
is_customer = True       # bool

print(type(name), type(orders), type(price), type(is_customer))

# f-strings: the easiest way to build text
print(f"{name} placed {orders} orders, total = {orders * price:.2f} €")

# COMMAND ----------

# Lists: ordered collections, positions start at 0 (and -1 = last element)
products = ["Laptop", "Mouse", "Keyboard"]
products.append("Monitor")
print(products)
print(products[0], products[-1], len(products))

# Dictionaries: key -> value
customer = {"id": 1, "name": "Rodrigo", "country": "PT"}
print(customer["name"])
customer["vip"] = True
print(customer)

# COMMAND ----------

# if / for
for p in products:
    if p.startswith("M"):
        print(f"{p} starts with M")
    else:
        print(f"{p} does not")

# List comprehension: a compact for-loop that builds a list
upper_products = [p.upper() for p in products]
print(upper_products)

# COMMAND ----------

# Functions
def total_with_vat(amount: float, vat: float = 0.23) -> float:
    """Returns the amount with VAT applied."""
    return round(amount * (1 + vat), 2)

print(total_with_vat(100))
print(total_with_vat(100, vat=0.06))

# COMMAND ----------

# A list of dictionaries = a "table" in plain Python. Keep this in mind for Block 3.
sales = [
    {"order_id": 1, "customer": "Lara",    "product": "Laptop",   "qty": 1, "price": 899.0},
    {"order_id": 2, "customer": "Rodrigo", "product": "Mouse",    "qty": 2, "price": 19.9},
    {"order_id": 3, "customer": "Lara",    "product": "Keyboard", "qty": 1, "price": 49.9},
]
total = sum(s["qty"] * s["price"] for s in sales)
print(f"Total revenue: {total:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Block 2 · From Python to Spark
# MAGIC
# MAGIC | | Python list | pandas DataFrame | **Spark DataFrame** |
# MAGIC |---|---|---|---|
# MAGIC | Where it runs | 1 machine | 1 machine | **many machines (cluster)** |
# MAGIC | Size | small | fits in memory | **huge** |
# MAGIC | Execution | immediate | immediate | **lazy** |
# MAGIC
# MAGIC - `spark` is the **SparkSession**: your entry point to Spark. In Databricks it already exists.
# MAGIC - **Transformations** (`select`, `filter`, `withColumn`, `groupBy`…) only build a *plan*. Nothing runs yet.
# MAGIC - **Actions** (`show`, `display`, `count`, `collect`, `write`…) execute the plan.
# MAGIC - This is called **lazy evaluation**: Spark waits until it sees the whole plan, then optimizes it.

# COMMAND ----------

spark  # already created for you

# COMMAND ----------

# MAGIC %md
# MAGIC > 🎤 *Trainer:* use a restaurant analogy. The **driver** is the head chef who reads the order (your code) and plans the work; the **executors** are the cooks who each prepare part of it in parallel. A **transformation** is writing the recipe; an **action** is "serve it now!". Spark architecture in detail is day 3.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Block 3 · Your first DataFrame

# COMMAND ----------

# From the Python list of dictionaries above
df_sales = spark.createDataFrame(sales)
display(df_sales)

# COMMAND ----------

df_sales.printSchema()      # column names and types
print(df_sales.count())     # action: number of rows
print(df_sales.columns)     # list of column names

# COMMAND ----------

# Explicit schema (recommended in real pipelines: no guessing of types)
# Each StructField = (column name, type, can it be null?)
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

schema = StructType([
    StructField("order_id", IntegerType(), False),
    StructField("customer", StringType(), True),
    StructField("product", StringType(), True),
    StructField("qty", IntegerType(), True),
    StructField("price", DoubleType(), True),
])
rows = [(s["order_id"], s["customer"], s["product"], s["qty"], s["price"]) for s in sales]
df_sales = spark.createDataFrame(rows, schema)
df_sales.printSchema()

# COMMAND ----------

# Reading an existing table (Databricks ships sample data in the `samples` catalog)
df_trips = spark.table("samples.nyctaxi.trips")
display(df_trips.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Block 4 · Everyday operations — PySpark and SQL side by side
# MAGIC The same question can be answered in PySpark or SQL. Spark runs both through the **same engine**.
# MAGIC
# MAGIC | SQL | PySpark |
# MAGIC |---|---|
# MAGIC | `SELECT a, b` | `df.select("a", "b")` |
# MAGIC | `SELECT *, x * y AS z` | `df.withColumn("z", F.col("x") * F.col("y"))` |
# MAGIC | `WHERE a > 10` | `df.filter(F.col("a") > 10)` |
# MAGIC | `GROUP BY a` + `SUM(b)` | `df.groupBy("a").agg(F.sum("b"))` |
# MAGIC | `ORDER BY a DESC` | `df.orderBy(F.desc("a"))` |
# MAGIC | `LIMIT 10` | `df.limit(10)` |
# MAGIC
# MAGIC > 🎤 *Trainer:* keep this table on screen while doing the exercises. Methods can be **chained** (one after the other), which reads top-to-bottom like a SQL query. Use `\` or parentheses to split long chains over several lines.

# COMMAND ----------

# `F` is the usual alias for the library of column functions (col, sum, count, upper, when…)
from pyspark.sql import functions as F

# select + new column
df = df_sales.select("customer", "product", "qty", "price") \
             .withColumn("amount", F.col("qty") * F.col("price"))
display(df)

# COMMAND ----------

# filter (where)
display(df.filter(F.col("amount") > 40))

# COMMAND ----------

# groupBy + aggregations + orderBy
display(
    df.groupBy("customer")
      .agg(F.count("*").alias("n_orders"), F.round(F.sum("amount"), 2).alias("revenue"))
      .orderBy(F.desc("revenue"))
)

# COMMAND ----------

# The SAME in SQL: register the DataFrame as a temporary view first
df_sales.createOrReplaceTempView("v_sales")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customer,
# MAGIC        COUNT(*)                         AS n_orders,
# MAGIC        ROUND(SUM(qty * price), 2)       AS revenue
# MAGIC FROM v_sales
# MAGIC GROUP BY customer
# MAGIC ORDER BY revenue DESC

# COMMAND ----------

# And SQL from Python: spark.sql returns a DataFrame
df_from_sql = spark.sql("SELECT product, SUM(qty) AS units FROM v_sales GROUP BY product")
display(df_from_sql)

# COMMAND ----------

# Useful column functions
display(
    df_sales
      .withColumn("product_upper", F.upper("product"))
      .withColumn("size", F.when(F.col("price") > 100, "big").otherwise("small"))
      .withColumnRenamed("qty", "quantity")
      .drop("order_id")
)

# COMMAND ----------

# The same idea on a real-sized table: average fare by pickup zip
display(
    df_trips.groupBy("pickup_zip")
            .agg(F.count("*").alias("trips"), F.round(F.avg("fare_amount"), 2).alias("avg_fare"))
            .orderBy(F.desc("trips"))
            .limit(10)
)

# COMMAND ----------

# Peek at what Spark plans to do (lazy evaluation in action)
df_trips.filter(F.col("fare_amount") > 50).select("pickup_zip", "fare_amount").explain()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Block 5 · Exercises
# MAGIC Use `df_trips` (`samples.nyctaxi.trips`). Solve each one in **PySpark**, then try it in **SQL**.
# MAGIC
# MAGIC 1. How many trips are in the table?
# MAGIC 2. Show the 5 most expensive trips (`fare_amount`), only the columns `tpep_pickup_datetime`, `trip_distance`, `fare_amount`.
# MAGIC 3. Add a column `fare_per_mile` = `fare_amount / trip_distance` (careful with distance = 0!).
# MAGIC 4. Count trips per `dropoff_zip` and keep only zips with more than 100 trips.
# MAGIC 5. Write a Python function `classify(distance)` that returns "short" (< 2), "medium" (< 10) or "long", then do the same with `F.when` on the DataFrame.
# MAGIC
# MAGIC Try each one on your own first. We correct them together at the end.

# COMMAND ----------

# Exercise 1


# COMMAND ----------

# Exercise 2


# COMMAND ----------

# Exercise 3


# COMMAND ----------

# Exercise 4


# COMMAND ----------

# Exercise 5


# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ### 🎤 Solutions (trainer version only)

# COMMAND ----------

# SOLUTION
# 1
print(df_trips.count())

# 2
display(df_trips.orderBy(F.desc("fare_amount")).select("tpep_pickup_datetime", "trip_distance", "fare_amount").limit(5))

# 3
display(df_trips.withColumn(
    "fare_per_mile",
    F.when(F.col("trip_distance") > 0, F.round(F.col("fare_amount") / F.col("trip_distance"), 2))
))

# 4
display(df_trips.groupBy("dropoff_zip").count().filter(F.col("count") > 100).orderBy(F.desc("count")))

# 5
def classify(distance):
    if distance < 2:
        return "short"
    elif distance < 10:
        return "medium"
    return "long"

print(classify(1.5), classify(5), classify(20))

display(df_trips.withColumn(
    "trip_type",
    F.when(F.col("trip_distance") < 2, "short").when(F.col("trip_distance") < 10, "medium").otherwise("long")
).groupBy("trip_type").count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📝 Exam-style practice (exam sections 3.2–3.4)
# MAGIC Pick one answer for each question. We discuss them together.
# MAGIC
# MAGIC **Q1.** Which of these is an **action** in Spark?
# MAGIC
# MAGIC - A. filter()
# MAGIC - B. withColumn()
# MAGIC - C. count()
# MAGIC - D. select()
# MAGIC
# MAGIC **Q2.** Which PySpark code returns the total `amount` per `customer`?
# MAGIC
# MAGIC - A. df.select('customer').sum('amount')
# MAGIC - B. df.groupBy('customer').agg(F.sum('amount'))
# MAGIC - C. df.filter('customer').agg('amount')
# MAGIC - D. df.orderBy('customer').sum()
# MAGIC
# MAGIC **Q3.** What does `df.createOrReplaceTempView('v_sales')` allow you to do?
# MAGIC
# MAGIC - A. Save the DataFrame as a Delta table in Unity Catalog
# MAGIC - B. Query the DataFrame with SQL during the current session
# MAGIC - C. Share the DataFrame with all workspace users
# MAGIC - D. Cache the DataFrame on disk
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🎤 Exam answers
# MAGIC - **Q1: C** — count() triggers execution; the others are lazy transformations.
# MAGIC - **Q2: B** — groupBy + agg is the PySpark equivalent of GROUP BY + SUM.
# MAGIC - **Q3: B** — A temporary view exists only in the current Spark session and is not persisted.
