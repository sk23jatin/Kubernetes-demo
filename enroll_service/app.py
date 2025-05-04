from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests

app = Flask(__name__)
# client = MongoClient("mongodb://localhost:27017")

client = MongoClient("mongodb://appuser:secretpw@demo-mongo-mongodb-0.demo-mongo-mongodb-headless.demo-mongo.svc.cluster.local:27017/appdb?replicaSet=rs0")

db = client.appdb
enrollments = db.enrollments

@app.route("/enroll/<course_id>/<student_id>", methods=["POST"])
def enroll_student(course_id, student_id):
    if not course_id or not student_id:
        return jsonify({"error": "course_id and student_id are required"}), 400

    # Enroll the student in the course
    enrollment_data = {"course_id": course_id, "student_id": student_id}
    result = enrollments.insert_one(enrollment_data)
    return jsonify({"message": "Student enrolled successfully", "id": str(result.inserted_id)}), 201

@app.route("/enrollments", methods=["GET"])
def get_all_enrollments():
    all_enrollments = enrollments.find()
    result = []
    for enrollment in all_enrollments:
        enrollment["_id"] = str(enrollment["_id"])
        result.append(enrollment)
    return jsonify(result)


@app.route("/enrollments/course/<course_id>", methods=["GET"])
def get_students_by_course(course_id):
    if not course_id:
        return jsonify({"error": "course_id is required"}), 400

    students = enrollments.find({"course_id": course_id})
    student_ids = [enrollment["student_id"] for enrollment in students]
    return jsonify({"course_id": course_id, "student_ids": student_ids}), 200


@app.route("/enrollments/student/<student_id>", methods=["GET"])
def get_courses_by_student(student_id):
    if not student_id:
        return jsonify({"error": "student_id is required"}), 400

    courses = enrollments.find({"student_id": student_id})
    course_ids = [enrollment["course_id"] for enrollment in courses]
    return jsonify({"student_id": student_id, "course_ids": course_ids}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)

    # Example cURL commands for the APIs:

    # cURL command to enroll a student in a course
    # Replace <course_id> and <student_id> with actual values
    # curl -X POST http://localhost:5003/enroll/<course_id>/<student_id>

    # cURL command to get all enrollments
    # curl -X GET http://localhost:5003/enrollments

    # cURL command to get students by course
    # Replace <course_id> with an actual value
    # curl -X GET http://localhost:5003/enrollments/course/<course_id>

    # cURL command to get courses by student
    # Replace <student_id> with an actual value
    # curl -X GET http://localhost:5003/enrollments/student/<student_id>