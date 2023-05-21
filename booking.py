import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from PIL import Image, ImageTk
import csv
from datetime import datetime, timedelta
from motor import *
from schedule import *


def show_booking_list():
    now = datetime.now().replace(second=0, microsecond=0)
    booking_list_window = tk.Toplevel()
    booking_list_window.title("Booking")
    booking_list_window.geometry("1400x600")

    tree = ttk.Treeview(booking_list_window)
    tree['columns'] = ('Number', 'Booking ID', 'Customer ID', 'Motor ID', 'Book At', 'Start At', 'End At', 'Booking Time', 'Late Time', 'Status', 'Total')

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Number", anchor=tk.CENTER, width=50)
    tree.column("Booking ID", anchor=tk.W, width=100)
    tree.column("Customer ID", anchor=tk.W, width=100)
    tree.column("Motor ID", anchor=tk.W, width=100)
    tree.column("Book At", anchor=tk.W, width=150)
    tree.column("Start At", anchor=tk.W, width=150)
    tree.column("End At", anchor=tk.W, width=150)
    tree.column("Booking Time", anchor=tk.W, width=100)
    tree.column("Late Time", anchor=tk.W, width=100)
    tree.column("Status", anchor=tk.W, width=100)
    tree.column("Total", anchor=tk.W, width=100)

    tree.heading("Number", text="No.")
    tree.heading("Booking ID", text="Booking ID")
    tree.heading("Customer ID", text="Customer ID")
    tree.heading("Motor ID", text="Motor ID")
    tree.heading("Book At", text="Book At")
    tree.heading("Start At", text="Start At")
    tree.heading("End At", text="End At")
    tree.heading("Booking Time", text="Booking Time")
    tree.heading("Late Time", text="Late Time")
    tree.heading("Status", text="Status")
    tree.heading("Total", text="Total")

    with open('./data/booking.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            tree.insert("", tk.END, values=row[:len(row)-1])

    tree.pack()

    with open('./data/booking.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)  #Đọc dữ liệu thành danh sách

    for row in data[1:]:
        str_end_at = row[6]
        str_start_at = row[5]
        end_at = datetime.strptime(str_end_at, "%m/%d/%Y %H:%M")
        start_at = datetime.strptime(str_start_at, "%m/%d/%Y %H:%M")
        status = row[9]
        booking_id = row[1]
        customer_id = row[2]

        total = float(row[10])
        motor_id = row[3]
        pelnaty_rate = 1.2 #Phạt khi trả xe trễ
        booking_time = float(row[7])
        price = 0

        with open("./data/motor.csv", "r+", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for rows in reader:
                if rows[5] == motor_id:
                    price = float(rows[9])
                    break

        if start_at <= now and status == "Booking":
            row[9] = "Processing"
            row[10] = int(price) * booking_time

            #Cập nhật history
            motor_history_text = f"Status: {status} -> {row[9]}\n"
            motor_history_text += f"Total: {total} -> {row[10]}\n"

            with open(f"./history/motor/{motor_id}.txt", "a", encoding="utf-8") as history_file:
                history_file.write(f"**Auto updated for {booking_id} at {now}:\n")
                history_file.write(motor_history_text)
                history_file.write("-" * 20 + "\n")

            #Thay đổi trạng thái thành Rented
            with open('./data/motor.csv', 'r+', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if motor_id in row[5]:
                        row[8] = "Rented"
                        break
                #Ghi lại dữ liệu vào tệp
                file.seek(0)  #Đặt con trỏ của tệp về đầu tệp
                writer = csv.writer(file)
                writer.writerows(rows)
                file.truncate()  #Xoá dữ liệu cũ từ vị trí hiện tại

        if end_at < now and status in ["Processing", "Being Late"]:
            row[6] = now.strftime("%m/%d/%Y %H:%M")
            row[9] = "Being Late"
            row[8] = round((now - (start_at + timedelta(hours=float(booking_time)))).total_seconds()/3600,2)
            row[10] = total + price*pelnaty_rate*float(row[8])
            #Cập nhật history
            if status == "Processing":
                motor_history_text = f"Late time:0 -> {row[8]}\n"
                motor_history_text += f"Status: {status} -> {row[9]}\n"
                motor_history_text += f"Total: {total} -> {row[10]}\n"

                with open(f"./history/motor/{motor_id}.txt", "a", encoding="utf-8") as history_file:
                    history_file.write(f"**Auto updated for {booking_id} at {now}:\n")
                    history_file.write(motor_history_text)
                    history_file.write("-" * 20 + "\n")

    def write_data_to_file():
        #Ghi dữ liệu vào file (trừ dòng đầu)
        with open('./data/booking.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data[0])  # Ghi lại dòng đầu (header)
            writer.writerows(data[1:])  # Ghi lại dữ liệu từ dòng thứ hai trở đi

    def close_window():
        write_data_to_file()
        booking_list_window.destroy()

    booking_list_window.protocol("WM_DELETE_WINDOW", close_window)  #Kết nối nút clode với hàm close_window()

    def open_book_booking_window():
        # Add 1 booking, chỉ cần điền Customer ID, Motor ID, Start At, Booking Time, mấy kia tự cập nhật

        add_booking_window = tk.Toplevel()
        add_booking_window.title("Book")
        add_booking_window.geometry("400x400")

        def open_customer_selection_window():
            customer_selection_window = tk.Toplevel()
            customer_selection_window.title("Choosing Customer")
            customer_selection_window.geometry("600x400")

            customer_tree = ttk.Treeview(customer_selection_window)
            customer_tree['columns'] = ('Number', 'Name', 'Gender', 'Age', 'From', 'Customer ID', 'Address', 'Tel', 'Mail')

            customer_tree.column("#0", width=0, stretch=tk.NO)
            customer_tree.column("Number", anchor=tk.CENTER, width=50)
            customer_tree.column("Name", anchor=tk.W, width=150)
            customer_tree.column("Gender", anchor=tk.W, width=50)
            customer_tree.column("Age", anchor=tk.W, width=50)
            customer_tree.column("From", anchor=tk.W, width=100)
            customer_tree.column("Customer ID", anchor=tk.W, width=100)
            customer_tree.column("Address", anchor=tk.W, width=200)
            customer_tree.column("Tel", anchor=tk.W, width=100)
            customer_tree.column("Mail", anchor=tk.W, width=150)

            customer_tree.heading("Number", text="No.")
            customer_tree.heading("Name", text="Name")
            customer_tree.heading("Gender", text="Gender")
            customer_tree.heading("Age", text="Age")
            customer_tree.heading("From", text="From")
            customer_tree.heading("Customer ID", text="ID")
            customer_tree.heading("Address", text="Address")
            customer_tree.heading("Tel", text="Tel")
            customer_tree.heading("Mail", text="Mail")

            with open('./data/customer.csv', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Bỏ qua dòng tiêu đề trong file
                for row in reader:
                    customer_tree.insert("", tk.END, values=row[:len(row) - 1])

            customer_tree.pack()

            def select_customer():
                selected_item = customer_tree.selection()
                if selected_item:
                    customer_id = customer_tree.item(selected_item)['values'][5]
                    entry_customer_id.config(state="normal")
                    entry_customer_id.delete(0, tk.END)
                    entry_customer_id.insert(0, customer_id)
                    entry_customer_id.config(state='readonly')
                    customer_selection_window.destroy()
                else:
                    messagebox.showwarning("Warning", "Please select customer before confirming!")

            button_confirm = ttk.Button(customer_selection_window, text="Confirm", command=select_customer)
            button_confirm.pack()

        label_customer_id = tk.Label(add_booking_window, text="Customer ID:")
        label_customer_id.pack()
        entry_customer_id = tk.Entry(add_booking_window, state="readonly")
        entry_customer_id.pack()
        button_select_customer = ttk.Button(add_booking_window, text="Customer Options",
                                            command=open_customer_selection_window)
        button_select_customer.pack()

        def open_motor_selection_window():
            motor_selection_window = tk.Toplevel()
            motor_selection_window.title("Motor Options")
            motor_selection_window.geometry("600x400")

            motor_tree = ttk.Treeview(motor_selection_window)
            motor_tree['columns'] = ('Number', 'Name', 'Brand', 'Year', 'Type', 'Motor ID', 'Distance Traveled', 'Status', 'Condition', 'Price')

            motor_tree.column("#0", width=0, stretch=tk.NO)
            motor_tree.column("Number", anchor=tk.CENTER, width=50)
            motor_tree.column("Name", anchor=tk.W, width=150)
            motor_tree.column("Brand", anchor=tk.W, width=100)
            motor_tree.column("Year", anchor=tk.W, width=100)
            motor_tree.column("Type", anchor=tk.W, width=100)
            motor_tree.column("Motor ID", anchor=tk.W, width=100)
            motor_tree.column("Distance Traveled", anchor=tk.W, width=100)
            motor_tree.column("Condition", anchor=tk.W, width=100)
            motor_tree.column("Status", anchor=tk.W, width=100)
            motor_tree.column("Price", anchor=tk.W, width=100)

            motor_tree.heading("Number", text="No.")
            motor_tree.heading("Name", text="Name")
            motor_tree.heading("Brand", text="Brand")
            motor_tree.heading("Year", text="Year")
            motor_tree.heading("Type", text="Type")
            motor_tree.heading("Motor ID", text="Motor ID")
            motor_tree.heading("Distance Traveled", text="Distance Traveled")
            motor_tree.heading("Status", text="Status")
            motor_tree.heading("Condition", text="Condition")
            motor_tree.heading("Price", text="Price per hour")

            with open('./data/motor.csv', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    motor_tree.insert("", tk.END, values=row[:len(row) - 2])

            motor_tree.pack()

            def select_motor():
                selected_item = motor_tree.selection()
                if selected_item:
                    motor_id = motor_tree.item(selected_item)['values'][5]
                    motor_status = motor_tree.item(selected_item)['values'][7]
                    if motor_status == 'Serviced':
                        messagebox.showwarning("Warning", "Motor is under warranty. Please choose another motorcycle!")
                    else:
                        entry_motor_id.config(state="normal")
                        entry_motor_id.delete(0, tk.END)
                        entry_motor_id.insert(0, motor_id)
                        entry_motor_id.config(state='readonly')
                        motor_selection_window.destroy()
                else:
                    messagebox.showwarning("Warning", "Please select motor before confirming!")

            button_confirm = ttk.Button(motor_selection_window, text="Confirm", command=select_motor)
            button_confirm.pack()

        label_motor_id = tk.Label(add_booking_window, text="Motor ID:")
        label_motor_id.pack()
        entry_motor_id = tk.Entry(add_booking_window, state="readonly")
        entry_motor_id.pack()
        button_select_motor = ttk.Button(add_booking_window, text="Motor Options", command=open_motor_selection_window)
        button_select_motor.pack()

        def open_start_time_picker():
            time_picker_window = tk.Toplevel(add_booking_window)

            label_year = tk.Label(time_picker_window, text="Year:")
            label_year.grid(row=0, column=0)
            entry_year = tk.Entry(time_picker_window)
            entry_year.insert(0, now.year)
            entry_year.grid(row=0, column=1)

            label_month = tk.Label(time_picker_window, text="Month:")
            label_month.grid(row=0, column=2)
            entry_month = tk.Entry(time_picker_window)
            entry_month.insert(0, now.month)
            entry_month.grid(row=0, column=3)

            label_day = tk.Label(time_picker_window, text="Day:")
            label_day.grid(row=0, column=4)
            entry_day = tk.Entry(time_picker_window)
            entry_day.insert(0, now.day)
            entry_day.grid(row=0, column=5)

            label_hour = tk.Label(time_picker_window, text="Hour:")
            label_hour.grid(row=1, column=0)
            entry_hour = tk.Entry(time_picker_window)
            entry_hour.insert(0, now.hour)
            entry_hour.grid(row=1, column=1)

            label_minute = ttk.Label(time_picker_window, text="Minute:")
            label_minute.grid(row=1, column=2)
            combo_minute = ttk.Combobox(time_picker_window,
                                      values=["00", "15", "30", "45"],
                                      state="readonly")
            combo_minute.set("00")
            combo_minute.grid(row=1, column=3)

            def confirm_time():
                if not (entry_year.get() and entry_month.get() and entry_day.get() and combo_minute.get()):
                    messagebox.showerror("Error", "Please fill in the start time information!")
                    return
                start_time = datetime(int(entry_year.get()), int(entry_month.get()), int(entry_day.get()),
                                      int(entry_hour.get()), int(combo_minute.get()), 0)
                if start_time < now:
                    messagebox.showerror("Lỗi", "Invalid start time!")
                    return
                entry_start_at.config(state="normal")
                entry_start_at.delete(0, tk.END)
                entry_start_at.insert(0, start_time.strftime("%m/%d/%Y %H:%M:%S"))
                entry_start_at.config(state="readonly")
                time_picker_window.destroy()

            button_confirm = ttk.Button(time_picker_window, text="Confirm", command=confirm_time)
            button_confirm.grid(row=2, column=2, columnspan=3)

        label_start_at = ttk.Label(add_booking_window, text="Start at:")
        label_start_at.pack()
        entry_start_at = ttk.Entry(add_booking_window, state="readonly")
        entry_start_at.pack()
        button_open_time_picker = ttk.Button(add_booking_window, text="Time Options", command=open_start_time_picker)
        button_open_time_picker.pack()

        label_booking_time = ttk.Label(add_booking_window, text="Booking Time:")
        label_booking_time.pack()
        spinbox_booking_time = ttk.Spinbox(add_booking_window, from_=2, to=48, increment=0.5)
        spinbox_booking_time.pack()

        label_note = tk.Label(add_booking_window, text="Note:")
        label_note.pack()
        entry_note = tk.Text(add_booking_window, width=50, height=5)
        entry_note.pack()

        def add_booking():
            customer_id = entry_customer_id.get()
            motor_id = entry_motor_id.get()
            start_time = datetime.strptime(entry_start_at.get(), "%m/%d/%Y %H:%M:%S")
            start_at = start_time.strftime("%m/%d/%Y %H:%M")
            booking_time = spinbox_booking_time.get()
            note = entry_note.get("1.0", "end-1c")

            #Check fill completely
            if not (customer_id and motor_id and start_at and booking_time):
                messagebox.showerror("Error", "Please fill in the booking information completely!")
                return

            book_at = now.strftime("%m/%d/%Y %H:%M")

            #Tạo Booking_ID
            if now.hour < 12:
                session = "M"
            elif now.hour < 18:
                session = "A"
            else:
                session = "E"
            date_format = now.strftime("%d%m%y")
            count_booking = 0
            with open("./data/booking.csv", "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    datetime_str = row[4]  # Lấy dữ liệu từ cột 4
                    booking_datetime = datetime.strptime(datetime_str, "%m/%d/%Y %H:%M")
                    if booking_datetime.date() == now.date():
                        count_booking += 1
            booking_id = session + date_format + "." + str(count_booking + 1)

            #Convert từ string về datetime :v hay qá
            end_time =start_time + timedelta(hours=float(booking_time))
            end_at = end_time.strftime("%m/%d/%Y %H:%M")

            late_time = 0
            #Cập nhật total (cọc tiền trước khi thuê xe)
            deposit_rate = 0.5 # Tỉ lệ cọc
            price = 0
            with open('./data/motor.csv', "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row[5] == motor_id:
                        price = float(row[9])
                        break
            total = deposit_rate*price*float(booking_time)
            status = "Booking"
            note_path = f"./note/{booking_id}.txt"
            next_index = len(data)

            if add_schedule(motor_id, booking_id, start_at, end_at) == 0:
                messagebox.showerror("Error", f"Motor was booked around this time!")
                return


            #Thao tác note
            try:
                with open(note_path, "w", encoding="utf-8") as file:
                    file.write(note)
                messagebox.showinfo("Information", f"Notes have been saved to {booking_id}.txt file successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving notes to file {booking_id}.txt: {str(e)}") #In lỗi file

            tree.insert("", tk.END, values=(next_index, booking_id, customer_id, motor_id, book_at, start_at, end_at, booking_time,  late_time, status, total))
            data.append((next_index, booking_id, customer_id, motor_id, book_at, start_at, end_at, booking_time, late_time, status, total, note_path))
            #Lưu thông tin chỉnh sửa vào file historypath

            motor_history_text = f"Customer ID: {customer_id}\n"
            motor_history_text += f"Start at: {start_at}\n"
            motor_history_text += f"End at: {end_at}\n"
            motor_history_text += f"Booking time: {booking_time}\n"
            motor_history_text += f"Late time: {late_time}\n"
            motor_history_text += f"Status: {status}\n"
            motor_history_text += f"Total: {total}\n"

            with open(f"./history/motor/{motor_id}.txt", "a", encoding="utf-8") as history_file:
                history_file.write(f"**Booked for {booking_id} at {now}:\n")
                history_file.write(motor_history_text)
                history_file.write("-" * 20 + "\n")

            add_booking_window.destroy()

        button_add = ttk.Button(add_booking_window, text="Add", command=add_booking)
        button_add.pack()

    def open_update_booking_window():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a booking to update.")
            return
        booking_info = tree.item(selected_item)['values']
        selected_booking_id = booking_info[1]
        selected_booking_status = booking_info[9]
        selected_motor_id = booking_info[3]
        if selected_booking_status in ["Failed-Unbook", "Failed-Delete"]:
            messagebox.showerror("Error", "Cannot update a canceled booking!")
            return
        elif selected_booking_status == "Completed":
            messagebox.showerror("Error", "Cannot update a completed booking!")
            return
        update_booking_window = tk.Toplevel()
        update_booking_window.title("Update")
        update_booking_window.geometry("400x400")

        if selected_booking_status in ["Processing", "Being Late"]:
            label_status = tk.Label(update_booking_window, text="Updated Status:")
            label_status.pack()
            entry_status = tk.Entry(update_booking_window)
            entry_status.pack()
            entry_status.insert(0, "Completed")
            entry_status.config(state="disabled")

            label_distance = tk.Label(update_booking_window, text="Distance:")
            label_distance.pack()
            spinbox_distance = tk.Spinbox(update_booking_window, from_=500, to=20000)
            spinbox_distance.pack()

            with open(f'./note/{selected_booking_id}.txt', "r", encoding="utf-8") as file:
                note_content = file.read()

            label_note = tk.Label(update_booking_window, text="Note:")
            label_note.pack()
            entry_note = tk.Text(update_booking_window, width=50, height=5)
            entry_note.insert("1.0", note_content)
            entry_note.pack()
        elif selected_booking_status == "Booking":

            label_status = tk.Label(update_booking_window, text="Updated Status:")
            label_status.pack()
            entry_status = tk.Entry(update_booking_window)
            entry_status.pack()
            entry_status.insert(0, "Booking")
            entry_status.config(state="disabled")

            def open_start_time_picker():
                time_picker_window = tk.Toplevel(update_booking_window)
                label_year = tk.Label(time_picker_window, text="Year:")
                label_year.grid(row=0, column=0)
                entry_year = tk.Entry(time_picker_window)
                entry_year.insert(0, now.year)
                entry_year.grid(row=0, column=1)

                label_month = tk.Label(time_picker_window, text="Month:")
                label_month.grid(row=0, column=2)
                entry_month = tk.Entry(time_picker_window)
                entry_month.insert(0, now.month)
                entry_month.grid(row=0, column=3)

                label_day = tk.Label(time_picker_window, text="Day:")
                label_day.grid(row=0, column=4)
                entry_day = tk.Entry(time_picker_window)
                entry_day.insert(0, now.day)
                entry_day.grid(row=0, column=5)

                label_hour = tk.Label(time_picker_window, text="Hour:")
                label_hour.grid(row=1, column=0)
                entry_hour = tk.Entry(time_picker_window)
                entry_hour.insert(0, now.hour)
                entry_hour.grid(row=1, column=1)

                label_minute = tk.Label(time_picker_window, text="Minute:")
                label_minute.grid(row=1, column=2)
                combo_minute = ttk.Combobox(time_picker_window,
                                            values=["00", "15", "30", "45"],
                                            state="readonly")
                combo_minute.set("00")
                combo_minute.grid(row=1, column=3)
                def confirm_time():
                    if not (entry_year.get() and entry_month.get() and entry_day.get() and combo_minute.get()):
                        messagebox.showerror("Error", "Please fill in the start time information!")
                        return
                    start_time = datetime(int(entry_year.get()), int(entry_month.get()), int(entry_day.get()),
                                          int(entry_hour.get()), int(combo_minute.get()), 0)
                    if start_time < now:
                        messagebox.showerror("Error", "Invalid start time!")
                        return
                    entry_start_at.config(state="normal")
                    entry_start_at.delete(0, tk.END)
                    entry_start_at.insert(0, start_time.strftime("%m/%d/%Y %H:%M:%S"))
                    entry_start_at.config(state="readonly")
                    time_picker_window.destroy()
                button_confirm = ttk.Button(time_picker_window, text="Confirm", command=confirm_time)
                button_confirm.grid(row=2, column=2, columnspan=3)
            label_start_at = ttk.Label(update_booking_window, text="Start at:")
            label_start_at.pack()
            entry_start_at = ttk.Entry(update_booking_window, state="readonly")
            entry_start_at.pack()
            button_open_time_picker = ttk.Button(update_booking_window, text="Time Options", command=open_start_time_picker)
            button_open_time_picker.pack()

            label_booking_time = ttk.Label(update_booking_window, text="Booking Time:")
            label_booking_time.pack()
            spinbox_booking_time = ttk.Spinbox(update_booking_window, from_=2, to=48, increment=0.5)
            spinbox_booking_time.pack()

            with open(f'./note/{selected_booking_id}.txt', "r", encoding="utf-8") as file:
                note_content = file.read()

            label_note = tk.Label(update_booking_window, text="Note:")
            label_note.pack()
            entry_note = tk.Text(update_booking_window, width=50, height=5)
            entry_note.insert("1.0", note_content)
            entry_note.pack()
        def confirm_booking_status():
            status = entry_status.get()
            note = entry_note.get("1.0", "end-1c")
            if selected_booking_status == "Booking":
                start_time = datetime.strptime(entry_start_at.get(), "%m/%d/%Y %H:%M:%S")
                start_at = start_time.strftime("%m/%d/%Y %H:%M")
                booking_time = spinbox_booking_time.get()
            elif selected_booking_status in ["Processing", "Being Late"]:
                distance = spinbox_distance.get()
            for row in data[1:]:
                if row[1] == selected_booking_id:
                    row[9] = status
                    if selected_booking_status == "Booking":
                        row[5] = start_at
                        row[7] = booking_time
                        motor_history_text = f"Start at: {booking_info[5]} -> {start_at}\n"
                        motor_history_text += f"Booking Time: {booking_info[7]} -> {booking_time}\n"
                        motor_history_text += f"Status: {booking_info[9]} -> Booking\n"

                        with open(f"./history/motor/{motor_id}.txt", "a", encoding="utf-8") as history_file:
                            history_file.write(f"**Updated for {selected_booking_id} at {now}:\n")
                            history_file.write(motor_history_text)
                            history_file.write("-" * 20 + "\n")
                    elif selected_booking_status in ["Processing", "Being Late"]:
                        updated_rows = []  # Danh sách chứa các hàng đã được thay đổi

                        with open('./data/motor.csv', "r", newline="", encoding="utf-8") as file:
                            reader = csv.reader(file)
                            for row in reader:
                                if row[5] == selected_motor_id:
                                    row[7] = str(int(row[7]) + int(distance)) #Cộng distance vào phần tử thứ 6
                                    row[8] = "Ready"
                                updated_rows.append(row)  #Thêm hàng đã được thay đổi vào danh sách

                        with open('./data/motor.csv', 'w', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerows(updated_rows)

                            motor_history_text = f"Distance:{int(row[7]) - int(distance)} -> {int(row[7])}\n"
                            motor_history_text += f"Status: Rented -> Ready\n"
                            with open(f"./history/motor/{selected_motor_id}.txt", "a", encoding="utf-8") as history_file:
                                history_file.write(f"**Completed {selected_booking_id} at {now}:\n")
                                history_file.write(f"**Adjusted at {now}:\n")
                                history_file.write(motor_history_text)
                                history_file.write("-" * 20 + "\n")
                    break
            with open('./data/booking.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)

            with open(f'./note/{selected_booking_id}.txt', "w", encoding="utf-8") as file:
                file.write(note)

            if note != note_content:
                motor_history_text = f"Note has just been adjusted"

                with open(f"./history/motor/{motor_id}.txt", "a", encoding="utf-8") as history_file:
                    history_file.write(f"**Updated for {selected_booking_id} at {now}:\n")
                    history_file.write(motor_history_text)
                    history_file.write("-" * 20 + "\n")

            update_booking_window.destroy()

        button_confirm = ttk.Button(update_booking_window, text="Confirm", width=25, command=confirm_booking_status)
        button_confirm.pack()
    def cancel_booking():
        pass
    def open_search_booking_window():
        pass
    def open_sort_booking_window():
        pass
    def open_view_booking_window():
        pass
    def refresh_booking_list():
        write_data_to_file()
        booking_list_window.destroy()
        show_booking_list()

    # Thêm các button chức năng
    button_frame = tk.Frame(booking_list_window)
    button_frame.pack(pady=10)

    button_book = ttk.Button(booking_list_window, text="Book", width=25, command=open_book_booking_window)        #Add 1 booking, chỉ cần điền Booking ID, Customer ID, Book At, Start At, Booking Time, mấy kia tự cập nhật
    button_book.pack(side="left", padx=5)

    button_update = ttk.Button(booking_list_window, text="Update", width=25, command=open_update_booking_window)    #Chỉ có thể update status và note của Booking
    button_update.pack(side="left", padx=5)

    button_cancel = ttk.Button(booking_list_window, text="Cancel", width=25, command=cancel_booking)
    button_cancel.pack(side="left", padx=5)

    button_search = ttk.Button(booking_list_window, text="Search", width=25, command=open_search_booking_window)
    button_search.pack(side="left", padx=5)

    button_sort = ttk.Button(booking_list_window, text="Sort", width=25, command=open_sort_booking_window)
    button_sort.pack(side="left", padx=5)

    button_view = ttk.Button(booking_list_window, text="View", width=25, command=open_view_booking_window)        #Xem note_path của mỗi Booking
    button_view.pack(side="left", padx=5)

    button_refresh = ttk.Button(booking_list_window, text="Refresh", width=25, command=refresh_booking_list)
    button_refresh.pack(side="left", padx=5)
