# Mergington High School Activities API

A FastAPI application that allows students to view and sign up for extracurricular activities. 
This version uses a persistent database (MySQL or SQLite) for reliable data storage and multi-user access.

## Features

- View all available extracurricular activities
- Sign up for activities with persistent data storage
- Support for multiple user roles (student, teacher, admin)
- Database-backed storage with ORM (SQLAlchemy)
- Support for both MySQL (production) and SQLite (development)
- Extensible schema for future features like announcements, events, surveys, and membership workflows

## Getting Started

1. Install the dependencies:

   ```bash
   pip install -r ../requirements.txt
   ```

2. Configure your database (optional):

   - Copy `.env.example` to `.env` if you want to customize database settings
   - Default uses SQLite for development: `activities.db`
   - For MySQL production: update `DATABASE_URL` in `.env`

3. Run the application:

   ```bash
   python app.py
   ```

   The database will be automatically initialized on first run with seed data.

4. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## Database Setup

### Development (SQLite - Default)

The application automatically uses SQLite for development. The database file `activities.db` will be created in the project root on first run.

### Production (MySQL)

To use MySQL:

1. Install MySQL and create a database:
   ```sql
   CREATE DATABASE mergington_activities;
   ```

2. Update `.env` with your MySQL credentials:
   ```
   DATABASE_URL=mysql+mysql-connector-python://user:password@localhost:3306/mergington_activities
   ```

3. Run the application - tables will be created automatically

### Manual Database Initialization

If needed, you can manually initialize the database:

```bash
python ../init_db.py          # Create tables
python ../init_db.py --reset  # Reset database (WARNING: deletes all data)
```

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister from an activity                                    |

## Data Model

The application uses a comprehensive ORM-based data model:

### Core Tables

1. **Activities** - Extracurricular activities/clubs:
   - name (unique identifier)
   - description
   - schedule
   - category (for filtering)
   - max_participants
   - is_active
   - timestamps

2. **Users** - Students, teachers, and admins:
   - email (unique identifier)
   - username
   - role (student, teacher, admin)
   - timestamps

3. **Activity_Participants** (junction table):
   - Many-to-many relationship between Users and Activities
   - Tracks who is signed up for what

### Future-Ready Tables (for planned features)

- **Memberships** - For membership request/approval workflows
- **Announcements** - Club announcements and communications
- **Events** - Event scheduling and calendar management
- **Surveys** - Questionnaires and feedback collection
- **SurveyQuestions** & **SurveyResponses** - Survey data storage

## Data Persistence

All data is now persisted in the database:
- Data survives server restarts
- Supports concurrent access from multiple users
- Optimized queries with proper database indexing
- connection pooling for better performance
