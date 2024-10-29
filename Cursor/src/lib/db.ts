import Database from 'better-sqlite3'
import path from 'path'
import fs from 'fs'

// Ensure the data directory exists
const dataDir = path.join(process.cwd(), 'data')
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir)
}

// Create database in the data directory
const dbPath = path.join(dataDir, 'database.sqlite')

// Create database connection with proper settings but without verbose logging
const db = new Database(dbPath, { 
  fileMustExist: false // Allow creating new database file
})

// Enable foreign keys and WAL mode for better performance and reliability
db.pragma('foreign_keys = ON')
db.pragma('journal_mode = WAL')

// Create tables only if they don't exist
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL,
    lastActive TEXT NOT NULL,
    password TEXT NOT NULL
  );

  CREATE TABLE IF NOT EXISTS sensors (
    id TEXT PRIMARY KEY,
    equipmentId TEXT NOT NULL,
    apiId TEXT NOT NULL,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL,
    item TEXT NOT NULL
  );

  CREATE TABLE IF NOT EXISTS access_rules (
    id TEXT PRIMARY KEY,
    userId TEXT NOT NULL,
    sensorId TEXT NOT NULL,
    view BOOLEAN NOT NULL DEFAULT 0,
    control BOOLEAN NOT NULL DEFAULT 0,
    configure BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (sensorId) REFERENCES sensors(id) ON DELETE CASCADE
  );
`)

export default db 