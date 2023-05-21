import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from PIL import Image, ImageTk
import csv
import os
from datetime import datetime
from booking import *

def show_motor_list():

    motor_list_window = tk.Toplevel()
    motor_list_window.title("Motor")
    motor_list_window.geometry("1080x420")

    tree_frame = ttk.Frame(motor_list_window)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    #Create a vertical scroll bar
    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set)
    scrollbar.configure(command=tree.yview)

    tree['columns'] = ('Number', 'Name', 'Brand', 'Year', 'Type', 'Motor ID', 'Condition', 'Distance Traveled', 'Status', 'Price')

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Number", anchor=tk.CENTER, width=50)
    tree.column("Name", anchor=tk.W, width=150)
    tree.column("Brand", anchor=tk.W, width=100)
    tree.column("Year", anchor=tk.W, width=100)
    tree.column("Type", anchor=tk.W, width=100)
    tree.column("Motor ID", anchor=tk.W, width=100)
    tree.column("Condition", anchor=tk.W, width=100)
    tree.column("Distance Traveled", anchor=tk.W, width=100)
    tree.column("Status", anchor=tk.W, width=100)
    tree.column("Price", anchor=tk.W, width=100)

    tree.heading("Number", text="No.")
    tree.heading("Name", text="Name")
    tree.heading("Brand", text="Brand")
    tree.heading("Year", text="Year")
    tree.heading("Type", text="Type")
    tree.heading("Motor ID", text="Motor ID")
    tree.heading("Condition", text="Condition")
    tree.heading("Distance Traveled", text="Distance Traveled")
    tree.heading("Status", text="Status")
    tree.heading("Price", text="Price per hour")

    with open('./data/motor.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  #Bỏ qua dòng tiêu đề trong file
        for row in reader:
            tree.insert("", tk.END, values=row[:len(row) - 2])

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def open_add_motor_window():
        add_motor_window = tk.Toplevel()
        add_motor_window.title("Add")
        add_motor_window.geometry("400x400")

        label_name = tk.Label(add_motor_window, text="Name:")
        label_name.pack()
        entry_name = tk.Entry(add_motor_window)
        entry_name.pack()

        label_brand = tk.Label(add_motor_window, text="Brand:")
        label_brand.pack()
        entry_brand = tk.Entry(add_motor_window)
        entry_brand.pack()

        label_year = tk.Label(add_motor_window, text="The year of manufacture:")
        label_year.pack()
        spinbox_year = tk.Spinbox(add_motor_window, from_=1900, to=2023)
        spinbox_year.pack()

        label_type = tk.Label(add_motor_window, text="Type:")
        label_type.pack()
        combo_type = ttk.Combobox(add_motor_window,
                                  values=["Manual", "Scooter", "Sport", "Adventure", "Cruiser", "Standard", "Electric"],
                                  state="readonly")
        combo_type.pack()

        label_motor_id = tk.Label(add_motor_window, text="Motor ID:")
        label_motor_id.pack()
        entry_motor_id = tk.Entry(add_motor_window)
        entry_motor_id.pack()

        label_condition = tk.Label(add_motor_window, text="Condition:")
        label_condition.pack()
        combo_condition = ttk.Combobox(add_motor_window, values=["Excellent", "Good", "Average", "Bad"],
                                       state="readonly")
        combo_condition.pack()

        label_distance = tk.Label(add_motor_window, text="Distance Traveled:")
        label_distance.pack()
        spinbox_distance = tk.Spinbox(add_motor_window, from_=500, to=200000)
        spinbox_distance.pack()

        label_price = tk.Label(add_motor_window, text="Price per hour:")
        label_price.pack()
        entry_price = tk.Entry(add_motor_window)
        entry_price.pack()

        def add_motor():
            name = entry_name.get()
            brand = entry_brand.get()
            year = spinbox_year.get()
            type = combo_type.get()
            motor_id = entry_motor_id.get()
            condition = combo_condition.get()
            distance = spinbox_distance.get()
            status = "Ready"
            price = entry_price.get()
            imagepath = f"./image/{motor_id}.png"
            historypath = f"./history/motor/{motor_id}.txt"

            if not (name and brand and year and type and motor_id and condition and price and distance):
                messagebox.showerror("Error", "Please fill in the motor information completely!")
                return

            #Tạo file history
            motor_history_text = f"Name: {name}\n"
            motor_history_text += f"Brand: {brand}\n"
            motor_history_text += f"Year Of Manufacture: {year}\n"
            motor_history_text += f"Type: {type}\n"
            motor_history_text += f"Motor ID: {motor_id}\n"
            motor_history_text += f"Condition: {condition}\n"
            motor_history_text += f"Distance Traveled: {distance}\n"
            motor_history_text += f"Status: {status}\n"
            motor_history_text += f"Price per hour: {price}\n"
            try:
                with open(historypath, "w", encoding="utf-8") as history_file:
                    history_file.write(f"**Added at {datetime.now()}:\n")
                    history_file.write(motor_history_text)
                    history_file.write("-" * 20 + "\n")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving notes to file {motor_id}.txt: {str(e)}")

            #Thêm thông tin motor mới vào file
            with open('./data/motor.csv', 'r+', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)
                next_index = len(rows)

                writer = csv.writer(file)
                writer.writerow([next_index] + [name, brand, year, type, motor_id, condition, distance, status, price, imagepath, historypath])

            tree.insert("", tk.END, values=(next_index, name, brand, year, type, motor_id, condition, distance, status, price))

            add_motor_window.destroy()

        button_add = tk.Button(add_motor_window, text="Add", command=add_motor)
        button_add.pack()

    def open_adjust_motor_window():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a motor to adjust.")
            return

        motor_info = tree.item(selected_item)['values']
        selected_motor_id = motor_info[5]
        number = motor_info[0]

        adjust_motor_window = tk.Toplevel()
        adjust_motor_window.title("Adjust")
        adjust_motor_window.geometry("400x400")

        label_name = tk.Label(adjust_motor_window, text="Name:")
        label_name.pack()
        entry_name = tk.Entry(adjust_motor_window)
        entry_name.insert(0, motor_info[1])
        entry_name.pack()

        label_brand = tk.Label(adjust_motor_window, text="Brand:")
        label_brand.pack()
        entry_brand = tk.Entry(adjust_motor_window)
        entry_brand.insert(0, motor_info[2])
        entry_brand.pack()

        label_year = tk.Label(adjust_motor_window, text="The Year Of Manufacture:")
        label_year.pack()
        spinbox_year = tk.Spinbox(adjust_motor_window, from_=1900, to=2023)
        spinbox_year.insert(0, motor_info[3])
        spinbox_year.pack()

        label_type = tk.Label(adjust_motor_window, text="Type:")
        label_type.pack()
        combo_type = ttk.Combobox(adjust_motor_window,
                                  values=["Manual", "Scooter", "Sport", "Adventure", "Cruiser", "Standard", "Electric"],
                                  state="readonly")
        combo_type.set(motor_info[4])
        combo_type.pack()

        label_motor_id = tk.Label(adjust_motor_window, text="Motor ID:")
        label_motor_id.pack()
        entry_motor_id = tk.Entry(adjust_motor_window)
        entry_motor_id.insert(0, motor_info[5])
        entry_motor_id.pack()

        label_condition = tk.Label(adjust_motor_window, text="Condition:")
        label_condition.pack()
        combo_condition = ttk.Combobox(adjust_motor_window, values=["Excellent", "Good", "Average", "Bad"],
                                       state="readonly")
        combo_condition.set(motor_info[6])
        combo_condition.pack()


        label_distance = tk.Label(adjust_motor_window, text="The Year Of Manufacture:")
        label_distance.pack()
        spinbox_distance = tk.Spinbox(adjust_motor_window, from_=1900, to=2023)
        spinbox_distance.insert(0, motor_info[6])
        spinbox_distance.pack()

        label_price = tk.Label(adjust_motor_window, text="Price per hour:")
        label_price.pack()
        entry_price = tk.Entry(adjust_motor_window)
        entry_price.insert(0, motor_info[8])
        entry_price.pack()

        def adjust_motor():
            name = entry_name.get()
            brand = entry_brand.get()
            year = spinbox_year.get()
            type = combo_type.get()
            motor_id = entry_motor_id.get()
            condition = combo_condition.get()
            distance = spinbox_distance.get()
            status = "Ready"
            price = entry_price.get()
            imagepath = f"./image/{motor_id}.png"
            historypath = f"./history/motor/{motor_id}.txt"

            #Kiểm tra xem tất cả các trường thông tin đã được điền đầy đủ hay không
            if not (name and brand and year and type and motor_id and condition and price and distance):
                messagebox.showerror("Error", "Please fill in the motor information completely!")
                return

            with open('./data/motor.csv', 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)

            for i in range(len(rows)):
                if rows[i][5] == str(selected_motor_id):
                    rows[i][1] = name
                    rows[i][2] = brand
                    rows[i][3] = year
                    rows[i][4] = type
                    rows[i][5] = motor_id
                    rows[i][6] = condition
                    rows[i][7] = distance
                    rows[i][8] = status
                    rows[i][9] = price
                    rows[i][10] = imagepath
                    rows[i][11] = historypath
                    break

            #Ghi lại toàn bộ dữ liệu vào file
            with open('./data/motor.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            #Lưu thông tin chỉnh sửa vào file historypath
            if name != motor_info[1]:
                motor_history_text = f"name: {motor_info[1]} -> {name}\n"
            if brand != motor_info[2]:
                motor_history_text += f"brand: {motor_info[2]} -> {brand}\n"
            if year != motor_info[3]:
                motor_history_text += f"Year Of Manufacture: {motor_info[3]} -> {year}\n"
            if type != motor_info[4]:
                motor_history_text += f"Type: {motor_info[4]} -> {type}\n"
            if motor_id != selected_motor_id:
                #Nếu motor_id thay đổi, đổi tên file historypath
                old_historypath = f"./history/motor/{selected_motor_id}.txt"
                if os.path.exists(old_historypath):
                    os.rename(old_historypath, historypath)
                motor_history_text += f"Motor ID: {motor_info[5]} -> {motor_id}\n"
            if distance != motor_info[6]:
                motor_history_text += f"Condition: {motor_info[6]} -> {condition}\n"
            if condition != motor_info[7]:
                motor_history_text += f"Distance Traveled: {motor_info[7]} -> {distance}\n"
            if price != motor_info[9]:
                motor_history_text += f"Price per hour: {motor_info[9]} -> {price}\n"

            with open(historypath, "a", encoding="utf-8") as history_file:
                history_file.write(f"**Adjusted at {datetime.now()}:")
                history_file.write(motor_history_text)
                history_file.write("-" * 20 + "\n")

            #Cập nhật hiển thị trên cây
            tree.item(selected_item, values=(number, name, brand, year, type, motor_id, condition, status, price))

            adjust_motor_window.destroy()

        button_adjust = tk.Button(adjust_motor_window, text="Adjust", command=adjust_motor)
        button_adjust.pack()

    def delete_motor():
        #Kiểm tra xem có hàng nào được chọn hay không
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a motor to delete.")
            return

        #Lấy thông tin từ hàng được chọn
        motor_info = tree.item(selected_item)['values']
        selected_motor_id = motor_info[5]

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this motor?")

        if confirm:
            tree.delete(selected_item)

            #Xóa dữ liệu xe máy trong file
            with open('./data/motor.csv', 'r+', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)

                #Tìm và xóa dòng chứa thông tin xe máy dựa trên motor_id
                for i in range(len(rows)):
                    if rows[i][5] == str(selected_motor_id):
                        del rows[i]
                        break

                #Cập nhật lại số thứ tự cho toàn bộ các hàng còn lại trong bảng và trong file
                for i in range(len(rows)):
                    rows[i][0] = str(i)

                file.seek(0)
                writer = csv.writer(file)
                writer.writerows(rows)
                file.truncate()
            if os.path.exists(f"./history/motor/{selected_motor_id}.txt"):
                os.remove( f"./history/motor/{selected_motor_id}.txt")

            messagebox.showinfo("Success", "Motor was deleted successfully.")

    def service_motor():
        #Kiểm tra xem có hàng nào được chọn hay không
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một xe máy để sửa chữa.")
            return

        motor_info = tree.item(selected_item)['values']
        selected_motor_id = motor_info[5]
        selected_status = motor_info[8]
        if selected_status == "Ready":
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to service this motor?")
            if confirm:
                with open('./data/motor.csv', 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    rows = list(reader)
                for i in range(len(rows)):
                    if rows[i][5] == str(selected_motor_id):
                        rows[i][8] = 'Serviced'
                        break
                #Ghi lại toàn bộ dữ liệu vào file
                with open('./data/motor.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
                #Cập nhật giá trị của cột 8 thành "serviced"
                tree.set(selected_item, column=8, value="Serviced")

                messagebox.showinfo("Success", "Motor was serviced successfully.")
                with open(f"./history/motor/{selected_motor_id}.txt", "a", encoding="utf-8") as history_file:
                    history_file.write(f"Adjusted at {datetime.now()}:\n")
                    history_file.write("Status: Ready -> Serviced\n")
                    history_file.write("-" * 20 + "\n")
        elif selected_status == "Serviced":
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to unservice this motor?")
            if confirm:
                with open('./data/motor.csv', 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    rows = list(reader)
                for i in range(len(rows)):
                    if rows[i][5] == str(selected_motor_id):
                        rows[i][8] = 'Ready'
                        break
                #Ghi lại toàn bộ dữ liệu vào file
                with open('./data/motor.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
                #Cập nhật giá trị của cột 8 thành "serviced"
                tree.set(selected_item, column=8, value="Ready")

                messagebox.showinfo("Success", "Motor was unserviced successfully.")
                with open(f"./history/motor/{selected_motor_id}.txt", "a", encoding="utf-8") as history_file:
                    history_file.write(f"Adjusted at {datetime.now()}:\n")
                    history_file.write("Status: Serviced -> Ready\n")
                    history_file.write("-" * 20 + "\n")
        else:
            messagebox.showwarning("Warning", "Rented motor is not able to be serviced!.")
    def open_search_motor_window():
        search_motor_window = tk.Toplevel()
        search_motor_window.title("Search")
        search_motor_window.geometry("1000x400")

        label_motor_id = tk.Label(search_motor_window, text="Motor ID:")
        label_motor_id.pack()
        entry_motor_id = tk.Entry(search_motor_window)
        entry_motor_id.pack()

        tree_search = ttk.Treeview(search_motor_window)
        tree_search['columns'] = ('Number', 'Name', 'Brand', 'Year', 'Type', 'Motor ID', 'Condition', 'Distance Traveled', 'Status',  'Price')

        tree_search.column("#0", width=0, stretch=tk.NO)
        tree_search.column("Number", anchor=tk.CENTER, width=50)
        tree_search.column("Name", anchor=tk.W, width=150)
        tree_search.column("Brand", anchor=tk.W, width=100)
        tree_search.column("Year", anchor=tk.W, width=100)
        tree_search.column("Type", anchor=tk.W, width=100)
        tree_search.column("Motor ID", anchor=tk.W, width=100)
        tree_search.column("Condition", anchor=tk.W, width=100)
        tree_search.column("Distance Traveled", anchor=tk.W, width=100)
        tree_search.column("Status", anchor=tk.W, width=100)
        tree_search.column("Price", anchor=tk.W, width=100)

        tree_search.heading("Number", text="No.")
        tree_search.heading("Name", text="Name")
        tree_search.heading("Brand", text="Brand")
        tree_search.heading("Year", text="Year")
        tree_search.heading("Type", text="Type")
        tree_search.heading("Motor ID", text="Motor ID")
        tree_search.heading("Condition", text="Condition")
        tree_search.heading("Distance Traveled", text="Distance Traveled")
        tree_search.heading("Status", text="Status")
        tree_search.heading("Price", text="Price per hour")

        def search_motor():
            motor_id = entry_motor_id.get()

            if not motor_id:
                messagebox.showerror("Error", "Please enter the Motor ID!")
                return

            found = False

            with open('./data/motor.csv', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row[5] == motor_id:
                        tree_search.delete(*tree_search.get_children())
                        tree_search.insert("", tk.END, values=row[:len(row) - 2])
                        found = True
                        break

            if not found:
                messagebox.showwarning("Warning", "Motor ID not found!")

        button_search = tk.Button(search_motor_window, text="Search", command=search_motor)
        button_search.pack()

        tree_search.pack()

    def open_sort_motor_window():
        sort_window = tk.Toplevel()
        sort_window.title("Sort")
        sort_window.geometry("600x400")

        label_sort_by = tk.Label(sort_window, text="Sort by:")
        label_sort_by.pack()
        combo_sort_by = ttk.Combobox(sort_window,
                                     values=["Name", "Brand", "Year", "Type", "Motor ID", "Condition", "Distance Traveled", "Status",
                                             "Price"],
                                     state="readonly")
        combo_sort_by.pack()

        label_sort_order = tk.Label(sort_window, text="Sort order:")
        label_sort_order.pack()
        combo_sort_order = ttk.Combobox(sort_window, values=["Ascending", "Descending"], state="readonly")
        combo_sort_order.pack()

        def confirm_sort():
            sort_by = combo_sort_by.get()
            sort_order = combo_sort_order.get()

            if not (sort_by and sort_order):
                messagebox.showerror("Error", "Please fill completely!")
                return

            with open('./data/motor.csv', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                rows = list(reader)

                if sort_by == "Name":
                    column_index = 1
                elif sort_by == "Brand":
                    column_index = 2
                elif sort_by == "Year":
                    column_index = 3
                elif sort_by == "Type":
                    column_index = 4
                elif sort_by == "Motor ID":
                    column_index = 5
                elif sort_by == "Condition":
                    column_index = 6
                elif sort_by == "Distance Traveled":
                    column_index = 7
                elif sort_by == "Status":
                    column_index = 8
                elif sort_by == "Price":
                    column_index = 9

                sorted_rows = sorted(rows, key=lambda x: x[column_index], reverse=(sort_order == "Descending"))

            sorted_window = tk.Toplevel()
            sorted_window.title("Sorted Motor List")
            sorted_window.geometry("1080x600")

            sorted_tree = ttk.Treeview(sorted_window)
            sorted_tree['columns'] = ('Number', 'Name', 'Brand', 'Year', 'Type', 'Motor ID','Condition', 'Distance Traveled', 'Status', 'Price')

            sorted_tree.column("#0", width=0, stretch=tk.NO)
            sorted_tree.column("Number", anchor=tk.CENTER, width=50)
            sorted_tree.column("Name", anchor=tk.W, width=150)
            sorted_tree.column("Brand", anchor=tk.W, width=100)
            sorted_tree.column("Year", anchor=tk.W, width=100)
            sorted_tree.column("Type", anchor=tk.W, width=100)
            sorted_tree.column("Motor ID", anchor=tk.W, width=100)
            sorted_tree.column("Condition", anchor=tk.W, width=100)
            sorted_tree.column("Distance Traveled", anchor=tk.W, width=100)
            sorted_tree.column("Status", anchor=tk.W, width=100)
            sorted_tree.column("Price", anchor=tk.W, width=100)

            sorted_tree.heading("Number", text="No.")
            sorted_tree.heading("Name", text="Name")
            sorted_tree.heading("Brand", text="Brand")
            sorted_tree.heading("Year", text="Year")
            sorted_tree.heading("Type", text="Type")
            sorted_tree.heading("Motor ID", text="Motor ID")
            sorted_tree.heading("Condition", text="Condition")
            sorted_tree.heading("Distance Traveled", text="Distance Traveled")
            sorted_tree.heading("Status", text="Status")
            sorted_tree.heading("Price", text="Price per hour")

            for row in sorted_rows:
                sorted_tree.insert("", tk.END, values=row[:len(row) - 2])

            sorted_tree.pack()

        button_confirm = tk.Button(sort_window, text="Confirm", command=confirm_sort)
        button_confirm.pack()

    def open_view_motor_window():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a motor to view.")
            return

        motor_info = tree.item(selected_item)['values']
        selected_motor_id = motor_info[5]

        def view_motor_history():
            def get_history_path(motor):
                with open('./data/motor.csv', 'r') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)
                    for row in csv_reader:
                        if row[5] == motor:
                            return row[11]
            historypath = get_history_path(str(selected_motor_id))

            #Tạo cửa sổ mới để hiển thị lịch sử
            history_window = tk.Toplevel()
            history_window.title("Motor History")

            #Tạo một Text widget để hiển thị nội dung của file
            text_widget = tk.Text(history_window)
            text_widget.pack(fill=tk.BOTH, expand=True)

            #Đọc nội dung từ file và hiển thị trong widget
            with open(historypath, "r", encoding="utf-8") as file:
                file_content = file.read()
                text_widget.insert(tk.END, file_content)

            #Thiết lập các thuộc tính của Text widget
            text_widget.configure(state="disabled")  #Không cho phép chỉnh sửa nội dung

        def view_motor_image():
            def get_image_path(motor):
                with open('./data/motor.csv', 'r') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)
                    for row in csv_reader:
                        if row[5] == motor:
                            return row[10]
                return None
            #Ép kiểu fix bug :v
            imagepath = get_image_path(str(selected_motor_id))
            if imagepath:
                view_image_window = tk.Toplevel()
                view_image_window.title("View Image")

                motor_image = Image.open(imagepath)
                motor_image = motor_image.resize((667, 375))
                motor_photo = ImageTk.PhotoImage(motor_image)

                image_display = tk.Label(view_image_window, image=motor_photo)
                image_display.image = motor_photo
                image_display.pack()
            else:
                tk.messagebox.showinfo("Error", "Image not found.")

        view_motor_window = tk.Toplevel()
        view_motor_window.title("View")

        view_history_button = tk.Button(view_motor_window, text="View History", command=view_motor_history)
        view_history_button.pack()

        view_image_button = tk.Button(view_motor_window, text="View Image", command=view_motor_image)
        view_image_button.pack()

    #Thêm các button chức năng
    button_frame = tk.Frame(motor_list_window, border=1, relief=tk.RAISED)
    button_frame.pack(pady=10)

    button_add = tk.Button(motor_list_window, text="Add", width=15, border=5, bg="#d7f9fa", font=('Cambria', 12, 'bold'), command=open_add_motor_window)
    button_add.pack(side="left", padx=5)

    button_delete = tk.Button(motor_list_window, text="Delete", width=15, bg="#d7f9fa", border=5, font=('Cambria', 12, 'bold'), command=delete_motor)
    button_delete.pack(side="left", padx=5)

    button_adjust = tk.Button(motor_list_window, text="Adjust", width=15, bg="#d7f9fa", border=5, font=('Cambria', 12, 'bold'), command=open_adjust_motor_window)
    button_adjust.pack(side="left", padx=5)

    button_search = tk.Button(motor_list_window, text="Search", width=15, bg="#d7f9fa", border=5, font=('Cambria', 12, 'bold'), command=open_search_motor_window)
    button_search.pack(side="left", padx=5)

    button_sort = tk.Button(motor_list_window, text="Sort", width=15, bg="#d7f9fa", border=5, font=('Cambria', 12, 'bold'), command=open_sort_motor_window)
    button_sort.pack(side="left", padx=5)

    button_service = tk.Button(motor_list_window, text="Service/Unservice", width=15, bg="#d7f9fa", border=5, font=('Cambria', 12, 'bold'), command=service_motor)
    button_service.pack(side="left", padx=5)

    button_view = tk.Button(motor_list_window, text="View", width=15, bg="#d7f9fa", font=('Cambria', 12, 'bold'), border=5, command=open_view_motor_window)
    button_view.pack(side="left", padx=5)
