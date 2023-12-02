from database import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from logical import CalendarProblem,Calendar,GeneticSearch
from copy import deepcopy
taskList = []
root = Tk()
name = StringVar()
deadline = IntVar()
satisfy = IntVar()
def is_valid_deadline(value):
    try:
        deadline = int(value)
        return 12 <= deadline <= 24
    except ValueError:
        return False

def is_valid_input():
    return bool(name.get() and deadline.get() and satisfy.get())

def add():
    if not is_valid_deadline(deadline.get()):
        messagebox.showerror("Lỗi", "Deadline phải nằm trong khoảng từ 12 đến 24")
        return

    if not is_valid_input():
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
        return

    taskList.append({
        'name': name.get(),
        'deadline': deadline.get(),
        'satisfy': satisfy.get()
    })
    show()
    reset()
    
def show():
    tree.delete(*tree.get_children())
    for task in taskList:
        tree.insert("", "end", values=(task['name'], task['deadline'], task['satisfy']))

def sapxepLich():
    global taskList
    myProblem = CalendarProblem(taskList)

    genetic1 = GeneticSearch(myProblem)

    genetic1.execute(fringe_size = 200, num_generation = 100)
    taskList = deepcopy(genetic1.result.state)
    show()

def delete_selected():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một task để xoá.")
        return

    for item in selected_items:
        index = tree.index(item)
        if index is not None:
            taskList.pop(index)

    show()



def reset():
    name.set("")
    deadline.set("")
    satisfy.set("")



def exit_application():
    result = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn thoát ứng dụng?")
    if result:
        root.quit()



root.title('Quản lí task và deadline')
root.geometry('720x550')
root.resizable(False, False)

Label(root, text='ỨNG DỤNG QUẢN LÍ TASK', fg='red', font=('Times New Roman', 26, 'bold'), width=25).grid(row=0)

tree = ttk.Treeview(root, columns=("Task", "Deadline", "Satisfy"), show="headings")
tree.heading("Task", text="Task")
tree.heading("Deadline", text="Deadline")
tree.heading("Satisfy", text="Satisfy")
tree.column("Task", width=400)
tree.column("Deadline", width=150)
tree.column("Satisfy", width=150)
tree.grid(row=1, columnspan=2)

Label(root, text='Tên task:', font=('Times New Roman', 16, 'bold')).grid(row=2, column=0)
Entry(root, width=40, textvariable=name).grid(row=2, column=1)

Label(root, text='Hạn chót:', font=('Times New Roman', 16, 'bold')).grid(row=3, column=0)
Entry(root, width=40, textvariable=deadline).grid(row=3, column=1)

Label(root, text='Độ thoả mãn:', font=('Times New Roman', 16, 'bold')).grid(row=4, column=0)
Entry(root, width=40, textvariable=satisfy).grid(row=4, column=1)

button = Frame(root)
Button(button, text='Thêm', command=add).pack(side=LEFT)
Button(button, text='Xoá', command=delete_selected).pack(side=LEFT)
Button(button, text='Sắp xếp', command=sapxepLich).pack(side=LEFT)
Button(button, text='Thoát', command=exit_application).pack(side=LEFT)
button.grid(row=5, column=1, columnspan=2)

# Initialize taskList with the provided data
# tasks = [
#     {
#         'name': "mobile",
#         'satisfy': 20,
#         'deadline': 24
#     },
#     {
#         'name': "phân tích thiết kế hệ thống",
#         'satisfy': 20,
#         'deadline': 13
#     },
#     {
#         'name': "QAQC",
#         'satisfy': 40,
#         'deadline': 15
#     },
#     {
#         'name': "Trí tuệ nhân tạo",
#         'satisfy': 30,
#         'deadline': 16
#     },
#     {
#         'name': "Phát triển web",
#         'satisfy': 60,
#         'deadline': 17
#     }
# ]

# taskList = tasks  # Initialize taskList with the provided data

show()  # Display the initial data

root.mainloop()
