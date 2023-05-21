import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from PIL import Image, ImageTk
import csv
import time
from datetime import datetime
from motor import *
from customer import *
from booking import *

def authenticate():
    username = entry_username.get()
    password = entry_password.get()
    if username == "linh" and password == "1":
        messagebox.showinfo("Notification", "Logged in successfully!")
        show_main_menu()
        login_window.withdraw()
    else:
        messagebox.showerror("Error", "Incorrect username or password!")

# Cửa sổ đăng nhập
login_window = tk.Tk()
login_window.title("Log In")
login_window.geometry("1000x535")

# Ảnh nền
background_image = Image.open("./image/Login.png")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(login_window, image = background_photo)
background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

# Tạo label frame với style mới
login_frame = tk.LabelFrame(login_window, bg="#8E7B5C", bd=3)
login_frame.place(relx=0.22, rely=0.5, anchor="center", width=300, height=180)

# Tạo các label và entry
label_username = tk.Label(login_frame, text="ID:", font=('Times New Roman', 16, 'bold'), bg="#8E7B5C")
label_username.pack()

entry_username = tk.Entry(login_frame, font=('Times New Roman', 16), bd=3)
entry_username.pack()

label_password = tk.Label(login_frame, text="Password:", font=('Times New Roman', 16, 'bold'), bg="#8E7B5C")
label_password.pack()

entry_password = tk.Entry(login_frame, show="*", font=('Times New Roman', 16), bd=3)
entry_password.pack()

# Xử lý sự kiện đăng nhập
def login(event):
    authenticate()
button_login = tk.Label(login_frame, text="Log In", font=('Times New Roman', 16, 'bold'), relief="solid", bd=2, padx=5, pady=5, bg="#DEB887", cursor="hand2", activebackground="#00BFFF", width=10)
button_login.pack()
button_login.bind("<Button-1>", login)
entry_password.bind("<Return>", login)

# Cửa sổ main menu
main_menu_window = tk.Toplevel()
main_menu_window.title("Main Menu")
main_menu_window.geometry("1366x768")
main_menu_window.withdraw()

# Ảnh nền main menu
main_menu_background_image = Image.open("./image/Menu.png")
main_menu_background_photo = ImageTk.PhotoImage(main_menu_background_image)
main_menu_background_label = tk.Label(main_menu_window, image = main_menu_background_photo)
main_menu_background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)


# Hàm hiển thị main menu
def show_main_menu():
    main_menu_window.deiconify()
    login_window.withdraw()

# Tạo khung menu
menu_frame = tk.LabelFrame(main_menu_window, text="Menu", font=('Times New Roman', 16, 'bold'), width=500, height=500, bg="#FFFDD0")
menu_frame.place(relx=0.25, rely=0.55, anchor="center", width=300, height=370)

# Thêm chức năng vào menu_frame
button_booking = tk.Button(menu_frame, text="Booking", font=('Times New Roman', 16, 'bold'), width=20, height=2, cursor="hand2", bg="#63B7B7", command=show_booking_list)
button_booking.pack(padx=3, pady=3)

button_motor = tk.Button(menu_frame, text="Motor", font=('Times New Roman', 16, 'bold'), width=20, height=2, cursor="hand2", bg="#63B7B7", command=show_motor_list)
button_motor.pack(padx=3, pady=3)

button_customer = tk.Button(menu_frame, text="Customer", font=('Times New Roman', 16, 'bold'), width=20, height=2, cursor="hand2", bg="#63B7B7", command=show_customer_list)
button_customer.pack(padx=3, pady=3)

button_report = tk.Button(menu_frame, text="Report", font=('Times New Roman', 16, 'bold'), width=20, height=2, cursor="hand2", bg="#63B7B7")
button_report.pack(padx=3, pady=3)

def exit():
    main_menu_window.destroy()
    login_window.deiconify()

button_exit = tk.Button(menu_frame, text="Exit", font=('Times New Roman', 16, 'bold'), width=20, height=2, cursor="hand2", bg="#63B7B7", command=exit)
button_exit.pack(padx=3, pady=3)

# Hàm cập nhật thời gian

#Hàm cập nhật ngày tháng
def update_datetime():
    current_datetime = datetime.now()  # Lấy ngày và giờ hiện tại
    date_time_label.config(text=current_datetime.strftime("%d/%m/%Y %H:%M:%S"))  # Cập nhật nội dung của nhãn ngày và giờ
    date_time_label.after(1000, update_datetime)  # Lặp lại hàm sau 1 giây (1000 milliseconds)

# Tạo khung đậm
date_time_frame = tk.LabelFrame(main_menu_window, text="Date and Time",font=('Times New Roman', 14, 'bold'), width=200, height=100, bg="#63B7B7")
date_time_frame.place(relx=0.5, rely=0.85, width=200, height=100)
# Tạo nhãn ngày và giờ
date_time_label = tk.Label(date_time_frame, text="", font=('Times New Roman', 16, 'bold'), bg="#FFFDD0")
date_time_label.pack(padx=15, pady=15)

# Bắt đầu cập nhật ngày và thời gian
update_datetime()

login_window.mainloop()