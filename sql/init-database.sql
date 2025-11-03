SELECT 'CREATE DATABASE restoops'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'restoops')\gexec

\echo 'Setting up RestoOps tables...';
\i /docker-entrypoint-initdb.d/02-init-tables.sql

\c restoops
GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;

\echo '✅ PostgreSQL database created successfully!'
\echo '   - restoops (Menu and Reservation data)'
