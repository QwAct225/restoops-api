\c restoops;

\echo '📊 Loading data from CSV files...';

\set ON_ERROR_STOP off
\copy menu_data(id, nama_menu, harga, variants, sold_out, image_url) FROM '/docker-entrypoint-initdb.d/data/menu_data.csv' DELIMITER ',' CSV HEADER;
\set ON_ERROR_STOP on

\set ON_ERROR_STOP off
\copy reservation_data(id, name, reservation_table, token, ordered_menu, duration) FROM '/docker-entrypoint-initdb.d/data/reservation_data.csv' DELIMITER ',' CSV HEADER;
\set ON_ERROR_STOP on

\echo '📈 Data loading summary:';
SELECT 'Menu items loaded: ' || COUNT(*)::text FROM menu_data;
SELECT 'Reservations loaded: ' || COUNT(*)::text FROM reservation_data;

\echo '✅ Data loading completed!';
