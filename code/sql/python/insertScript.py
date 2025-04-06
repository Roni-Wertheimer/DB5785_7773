import random
import datetime

# פונקציה ליצירת תאריכים רנדומליים
def random_date(start_year=2022, end_year=2025):
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + datetime.timedelta(days=random_days)

# יצירת נתונים עבור Housekeeping
def create_housekeeping_data():
    housekeeping_data = []
    for task_id in range(1, 401):
        task_date = random_date()
        status = random.choice(["Pending", "In Progress", "Completed"])
        room_id = random.randint(1, 400)
        housekeeping_data.append((task_id, task_date, status, room_id))
    return housekeeping_data

# יצירת נתונים עבור MaintenanceRequest
def create_maintenance_request_data():
    maintenance_request_data = []
    for request_id in range(1, 401):
        issue_description = "Issue " + str(request_id)
        request_date = random_date()
        status = random.choice(["Pending", "In Progress", "Completed"])
        room_id = random.randint(1, 400)
        maintenance_request_data.append((request_id, issue_description, request_date, status, room_id))
    return maintenance_request_data

# יצירת נתונים עבור AssignKeepingStaff
def create_assign_keeping_staff_data():
    assign_keeping_staff_data = []
    for task_id in range(1, 401):
        staff_id = random.randint(1, 400)
        assign_keeping_staff_data.append((task_id, staff_id))
    return assign_keeping_staff_data

# יצירת נתונים עבור AssignMaintenanceStaff
def create_assign_maintenance_staff_data():
    assign_maintenance_staff_data = []
    for request_id in range(1, 401):
        staff_id = random.randint(1, 400)
        assign_maintenance_staff_data.append((request_id, staff_id))
    return assign_maintenance_staff_data

# יצירת נתונים עבור MaintenanceInventory
def create_maintenance_inventory_data():
    maintenance_inventory_data = []
    for request_id in range(1, 401):
        usage_id = random.randint(1, 400)
        maintenance_inventory_data.append((request_id, usage_id))
    return maintenance_inventory_data

# יצירת נתונים עבור KeepingInventory
def create_keeping_inventory_data():
    keeping_inventory_data = []
    for usage_id in range(1, 401):
        task_id = random.randint(1, 400)
        keeping_inventory_data.append((usage_id, task_id))
    return keeping_inventory_data

# יצירת סקריפט INSERT
def create_insert_script():
    # פותח קובץ SQL בו ייכתבו כל פקודות ה-INSERT
    with open("insert_tables.sql", "w") as file:
        # הכנסת נתונים ל-Housekeeping
        housekeeping_data = create_housekeeping_data()
        for record in housekeeping_data:
            file.write(f"INSERT INTO Housekeeping (TaskID, TaskDate, Status, RoomId) VALUES ({record[0]}, '{record[1]}', '{record[2]}', {record[3]});\n")

        # הכנסת נתונים ל-MaintenanceRequest
        maintenance_request_data = create_maintenance_request_data()
        for record in maintenance_request_data:
            file.write(f"INSERT INTO MaintenanceRequest (RequestId, IssueDescription, RequestDate, Status, RoomId) VALUES ({record[0]}, '{record[1]}', '{record[2]}', '{record[3]}', {record[4]});\n")

        # הכנסת נתונים ל-AssignKeepingStaff
        assign_keeping_staff_data = create_assign_keeping_staff_data()
        for record in assign_keeping_staff_data:
            file.write(f"INSERT INTO AssignKeepingStaff (TaskID, StaffId) VALUES ({record[0]}, {record[1]});\n")

        # הכנסת נתונים ל-AssignMaintenanceStaff
        assign_maintenance_staff_data = create_assign_maintenance_staff_data()
        for record in assign_maintenance_staff_data:
            file.write(f"INSERT INTO AssignMaintenanceStaff (RequestId, StaffId) VALUES ({record[0]}, {record[1]});\n")

        # הכנסת נתונים ל-MaintenanceInventory
        maintenance_inventory_data = create_maintenance_inventory_data()
        for record in maintenance_inventory_data:
            file.write(f"INSERT INTO MaintenanceInventory (RequestId, UsageId) VALUES ({record[0]}, {record[1]});\n")

        # הכנסת נתונים ל-KeepingInventory
        keeping_inventory_data = create_keeping_inventory_data()
        for record in keeping_inventory_data:
            file.write(f"INSERT INTO KeepingInventory (UsageId, TaskID) VALUES ({record[0]}, {record[1]});\n")

    print("SQL script created successfully!")

# הרצת הסקריפט ליצור את פקודות ה-INSERT
create_insert_script()
