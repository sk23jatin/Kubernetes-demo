from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests

app = Flask(__name__)

# student_service_url  = "http://localhost:5001"
# course_service_url  = "http://localhost:5002"
# enroll_service_url = "http://localhost:5003"

student_service_url  = "http://student-service.services.svc.cluster.local:5001"
course_service_url  = "http://course-service.services.svc.cluster.local:5002"
enroll_service_url = "http://enroll-service.services.svc.cluster.local:5003"


# client = MongoClient("mongodb://localhost:27017")


client = MongoClient("mongodb://appuser:secretpw@demo-mongo-mongodb-0.demo-mongo-mongodb-headless.demo-mongo.svc.cluster.local:27017/appdb?replicaSet=rs0")

db = client.appdb
@app.route("/clear-databases", methods=["DELETE"])
def clear_databases():
    try:
        db.courses.delete_many({})
        db.enrollments.delete_many({})
        db.students.delete_many({})
        return jsonify({"message": "All databases cleared successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        # Example cURL command to clear all databases:
        # curl -X DELETE http://localhost:5004/clear-databases


# enroll api's
@app.route("/enroll/<course_id>/<student_id>", methods=["POST"])
def enroll_student(course_id, student_id):
    if not course_id or not student_id:
        return jsonify({"error": "course_id and student_id are required"}), 400

    # Check if the student exists by calling the student service
    student_response = requests.get(f"{student_service_url}/student/{student_id}")
    if student_response.status_code != 200:
        return jsonify({"error": "Student not found"}), 404

    # Check if the course exists by calling the course service
    course_response = requests.get(f"{course_service_url}/course/{course_id}")
    if course_response.status_code != 200:
        return jsonify({"error": "Course not found"}), 404

    # Enroll the student in the course using the enroll service
    enrollment_response = requests.post(f"{enroll_service_url}/enroll/{course_id}/{student_id}")
    if enrollment_response.status_code != 201:
        return jsonify({"error": "Failed to enroll student"}), enrollment_response.status_code

    return jsonify(enrollment_response.json()), 201

@app.route("/enrollments", methods=["GET"])
def get_all_enrollments():
    response = requests.get(f"{enroll_service_url}/enrollments")
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch enrollments"}), response.status_code
    enrollments = response.json()
    combined_data = []

    for enrollment in enrollments:
        course_id = enrollment.get("course_id")
        student_id = enrollment.get("student_id")

        # Fetch course data
        course_data = requests.get(f"{course_service_url}/course/{course_id}").json()

        # Fetch student data
        student_data = requests.get(f"{student_service_url}/student/{student_id}").json()

        # Combine data
        combined_data.append({
            "enrollment_id": enrollment.get("_id"),
            "course": course_data,
            "student": student_data
        })

    return jsonify(combined_data), 200


@app.route("/enrollments/course/<course_id>", methods=["GET"])
def get_students_by_course(course_id):
    if not course_id:
        return jsonify({"error": "course_id is required"}), 400

    response = requests.get(f"{enroll_service_url}/enrollments/course/{course_id}")
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch enrollments"}), response.status_code

    course_data = requests.get(f"{course_service_url}/course/{course_id}").json()
    student_ids = response.json().get("student_ids", [])
    students_data = [requests.get(f"{student_service_url}/student/{student_id}").json() for student_id in student_ids]

    combined_data = {
        "course": course_data,
        "students": students_data
    }
    return jsonify(combined_data), 200


@app.route("/enrollments/student/<student_id>", methods=["GET"])
def get_courses_by_student(student_id):
    if not student_id:
        return jsonify({"error": "student_id is required"}), 400

    response = requests.get(f"{enroll_service_url}/enrollments/student/{student_id}")
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch enrollments"}), response.status_code

    enrollment_data = response.json()
    course_ids = enrollment_data.get("course_ids", [])
    student_id = enrollment_data.get("student_id")

    # Fetch student data
    student_data = requests.get(f"{student_service_url}/student/{student_id}").json()

    # Fetch course data for each course_id
    courses_data = [requests.get(f"{course_service_url}/course/{course_id}").json() for course_id in course_ids]

    combined_data = {
        "student": student_data,
        "courses": courses_data
    }

    return jsonify(combined_data), 200


# course api's


@app.route("/courses", methods=["POST"])
def create_course():
    data = request.json
    response = requests.post(f"{course_service_url}/courses", json=data)
    if response.status_code != 201:
        return jsonify({"error": "Failed to create course"}), response.status_code
    return jsonify(response.json()), 201

@app.route("/course/<course_id>", methods=["GET"])
def get_course(course_id):
    response = requests.get(f"{course_service_url}/course/{course_id}")
    if response.status_code != 200:
        return jsonify({"error": "Course not found"}), response.status_code
    return jsonify(response.json()), 200

@app.route("/courses", methods=["GET"])
def get_all_courses():
    response = requests.get(f"{course_service_url}/courses")
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch courses"}), response.status_code
    return jsonify(response.json()), 200

    # Example cURL commands for the Course APIs:

    # cURL command to create a course
    # Replace <course_data> with actual JSON data for the course
    # curl -X POST -H "Content-Type: application/json" -d '{"course_id": "MAT101", "name": "Introduction to Mathematics", "credits": 4}' http://localhost:5004/courses
    # curl -X POST -H "Content-Type: application/json" -d '{"course_id": "PHY101", "name": "Physics Fundamentals", "credits": 3}' http://localhost:5004/courses
    # curl -X POST -H "Content-Type: application/json" -d '{"course_id": "CHE101", "name": "Basic Chemistry", "credits": 4}' http://localhost:5004/courses

    # cURL command to get a course by ID
    # Replace <course_id> with an actual value
    # curl -X GET http://localhost:5004/course/<course_id>

    # cURL command to get all courses
    # curl -X GET http://localhost:5004/courses


#student api's

@app.route("/student", methods=["POST"])
def create_student():
    data = request.json
    response = requests.post(f"{student_service_url}/student", json=data)
    if response.status_code != 201:
        return jsonify({"error": "Failed to create student"}), response.status_code
    return jsonify(response.json()), 201

@app.route("/student/<student_id>", methods=["GET"])
def get_student(student_id):
    response = requests.get(f"{student_service_url}/student/{student_id}")
    if response.status_code != 200:
        return jsonify({"error": "Student not found"}), response.status_code
    return jsonify(response.json()), 200


@app.route("/students", methods=["GET"])
def get_all_students():
    response = requests.get(f"{student_service_url}/students")
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch students"}), response.status_code
    return jsonify(response.json()), 200



# Example cURL command to create a student:
# curl -X POST -H "Content-Type: application/json" -d '{"student_id": "S101", "name": "John Doe", "age": 20, "major": "Computer Science"}' http://localhost:5004/student
# curl -X POST -H "Content-Type: application/json" -d '{"student_id": "S102", "name": "Jane Smith", "age": 22, "major": "Mathematics"}' http://localhost:5004/student
# curl -X POST -H "Content-Type: application/json" -d '{"student_id": "S103", "name": "Alice Johnson", "age": 19, "major": "Physics"}' http://localhost:5004/student
# curl -X POST -H "Content-Type: application/json" -d '{"student_id": "S104", "name": "Bob Brown", "age": 21, "major": "Chemistry"}' http://localhost:5004/student

# Example cURL command to get a student by ID:
# curl -X GET http://localhost:5004/student/<student_id>

# Example cURL command to get all students:
# curl -X GET http://localhost:5004/students


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004)

    # Example cURL commands for the APIs:

    # cURL command to enroll a student in a course
    # Replace <course_id> and <student_id> with actual values
    # curl -X POST http://localhost:5004/enroll/<course_id>/<student_id>

    # cURL command to get all enrollments
    # curl -X GET http://localhost:5004/enrollments

    # cURL command to get students by course
    # Replace <course_id> with an actual value
    # curl -X GET http://localhost:5004/enrollments/course/<course_id>

    # cURL command to get courses by student
    # Replace <student_id> with an actual value
    # curl -X GET http://localhost:5004/enrollments/student/<student_id>