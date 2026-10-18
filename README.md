# Student Management REST API

## Aim
To develop a REST API using Python Flask and SQLite.

## Features
- Add a student
- View all students
- View a student by ID
- Update student details
- Delete a student
- JSON validation and error handling
- SQLite database storage

## Technologies
- Python
- Flask
- SQLite
- REST API

## Installation
pip install -r requirements.txt

## Run
python app.py

## API Endpoints

| Method | Endpoint | Purpose |
| POST | /students | Add student |
| GET | /students | List students |
| GET | /students/1 | Get student |
| PUT | /students/1 | Update student |
| DELETE | /students/1 | Delete student |