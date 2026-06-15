-- WMS Database Schema

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL, -- 'admin', 'warehouse_keeper', 'supervisor'
    job_title TEXT,
    department TEXT,
    status TEXT DEFAULT 'active',
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Suppliers Table
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    notes TEXT,
    is_deleted INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Warehouse Locations Table
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, -- 'مخزن رئيسي', 'رف A1', etc.
    description TEXT,
    is_deleted INTEGER DEFAULT 0
);

-- Items Table
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category TEXT,
    unit TEXT,
    location_id INTEGER,
    min_stock INTEGER DEFAULT 0,
    current_stock INTEGER DEFAULT 0,
    image_path TEXT,
    description TEXT,
    is_deleted INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

-- Stock Movements (In/Out)
CREATE TABLE IF NOT EXISTS movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL, -- 'IN' (Receiving), 'OUT' (Issuing)
    reference_no TEXT NOT NULL, -- Invoice number or operation ID
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    supplier_id INTEGER, -- For IN
    received_by TEXT, -- For IN
    issuing_entity TEXT, -- For OUT (الجهة المستلمة)
    receiver_name TEXT, -- For OUT (اسم الشخص المستلم)
    employee_name TEXT, -- For OUT (الموظف الذي قام بالصرف)
    reason TEXT, -- For OUT
    notes TEXT,
    discount_percent REAL DEFAULT 0,
    discount_amount REAL DEFAULT 0,
    subtotal REAL DEFAULT 0,
    final_total REAL DEFAULT 0,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

-- Movement Items (Details)
CREATE TABLE IF NOT EXISTS movement_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movement_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL DEFAULT 0, -- For IN
    FOREIGN KEY (movement_id) REFERENCES movements(id),
    FOREIGN KEY (item_id) REFERENCES items(id)
);

-- Audit Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    table_name TEXT,
    record_id INTEGER,
    details TEXT,
    old_value TEXT,
    new_value TEXT,
    device_name TEXT,
    ip_address TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Company Settings
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT DEFAULT 'American Marine Services Free-Zone',
    logo_path TEXT,
    address TEXT,
    phone TEXT,
    email TEXT
);

-- Initialize default settings
INSERT INTO settings (company_name) SELECT 'American Marine Services Free-Zone' WHERE NOT EXISTS (SELECT 1 FROM settings);
