import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from PIL import Image, ImageTk
import csv
import os


def show_customer_list():
    customer_list_window = tk.Toplevel()
    customer_list_window.title("Customer")
    customer_list_window.geometry("1000x600")

    tree = ttk.Treeview(customer_list_window)
    tree['columns'] = ('Number', 'Name', 'Gender', 'Age', 'From', 'Customer ID', 'Address', 'Tel', 'Mail')

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Number", anchor=tk.CENTER, width=50)
    tree.column("Name", anchor=tk.W, width=150)
    tree.column("Gender", anchor=tk.W, width=50)
    tree.column("Age", anchor=tk.W, width=50)
    tree.column("From", anchor=tk.W, width=100)
    tree.column("Customer ID", anchor=tk.W, width=100)
    tree.column("Address", anchor=tk.W, width=200)
    tree.column("Tel", anchor=tk.W, width=100)
    tree.column("Mail", anchor=tk.W, width=150)

    tree.heading("Number", text="No.")
    tree.heading("Name", text="Name")
    tree.heading("Gender", text="Gender")
    tree.heading("Age", text="Age")
    tree.heading("From", text="From")
    tree.heading("Customer ID", text="ID")
    tree.heading("Address", text="Address")
    tree.heading("Tel", text="Tel")
    tree.heading("Mail", text="Mail")

    with open('./data/customer.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            tree.insert("", tk.END, values=row[:len(row) - 1])

    tree.pack()

    def open_add_customer_window():
        add_customer_window = tk.Toplevel()
        add_customer_window.title("Add")
        add_customer_window.geometry("400x400")

        label_name = ttk.Label(add_customer_window, text="Name:")
        label_name.pack()
        entry_name = ttk.Entry(add_customer_window)
        entry_name.pack()

        label_gender = ttk.Label(add_customer_window, text="Gender:")
        label_gender.pack()
        combo_gender = ttk.Combobox(add_customer_window, values=["M", "F"], state="readonly")
        combo_gender.pack()

        label_age = ttk.Label(add_customer_window, text="Age:")
        label_age.pack()
        spinbox_age = ttk.Spinbox(add_customer_window, from_=15, to=90)
        spinbox_age.pack()

        label_from = ttk.Label(add_customer_window, text="From:")
        label_from.pack()
        combo_from= ttk.Combobox(add_customer_window,
                                  values=["Local", "Other Localities", "Foreign"],
                                  state="readonly")
        combo_from.pack()

        label_id = ttk.Label(add_customer_window, text="Customer ID:")
        label_id.pack()
        entry_id = ttk.Entry(add_customer_window)
        entry_id.pack()

        label_address = ttk.Label(add_customer_window, text="Address:")
        label_address .pack()
        entry_address = ttk.Entry(add_customer_window)
        entry_address.pack()

        label_tel = ttk.Label(add_customer_window, text="Tel:")
        label_tel.pack()
        entry_tel = ttk.Entry(add_customer_window)
        entry_tel.pack()

        label_mail = ttk.Label(add_customer_window, text="Mail:")
        label_mail.pack()
        entry_mail = ttk.Entry(add_customer_window)
        entry_mail.pack()

        label_doc = ttk.Label(add_customer_window, text="Doc Path:")
        label_doc.pack()
        entry_doc = ttk.Entry(add_customer_window)
        entry_doc.pack()

        def add_customer():
            name = entry_name.get()
            gender = combo_gender.get()
            age = spinbox_age.get()
            comefrom = combo_from.get()
            customer_id = entry_id.get()
            address = entry_address.get()
            tel = entry_tel.get()
            mail = entry_mail.get()
            docpath = entry_doc.get()

            if not (name and gender and age and comefrom and customer_id and address and tel and mail and docpath):
                messagebox.showerror("Error", "Please fill in the customer information completely!")
                return

            # Thêm thông tin motor mới vào file
            with open('./data/customer.csv', 'r+', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)
                next_index = len(rows)

                writer = csv.writer(file)
                writer.writerow([next_index] + [name, gender, age, comefrom, customer_id, address, tel, mail, docpath])

            tree.insert("", tk.END, values=(next_index, name, gender, age, comefrom, customer_id, address, tel, mail))

            add_customer_window.destroy()

        button_add = ttk.Button(add_customer_window, text="Add", command=add_customer)
        button_add.pack()

    def open_adjust_customer_window():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a motor to adjust.")
            return

        customer_info = tree.item(selected_item)['values']
        selected_customer_id = customer_info[5]
        number = customer_info[0]

        adjust_customer_window = tk.Toplevel()
        adjust_customer_window.title("Adjust")
        adjust_customer_window.geometry("400x400")

        label_name = ttk.Label(adjust_customer_window, text="Name:")
        label_name.pack()
        entry_name = ttk.Entry(adjust_customer_window)
        entry_name.insert(0, customer_info[1])
        entry_name.pack()

        label_gender = ttk.Label(adjust_customer_window, text="Gender:")
        label_gender.pack()
        combo_gender = ttk.Combobox(adjust_customer_window, values=["M", "F"], state="readonly")
        combo_gender.set(customer_info[2])
        combo_gender.pack()

        label_age = ttk.Label(adjust_customer_window, text="Age:")
        label_age.pack()
        spinbox_age = ttk.Spinbox(adjust_customer_window, from_=15, to=90)
        spinbox_age.set(customer_info[3])
        spinbox_age.pack()

        label_from = ttk.Label(adjust_customer_window, text="From:")
        label_from.pack()
        combo_from = ttk.Combobox(adjust_customer_window,
                                  values=["Local", "Other Localities", "Foreign"],
                                  state="readonly")
        combo_from.set(customer_info[4])
        combo_from.pack()

        label_id = ttk.Label(adjust_customer_window, text="Customer ID:")
        label_id.pack()
        entry_id = ttk.Entry(adjust_customer_window)
        entry_id.insert(0, customer_info[5])
        entry_id.pack()

        label_address = ttk.Label(adjust_customer_window, text="Address:")
        label_address.pack()
        entry_address = ttk.Entry(adjust_customer_window)
        entry_address.insert(0, customer_info[6])
        entry_address.pack()

        label_tel = ttk.Label(adjust_customer_window, text="Tel:")
        label_tel.pack()
        entry_tel = ttk.Entry(adjust_customer_window)
        entry_tel.insert(0, customer_info[7])
        entry_tel.pack()

        label_mail = ttk.Label(adjust_customer_window, text="Mail:")
        label_mail.pack()
        entry_mail = ttk.Entry(adjust_customer_window)
        entry_mail.insert(0, customer_info[8])
        entry_mail.pack()

        with open('./data/customer.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

            label_doc = ttk.Label(adjust_customer_window, text="Doc Path:")
            label_doc.pack()
            entry_doc = ttk.Entry(adjust_customer_window)
            entry_doc.insert(0, rows[int(number)][9])
            entry_doc.pack()

        def adjust_customer():
            name = entry_name.get()
            gender = combo_gender.get()
            age = spinbox_age.get()
            comefrom = combo_from.get()
            customer_id = entry_id.get()
            address = entry_address.get()
            tel = entry_tel.get()
            mail = entry_mail.get()
            docpath = entry_doc.get()

            if not (name and gender and age and comefrom and customer_id and address and tel and mail and docpath):
                messagebox.showerror("Error", "Please fill in the customer information completely!")
                return

            with open('./data/customer.csv', 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)

            for i in range(len(rows)):
                if rows[i][5] == str(selected_customer_id):
                    rows[i][1] = name
                    rows[i][2] = gender
                    rows[i][3] = age
                    rows[i][4] = comefrom
                    rows[i][5] = customer_id
                    rows[i][6] = address
                    rows[i][7] = tel
                    rows[i][8] = mail
                    rows[i][9] = docpath
                    break

            #Ghi lại toàn bộ dữ liệu vào file
            with open('./data/customer.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            #Cập nhật hiển thị trên cây
            tree.item(selected_item, values=(number, name, gender, age, comefrom, customer_id, address, tel, mail))

            adjust_customer_window.destroy()

        button_adjust = ttk.Button(adjust_customer_window, text="Adjust", command=adjust_customer)
        button_adjust.pack()

    def delete_customer():
        #Kiểm tra xem có hàng nào được chọn hay không
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a customer to delete.")
            return

        #Lấy thông tin từ hàng được chọn
        customer_info = tree.item(selected_item)['values']
        selected_customer_id = customer_info[5]

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?")

        if confirm:
            tree.delete(selected_item)

            #Xóa dữ liệu xe máy trong file
            with open('./data/customer.csv', 'r+', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)

                #Tìm và xóa dòng chứa thông tin xe máy dựa trên motor_id
                for i in range(len(rows)):
                    if rows[i][5] == str(selected_customer_id):
                        del rows[i]
                        break

                #Cập nhật lại số thứ tự cho toàn bộ các hàng còn lại trong bảng và trong file
                for i in range(len(rows)):
                    rows[i][0] = str(i)

                file.seek(0)
                writer = csv.writer(file)
                writer.writerows(rows)
                file.truncate()

            messagebox.showinfo("Success", "Customer was deleted successfully.")

    def open_search_customer_window():
        search_customer_window = tk.Toplevel()
        search_customer_window.title("Search")
        search_customer_window.geometry("1000x400")

        label_customer_id = ttk.Label(search_customer_window, text="Customer ID:")
        label_customer_id.pack()
        entry_customer_id = ttk.Entry(search_customer_window)
        entry_customer_id.pack()

        tree_search = ttk.Treeview(search_customer_window)
        tree_search['columns'] = ('Number', 'Name', 'Gender', 'Age', 'From', 'Customer ID', 'Address', 'Tel', 'Mail')

        tree_search.column("#0", width=0, stretch=tk.NO)
        tree_search.column("Number", anchor=tk.CENTER, width=50)
        tree_search.column("Name", anchor=tk.W, width=150)
        tree_search.column("Gender", anchor=tk.W, width=50)
        tree_search.column("Age", anchor=tk.W, width=50)
        tree_search.column("From", anchor=tk.W, width=100)
        tree_search.column("Customer ID", anchor=tk.W, width=100)
        tree_search.column("Address", anchor=tk.W, width=200)
        tree_search.column("Tel", anchor=tk.W, width=100)
        tree_search.column("Mail", anchor=tk.W, width=150)

        tree_search.heading("Number", text="No.")
        tree_search.heading("Name", text="Name")
        tree_search.heading("Gender", text="Gender")
        tree_search.heading("Age", text="Age")
        tree_search.heading("From", text="From")
        tree_search.heading("Customer ID", text="ID")
        tree_search.heading("Address", text="Address")
        tree_search.heading("Tel", text="Tel")
        tree_search.heading("Mail", text="Mail")

        def search_customer():
            customer_id = entry_customer_id.get()

            if not customer_id:
                messagebox.showwarning("Warning", "Please enter the Customer ID!")
                return

            found = False

            with open('./data/customer.csv', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row[5] == customer_id:
                        tree_search.delete(*tree_search.get_children())
                        tree_search.insert("", tk.END, values=row[:len(row) - 1])
                        found = True
                        break

            if not found:
                messagebox.showerror("Error", "Customer ID not found!")

        button_search = ttk.Button(search_customer_window, text="Search", command=search_customer)
        button_search.pack()

        tree_search.pack()
    def open_sort_customer_window():
        sort_window = tk.Toplevel()
        sort_window.title("Sort")
        sort_window.geometry("400x400")

        label_sort_by = ttk.Label(sort_window, text="Sort by:")
        label_sort_by.pack()
        combo_sort_by = ttk.Combobox(sort_window,
                                     values=["Name", "Gender", "Age", "From", "Customer ID", "Address", "Tel",
                                             "Mail"],
                                     state="readonly")
        combo_sort_by.pack()

        label_sort_order = ttk.Label(sort_window, text="Sort order:")
        label_sort_order.pack()
        combo_sort_order = ttk.Combobox(sort_window, values=["Ascending", "Descending"], state="readonly")
        combo_sort_order.pack()

        def confirm_sort():
            sort_by = combo_sort_by.get()
            sort_order = combo_sort_order.get()

            if not (sort_by and sort_order):
                messagebox.showerror("Error", "Please fill completely!")
                return

            with open('./data/customer.csv', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                rows = list(reader)

                if sort_by == "Name":
                    column_index = 1
                elif sort_by == "Gender":
                    column_index = 2
                elif sort_by == "Age":
                    column_index = 3
                elif sort_by == "From":
                    column_index = 4
                elif sort_by == "Customer ID":
                    column_index = 5
                elif sort_by == "Address":
                    column_index = 6
                elif sort_by == "Tel":
                    column_index = 7
                elif sort_by == "Mail":
                    column_index = 8

                sorted_rows = sorted(rows, key=lambda x: x[column_index], reverse=(sort_order == "Descending"))

            sorted_window = tk.Toplevel()
            sorted_window.title("Sorted Customer List")
            sorted_window.geometry("1000x600")

            sorted_tree = ttk.Treeview(sorted_window)
            sorted_tree['columns'] = ('Number', 'Name', 'Gender', 'Age', 'From', 'Customer ID', 'Address', 'Tel', 'Mail')

            sorted_tree.column("#0", width=0, stretch=tk.NO)
            sorted_tree.column("Number", anchor=tk.CENTER, width=50)
            sorted_tree.column("Name", anchor=tk.W, width=150)
            sorted_tree.column("Gender", anchor=tk.W, width=50)
            sorted_tree.column("Age", anchor=tk.W, width=50)
            sorted_tree.column("From", anchor=tk.W, width=100)
            sorted_tree.column("Customer ID", anchor=tk.W, width=100)
            sorted_tree.column("Address", anchor=tk.W, width=200)
            sorted_tree.column("Tel", anchor=tk.W, width=100)
            sorted_tree.column("Mail", anchor=tk.W, width=150)

            sorted_tree.heading("Number", text="No.")
            sorted_tree.heading("Name", text="Name")
            sorted_tree.heading("Gender", text="Gender")
            sorted_tree.heading("Age", text="Age")
            sorted_tree.heading("From", text="From")
            sorted_tree.heading("Customer ID", text="ID")
            sorted_tree.heading("Address", text="Address")
            sorted_tree.heading("Tel", text="Tel")
            sorted_tree.heading("Mail", text="Mail")

            for row in sorted_rows:
                sorted_tree.insert("", tk.END, values=row[:len(row) - 1])

            sorted_tree.pack()

        button_confirm = ttk.Button(sort_window, text="Confirm", command=confirm_sort)
        button_confirm.pack()

    def open_view_customer_window():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a customer to view.")
            return

        customer_info = tree.item(selected_item)['values']
        selected_customer_id = customer_info[5]

        def view_customer_history():
            pass

        def view_customer_doc():
            def get_doc_path(customer):
                with open('./data/customer.csv', 'r') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)
                    for row in csv_reader:
                        if row[5] == str(customer):
                            return row[9]
                return None

            #docpath = "D:\Materials\Project\Student\doc\doc1.pdf"
            try:
                docpath = get_doc_path(selected_customer_id)
                #lệnh hệ thôống mở file pdf trên window
                os.startfile(docpath)
            except OSError:
                messagebox.showerror("Error", "Invalid Document Path!")

        view_customer_window = tk.Toplevel()
        view_customer_window.title("View")

        view_history_button = tk.Button(view_customer_window, text="View History", command=view_customer_history)
        view_history_button.pack()

        view_doc_button = tk.Button(view_customer_window, text="View Doc", command=view_customer_doc)
        view_doc_button.pack()

    #Thêm các button chức năng
    button_frame = tk.Frame(customer_list_window)
    button_frame.pack(pady=10)

    button_add = ttk.Button(customer_list_window, text="Add", width=25, command=open_add_customer_window)
    button_add.pack(side="left", padx=5)

    button_delete = ttk.Button(customer_list_window, text="Delete", width=25, command=delete_customer)
    button_delete.pack(side="left", padx=5)

    button_adjust = ttk.Button(customer_list_window, text="Adjust", width=25, command=open_adjust_customer_window)
    button_adjust.pack(side="left", padx=5)

    button_search = ttk.Button(customer_list_window, text="Search", width=25, command=open_search_customer_window)
    button_search.pack(side="left", padx=5)

    button_sort = ttk.Button(customer_list_window, text="Sort", width=25, command=open_sort_customer_window)
    button_sort.pack(side="left", padx=5)

    button_view = tk.Button(customer_list_window, text="View", width=25, command=open_view_customer_window)
    button_view.pack(side="left", padx=5)