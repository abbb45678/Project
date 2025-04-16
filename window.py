import tkinter as tk
from tkinter import messagebox
from Main import Manager, Student, Course, Grade


def verify_credentials(username, password, users):
    return users.get(username) == password


def login():
    users=manager.load_user_data()
    username = entry_username.get()
    password = entry_password.get()
    if verify_credentials(username, password, users):
        messagebox.showinfo("登录成功", "欢迎进入系统！")
        login_frame.pack_forget()
        main_menu_frame.pack(pady=30)
    else:
        messagebox.showerror("登录失败", "用户名或密码错误！")


def create_menu_button(text, command):
    return tk.Button(main_menu_frame, text=text, command=command, font=("Arial", 12), bg="#2196F3", fg="white",
                     width=20)


def add_user_window():
    add_user_window = tk.Toplevel(root)
    add_user_window.title("注册用户")
    add_user_window.geometry("500x300")
    add_user_window.resizable(False, False)
    add_user_window.config(bg="#f5f5f5")

    title_label = tk.Label(add_user_window, text="注册新用户", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.grid(row=0, columnspan=4, pady=25)

    def create_entry(label_text, row):
        label = tk.Label(add_user_window, text=label_text, font=("Arial", 12), bg="#f5f5f5")
        label.grid(row=row, column=0, pady=10, padx=20, sticky="e")
        entry = tk.Entry(add_user_window, font=("Arial", 12), width=25)
        entry.grid(row=row, column=1, pady=10, padx=20)
        return entry

    entry_username = create_entry("用户名:", 1)
    entry_password = create_entry("密码:", 2)
    entry_password.config(show="*")

    def save_user():
        new_username = entry_username.get()
        new_password = entry_password.get()

        if new_username and new_password:
            try:
                manager.add_user(new_username, new_password)
                messagebox.showinfo("成功", "用户注册成功！", parent=add_user_window)
                add_user_window.destroy()

            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{e}", parent=add_user_window)
        else:
            messagebox.showerror("错误", "用户名和密码不能为空！", parent=add_user_window)

    button_save = tk.Button(add_user_window, text="保存", command=save_user, font=("Arial", 12),
                            bg="#4CAF50", fg="white", width=15, relief="raised", bd=2)
    button_save.grid(row=4, column=1, pady=10, padx=20, sticky="e")

    button_return = tk.Button(add_user_window, text="返回登录", command=add_user_window.destroy, font=("Arial", 12),
                              bg="#2196F3", fg="white", width=15, relief="raised", bd=2)
    button_return.grid(row=5, column=1, pady=10, padx=20, sticky="e")


def add_student_window():
    add_student_window = tk.Toplevel(root)
    add_student_window.title("添加学生的基本信息")
    add_student_window.geometry("500x350")
    add_student_window.resizable(False, False)  # 禁止调整窗口大小
    add_student_window.config(bg="#f5f5f5")

    title_label = tk.Label(add_student_window, text="添加学生的基本信息", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.grid(row=0, columnspan=2, pady=20)

    label_id = tk.Label(add_student_window, text="ID:", font=("Arial", 12), bg="#f5f5f5")
    label_id.grid(row=1, column=0, pady=10, padx=20, sticky="e")
    entry_id = tk.Entry(add_student_window, font=("Arial", 12), width=25)
    entry_id.grid(row=1, column=1, pady=10, padx=20)

    label_name = tk.Label(add_student_window, text="姓名:", font=("Arial", 12), bg="#f5f5f5")
    label_name.grid(row=2, column=0, pady=10, padx=20, sticky="e")
    entry_name = tk.Entry(add_student_window, font=("Arial", 12), width=25)
    entry_name.grid(row=2, column=1, pady=10, padx=20)

    label_age = tk.Label(add_student_window, text="年龄:", font=("Arial", 12), bg="#f5f5f5")
    label_age.grid(row=3, column=0, pady=10, padx=20, sticky="e")
    entry_age = tk.Entry(add_student_window, font=("Arial", 12), width=25)
    entry_age.grid(row=3, column=1, pady=10, padx=20)

    def save_student():
        student_id = entry_id.get()
        name = entry_name.get()
        age = entry_age.get()
        if student_id and name and age:
            try:
                age = int(age)  # 确保年龄是整数
                success, message = manager.add_student(Student(student_id, name, age))
                if success:
                    # 弹出提示窗口，父窗口为当前的 add_student_window
                    messagebox.showinfo("成功", message, parent=add_student_window)
                else:
                    messagebox.showerror("错误", message, parent=add_student_window)
            except ValueError:
                messagebox.showerror("错误", "请输入有效的年龄！", parent=add_student_window)
        else:
            messagebox.showerror("错误", "请输入所有信息！", parent=add_student_window)

    def return_to_main_menu():
        add_student_window.destroy()

    button_save = tk.Button(add_student_window, text="保存", command=save_student, font=("Arial", 12),
                            bg="#4CAF50", fg="white", width=15, relief="raised", bd=2)
    button_save.grid(row=4, column=1, pady=10, padx=20, sticky="e")

    button_return = tk.Button(add_student_window, text="返回主菜单", command=return_to_main_menu, font=("Arial", 12),
                              bg="#2196F3", fg="white", width=15, relief="raised", bd=2)
    button_return.grid(row=5, column=1, pady=10, padx=20, sticky="e")


def change_grade_window():
    change_grades_window = tk.Toplevel(root)
    change_grades_window.title("修改学生成绩")
    change_grades_window.geometry("500x350")
    change_grades_window.resizable(False, False)  # 禁止调整窗口大小
    change_grades_window.config(bg="#f5f5f5")

    title_label = tk.Label(change_grades_window, text="修改学生成绩", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.grid(row=0, columnspan=2, pady=20)

    label_student_id_or_name = tk.Label(change_grades_window, text="学生ID或姓名:", font=("Arial", 12), bg="#f5f5f5")
    label_student_id_or_name.grid(row=1, column=0, pady=10, padx=20, sticky="e")
    entry_student_id_or_name = tk.Entry(change_grades_window, font=("Arial", 12), width=25)
    entry_student_id_or_name.grid(row=1, column=1, pady=10, padx=20)

    label_course_id = tk.Label(change_grades_window, text="选择科目ID:", font=("Arial", 12), bg="#f5f5f5")
    label_course_id.grid(row=2, column=0, pady=10, padx=20, sticky="e")
    entry_course_id = tk.Entry(change_grades_window, font=("Arial", 12), width=25)
    entry_course_id.grid(row=2, column=1, pady=10, padx=20)

    label_new_score = tk.Label(change_grades_window, text="新成绩:", font=("Arial", 12), bg="#f5f5f5")
    label_new_score.grid(row=3, column=0, pady=10, padx=20, sticky="e")
    entry_new_score = tk.Entry(change_grades_window, font=("Arial", 12), width=25)
    entry_new_score.grid(row=3, column=1, pady=10, padx=20)

    def update_grade():
        student_id_or_name = entry_student_id_or_name.get()
        course_id = entry_course_id.get()
        new_score = entry_new_score.get()

        if not student_id_or_name or not course_id or not new_score:
            messagebox.showerror("错误", "请输入所有信息！", parent=change_grades_window)
            return

        try:
            new_score = float(new_score)
            if not (0 < new_score < 100):
                messagebox.showerror("错误", "成绩必须大于0且小于100！", parent=change_grades_window)
                return

            # 如果输入的是学生姓名，先查询对应的学生ID
            if not student_id_or_name.isdigit():
                manager.cursor.execute('''
                SELECT student_id FROM students WHERE name = ?
                ''', (student_id_or_name,))
                student = manager.cursor.fetchone()
                if not student:
                    messagebox.showerror("错误", f"未找到学生 {student_id_or_name}", parent=change_grades_window)
                    return
                student_id_or_name = student[0]

            # 调用 Manager 的 change_grades 方法
            success, message = manager.change_grades(student_id_or_name, course_id, new_score)
            if success:
                messagebox.showinfo("成功", message, parent=change_grades_window)
            else:
                messagebox.showerror("错误", message, parent=change_grades_window)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的成绩！", parent=change_grades_window)

    button_update = tk.Button(change_grades_window, text="更新成绩", command=update_grade, font=("Arial", 12),
                              bg="#4CAF50", fg="white", width=15, relief="raised", bd=2)
    button_update.grid(row=4, columnspan=2, pady=10)

    def return_to_main_menu():
        change_grades_window.destroy()

    button_return = tk.Button(change_grades_window, text="返回主菜单", command=return_to_main_menu, font=("Arial", 12),
                              bg="#2196F3", fg="white", width=15, relief="raised", bd=2)
    button_return.grid(row=5, columnspan=2, pady=10)


def add_grade_window():
    add_score_window = tk.Toplevel(root)
    add_score_window.title("添加学生的成绩")
    add_score_window.geometry("500x350")
    add_score_window.resizable(False, False)  # 禁止调整窗口大小
    add_score_window.config(bg="#f5f5f5")

    title_label = tk.Label(add_score_window, text="添加成绩", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.grid(row=0, columnspan=2, pady=20)

    label_student_id = tk.Label(add_score_window, text="学生ID:", font=("Arial", 12), bg="#f5f5f5")
    label_student_id.grid(row=1, column=0, pady=10, padx=20, sticky="e")
    entry_student_id = tk.Entry(add_score_window, font=("Arial", 12), width=25)
    entry_student_id.grid(row=1, column=1, pady=10, padx=20)

    label_course_id = tk.Label(add_score_window, text="课程ID:", font=("Arial", 12), bg="#f5f5f5")
    label_course_id.grid(row=2, column=0, pady=10, padx=20, sticky="e")
    entry_course_id = tk.Entry(add_score_window, font=("Arial", 12), width=25)
    entry_course_id.grid(row=2, column=1, pady=10, padx=20)

    label_score = tk.Label(add_score_window, text="成绩:", font=("Arial", 12), bg="#f5f5f5")
    label_score.grid(row=3, column=0, pady=10, padx=20, sticky="e")
    entry_score = tk.Entry(add_score_window, font=("Arial", 12), width=25)
    entry_score.grid(row=3, column=1, pady=10, padx=20)

    def save_score():
        student_id = entry_student_id.get()
        course_id = entry_course_id.get()
        score = entry_score.get()

        if not student_id or not course_id or not score:
            messagebox.showerror("错误", "请输入所有信息！", parent=add_score_window)
            return

        try:
            score = float(score)
            # 检查成绩是否在合理范围内
            if not (0 < score < 100):
                messagebox.showerror("错误", "成绩必须大于0且小于100！", parent=add_score_window)
                return

            success, message = manager.add_grade(Grade(student_id, course_id, score))
            if success:
                messagebox.showinfo("成功", message, parent=add_score_window)
            else:
                messagebox.showerror("错误", message, parent=add_score_window)

        except ValueError:
            messagebox.showerror("错误", "请输入有效的成绩！", parent=add_score_window)

    def return_to_main_menu():
        add_score_window.destroy()

    button_save = tk.Button(add_score_window, text="保存", command=save_score, font=("Arial", 12),
                            bg="#4CAF50", fg="white", width=15, relief="raised", bd=2)
    button_save.grid(row=4, column=1, pady=10, padx=20, sticky="e")

    button_return = tk.Button(add_score_window, text="返回主菜单", command=return_to_main_menu, font=("Arial", 12),
                              bg="#2196F3", fg="white", width=15, relief="raised", bd=2)
    button_return.grid(row=5, column=1, pady=10, padx=20, sticky="e")

    def return_to_main_menu():
        add_score_window.destroy()

    button_save = tk.Button(add_score_window, text="保存", command=save_score, font=("Arial", 12),
                            bg="#4CAF50", fg="white", width=15, relief="raised", bd=2)
    button_save.grid(row=4, column=1, pady=10, padx=20, sticky="e")

    button_return = tk.Button(add_score_window, text="返回主菜单", command=return_to_main_menu, font=("Arial", 12),
                              bg="#2196F3", fg="white", width=15, relief="raised", bd=2)
    button_return.grid(row=5, column=1, pady=10, padx=20, sticky="e")


def show_course_window():
    show_course_window = tk.Toplevel(root)
    show_course_window.title("显示所有已有课程")
    show_course_window.geometry("600x400")
    show_course_window.resizable(False, False)
    show_course_window.config(bg="#f5f5f5")

    # 整体布局框架
    main_frame = tk.Frame(show_course_window, bg="#f5f5f5")
    main_frame.pack(fill="both", expand=True)

    # 标题标签
    title_label = tk.Label(main_frame, text="所有课程信息", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.pack(pady=10)

    # 带滚动条的文本框框架
    text_frame = tk.Frame(main_frame)
    text_frame.pack(padx=20, fill="both", expand=True)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text_area = tk.Text(text_frame,
                        font=("Arial", 12),
                        bg="white",
                        fg="black",
                        yscrollcommand=scrollbar.set,
                        height=15)
    text_area.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=text_area.yview)

    # 填充课程数据
    courses = manager.show_courses()
    for course in courses:
        text_area.insert(tk.END, f"课程ID: {course[0]}, 课程名称: {course[1]}\n")

    # 按钮框架
    button_frame = tk.Frame(main_frame, bg="#f5f5f5")
    button_frame.pack(pady=10, fill="x")

    button_back = tk.Button(button_frame, text="返回主菜单", command=show_course_window.destroy,
                            font=("Arial", 12),
                            bg="#2196F3",
                            fg="white",
                            width=15,
                            relief="raised",
                            bd=2)
    button_back.pack(pady=10)


def add_course_window():
    add_course_window = tk.Toplevel(root)
    add_course_window.title("添加新的课程")
    add_course_window.geometry("500x350")
    add_course_window.resizable(False, False)  # 禁止调整窗口大小
    add_course_window.config(bg="#f5f5f5")

    title_label = tk.Label(add_course_window, text="添加新的课程", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.grid(row=0, columnspan=2, pady=20)

    label_id = tk.Label(add_course_window, text="课程ID:", font=("Arial", 12), bg="#f5f5f5")
    label_id.grid(row=1, column=0, pady=10, padx=20, sticky="e")
    entry_id = tk.Entry(add_course_window, font=("Arial", 12), width=25)
    entry_id.grid(row=1, column=1, pady=10, padx=20)

    label_name = tk.Label(add_course_window, text="课程名称:", font=("Arial", 12), bg="#f5f5f5")
    label_name.grid(row=2, column=0, pady=10, padx=20, sticky="e")
    entry_name = tk.Entry(add_course_window, font=("Arial", 12), width=25)
    entry_name.grid(row=2, column=1, pady=10, padx=20)

    def save_course():
        course_id = entry_id.get()
        course_name = entry_name.get()
        if course_id and course_name:
            success, message = manager.add_course(Course(course_id, course_name))
            if success:
                # 弹出提示窗口，父窗口为当前的 add_course_window
                messagebox.showinfo("成功", message, parent=add_course_window)
            else:
                messagebox.showerror("错误", message, parent=add_course_window)
        else:
            messagebox.showerror("错误", "请输入所有信息！", parent=add_course_window)

    def return_to_main_menu():
        add_course_window.destroy()

    button_save = tk.Button(add_course_window, text="保存", command=save_course, font=("Arial", 12),
                            bg="#4CAF50", fg="white", width=15, relief="raised", bd=2)
    button_save.grid(row=4, column=1, pady=10, padx=20, sticky="e")

    button_return = tk.Button(add_course_window, text="返回主菜单", command=return_to_main_menu, font=("Arial", 12),
                              bg="#2196F3", fg="white", width=15, relief="raised", bd=2)
    button_return.grid(row=5, column=1, pady=10, padx=20, sticky="e")


def show_all_students_window():
    show_all_students_window = tk.Toplevel(root)
    show_all_students_window.title("显示学生的所有信息")
    show_all_students_window.geometry("700x400")
    show_all_students_window.resizable(False, False)
    show_all_students_window.config(bg="#f5f5f5")

    # 整体布局框架
    main_frame = tk.Frame(show_all_students_window, bg="#f5f5f5")
    main_frame.pack(fill="both", expand=True)

    # 标题标签
    title_label = tk.Label(main_frame, text="所有学生信息", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.pack(pady=10)

    # 带滚动条的文本框框架
    text_frame = tk.Frame(main_frame)
    text_frame.pack(padx=20, fill="both", expand=True)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text_area = tk.Text(text_frame,
                        font=("Arial", 12),
                        bg="white",
                        fg="black",
                        yscrollcommand=scrollbar.set,
                        height=15)
    text_area.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=text_area.yview)

    # 填充学生数据
    students = manager.show_all_message()
    for student_id, info in students.items():
        student_info = f"学生ID: {info['student_id']}, 姓名: {info['name']}, 年龄: {info['age']}\n"
        for course_name, score in info["courses"].items():
            student_info += f"  {course_name}成绩: {score}\t"
        student_info += f"  平均成绩: {info['average_score']:.2f}\n"
        text_area.insert(tk.END, student_info + "\n")

    # 按钮框架
    button_frame = tk.Frame(main_frame, bg="#f5f5f5")
    button_frame.pack(pady=10, fill="x")

    button_back = tk.Button(button_frame, text="返回主菜单", command=show_all_students_window.destroy,
                            font=("Arial", 12),
                            bg="#2196F3",
                            fg="white",
                            width=15,
                            relief="raised",
                            bd=2)
    button_back.pack(pady=10)


def change_students_window():
    change_students_window = tk.Toplevel(root)
    change_students_window.title("修改学生信息")
    change_students_window.geometry("500x350")
    change_students_window.resizable(False, False)  # 禁止调整窗口大小
    change_students_window.config(bg="#f5f5f5")

    title_label = tk.Label(change_students_window, text="修改学生信息", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.grid(row=0, columnspan=2, pady=20)

    label_student_id = tk.Label(change_students_window, text="学生ID:", font=("Arial", 12), bg="#f5f5f5")
    label_student_id.grid(row=1, column=0, pady=10, padx=20, sticky="e")
    entry_student_id = tk.Entry(change_students_window, font=("Arial", 12), width=25)
    entry_student_id.grid(row=1, column=1, pady=10, padx=20)

    label_new_name = tk.Label(change_students_window, text="新姓名:", font=("Arial", 12), bg="#f5f5f5")
    label_new_name.grid(row=2, column=0, pady=10, padx=20, sticky="e")
    entry_new_name = tk.Entry(change_students_window, font=("Arial", 12), width=25)
    entry_new_name.grid(row=2, column=1, pady=10, padx=20)

    label_new_age = tk.Label(change_students_window, text="新年龄:", font=("Arial", 12), bg="#f5f5f5")
    label_new_age.grid(row=3, column=0, pady=10, padx=20, sticky="e")
    entry_new_age = tk.Entry(change_students_window, font=("Arial", 12), width=25)
    entry_new_age.grid(row=3, column=1, pady=10, padx=20)

    def update_student():
        student_id = entry_student_id.get()
        new_name = entry_new_name.get().strip() if entry_new_name.get().strip() else None
        new_age = entry_new_age.get().strip() if entry_new_age.get().strip() else None

        if not student_id:
            messagebox.showerror("错误", "请输入学生ID！", parent=change_students_window)
            return

        success, message = manager.change_students(student_id, name=new_name, age=new_age)
        if success:
            messagebox.showinfo("成功", message, parent=change_students_window)
        else:
            messagebox.showerror("错误", message, parent=change_students_window)

    def return_to_main_menu():
        change_students_window.destroy()

    button_update = tk.Button(change_students_window, text="更新", command=update_student, font=("Arial", 12),
                              bg="#4CAF50", fg="white", width=15, relief="raised", bd=2)
    button_update.grid(row=5, columnspan=2, pady=10)

    button_return = tk.Button(change_students_window, text="返回主菜单", command=return_to_main_menu,
                              font=("Arial", 12),
                              bg="#2196F3", fg="white", width=15, relief="raised", bd=2)
    button_return.grid(row=6, columnspan=2, pady=10)


def delete_students_window():
    delete_students_window = tk.Toplevel(root)
    delete_students_window.title("删除学生记录")
    delete_students_window.geometry("500x300")
    delete_students_window.resizable(False, False)  # 禁止调整窗口大小
    delete_students_window.config(bg="#f5f5f5")

    title_label = tk.Label(delete_students_window, text="删除学生记录", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.grid(row=0, columnspan=2, pady=20)

    label_identifier = tk.Label(delete_students_window, text="输入学生ID或姓名:", font=("Arial", 12), bg="#f5f5f5")
    label_identifier.grid(row=1, column=0, pady=10, padx=20, sticky="e")
    entry_identifier = tk.Entry(delete_students_window, font=("Arial", 12), width=25)
    entry_identifier.grid(row=1, column=1, pady=10, padx=20)

    def delete_student():
        identifier = entry_identifier.get()
        if not identifier:
            messagebox.showerror("错误", "请输入学生ID或姓名！", parent=delete_students_window)
            return

        success, message = manager.delete_students(identifier)
        if success:
            messagebox.showinfo("成功", message, parent=delete_students_window)
        else:
            messagebox.showerror("错误", message, parent=delete_students_window)

    def return_to_main_menu():
        delete_students_window.destroy()

    button_delete = tk.Button(delete_students_window, text="删除", command=delete_student, font=("Arial", 12),
                              bg="#4CAF50", fg="white", width=15, relief="raised", bd=2)
    button_delete.grid(row=2, columnspan=2, pady=10)

    button_return = tk.Button(delete_students_window, text="返回主菜单", command=return_to_main_menu,
                              font=("Arial", 12),
                              bg="#2196F3", fg="white", width=15, relief="raised", bd=2)
    button_return.grid(row=3, columnspan=2, pady=10)


def search_student_window():
    search_student_window = tk.Toplevel(root)
    search_student_window.title("查询学生")
    search_student_window.geometry("500x450")
    search_student_window.resizable(False, False)  # 禁止调整窗口大小
    search_student_window.config(bg="#f5f5f5")

    title_label = tk.Label(search_student_window, text="查询学生信息", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.grid(row=0, columnspan=2, pady=20)

    label_search = tk.Label(search_student_window, text="输入学号或姓名:", font=("Arial", 12), bg="#f5f5f5")
    label_search.grid(row=1, column=0, pady=10, padx=20, sticky="e")
    entry_search = tk.Entry(search_student_window, font=("Arial", 12), width=25)
    entry_search.grid(row=1, column=1, pady=10, padx=20)

    text_area = tk.Text(search_student_window, font=("Arial", 12), bg="white", fg="black", height=10, width=40)
    text_area.grid(row=3, columnspan=2, pady=10, padx=20)

    def search():
        search_message = entry_search.get()
        if not search_message:
            messagebox.showerror("错误", "请输入学号或姓名！", parent=search_student_window)
            return

        students = manager.search_student(search_message)
        if not students:
            messagebox.showinfo("未找到", "未找到匹配的学生信息！", parent=search_student_window)
        else:
            text_area.delete(1.0, tk.END)
            for student in students:
                text_area.insert(tk.END, f"学生ID: {student[0]}, 姓名: {student[1]}, 年龄: {student[2]}\n")

    def return_to_main_menu():
        search_student_window.destroy()

    button_search = tk.Button(search_student_window, text="查询", command=search, font=("Arial", 12),
                              bg="#4CAF50", fg="white", width=15, relief="raised", bd=2)
    button_search.grid(row=2, columnspan=2, pady=10)

    button_return = tk.Button(search_student_window, text="返回主菜单", command=return_to_main_menu, font=("Arial", 12),
                              bg="#2196F3", fg="white", width=15, relief="raised", bd=2)
    button_return.grid(row=4, columnspan=2, pady=10)


def sort_by_computer_window():
    sort_by_computer_window = tk.Toplevel(root)
    sort_by_computer_window.title("按计算机成绩排序")
    sort_by_computer_window.geometry("600x400")
    sort_by_computer_window.resizable(False, False)
    sort_by_computer_window.config(bg="#f5f5f5")

    # 窗口内容采用垂直布局管理
    main_frame = tk.Frame(sort_by_computer_window, bg="#f5f5f5")
    main_frame.pack(fill="both", expand=True)

    # 标题标签
    title_label = tk.Label(main_frame, text="按计算机成绩排序", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.pack(pady=10)

    # 创建带滚动条的文本框容器
    text_frame = tk.Frame(main_frame)
    text_frame.pack(padx=20, fill="both", expand=True)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text_area = tk.Text(text_frame,
                        font=("Arial", 12),
                        bg="white",
                        fg="black",
                        yscrollcommand=scrollbar.set,
                        height=15)
    text_area.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=text_area.yview)

    # 添加数据
    students = manager.sort_students_by_computer_score()
    for student in students:
        text_area.insert(tk.END, f"学生ID: {student[0]}, 姓名: {student[1]}, 计算机成绩: {student[2]}\n")

    # 底部按钮容器
    button_frame = tk.Frame(main_frame, bg="#f5f5f5")
    button_frame.pack(pady=10, fill="x")

    button_back = tk.Button(button_frame,
                            text="返回主菜单",
                            command=sort_by_computer_window.destroy,
                            font=("Arial", 12),
                            bg="#2196F3",
                            fg="white",
                            width=15,
                            relief="raised",
                            bd=2)
    button_back.pack(pady=10)


def sort_by_average_window():
    sort_by_average_window = tk.Toplevel(root)
    sort_by_average_window.title("按平均成绩排序")
    sort_by_average_window.geometry("600x400")
    sort_by_average_window.resizable(False, False)
    sort_by_average_window.config(bg="#f5f5f5")

    # 整体内容框架
    main_frame = tk.Frame(sort_by_average_window, bg="#f5f5f5")
    main_frame.pack(fill="both", expand=True)

    # 标题标签
    title_label = tk.Label(main_frame, text="按平均成绩排序", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.pack(pady=10)

    # 带滚动条的文本框框架
    text_frame = tk.Frame(main_frame)
    text_frame.pack(padx=20, fill="both", expand=True)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text_area = tk.Text(text_frame,
                        font=("Arial", 12),
                        bg="white",
                        fg="black",
                        yscrollcommand=scrollbar.set,
                        height=15)
    text_area.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=text_area.yview)

    # 填充数据
    students = manager.sort_students_by_average_score()
    for student in students:
        text_area.insert(tk.END, f"学生ID: {student[0]}, 姓名: {student[1]}, 平均成绩: {student[2]:.2f}\n")

    # 按钮框架
    button_frame = tk.Frame(main_frame, bg="#f5f5f5")
    button_frame.pack(pady=10, fill="x")

    button_back = tk.Button(button_frame, text="返回主菜单", command=sort_by_average_window.destroy,
                            font=("Arial", 12),
                            bg="#2196F3",
                            fg="white",
                            width=15,
                            relief="raised",
                            bd=2)
    button_back.pack(pady=10)


def analyse_class_performance_window():
    analyse_class_performance_window = tk.Toplevel(root)
    analyse_class_performance_window.title("班级成绩分析")
    analyse_class_performance_window.geometry("700x400")
    analyse_class_performance_window.resizable(False, False)
    analyse_class_performance_window.config(bg="#f5f5f5")

    # 整体内容框架
    main_frame = tk.Frame(analyse_class_performance_window, bg="#f5f5f5")
    main_frame.pack(fill="both", expand=True)

    # 标题标签
    title_label = tk.Label(main_frame, text="班级成绩分析", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.pack(pady=10)

    # 带滚动条的文本框框架
    text_frame = tk.Frame(main_frame)
    text_frame.pack(padx=20, fill="both", expand=True)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text_area = tk.Text(text_frame,
                        font=("Arial", 12),
                        bg="white",
                        fg="black",
                        yscrollcommand=scrollbar.set,
                        height=15)
    text_area.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=text_area.yview)

    # 填充数据
    results = manager.analyze_class_performance()
    for result in results:
        text_area.insert(tk.END,
                         f"课程: {result[0]}, 最高分: {result[2]:.2f}, 最低分: {result[3]:.2f}, 平均分: {result[1]:.2f}, 及格率: {result[4]:.2f}%, 优秀率: {result[5]:.2f}%\n")

    # 找到平均分最高和最低的课程
    sorted_results = sorted(results, key=lambda x: x[1])
    lowest_course = sorted_results[0][0]
    highest_course = sorted_results[-1][0]

    summary_message = f"本班的{highest_course}平均分最高，继续保持，但是{lowest_course}平均分最低，需要努力提高！"

    def show_summary():
        messagebox.showinfo("班级成绩总结", summary_message)
        analyse_class_performance_window.destroy()

    # 按钮框架
    button_frame = tk.Frame(main_frame, bg="#f5f5f5")
    button_frame.pack(pady=10, fill="x")

    button_confirm = tk.Button(button_frame, text="确定", command=show_summary,
                               font=("Arial", 12), bg="#4CAF50", fg="white", width=15, relief="raised", bd=2)
    button_confirm.pack(pady=10)


def out_of_system_window():
    response = messagebox.askyesno("退出系统", "您确定要退出系统吗？")
    if response:
        root.destroy()


root = tk.Tk()
root.title("学生成绩管理系统")
root.geometry("500x450")
root.resizable(False, False)  # 禁止调整窗口大小
root.config(bg="#f0f0f0")

# 创建登录界面
login_frame = tk.Frame(root, bg="#f0f0f0")
login_frame.pack(expand=True, fill="both", pady=50)

# 添加标题
title_label = tk.Label(login_frame, text="学生成绩管理系统", font=("Arial", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=20)

# 创建标签和输入框
label_username = tk.Label(login_frame, text="用户名:", bg="#f0f0f0", font=("Arial", 12))
label_username.pack(pady=5)

entry_username = tk.Entry(login_frame, font=("Arial", 12), width=30)
entry_username.pack(pady=5)

label_password = tk.Label(login_frame, text="密码:", bg="#f0f0f0", font=("Arial", 12))
label_password.pack(pady=5)

entry_password = tk.Entry(login_frame, show="*", font=("Arial", 12), width=30)
entry_password.pack(pady=5)

# 创建登录按钮
button_login = tk.Button(login_frame, text="登录", command=login, font=("Arial", 12), bg="#4CAF50", fg="white",
                         width=20)
button_login.pack(pady=20)

# 创建注册按钮
button_register = tk.Button(login_frame, text="注册", command=add_user_window, font=("Arial", 12), bg="#4CAF50",
                            fg="white",
                            width=20)
button_register.pack(pady=25)

# 创建主菜单界面
main_menu_frame = tk.Frame(root, bg="#f0f0f0")
main_menu_frame.columnconfigure(0, weight=1)
main_menu_frame.columnconfigure(1, weight=1)

manager = Manager()

# 创建标题
main_menu_title = tk.Label(main_menu_frame, text="主菜单", font=("Arial", 14, "bold"), bg="#f0f0f0")
main_menu_title.grid(row=0, column=0, columnspan=2, pady=10)

# 创建按钮
button_add_student = create_menu_button("添加学生(基本信息)", add_student_window)
button_add_student.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

button_add_grade = create_menu_button("添加学生(成绩信息)", add_grade_window)
button_add_grade.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

button_show_course = create_menu_button("显示所有已有课程", show_course_window)
button_show_course.grid(row=3, column=0, pady=5, padx=10, sticky="ew")

button_add_course = create_menu_button("添加新课程", add_course_window)
button_add_course.grid(row=4, column=0, pady=5, padx=10, sticky="ew")

button_show_students = create_menu_button("显示所有学生信息", show_all_students_window)
button_show_students.grid(row=5, column=0, pady=5, padx=10, sticky="ew")

button_change_student = create_menu_button("修改学生信息", change_students_window)
button_change_student.grid(row=6, column=0, pady=5, padx=10, sticky="ew")

button_change_grade = create_menu_button("修改学生成绩", change_grade_window)
button_change_grade.grid(row=7, column=0, pady=5, padx=10, sticky="ew")

button_search_student = create_menu_button("查询学生", search_student_window)
button_search_student.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

button_delete_student = create_menu_button("删除学生记录", delete_students_window)
button_delete_student.grid(row=2, column=1, pady=5, padx=10, sticky="ew")

button_sort_computer = create_menu_button("按计算机成绩排序", sort_by_computer_window)
button_sort_computer.grid(row=3, column=1, pady=5, padx=10, sticky="ew")

button_sort_average = create_menu_button("按平均成绩排序", sort_by_average_window)
button_sort_average.grid(row=4, column=1, pady=5, padx=10, sticky="ew")

button_analyze = create_menu_button("班级成绩分析", analyse_class_performance_window)
button_analyze.grid(row=5, column=1, pady=5, padx=10, sticky="ew")

button_exit = create_menu_button("退出系统", out_of_system_window)
button_exit.grid(row=6, column=1, pady=5, padx=10, sticky="ew")

# 添加分隔线
separator = tk.Frame(main_menu_frame, height=2, bg="#cccccc")
separator.grid(row=8, column=0, columnspan=2, sticky="ew", pady=10)

root.mainloop()
