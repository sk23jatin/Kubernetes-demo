from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
# client = MongoClient("mongodb://localhost:27017")


client = MongoClient("mongodb://appuser:secretpw@demo-mongo-mongodb-0.demo-mongo-mongodb-headless.demo-mongo.svc.cluster.local:27017/appdb?replicaSet=rs0")

db = client.appdb
students = db.students

@app.route("/student", methods=["POST"])
def create_student():
    data = request.json
    result = students.insert_one(data)
    return jsonify({"message": "Student created", "id": str(result.inserted_id)}), 201

@app.route("/student/<student_id>", methods=["GET"])
def get_student(student_id):
    student = students.find_one({"student_id": student_id})
    if not student:
        return jsonify({"error": "Student not found"}), 404
    student["_id"] = str(student["_id"])
    return jsonify(student)

@app.route("/students", methods=["GET"])
def get_all_students():
    all_students = students.find()
    result = []
    for student in all_students:
        student["_id"] = str(student["_id"])
        result.append(student)
    return jsonify(result)


if __name__ == "__main__":

    app.run(port=5001)
    # Example curl commands for the APIs:

    # To create a student:
    # curl -X POST -H "Content-Type: application/json" -d '{"name": "John Doe", "age": 20, "major": "Computer Science", "student_id": "CS102"}' http://localhost:5001/student

    # To get a student by student_id:
    # curl http://localhost:5001/student/<student_id>

    # To get all students:
    # curl http://localhost:5001/students



#
# helm install demo-mongo bitnami/mongodb  --namespace demo-mongo  --set architecture=replicaset  --set auth.rootPassword=changeme  --set auth.username=appuser  --set auth.password=secretpw  --set auth.database=appdb
#
# NAME: demo-mongo
# LAST DEPLOYED: Sat May  3 19:17:25 2025
# NAMESPACE: demo-mongo
# STATUS: deployed
# REVISION: 1
# TEST SUITE: None
# NOTES:
# CHART NAME: mongodb
# CHART VERSION: 16.5.5
# APP VERSION: 8.0.9
#
# Did you know there are enterprise versions of the Bitnami catalog? For enhanced secure software supply chain features, unlimited pulls from Docker, LTS support, or application customization, see Bitnami Premium or Tanzu Application Catalog. See https://www.arrow.com/globalecs/na/vendors/bitnami for more information.
#
# ** Please be patient while the chart is being deployed **
#
# MongoDB&reg; can be accessed on the following DNS name(s) and ports from within your cluster:
#
#     demo-mongo-mongodb-0.demo-mongo-mongodb-headless.demo-mongo.svc.cluster.local:27017
#     demo-mongo-mongodb-1.demo-mongo-mongodb-headless.demo-mongo.svc.cluster.local:27017
#
# To get the root password run:
#
#     export MONGODB_ROOT_PASSWORD=$(kubectl get secret --namespace demo-mongo demo-mongo-mongodb -o jsonpath="{.data.mongodb-root-password}" | base64 -d)
#
# To get the password for "appuser" run:
#
#     export MONGODB_PASSWORD=$(kubectl get secret --namespace demo-mongo demo-mongo-mongodb -o jsonpath="{.data.mongodb-passwords}" | base64 -d | awk -F',' '{print $1}')
#
# To connect to your database, create a MongoDB&reg; client container:
#
#     kubectl run --namespace demo-mongo demo-mongo-mongodb-client --rm --tty -i --restart='Never' --env="MONGODB_ROOT_PASSWORD=$MONGODB_ROOT_PASSWORD" --image docker.io/bitnami/mongodb:8.0.9-debian-12-r0 --command -- bash
#
# Then, run the following command:
#     mongosh admin --host "demo-mongo-mongodb-0.demo-mongo-mongodb-headless.demo-mongo.svc.cluster.local:27017,demo-mongo-mongodb-1.demo-mongo-mongodb-headless.demo-mongo.svc.cluster.local:27017" --authenticationDatabase admin -u $MONGODB_ROOT_USER -p $MONGODB_ROOT_PASSWORD
#
# WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
#   - arbiter.resources
#   - resources
# +info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/




# mongodb://appuser:secretpw@demo-mongo-mongodb.demo-mongo.svc.cluster.local:27017/appdb?replicaSet=rs0
# appuser lives in the database you named in the Helm install (auth.database=appdb).
# When a connection string doesn’t say otherwise, the Mongo driver tries to
# authenticate against the admin database.
# Because appuser isn’t defined there, MongoDB returns code 18 AuthenticationFailed.
# /appdb or ?authSource=appdb – tells Mongo where appuser exists.
#
# replicaSet=rs0 – lets the driver discover the current primary (Bitnami names the set rs0).
#
# Use the cluster-IP service (demo-mongo-mongodb) or the headless service (demo-mongo-mongodb-headless), not the individual pod hostname, so you survive pod rescheduling.



