const BASE_URLS = {
  student: "http://localhost:5001",
  course: "http://localhost:5002",
  enrollment: "http://localhost:5003"
};

// 1. Add a new student
async function createStudent(studentData) {
  const response = await fetch(`${BASE_URLS.student}/student`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(studentData)
  });
  return response.json();
}

// 2. Get a student by ID
async function getStudent(studentId) {
  const response = await fetch(`${BASE_URLS.student}/student/${studentId}`);
  return response.json();
}

// 3. Get all students
async function getAllStudents() {
  const response = await fetch(`${BASE_URLS.student}/students`);
  return response.json();
}

// 4. Add a new course
async function createCourse(courseData) {
  const response = await fetch(`${BASE_URLS.course}/courses`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(courseData)
  });
  return response.json();
}

// 5. Get a course by ID
async function getCourse(courseId) {
  const response = await fetch(`${BASE_URLS.course}/course/${courseId}`);
  return response.json();
}

// 6. Get all courses
async function getAllCourses() {
  const response = await fetch(`${BASE_URLS.course}/courses`);
  return response.json();
}

// 7. Enroll a student in a course
async function enrollStudent(courseId, studentId) {
  const response = await fetch(`${BASE_URLS.enrollment}/enroll/${courseId}/${studentId}`, {
    method: "POST"
  });
  return response.json();
}

// 8. Get all enrollments
async function getAllEnrollments() {
  const response = await fetch(`${BASE_URLS.enrollment}/enrollments`);
  return response.json();
}

// Example usage
async function test() {
  const newStudent = {
    name: "John Doe",
    age: 20,
    major: "Computer Science",
    student_id: "CS102"
  };

  const newCourse = {
    course_id: "CSE101",
    name: "Introduction to Computer Science",
    credits: 4
  };

  const studentRes = await createStudent(newStudent);
  console.log("Student Created:", studentRes);

  const courseRes = await createCourse(newCourse);
  console.log("Course Created:", courseRes);

  // enroll student (replace with actual ids if needed)
  const enrollRes = await enrollStudent(newCourse.course_id, newStudent.student_id);
  console.log("Enrollment:", enrollRes);

  const enrollments = await getAllEnrollments();
  console.log("All Enrollments:", enrollments);
}

test();
