-- =====================================================
-- TFL DATA WAREHOUSE - IMPALA CURATED LAYER REGISTRATION
-- Run after curated_full_load.hql so Impala can see
-- the curated parquet tables for dashboard queries.
-- =====================================================

INVALIDATE METADATA tfl_db.dim_networks_curated;
INVALIDATE METADATA tfl_db.dim_lines_curated;
INVALIDATE METADATA tfl_db.dim_stations_curated;
INVALIDATE METADATA tfl_db.dim_date_curated;
INVALIDATE METADATA tfl_db.fact_station_lines_curated;
INVALIDATE METADATA tfl_db.fact_passenger_entry_exit_curated;

COMPUTE STATS tfl_db.dim_networks_curated;
COMPUTE STATS tfl_db.dim_lines_curated;
COMPUTE STATS tfl_db.dim_stations_curated;
COMPUTE STATS tfl_db.dim_date_curated;
COMPUTE STATS tfl_db.fact_station_lines_curated;
COMPUTE STATS tfl_db.fact_passenger_entry_exit_curated;
