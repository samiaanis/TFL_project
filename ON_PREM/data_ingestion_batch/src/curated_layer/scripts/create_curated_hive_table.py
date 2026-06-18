from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TFL Create Curated Hive Tables") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("=" * 60)
print("TFL - Creating Curated Hive External Tables")
print("=" * 60)

base_path = "/tmp/tfl_project_hadoop/curated"

spark.sql("USE tfl_db")

spark.sql(f"""
CREATE EXTERNAL TABLE IF NOT EXISTS dim_networks_curated (
    network_id     INT,
    network_name   STRING,
    network_type   STRING,
    load_timestamp TIMESTAMP
)
STORED AS PARQUET
LOCATION '{base_path}/dim_networks'
""")
print("dim_networks_curated created")

spark.sql(f"""
CREATE EXTERNAL TABLE IF NOT EXISTS dim_lines_curated (
    line_id            INT,
    line_name          STRING,
    line_color         STRING,
    night_service_flag STRING,
    load_timestamp     TIMESTAMP
)
STORED AS PARQUET
LOCATION '{base_path}/dim_lines'
""")
print("dim_lines_curated created")

spark.sql(f"""
CREATE EXTERNAL TABLE IF NOT EXISTS dim_stations_curated (
    station_id             INT,
    station_code           STRING,
    station_name           STRING,
    network_id             INT,
    network_name           STRING,
    has_london_underground STRING,
    has_elizabeth_line     STRING,
    has_overground         STRING,
    has_dlr                STRING,
    has_night_tube         STRING,
    active_status          STRING,
    load_timestamp         TIMESTAMP
)
STORED AS PARQUET
LOCATION '{base_path}/dim_stations'
""")
print("dim_stations_curated created")

spark.sql(f"""
CREATE EXTERNAL TABLE IF NOT EXISTS dim_date_curated (
    date_id        INT,
    year           INT,
    quarter        INT,
    month          INT,
    is_annual      STRING,
    period_label   STRING,
    period_start   DATE,
    period_end     DATE,
    load_timestamp TIMESTAMP
)
STORED AS PARQUET
LOCATION '{base_path}/dim_date'
""")
print("dim_date_curated created")

spark.sql(f"""
CREATE EXTERNAL TABLE IF NOT EXISTS fact_station_lines_curated (
    station_line_id INT,
    station_id      INT,
    station_name    STRING,
    line_id         INT,
    line_name       STRING,
    is_interchange  STRING,
    effective_from  DATE,
    effective_to    DATE,
    load_timestamp  TIMESTAMP
)
STORED AS PARQUET
LOCATION '{base_path}/fact_station_lines'
""")
print("fact_station_lines_curated created")

spark.sql(f"""
CREATE EXTERNAL TABLE IF NOT EXISTS fact_passenger_entry_exit_curated (
    entry_exit_id          INT,
    station_id             INT,
    station_name           STRING,
    year                   INT,
    total_entry_exit       BIGINT,
    estimated_entries      BIGINT,
    estimated_exits        BIGINT,
    passenger_volume_band  STRING,
    record_type            STRING,
    data_source            STRING,
    load_timestamp         TIMESTAMP
)
STORED AS PARQUET
LOCATION '{base_path}/fact_passenger_entry_exit'
""")
print("fact_passenger_entry_exit_curated created")

print("\nValidation - curated tables in tfl_db:")
spark.sql("SHOW TABLES IN tfl_db LIKE '*curated*'").show()

print("=" * 60)
print("Curated Hive tables created successfully")
print("=" * 60)

spark.stop()
