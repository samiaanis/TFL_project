-- =====================================================
-- TFL DATA WAREHOUSE - IMPALA RAW LAYER REGISTRATION
-- Run after create_raw_hive_table.hql so Impala can
-- see the raw external tables for dashboard queries.
-- =====================================================

INVALIDATE METADATA tfl_db.dim_networks;
INVALIDATE METADATA tfl_db.dim_lines;
INVALIDATE METADATA tfl_db.dim_stations;
INVALIDATE METADATA tfl_db.dim_date;
INVALIDATE METADATA tfl_db.fact_station_lines;
INVALIDATE METADATA tfl_db.fact_passenger_entry_exit;

COMPUTE STATS tfl_db.dim_networks;
COMPUTE STATS tfl_db.dim_lines;
COMPUTE STATS tfl_db.dim_stations;
COMPUTE STATS tfl_db.dim_date;
COMPUTE STATS tfl_db.fact_station_lines;
COMPUTE STATS tfl_db.fact_passenger_entry_exit;
