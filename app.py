from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "students.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                course TEXT NOT NULL
            )
        """)


@app.route("/")
def home():
    return jsonify({
        "message": "Student Management API is running"
    })


# CREATE - Add student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON body required"}), 400

    name = data.get("name")
    age = data.get("age")
    course = data.get("course")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Valid name required"}), 400

    if type(age) is not int or age < 1 or age > 120:
        return jsonify({"error": "Age must be 1 to 120"}), 400

    if not isinstance(course, str) or not course.strip():
        return jsonify({"error": "Valid course required"}), 400

    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
            (name.strip(), age, course.strip())
        )
        student_id = cursor.lastrowid

    return jsonify({
        "message": "Student added successfully",
        "id": student_id
    }), 201


# READ - Get all students
@app.route("/students", methods=["GET"])
def get_students():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM students"
        ).fetchall()

    return jsonify([dict(row) for row in rows])


# READ - Get one student
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        ).fetchone()

    if row is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(row))


# UPDATE - Update student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON body required"}), 400

    name = data.get("name")
    age = data.get("age")
    course = data.get("course")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Valid name required"}), 400

    if type(age) is not int or age < 1 or age > 120:
        return jsonify({"error": "Age must be 1 to 120"}), 400

    if not isinstance(course, str) or not course.strip():
        return jsonify({"error": "Valid course required"}), 400

    with get_db() as conn:
        cursor = conn.execute(
            """UPDATE students
               SET name = ?, age = ?, course = ?
               WHERE id = ?""",
            (name.strip(), age, course.strip(), student_id)
        )

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student updated successfully"})


# DELETE - Delete student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    with get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)