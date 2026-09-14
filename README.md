# Pentecost Church Platform

This project is being built as a complete church platform, not only as a static information website.

## Project Phases

### Phase 1: Public website foundation
- Home
- About
- Services
- Sermons
- Events
- Ministries
- Contact

Status: Implemented as a static website with multi-page navigation and church-themed design.

### Phase 2: Community and engagement features
- Verse of the Day
- Quote of the Day
- Gallery
- Prayer Request

Status: Core pages and UI are present. Prayer requests and daily content are currently mock/frontend-based and can be connected to the database later.

### Phase 3: Admin and content management
- Admin Login
- Admin Dashboard
- Content Management

Status: Admin login/dashboard shell has been added. Content management currently uses browser localStorage for demo purposes and should be upgraded to a real backend/admin API.

### Phase 4: Members, giving, notifications, and database
- Members
- Giving
- Notifications
- Database

Status: SQLite database structure and seed data have been created. Member, giving, and notification flows still need a proper backend/API layer for full production behavior.

### Phase 5: Authentication, security, payment integration, and deployment
- Authentication
- Security
- Payment Integration
- Deployment

Status: Pending implementation.

## Current Architecture

### Frontend
- HTML pages for public and member/admin areas
- CSS for branding and responsive layout
- JavaScript for interactivity, localStorage-based mock flows, tabs, search, and admin demo editing

### Backend foundation
- SQLite database structure under `backend/database/`
- Schema file: `backend/database/schema.sql`
- Seed file: `backend/database/seed.sql`
- Database initializer: `backend/database/init_db.py`

## Recommended next implementation order

1. Add a lightweight backend server (Node.js or Python Flask/FastAPI)
2. Build REST APIs for:
   - sermons
   - events
   - ministries
   - prayer requests
   - offerings
   - daily quotes
   - bible verses
   - gallery
   - contacts
3. Replace localStorage-only admin/member behavior with real authentication and database-backed CRUD
4. Add notifications and member dashboards powered by real data
5. Add payment integration for offerings and donations
6. Add security controls and deployment configuration

## Key goal

The project should evolve from a church website into a fully connected church platform where:
- visitors can browse public content
- members can log in and view personalized data
- admin can manage content through a dashboard
- the database stores the platform’s real content
- authentication, payments, and deployment are production-ready
