import csv
from datetime import datetime, timedelta
import os
import ast

def time_conv(time_str):
    datetime_obj = datetime.strptime(time_str, "%H:%M")
    time_obj = datetime_obj.time()
    return time_obj


def dmy_conv(dmy_str):
    datetime_obj = datetime.strptime(dmy_str, "%m/%d/%Y")
    dmy_str = datetime_obj.date()
    return dmy_str

def add_schedule(motor_id, booking_id, start_at, end_at):
    def check_schedule(stime, etime, time_list):
        if time_list == []:
            return True
        stime = time_conv(stime)
        etime = time_conv(etime)
        for i in time_list:
            for j in range(2):
                if (time_conv(i[0]) <= stime < time_conv(i[1])) or (time_conv(i[0]) < etime <= time_conv(i[1])) or (
                        stime <= time_conv(i[0]) < etime) or (stime < time_conv(i[1]) <= etime):
                    return False
        return True
    def write_file(motor_id_exists, check_file, schedule_name, header, new_data):
        if not motor_id_exists:
            file_mode = 'a'
            if not check_file:
                with open(schedule_name, mode=file_mode, newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerow(new_data)
            else:
                with open(schedule_name, mode=file_mode, newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(new_data)
        else:
            file_mode = 'w'
            with open(schedule_name, mode=file_mode, newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerow(new_data)

    sdmy = start_at.split(" ")[0]
    edmy = end_at.split(" ")[0]
    stime = start_at.split(" ")[1]
    etime = end_at.split(" ")[1]
    if dmy_conv(sdmy) < dmy_conv(edmy):
        etime = "23:59"
        gap_day = dmy_conv(sdmy) + timedelta(days=1)
        new_start_at = gap_day.strftime("%m/%d/%Y") + " " + "0:00"
        add_schedule(motor_id, booking_id, new_start_at, end_at)

    schedule_name = f'./schedule/{dmy_conv(sdmy).strftime("%d%m%y")}.csv'
    header = ['Motor ID', 'Time and Booking ID']
    motor_id_exists = False
    check_file = os.path.isfile(schedule_name)

    time_list = []

    if check_file:  # Kiểm tra file chưa tồn tại
        with open(schedule_name, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 0 and row[0] == str(motor_id):
                    motor_id_exists = True
                    time_list += [ast.literal_eval(item) for item in row[1:]]
                    break
    time = [stime, etime, booking_id]
    if check_schedule(stime, etime, time_list):
        time_list.append(time)
        time_list = sorted(time_list, key=lambda x: time_conv(x[0]))
        new_data = [motor_id] + time_list
        write_file(motor_id_exists, check_file, schedule_name, header, new_data)
        return 1
    else:

        return 0

