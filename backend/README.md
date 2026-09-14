# Pentecost Church Backend Setup

This folder contains a simple SQLite-based backend structure for the church website.

## Files

- `database/schema.sql` - database schema for all main tables
- `database/seed.sql` - sample data for testing and development

## Setup

1. Create a SQLite database file:
   ```bash
   sqlite3 backend/database/pentecost_church.db < backend/database/schema.sql
   sqlite3 backend/database/pentecost_church.db < backend/database/seed.sql
   ```

2. Use the database in your application code.

## Tables

- users
- members
- pastors
- ministries
- services
- sermons
- events
- bible_verses
- daily_quotes
- prayer_requests
- offerings
- announcements
- gallery
- contacts
- notifications
