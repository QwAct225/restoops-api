
\c restoops;

CREATE TABLE IF NOT EXISTS menu_data (
    id BIGINT PRIMARY KEY,
    nama_menu VARCHAR(200) NOT NULL,
    harga DECIMAL(10,2) NOT NULL,
    variants JSONB,
    sold_out VARCHAR(10) DEFAULT 'No',
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_menu_nama ON menu_data(nama_menu);
CREATE INDEX IF NOT EXISTS idx_menu_harga ON menu_data(harga);
CREATE INDEX IF NOT EXISTS idx_menu_sold_out ON menu_data(sold_out);

CREATE TABLE IF NOT EXISTS reservation_data (
    id BIGINT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    reservation_table INT NOT NULL,
    token VARCHAR(50) UNIQUE NOT NULL,
    ordered_menu JSONB NOT NULL,
    duration INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_reservation_name ON reservation_data(name);
CREATE INDEX IF NOT EXISTS idx_reservation_token ON reservation_data(token);
CREATE INDEX IF NOT EXISTS idx_reservation_table ON reservation_data(reservation_table);
CREATE INDEX IF NOT EXISTS idx_reservation_duration ON reservation_data(duration);

\echo '✅ Tables created successfully!'
\echo '   - menu_data'
\echo '   - reservation_data'

