import sqlite3


class Student:
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self.age = age

    def update_info(self, name=None, age=None):
        if name is not None:
            self.name = name
        if age is not None:
            self.age = age

    def __str__(self):
        return f"学生ID: {self.student_id}, 姓名: {self.name}, 年龄: {self.age}"


class Course:
    def __init__(self, course_id, name):
        self.course_id = course_id
        self.name = name

    def __str__(self):
        return f"课程ID: {self.course_id}, 课程名称: {self.name}"


class Grade:
    def __init__(self, student_id, course_id, score):
        self.student_id = student_id
        self.course_id = course_id
        self.score = score

    def __str__(self):
        return f"学生ID: {self.student_id}, 课程ID: {self.course_id}, 成绩: {self.score}"


class Manager:
    def __init__(self):
        self.connection = sqlite3.connect('school.db')
        self.cursor = self.connection.cursor()
        self.create_tables()
        self.load_data()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            student_id TEXT,
            course_id TEXT,
            score REAL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
        ''')
        self.connection.commit()

    def load_data(self):
        self.cursor.execute('SELECT COUNT(*) FROM students')
        if self.cursor.fetchone()[0] == 0:
            with open('Students.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    student_id, name, age = line.strip().split(',')
                    self.add_student(Student(student_id, name, int(age)))

        self.cursor.execute('SELECT COUNT(*) FROM courses')
        if self.cursor.fetchone()[0] == 0:
            courses = ['数学', '英语', '计算机']
            for course_name in courses:
                self.add_course(Course(course_name, course_name))

        self.cursor.execute('SELECT COUNT(*) FROM grades')
        if self.cursor.fetchone()[0] == 0:
            with open('Grades.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    student_id, course_name, score = line.strip().split(',')
                    self.add_grade(Grade(student_id, course_name, float(score)))

    def load_user_data(self):
        global users
        users = {}
        with open('User.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    username, password = parts
                    users[username] = password
                else:
                    print(f"警告：格式错误的行 - {line.strip()}")
        return users

    def add_user(self, new_name, new_password):
        user_info = f"{new_name},{new_password}\n"
        with open("user.txt", "a", encoding="utf-8") as f:
            f.write(user_info)

    def add_student(self, student):
        self.cursor.execute('SELECT * FROM students WHERE student_id = ?', (student.student_id,))
        existing_student = self.cursor.fetchone()
        if existing_student:
            return False, f"该学生ID {student.student_id} 已经存在，请重新输入。"
        self.cursor.execute('''
        INSERT INTO students (student_id, name, age)
        VALUES (?, ?, ?)
        ''', (student.student_id, student.name, student.age))
        self.connection.commit()
        return True, f"学生 {student.name} 已添加！"

    def add_course(self, course):
        self.cursor.execute('SELECT * FROM courses WHERE course_id = ?', (course.course_id,))
        existing_course = self.cursor.fetchone()
        if existing_course:
            return False, f"该课程ID {course.course_id} 已经存在，请重新输入。"
        self.cursor.execute('''
        INSERT INTO courses (course_id, name)
        VALUES (?, ?)
        ''', (course.course_id, course.name))
        self.connection.commit()
        return True, f"课程 {course.name} 已添加！"

    def add_grade(self, grade):
        # 检查成绩是否在合理范围内
        if not (0 < grade.score < 100):
            return False, f"成绩必须大于0且小于100，当前成绩为 {grade.score}"

        self.cursor.execute('''
        SELECT * FROM grades WHERE student_id = ? AND course_id = ?
        ''', (grade.student_id, grade.course_id))
        existing_grade = self.cursor.fetchone()

        # 如果已存在成绩记录，提示用户
        if existing_grade:
            return False, f"该学生的这门课程成绩为{existing_grade[2]}，无需添加！"

        self.cursor.execute('''
        INSERT INTO grades (student_id, course_id, score)
        VALUES (?, ?, ?)
        ''', (grade.student_id, grade.course_id, grade.score))

        # 提交更改
        self.connection.commit()
        return True, f"学生{grade.student_id}的{grade.course_id}成绩已成功添加！"

    def show_students(self):
        self.cursor.execute('SELECT * FROM students')
        return self.cursor.fetchall()

    def show_courses(self):
        self.cursor.execute('SELECT * FROM courses')
        return self.cursor.fetchall()

    def show_grades(self):
        self.cursor.execute('SELECT * FROM grades')
        return self.cursor.fetchall()

    def search_student(self, search_message):
        if search_message.isdigit():
            self.cursor.execute('SELECT * FROM students WHERE student_id = ?', (search_message,))
        else:
            self.cursor.execute('SELECT * FROM students WHERE name LIKE ?', ('%' + search_message + '%',))
        return self.cursor.fetchall()

    def sort_students_by_computer_score(self):
        self.cursor.execute('''
        SELECT s.student_id, s.name, g.score 
        FROM students s 
        JOIN grades g ON s.student_id = g.student_id 
        WHERE g.course_id = (SELECT course_id FROM courses WHERE name = "计算机") 
        ORDER BY g.score DESC
        ''')
        return self.cursor.fetchall()

    def sort_students_by_average_score(self):
        self.cursor.execute('''
        SELECT s.student_id, s.name, AVG(g.score) 
        FROM students s 
        JOIN grades g ON s.student_id = g.student_id 
        GROUP BY s.student_id 
        ORDER BY AVG(g.score) DESC
        ''')
        return self.cursor.fetchall()

    # 展示学生的所有信息包括学生的姓名，学号，年龄，各个科目的成绩信息
    def show_all_message(self):
        self.cursor.execute('''
        SELECT s.student_id, s.name, s.age, c.name AS course_name, g.score
        FROM students s
        LEFT JOIN grades g ON s.student_id = g.student_id
        LEFT JOIN courses c ON g.course_id = c.course_id
        ORDER BY s.student_id, c.name
        ''')
        results = self.cursor.fetchall()
        students = {}
        for row in results:
            student_id, name, age, course_name, score = row
            if student_id not in students:
                students[student_id] = {
                    "student_id": student_id,
                    "name": name,
                    "age": age,
                    "courses": {},
                    "average_score": 0.0
                }
            if course_name:
                students[student_id]["courses"][course_name] = score

        for student_id, info in students.items():
            scores = list(info["courses"].values())
            if scores:
                info["average_score"] = sum(scores) / len(scores)
            else:
                info["average_score"] = 0.0

        return students

    # 删除学生信息的函数，允许根据姓名或学号删除特定的学生
    def delete_students(self, identifier):
        if identifier.isdigit():  # 如果是学号
            self.cursor.execute('SELECT * FROM students WHERE student_id = ?', (identifier,))
        else:  # 如果是姓名
            self.cursor.execute('SELECT * FROM students WHERE name = ?', (identifier,))

        student = self.cursor.fetchone()
        if not student:
            return False, f"未找到学生 {identifier}"

        student_id = student[0]  # 获取学生ID
        self.cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        self.cursor.execute('DELETE FROM grades WHERE student_id = ?', (student_id,))
        self.connection.commit()
        return True, f"学生 {identifier} 已删除"

    # 修改学生信息的功能函数，用户输入学生姓名或学号，允许对已存储的学生的信息进行修改
    def change_students(self, student_id, name=None, age=None):
        self.cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
        student = self.cursor.fetchone()
        if not student:
            return False, f"未找到学生ID为 {student_id} 的学生"

        # 更新学生信息
        if name is not None and name.strip():  # 检查姓名是否为空
            self.cursor.execute('UPDATE students SET name = ? WHERE student_id = ?', (name, student_id))
        if age is not None and age.strip():  # 检查年龄是否为空
            self.cursor.execute('UPDATE students SET age = ? WHERE student_id = ?', (age, student_id))

        # 更新成绩信息

        self.connection.commit()
        return True, f"学生ID为 {student_id} 的信息已更新"

    def change_grades(self, student_id, course_id, new_score):
        # 检查学生是否存在
        self.cursor.execute('''
        SELECT * FROM students WHERE student_id = ?
        ''', (student_id,))
        student = self.cursor.fetchone()
        if not student:
            return False, f"未找到学生ID为 {student_id} 的学生"

        # 检查成绩是否存在
        self.cursor.execute('''
        SELECT * FROM grades WHERE student_id = ? AND course_id = ?
        ''', (student_id, course_id))
        existing_grade = self.cursor.fetchone()
        if not existing_grade:
            return False, f"未找到学生ID为 {student_id} 的 {course_id} 成绩"

        # 更新成绩
        self.cursor.execute('''
        UPDATE grades SET score = ? WHERE student_id = ? AND course_id = ?
        ''', (new_score, student_id, course_id))
        self.connection.commit()
        return True, f"学生ID为 {student_id} 的 {course_id} 成绩已更新为 {new_score}"

    def analyze_class_performance(self):
        self.cursor.execute('SELECT * FROM courses')
        courses = self.cursor.fetchall()
        results = []
        for course in courses:
            self.cursor.execute('''
            SELECT g.score FROM grades g WHERE g.course_id = ?
            ''', (course[0],))
            scores = [row[0] for row in self.cursor.fetchall()]
            if scores:
                avg_score = sum(scores) / len(scores)
                max_score = max(scores)
                min_score = min(scores)
                pass_rate = sum(1 for score in scores if score >= 60) / len(scores) * 100
                excellent_rate = sum(1 for score in scores if score >= 90) / len(scores) * 100
                results.append((course[1], avg_score, max_score, min_score, pass_rate, excellent_rate))
        return results

    def out_of_system(self):
        print("正在退出系统...")
        self.connection.close()
