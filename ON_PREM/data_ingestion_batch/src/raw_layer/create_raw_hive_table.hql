-- =====================================================
-- TFL DATA WAREHOUSE - HIVE RAW LAYER
-- Creates external tables over HDFS Sqoop output
-- =====================================================

-- =========================
-- STEP 1: DATABASE SETUP
-- =========================

CREATE DATABASE IF NOT EXISTS tfl_db;

USE tfl_db;

-- =========================
-- STEP 2: DIMENSION TABLES
-- =========================

CREATE EXTERNAL TABLE IF NOT EXISTS dim_networks (
  network_id INT,
  network_name VARCHAR(100),
  network_type VARCHAR(50),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/tmp/tfl_project_hadoop/dim_networks_full_load'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE IF NOT EXISTS dim_lines (
  line_id INT,
  line_name VARCHAR(100),
  line_color VARCHAR(7),
  is_night_service BOOLEAN,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/tmp/tfl_project_hadoop/dim_lines_full_load'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE IF NOT EXISTS dim_stations (
  station_id INT,
  nlc_code VARCHAR(20),
  station_name VARCHAR(200),
  network_id INT,
  has_london_underground BOOLEAN,
  has_elizabeth_line BOOLEAN,
  has_overground BOOLEAN,
  has_dlr BOOLEAN,
  has_night_tube BOOLEAN,
  is_active BOOLEAN,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/tmp/tfl_project_hadoop/dim_stations_full_load'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE IF NOT EXISTS dim_date (
  date_id INT,
  year INT,
  quarter INT,
  month INT,
  is_annual BOOLEAN,
  period_label VARCHAR(50),
  period_start DATE,
  period_end DATE,
  created_at TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/tmp/tfl_project_hadoop/dim_date_full_load'
TBLPROPERTIES ("skip.header.line.count"="1");

-- =========================
-- STEP 3: FACT TABLES
-- =========================

CREATE EXTERNAL TABLE IF NOT EXISTS fact_station_lines (
  station_line_id INT,
  station_id INT,
  line_id INT,
  is_interchange BOOLEAN,
  effective_from DATE,
  effective_to DATE,
  created_at TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/tmp/tfl_project_hadoop/fact_station_lines_full_load'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE IF NOT EXISTS fact_passenger_entry_exit (
  entry_exit_id INT,
  station_id INT,
  date_id INT,
  total_entry_exit INT,
  estimated_entries INT,
  estimated_exits INT,
  record_type VARCHAR(20),
  data_source VARCHAR(20),
  created_at TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/tmp/tfl_project_hadoop/fact_passenger_entry_exit_full_load'
TBLPROPERTIES ("skip.header.line.count"="1");

-- =========================
-- STEP 4: VALIDATION
-- =========================

SHOW TABLES;
