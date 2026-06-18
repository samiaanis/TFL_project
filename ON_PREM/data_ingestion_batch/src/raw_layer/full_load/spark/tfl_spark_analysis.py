from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, count, avg, desc
from pyspark.sql.types import IntegerType

spark = SparkSession.builder \
    .appName("TFL_Analysis_Group") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

OUTPUT_BASE = "/tmp/tfl_project_hadoop/gold"
HIVE_DB     = "tfl_db"

spark.sql(f"USE {HIVE_DB}")

print("=" * 60)
print("TFL Data Analysis Pipeline")
print("=" * 60)

# ============================================================
# LOAD ALL TABLES FROM HIVE (created by create_raw_hive_table.hql)
# ============================================================

print("\nLoading tables from Hive tfl_db...")

dim_date     = spark.table(f"{HIVE_DB}.dim_date")
dim_lines    = spark.table(f"{HIVE_DB}.dim_lines")
dim_networks = spark.table(f"{HIVE_DB}.dim_networks")
dim_stations = spark.table(f"{HIVE_DB}.dim_stations")
fact_pax     = spark.table(f"{HIVE_DB}.fact_passenger_entry_exit")
fact_lines   = spark.table(f"{HIVE_DB}.fact_station_lines")

print("All 6 tables loaded successfully")

# Helper: write analysis result to HDFS as parquet.
# Hive external table registration is handled by hive_ddl.hql (runs after this stage).
def save_gold_table(df, table_name):
    path = f"{OUTPUT_BASE}/{table_name}"
    df.write.mode("overwrite").parquet(path)
    print(f"Saved to HDFS: {path}")

# ============================================================
# ANALYSIS 1: Top 10 Busiest Stations
# ============================================================

print("\n" + "=" * 60)
print("ANALYSIS 1: Top 10 Busiest Stations")
print("=" * 60)

busiest_stations = fact_pax \
    .join(dim_stations, "station_id") \
    .groupBy("station_name") \
    .agg(_sum("total_entry_exit").alias("total_passengers")) \
    .orderBy(desc("total_passengers")) \
    .limit(10)

busiest_stations.show(truncate=False)
save_gold_table(busiest_stations, "gold_busiest_stations")

# ============================================================
# ANALYSIS 2: Passengers by Year
# ============================================================

print("\n" + "=" * 60)
print("ANALYSIS 2: Total Passengers by Year")
print("=" * 60)

passengers_by_year = fact_pax \
    .join(dim_date, "date_id") \
    .groupBy("year") \
    .agg(_sum("total_entry_exit").alias("total_passengers")) \
    .orderBy("year")

passengers_by_year.show(truncate=False)
save_gold_table(passengers_by_year, "gold_passengers_by_year")

# ============================================================
# ANALYSIS 3: Passengers by Tube Line
# ============================================================

print("\n" + "=" * 60)
print("ANALYSIS 3: Passengers by Tube Line")
print("=" * 60)

passengers_by_line = fact_pax \
    .join(fact_lines, "station_id") \
    .join(dim_lines, "line_id") \
    .groupBy("line_name") \
    .agg(_sum("total_entry_exit").alias("total_passengers")) \
    .orderBy(desc("total_passengers"))

passengers_by_line.show(truncate=False)
save_gold_table(passengers_by_line, "gold_passengers_by_line")

# ============================================================
# ANALYSIS 4: Passengers by Network
# ============================================================

print("\n" + "=" * 60)
print("ANALYSIS 4: Passengers by Network Type")
print("=" * 60)

passengers_by_network = fact_pax \
    .join(dim_stations, "station_id") \
    .join(dim_networks, "network_id") \
    .groupBy("network_name", "network_type") \
    .agg(_sum("total_entry_exit").alias("total_passengers")) \
    .orderBy(desc("total_passengers"))

passengers_by_network.show(truncate=False)
save_gold_table(passengers_by_network, "gold_passengers_by_network")

# ============================================================
# ANALYSIS 5: Interchange Stations
# ============================================================

print("\n" + "=" * 60)
print("ANALYSIS 5: Top Interchange Stations")
print("=" * 60)

interchange_stations = fact_lines \
    .join(dim_stations, "station_id") \
    .groupBy("station_name") \
    .agg(count("line_id").alias("num_lines")) \
    .orderBy(desc("num_lines")) \
    .limit(15)

interchange_stations.show(truncate=False)
save_gold_table(interchange_stations, "gold_interchange_stations")

# ============================================================
# ANALYSIS 6: Quarterly Trend
# ============================================================

print("=" * 60)
print("ANALYSIS 6: Passengers by Year and Quarter")
print("=" * 60)

passengers_by_year_quarter = fact_pax.join(
    dim_date,
    fact_pax.date_id == dim_date.date_id,
    "inner"
).select(
    fact_pax.total_entry_exit,
    dim_date.year,
    dim_date.quarter
).withColumn(
    "year", col("year").cast("int")
).withColumn(
    "quarter", col("quarter").cast("int")
).withColumn(
    "total_entry_exit", col("total_entry_exit").cast("long")
).groupBy(
    "year",
    "quarter"
).agg(
    _sum("total_entry_exit").alias("total_passengers")
).orderBy(
    "year",
    "quarter"
)

passengers_by_year_quarter.show()

passengers_by_year_quarter.write.mode("overwrite").parquet(
    f"{OUTPUT_BASE}/gold_passengers_by_year_quarter"
)

# ============================================================
# ANALYSIS 7: Night Tube Analysis
# ============================================================

print("\n" + "=" * 60)
print("ANALYSIS 7: Night Tube vs Regular Stations")
print("=" * 60)

night_tube_analysis = fact_pax \
    .join(dim_stations, "station_id") \
    .groupBy("has_night_tube") \
    .agg(
        count("station_id").alias("num_records"),
        _sum("total_entry_exit").alias("total_passengers"),
        avg("total_entry_exit").alias("avg_passengers_per_record")
    )

night_tube_analysis.show(truncate=False)
save_gold_table(night_tube_analysis, "gold_night_tube_analysis")

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("PIPELINE COMPLETE")
print("=" * 60)
print(f"Database: {HIVE_DB}")
print("Source tables: dim_date, dim_lines, dim_networks, dim_stations,")
print("               fact_passenger_entry_exit, fact_station_lines")
print("Gold tables:   gold_busiest_stations, gold_passengers_by_year,")
print("               gold_passengers_by_line, gold_passengers_by_network,")
print("               gold_interchange_stations, gold_quarterly_trend,")
print("               gold_night_tube_analysis")
print("=" * 60)

spark.stop()
