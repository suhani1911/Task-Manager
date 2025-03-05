
from tkinter import *
from tkinter import messagebox
import os
import time

CREDENTIALS_FILE = "authenticate.txt"

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("User Authentication")
        self.root.geometry("500x400+0+0")
        self.root.maxsize(1350, 700)
        self.root.minsize(1350, 700)

        title = Label(self.root, text="Task Manager", bg="#581845", fg="#DAF7A6", font=("times new roman", 30, "bold"), padx=15, pady=15)
        title.pack(fill=X)

        self.username_label = Label(self.root, text="Username:", font=("Arial", 20))
        self.username_label.pack(pady=10)

        self.username_entry = Entry(self.root, font=("Arial", 15))
        self.username_entry.pack(pady=5)

        self.password_label = Label(self.root, text="Password:", font=("Arial", 20))
        self.password_label.pack(pady=10)

        self.password_entry = Entry(self.root, show="*", font=("Arial", 15))
        self.password_entry.pack(pady=5)

        self.login_button = Button(self.root, text="Login", command=self.login_user, font=("Arial", 20), bg="green", fg="white")
        self.login_button.pack(pady=20)

        self.register_button = Button(self.root, text="Register", command=self.register_user, font=("Arial", 20), bg="blue", fg="white")
        self.register_button.pack(pady=5)

        lbl_footer = Label(self.root, text="Task Manager System ", font=("times new roman", 12), bg="#581845", fg="#FFFFFF")
        lbl_footer.pack(side=BOTTOM, fill=X) 

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the user exists and the password matches
        with open(CREDENTIALS_FILE, "r") as file:
            credentials = file.readlines()
            for credential in credentials:
                stored_username, stored_password = credential.strip().split(",")
                if username == stored_username and password == stored_password:
                    messagebox.showinfo("Login Success", "You have successfully logged in!")
                    self.taskManagerMenu(username)
                    self.root.withdraw()  # Close the login window
                    return
        messagebox.showwarning("Login Failed", "Invalid username or password!")

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if len(password) < 10:
            messagebox.showwarning("Invalid Password", "Password must be at least 10 characters.")
            return
        
        # Check if the username already exists
        with open(CREDENTIALS_FILE, "a+") as file:
            file.seek(0)
            credentials = file.readlines()
            for credential in credentials:
                stored_username, _ = credential.strip().split(",")
                if username == stored_username:
                    messagebox.showwarning("Username Exists", "Username already exists.")
                    return

            file.write(f"{username},{password}\n")
        messagebox.showinfo("Registration Successful", "You have successfully registered!")
        self.taskManagerMenu(username)
        self.root.withdraw() 
          
    def taskManagerMenu(self,username):
        self.new_win = Toplevel(self.root)
        self.new_obj = TaskManager(self.new_win,username)


class TaskManager:
    def __init__(self, root,username):
        self.root = root
        self.username=username
        self.root.geometry("500x400+0+0")
        self.root.maxsize(1350, 700)
        self.root.minsize(1350, 700)

        self.root.title("Task Manager System")
        title = Label(self.root, text="Task Manager", bg="#581845", fg="#DAF7A6", font=("times new roman", 30, "bold"), padx=15, pady=15)
        title.pack(fill=X)

        #----Clock----
        self.lbl_clock = Label(self.root, text="fTime: HH:MM:SS\t\tDate: DD-MM-YYYY\t\tWelcome, {self.username}", bg="#581845", fg="#DAF7A6", font=("times new roman", 15), padx=5, pady=5)
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #menu buttons
        LeftMenu = Frame(self.root, borderwidth=2, bg="#581845")
        LeftMenu.place(x=20, y=98, width=1310, height=700)
        
        btn_add_task = Button(LeftMenu, text="Add Task", command=self.add_task, bg="#CA8787", font=("times new roman", 20, "bold"), pady=31, borderwidth=2, relief="groove", cursor="hand2").pack(fill=X)
        btn_view_task = Button(LeftMenu, text="View Tasks", command=self.view_task, bg="#CA8787", font=("times new roman", 20, "bold"), pady=31, borderwidth=2, relief="groove", cursor="hand2").pack(fill=X)
        btn_mark_completed = Button(LeftMenu, text="Mark Completed", command=self.mark_completed, bg="#CA8787", font=("times new roman", 20, "bold"), pady=31, borderwidth=2, relief="groove", cursor="hand2").pack(fill=X)
        btn_delete_task = Button(LeftMenu, text="Delete Task", command=self.delete_task, bg="#CA8787", font=("times new roman", 20, "bold"), pady=31, borderwidth=2, relief="groove", cursor="hand2").pack(fill=X)
        btn_exit = Button(LeftMenu, text="Exit", command=self.root.destroy, bg="#CA8787", font=("times new roman", 20, "bold"), pady=31, borderwidth=2, relief="groove", cursor="hand2").pack(fill=X)

        # Footer section
        lbl_footer = Label(self.root, text="Task Manager Systems", font=("times new roman", 12), bg="#581845", fg="#FFFFFF")
        lbl_footer.pack(side=BOTTOM, fill=X)

        self.update_clock()

    def add_task(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = AddTaskWindow(self.new_win,"arya")

    def view_task(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ViewTaskWindow(self.new_win,"arya")

    def mark_completed(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = MarkCompletedWindow(self.new_win,"arya")

    def delete_task(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = DeleteTaskWindow(self.new_win,"arya")

    def update_clock(self):
        time_ = time.strftime("%I:%M:%S %p")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Time: {time_}\tDate: {date_}")
        self.lbl_clock.after(200, self.update_clock)


class AddTaskWindow:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Add New Task")
        self.root.geometry("1300x500+22+145")

        self.title_label = Label(self.root, text="Add New Task", font=("times new roman", 20, "bold"))
        self.title_label.pack(pady=20)

        # Task Description
        self.description_label = Label(self.root, text="Enter Task Description", font=("times new roman", 15))
        self.description_label.pack(pady=10)
        self.description_entry = Entry(self.root, font=("times new roman", 15), width=50)
        self.description_entry.pack(pady=10)

        self.tags_label = Label(self.root, text="Enter Task Tag", font=("times new roman", 15))
        self.tags_label.pack(pady=10)
        self.tags_entry = Entry(self.root, font=("times new roman", 15), width=50)
        self.tags_entry.pack(pady=10)

        self.add_with_tag_button = Button(self.root, text="Add Task with Tags", command=self.addTaskWithTag, font=("times new roman", 15), bg="#5cb85c", fg="white")
        self.add_with_tag_button.pack(pady=10)

        self.add_without_tag_button = Button(self.root, text="Add Task without Tags", command=self.addTaskWithoutTag, font=("times new roman", 15), bg="#5cb85c", fg="white")
        self.add_without_tag_button.pack(pady=10)

    def addTaskWithTag(self):
        description = self.description_entry.get().strip()
        tags = self.tags_entry.get().strip()
        if description and tags:
            task_id = self.getID()
            with open(f"{self.username}_tasks.txt", "a") as file:
                file.write(f"{task_id},{description},Not Completed,{tags}\n")
                print(os.path.isfile(f"{self.username}_tasks.txt"))
                print(os.getcwd())

            messagebox.showinfo("Success", "Task added with tags successfully!")
            self.root.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter both description and tags.")

    def addTaskWithoutTag(self):
        description = self.description_entry.get().strip()
        if description:
            task_id = self.getID()
            with open(f"{self.username}_tasks.txt", "a") as file:
                file.write(f"{task_id},{description},Not Completed,Not Mentioned\n")
            messagebox.showinfo("Success", "Task added without tags successfully!")
            self.root.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter a task description.")

    def getID(self):
        try:
            with open(f"{self.username}_tasks.txt", "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            lines = []
        return len(lines) + 1

class ViewTaskWindow:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("View Tasks")
        self.root.geometry("1300x500+22+145")

        self.get_id_user = IntVar()
        self.get_tag_user = StringVar()

        self.title_label = Label(self.root, text="View Tasks", font=("times new roman", 20, "bold"))
        self.title_label.pack(pady=20)

        # Task View Buttons
        self.add_with_tag_button = Button(self.root, text="View All Tasks", command=self.viewTaskAll, font=("times new roman", 15), bg="#5cb85c", fg="white").place(x=65, y=80, height=30, width=220)
        self.view_one_button = Button(self.root, text="View Task of Particular ID", command=self.viewTaskOne, font=("times new roman", 15), bg="#5cb85c", fg="white").place(x=65, y=120, height=30, width=220)
        self.get_id_user_entry = Entry(self.root, textvariable=self.get_id_user, font=("goudy old style", 15), bg="lightyellow")
        self.get_id_user_entry.place(x=295, y=122, width=100, height=28)

        self.view_completed_button = Button(self.root, text="View All Completed Tasks", command=self.viewTaskComplete, font=("times new roman", 15), bg="#5cb85c", fg="white").place(x=295, y=80, height=30, width=220)
        self.view_incomplete_button = Button(self.root, text="View All Incomplete Tasks", command=self.viewTaskIncomplete, font=("times new roman", 15), bg="#5cb85c", fg="white").place(x=525, y=80, height=30, width=220)
        self.view_tag_button = Button(self.root, text="View Task by Tag", command=self.viewTaskTag, font=("times new roman", 15), bg="#5cb85c", fg="white").place(x=410, y=120, height=30, width=220)
        
        self.get_tag_user_entry = Entry(self.root, textvariable=self.get_tag_user, font=("goudy old style", 15), bg="lightyellow")
        self.get_tag_user_entry.place(x=640, y=122, width=100, height=28)

        # Textbox to display task details
        self.task_output = Text(self.root, height=15, width=150)
        self.task_output.place(x=765, y=80, height=400, width=515)

    def viewTaskAll(self):
        tasks = loadTask(self.username)
        self.task_output.delete(1.0, END)
        if not tasks:
            self.task_output.insert(END, "No tasks found.\n")
            return

        for task in tasks:
            self.task_output.insert(END, f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Tag: {task['tags']}\n")

    def viewTaskOne(self):
        id=self.get_id_user.get()
        tasks = loadTask(self.username)
        flag=0
        self.task_output.delete(1.0, END)
        if not validateTask(id, tasks):
            self.task_output.insert(END, "Invalid ID, try again.\n")
            return
        if not tasks:
            self.task_output.insert(END, "No tasks found.\n")
            return

        for task in tasks:
            if id == task["id"]:
                flag=1
                self.task_output.insert(END, f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Tag: {task['tags']}\n")
        if flag==0:
            self.task_output.insert(END, "No task found.\n")

    def viewTaskComplete(self):
        tasks = loadTask(self.username)
        flag=0
        self.task_output.delete(1.0, END)
        if not tasks:
            self.task_output.insert(END, "No tasks found.\n")
            return

        for task in tasks:
            if "Completed" == task["status"]:
                flag=1
                self.task_output.insert(END, f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Tag: {task['tags']}\n")
        if flag==0:
            self.task_output.insert(END, "No tasks completed yet.\n")

    def viewTaskTag(self):
        tag = self.get_tag_user.get()
        tasks = loadTask(self.username)
        flag=0
        self.task_output.delete(1.0, END)
        if not tasks:
            self.task_output.insert(END, "No tasks found.\n")
            return
        for task in tasks:
            if tag == task["tags"]:
                flag=1
                self.task_output.insert(END, f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Tag: {task['tags']}\n")
        if flag==0:
            self.task_output.insert(END, "No task found.\n")

    def viewTaskIncomplete(self):
        tasks = loadTask(self.username)
        flag=0
        self.task_output.delete(1.0, END)
        if not tasks:
            self.task_output.insert(END, "No tasks found.\n")
            return

        for task in tasks:
            if "Completed" != task["status"]:
                flag=1
                self.task_output.insert(END, f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Tag: {task['tags']}\n")
        if flag==0:
            self.task_output.insert(END, "No incomplete tasks.\n")




class MarkCompletedWindow:
    def __init__(self, root,username):
        self.root = root
        self.username = username
        self.root.title("Mark Task as Completed")
        self.root.geometry("1300x500+22+145")

        self.get_id_user=IntVar()

        self.title_label = Label(self.root, text="Enter task ID", font=("times new roman", 20, "bold"))
        self.title_label.pack(pady=20)
        self.get_id_user_entry = Entry(self.root,textvariable=self.get_id_user,font=("times new roman", 15), width=50)
        self.get_id_user_entry.pack(pady=10)

        self.mark_button = Button(self.root, text="Mark Completed", command=self.mark_completed, font=("times new roman", 15), bg="#5cb85c", fg="white")
        self.mark_button.pack(pady=30)

    def mark_completed(self):
        task_id = self.get_id_user.get()
        tasks=loadTask(self.username)
        if validateTask(task_id,tasks):
            for task in tasks:
                if task["id"] == task_id:
                    task["status"] = "Completed"
            saveTask(self.username, tasks)
            messagebox.showinfo("Success", "Task marked as completed!")
            self.root.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter a task ID.")

class DeleteTaskWindow:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Delete Task")
        self.root.geometry("1300x500+22+145")

        self.title_label = Label(self.root, text="Enter Task ID to Delete", font=("times new roman", 20, "bold"))
        self.title_label.pack(pady=20)
        self.task_id_entry = Entry(self.root, font=("times new roman", 15), width=50)
        self.task_id_entry.pack(pady=10)

        # Delete Buttons
        self.delete_button = Button(self.root, text="Delete Task", command=self.deleteTaskOne, font=("times new roman", 15), bg="#d9534f", fg="white")
        self.delete_button.pack(pady=30)

        self.delete_all_button = Button(self.root, text="Delete All Tasks", command=self.deleteTaskAll, font=("times new roman", 15), bg="#d9534f", fg="white")
        self.delete_all_button.pack(pady=10)

    def deleteTaskOne(self):
        task_id = self.task_id_entry.get()
        if task_id:
            task_id = int(task_id)
            tasks = loadTask(self.username)
            if not validateTask(task_id, tasks):  # Check if task ID is valid
                messagebox.showwarning("Input Error", "Invalid Task ID.")
                return
            updated_tasks = [task for task in tasks if task["id"] != task_id]
            saveTask(self.username, updated_tasks)
            messagebox.showinfo("Success", "Task deleted successfully!")
            self.root.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter a task ID.")

    def deleteTaskAll(self):
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all tasks?")
        if confirm:
            saveTask(self.username, [])  # Empty task list
            messagebox.showinfo("Success", "All tasks deleted successfully!")
            self.root.destroy()

def validateTask(task_id, tasks):
    for task in tasks:
        if task["id"] == task_id:
            return True
    return False

def saveTask(username, tasks):
    with open(f"{username}_tasks.txt", "w") as file:
        for task in tasks:
            file.write(f"{task['id']},{task['description']},{task['status']},{task['tags']}\n")

# Fetch existing tasks
def loadTask(username):
    tasks = []
    try:
        with open(f"{username}_tasks.txt", "r") as file:
            for line in file:
                task_details = line.strip().split(",")
                tasks.append({"id": int(task_details[0]), "description": task_details[1], "status": task_details[2], "tags": task_details[3]})
    except FileNotFoundError:
        print(f"No tasks found for {username}.")
    return tasks

if __name__ == "__main__":
    root = Tk()
    app = LoginPage(root)
    root.mainloop()
