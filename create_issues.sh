#!/bin/bash

REPO="rajabhishek9060/skills-integrate-mcp-with-copilot"

# Array of issues to create
issues=(
  "Authentication & User Accounts|Add JWT-based authentication and user registration with password management and role-based access control (Student, Admin, Super Admin)"
  
  "Admin Dashboard|Create an admin interface for managing clubs, members, and system settings"
  
  "Persistent Database|Replace in-memory storage with a permanent database solution (MySQL/PostgreSQL) for data persistence"
  
  "Membership Request Workflow|Implement a request/approval system where students request to join clubs and admins approve or reject requests"
  
  "Q&A Forum Module|Add community discussion features allowing club members to ask questions and provide answers"
  
  "Announcement System|Enable club admins to publish announcements and news to club members"
  
  "Event Calendar & Scheduling|Integrate a calendar system for clubs to schedule and manage events"
  
  "File Upload Support|Add ability to upload and store profile images and club logos with size limits"
  
  "Club Management|Expand to full club creation, editing, and metadata management beyond just activities"
  
  "API Documentation|Generate automatic API documentation using Swagger/OpenAPI standards"
  
  "Enhanced Error Handling|Implement comprehensive error handling with custom exceptions and validation"
  
  "Modern Frontend Framework|Migrate from vanilla JavaScript to React with Redux for state management"
  
  "Advanced Styling|Upgrade CSS to use Tailwind CSS framework with icon libraries"
)

for issue in "${issues[@]}"; do
  IFS='|' read -r title body <<< "$issue"
  echo "Creating issue: $title"
  gh issue create --repo "$REPO" --title "$title" --body "$body"
done
