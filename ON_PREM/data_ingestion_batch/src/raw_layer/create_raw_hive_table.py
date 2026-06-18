from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TFL Create Raw Hive Tables") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("=" * 60)
print("TFL - Creating Raw Hive External Tables")
print("=" * 60)

spark.sql("CREATE DATABASE IF NOT EXISTS tfl_db")
spark.sql("USE tfl_db")

# DROP before CREATE so stale LOCATION paths from old runs are replaced
spark.sql("DROP TABLE IF EXISTS dim_networks")
spark.sql("""
CREATE EXTERNAL TABLE dim_networks (
  network_id    INT,
  network_name  STRING,
  network_type  STRING,
  created_at    TIMESTAMP,
  updated_at    TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/tmp/tfl_project_hadoop/dim_networks_full_load'
TBLPROPERTIES ('skip.header.line.count'='1')
""")
print("dim_networks created")

spark.sql("DROP TABLE IF EXISTS dim_lines")
spark.sql("""
CREATE EXTERNAL TABLE dim_lines (
  line_id          INT,
  line_name        STRING,
  line_color       STRING,
  is_night_service BOOLEAN,
  created_at       TIMESTAMP,
  updated_at       TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/tmp/tfl_project_hadoop/dim_lines_full_load'
TBLPROPERTIES ('skip.header.line.count'='1')
""")
print("dim_lines created")

spark.sql("DROP TABLE IF EXISTS dim_stations")
spark.sql("""
CREATE EXTERNAL TABLE dim_stations (
  station_id              INT,
  nlc_code                STRING,
  station_name            STRING,
  network_id              INT,
  has_london_underground  BOOLEAN,
  has_elizabeth_line      BOOLEAN,
  has_overground          BOOLEAN,
  has_dlr                 BOOLEAN,
  has_night_tube          BOOLEAN,
  is_active               BOOLEAN,
  created_at              TIMESTAMP,
  updated_at              TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/tmp/tfl_project_hadoop/dim_stations_full_load'
TBLPROPERTIES ('skip.header.line.count'='1')
""")
print("dim_stations created")

spark.sql("DROP TABLE IF EXISTS dim_date")
spark.sql("""
CREATE EXTERNAL TABLE dim_date (
  date_id      INT,
  year         INT,
  quarter      INT,
  month        INT,
  is_annual    BOOLEAN,
  period_label STRING,
  period_start DATE,
  period_end   DATE,
  created_at   TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/tmp/tfl_project_hadoop/dim_date_full_load'
TBLPROPERTIES ('skip.header.line.count'='1')
""")
print("dim_date created")

spark.sql("DROP TABLE IF EXISTS fact_station_lines")
spark.sql("""
CREATE EXTERNAL TABLE fact_station_lines (
  station_line_id INT,
  station_id      INT,
  line_id         INT,
  is_interchange  BOOLEAN,
  effective_from  DATE,
  effective_to    DATE,
  created_at      TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/tmp/tfl_project_hadoop/fact_station_lines_full_load'
TBLPROPERTIES ('skip.header.line.count'='1')
""")
print("fact_station_lines created")

spark.sql("DROP TABLE IF EXISTS fact_passenger_entry_exit")
spark.sql("""
CREATE EXTERNAL TABLE fact_passenger_entry_exit (
  entry_exit_id     INT,
  station_id        INT,
  date_id           INT,
  total_entry_exit  INT,
  estimated_entries INT,
  estimated_exits   INT,
  record_type       STRING,
  data_source       STRING,
  created_at        TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/tmp/tfl_project_hadoop/fact_passenger_entry_exit_full_load'
TBLPROPERTIES ('skip.header.line.count'='1')
""")
print("fact_passenger_entry_exit created")

print("\nValidation - tables in tfl_db:")
spark.sql("SHOW TABLES").show()

print("=" * 60)
print("Raw Hive tables created successfully")
print("=" * 60)

spark.stop()
