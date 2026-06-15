-- Enhanced ERP Database Schema V2 (Cleaned)

-- Update Users Table
ALTER TABLE users ADD COLUMN job_title TEXT;
ALTER TABLE users ADD COLUMN department TEXT;
ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active';

-- Update Audit Logs Table
ALTER TABLE audit_logs ADD COLUMN old_value TEXT;
ALTER TABLE audit_logs ADD COLUMN new_value TEXT;
ALTER TABLE audit_logs ADD COLUMN device_name TEXT;
ALTER TABLE audit_logs ADD COLUMN ip_address TEXT;

-- Update Movements Table
ALTER TABLE movements ADD COLUMN discount_percent REAL DEFAULT 0;
ALTER TABLE movements ADD COLUMN discount_amount REAL DEFAULT 0;
ALTER TABLE movements ADD COLUMN subtotal REAL DEFAULT 0;
ALTER TABLE movements ADD COLUMN final_total REAL DEFAULT 0;

-- Update Items Table
ALTER TABLE items ADD COLUMN qr_code TEXT;

-- Granular Permissions Table
CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    module TEXT NOT NULL, -- 'items', 'suppliers', 'stock', 'reports', 'users', 'settings'
    can_view INTEGER DEFAULT 0,
    can_add INTEGER DEFAULT 0,
    can_edit INTEGER DEFAULT 0,
    can_delete INTEGER DEFAULT 0,
    can_print INTEGER DEFAULT 0,
    can_export INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, module)
);
