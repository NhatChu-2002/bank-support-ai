PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS support_tickets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticket_number TEXT UNIQUE NOT NULL,    
  customer_name TEXT,
  message TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'unresolved',  -- unresolved / in_progress / resolved
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Helps fast lookup by ticket number
CREATE INDEX IF NOT EXISTS idx_support_tickets_ticket_number
ON support_tickets(ticket_number);
