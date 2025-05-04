from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests

app = Flask(__name__)
# client = MongoClient("mongodb://localhost:27017")


# student_service_url  = "http://localhost:5001"
# course_service_url  = "http://localhost:5002"

student_service_url  = "http://student-service.services.svc.cluster.local:5001"
course_service_url  = "http://course-service.services.svc.cluster.local:5002"

client = MongoClient("mongodb://appuser:secretpw@demo-mongo-mongodb-0.demo-mongo-mongodb-headless.demo-mongo.svc.cluster.local:27017/appdb?replicaSet=rs0")

db = client.appdb
enrollments = db.enrollments

@app.route("/enroll/<course_id>/<student_id>", methods=["POST"])
def enroll_student(course_id, student_id):
    if not course_id or not student_id:
        return jsonify({"error": "course_id and student_id are required"}), 400

    # Check if the student exists
    student_response = requests.get(f"{student_service_url}/student/{student_id}")
    if student_response.status_code != 200:
        return jsonify({"error": "Student not found"}), 404

    # Check if the course exists
    course_response = requests.get(f"{course_service_url}/course/{course_id}")
    if course_response.status_code != 200:
        return jsonify({"error": "Course not found"}), 404

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

if __name__ == "__main__":
    app.run(port=5003)

    # Example cURL commands for the APIs:

    # cURL command to enroll a student in a course
    # Replace <course_id> and <student_id> with actual values
    # curl -X POST http://localhost:5003/enroll/<course_id>/<student_id>

    # cURL command to get all enrollments
    # curl -X GET http://localhost:5003/enrollments