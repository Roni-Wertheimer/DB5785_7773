# Hotel Organization System  - Room & Housekeeping Division
### Student Name: Aharon Wertheimer  

---
# Stage 1
---

### Table of Contents

1. [Introduction](#introduction)
2. [ERD & DSD Diagrams](#erd--dsd-diagrams)
3. [Design Decisions](#design-decisions)
4. [Data Insertion Methods](#data-insertion-methods)
5. [Backup & Restore](#backup--restore)
6. [Select Queries](#part-a-select-queries)
7. [DELETE Queries](#part-b-delete-queries)
8. [UPDATE Queries](#part-c-update-queries)
9. [Rollback & Commit](#part-d-rollback--commit)
10. [Constraints](#part-e-constraints)
11. [DSD and ERD Diagrams](#dsd-and-erd-diagrams)  
12. [Integration Decisions](#integration-decisions)  
13. [Process and Commands Explanation](#process-and-commands-explanation)  
14. [Views](#views)  
    - [View 1 – Original Department](#view-1--original-department)  
    - [View 2 – Received Department](#view-2--received-department)  
15. [Queries on Views](#queries-on-views)
    - [Queries on view 1](#queries-on-view-1)  
    - [Queries on view 2](#queries-on-view-2) 
16. [Programs](#programs)
    - [Procedures](#procedures)  
    - [Functions](#functions)
    - [Main Programs](#main-programs)
    - [Triggers](#triggers) 

---

## Introduction

The **Hotel Organization** system is designed to manage the daily operational processes of a hotel.  
It includes several core modules such as:  
- Housekeeping and Maintenance task management  
- Task assignments to employees  
- Inventory tracking and equipment usage  

The system stores data about hotel rooms, staff, maintenance requests, housekeeping tasks, inventory usage, and more.  
Its main goal is to streamline hotel operations, ensure consistent maintenance, and improve the guest experience.

---

## ERD & DSD Diagrams

### ERD (Entity-Relationship Diagram):

![image ERD](https://github.com/user-attachments/assets/5c55c545-853b-4d8d-b839-fa8de5c81bec)


### DSD (Data Structure Diagram):

![image RS](https://github.com/user-attachments/assets/7e3ef2df-119d-4db9-836b-76d8bb119fd4)

---
# תיעוד ישויות וקשרים - מערכת ניהול מלון

## 1. RoomType (סוג חדר)
**מה זה:** מייצג סוגים שונים של חדרים במלון (למשל יחיד, זוגי, סוויטה).

**מאפיינים:**
- `RoomTypeId` – מזהה ייחודי.
- `TypeName` – שם סוג החדר.
- `MaxOccupancy` – מספר אורחים מקסימלי.
- `BasePrice` – מחיר בסיס ללילה.

**קשרים:**
- `Room.RoomTypeId` → קושר בין חדרים לסוג שלהם.

---

## 2. Staff (צוות)
**מה זה:** מייצג עובדים במלון.

**מאפיינים:**
- `StaffId` – מזהה ייחודי.
- `FirstName`, `LastName` – שם פרטי ומשפחה.
- `Role` – תפקיד (למשל מנקה, תחזוקה).
- `PhoneNumber` – טלפון.
- `EmploymentDate` – תאריך התחלת עבודה.
- `IsActive` – האם פעיל.

**קשרים:**
- מקושר ל-`Housekeeping` ו-`MaintenanceRequest` דרך טבלאות שיוך:
  - `AssignKeepingStaff`
  - `AssignMaintenanceStaff`

---

## 3. InventoryUsage (שימוש במלאי)
**מה זה:** מייצג פריטים שנעשה בהם שימוש (למשל חומרי ניקוי, חלקי חילוף).

**מאפיינים:**
- `UsageId` – מזהה שימוש.
- `ItemName` – שם פריט.
- `Quantity` – כמות.

**קשרים:**
- `KeepingInventory` – שימוש בפריטים במשימות ניקיון.
- `MaintenanceInventory` – שימוש בפריטים בבקשות תחזוקה.

---

## 4. Room (חדר)
**מה זה:** מייצג חדר במלון.

**מאפיינים:**
- `RoomId`, `RoomNumber` – מזהה ומספר חדר.
- `PricePerNight` – מחיר ללילה.
- `AvailabilityStatus`, `CleaningStatus` – זמינות וניקיון.
- `Floor` – קומה.
- `RoomTypeId` – סוג חדר.

**קשרים:**
- מקושר ל-`RoomType`
- מקושר ל-`Housekeeping` ו-`MaintenanceRequest` לפי `RoomId`.

---

## 5. Housekeeping (משימת ניקיון)
**מה זה:** מייצג משימת ניקיון בחדר.

**מאפיינים:**
- `TaskID`, `TaskDate`, `Status`, `RoomId`.

**קשרים:**
- `AssignKeepingStaff` – אנשי צוות שביצעו את המשימה.
- `KeepingInventory` – פריטי מלאי שנעשה בהם שימוש במשימה.

---

## 6. MaintenanceRequest (בקשת תחזוקה)
**מה זה:** מתעד תקלה או בעיה בחדר שדורשת טיפול.

**מאפיינים:**
- `RequestId`, `IssueDescription`, `RequestDate`, `Status`, `RoomId`.

**קשרים:**
- `AssignMaintenanceStaff` – אנשי צוות שטיפלו בבקשה.
- `MaintenanceInventory` – פריטי מלאי שנעשה בהם שימוש בטיפול.

---

## 7. AssignKeepingStaff
**מה זה:** טבלת קשר בין משימות ניקיון לעובדים שביצעו.

**קשר:** 
- Many-to-Many בין `Housekeeping` ל-`Staff`.

---

## 8. AssignMaintenanceStaff
**מה זה:** טבלת קשר בין בקשות תחזוקה לעובדים שטיפלו בהן.

**קשר:** 
- Many-to-Many בין `MaintenanceRequest` ל-`Staff`.

---

## 9. MaintenanceInventory
**מה זה:** טבלת קשר בין בקשות תחזוקה לפריטי מלאי שנעשה בהם שימוש.

**קשר:** 
- Many-to-Many בין `MaintenanceRequest` ל-`InventoryUsage`.

---

## 10. KeepingInventory
**מה זה:** טבלת קשר בין משימות ניקיון לפריטי מלאי שנעשה בהם שימוש.

**קשר:** 
- Many-to-Many בין `Housekeeping` ל-`InventoryUsage`.


---

## Design Decisions

1. **Separation between Housekeeping and Maintenance modules** – This was chosen to reflect the different responsibilities of hotel departments.
2. **Use of linking tables (AssignKeepingStaff / AssignMaintenanceStaff)** – These allow flexibility in assigning multiple staff members to multiple tasks.
3. **Dedicated Inventory tables** – To enable accurate tracking of item and equipment usage.

---

## Data Insertion Methods

To populate the database with realistic test data, we used three methods:

1. **Mockaroo – Online Data Generator**  
   Used to generate realistic mock data exported in CSV format.  
   ![image](https://github.com/user-attachments/assets/fbd50395-7136-465c-8835-14ecb9983446)
   ![image](https://github.com/user-attachments/assets/c9ca38e0-eb07-4bd7-ab32-5174a45b8741)
   ![image](https://github.com/user-attachments/assets/834c3b03-91e0-459e-a055-caee1d05f01a)
   ![image](https://github.com/user-attachments/assets/90e2a5d0-4885-46ef-9495-aee54adfeb29)





3. **GenerateData.com**  
   Another online platform to generate tabular data with various formats, used for fields not covered by Mockaroo.  
   ![image](https://github.com/user-attachments/assets/107e53e5-d720-45b8-9809-8595109b66e6)
   ![image](https://github.com/user-attachments/assets/5be8d1fe-170b-4662-9fad-595656ed23b8)



5. **Python Script – `generate_insert_script.py`**  
   A custom script written in Python that randomly generates and outputs SQL `INSERT` statements for all required tables.  
   ![image](https://github.com/user-attachments/assets/b0cec8dc-2de4-45c1-8092-098be8ac348d)
   ![image](https://github.com/user-attachments/assets/054d669f-d2ee-47c5-95bd-9f0b53439866)
   ![image](https://github.com/user-attachments/assets/5ed8a3c4-466b-49a3-a15a-075be3d41303)
   ![image](https://github.com/user-attachments/assets/f1750d42-d43c-4e36-b951-6193c517a037)
   ![image](https://github.com/user-attachments/assets/396b765d-f3a5-443e-a733-3473821863a8)
   ![image](https://github.com/user-attachments/assets/7c1ae749-d1b0-4051-87bd-e6da47f0d882)
   ![image](https://github.com/user-attachments/assets/2c22629b-15e7-4574-b326-7fdb6b1c7d70)
   ![image](https://github.com/user-attachments/assets/f43c2587-5e42-4411-9178-7a2d4724671d)






   


---

## Backup & Restore

### Performing a database backup using pgAdmin in Docker:
![image](https://github.com/user-attachments/assets/9a82d92c-3994-4083-b60d-1f59119c0b17)


### Restoring the database:
![image](https://github.com/user-attachments/assets/46098bab-3fba-42d0-aa1d-a6ebbdf9e6c1)

---


---
# Stage 2
---

# Report: SQL Queries and Database Operations – Hotel Room and Housekeeping Management System

---

## Part A: SELECT Queries

### Query 1
**Description:**  

השאילתה מחזירה רשימת חדרים שמתוכננים לניקיון היום וסטטוס המשימה שלהם הוא "ממתין". הפלט כולל את מספר החדר, סטטוס הניקיון, סוג החדר ותאריך המשימה.


**Execution and Result Screenshot:**  
![image](https://github.com/user-attachments/assets/4b07e1e7-6263-49ad-aa84-2bc0671a29f9)

---

### Query 2
**Description:**  

השאילתה מציגה סיכום חודשי של כמויות שימוש בפריטי מלאי לניקיון, כולל שם הפריט, החודש, השנה וסך הכמות שהשתמשו בה.

**Execution and Result Screenshot:**  
![image](https://github.com/user-attachments/assets/401cfffe-49bf-4021-b5e4-3a8706bd9c82)


---

### Query 3
**Description:**  

השאילתה מציגה את הממוצע של השימוש בחומרי הניקיון למשימת ניקיון לפי סוג החדר.



**Execution and Result Screenshot:**  
![image](https://github.com/user-attachments/assets/b6b7878b-0dda-4f62-af92-c942ce829e33)


---

### Query 4
**Description:**  

השאילתה מציגה את מספר בקשות התחזוקה הפתוחות לכל חדר, כולל סטטוסים "ממתין" או "בתהליך", וממיינת מהחדר עם הכי הרבה בקשות.


**Execution and Result Screenshot:**  
![image](https://github.com/user-attachments/assets/e1839506-15e6-496b-939c-e52de5f9bf00)


---

### Query 5
**Description:**  

השאילתה מציגה את השם המלא ומספר עבודות התחזוקה של כל העובדים שהיו להם עבודות תחזוקה החודש.


**Execution and Result Screenshot:**  
![image](https://github.com/user-attachments/assets/765c16ee-7026-4f30-83fe-3aea38c45e6d)


---

### Query 6 
**Description:**  

השאילתה מציגה את החדרים בהם לא בוצע ניקיון בשבוע האחרון.


**Execution and Result Screenshot:**  
![image](https://github.com/user-attachments/assets/25f5e52f-b40b-4235-8396-f7bba886773c)


---

### Query 7
**Description:**  

השאילתה מציגה את כל משימות הניקיון שבוצעו בשלושת החודשים האחרונים, כולל מספר חדר, קומה, סוג חדר, תאריך, סטטוס המשימה ושם העובד שביצע אותה.


**Execution and Result Screenshot:**  
![image](https://github.com/user-attachments/assets/9e54f5a5-9f1b-43fb-a77e-0cf14a216350)


---

### Query 8
**Description:** 

השאילתה מציגה את כל החדרים שהמחיר שלהם ללילה גבוה מהמחיר הבסיסי של סוג החדר.


**Execution and Result Screenshot:**  
![image](https://github.com/user-attachments/assets/5f91155f-d96c-4c95-8e45-383d4ec27cf8)


---

## Part B: DELETE Queries

### DELETE Query 1
**Description:**  

מחיקת משימות ניקיון שבוצעו לפני יותר משנה


**Before DELETE – Screenshot of table:**  
![image](https://github.com/user-attachments/assets/83917d91-697d-41c9-bc71-636adf589edd)


**Execution and After DELETE Screenshot:**  
![image](https://github.com/user-attachments/assets/21f39b93-dde4-4cab-a9f9-42a9184f7e16)


---

### DELETE Query 2
**Description:**  

מחיקת הקצאות תחזוקה לעובדים שהתפטרו


**Before DELETE – Screenshot of table:**  
![image](https://github.com/user-attachments/assets/d8d70b1f-7ea4-4f5f-b28d-1e13b6727163)


**Execution and After DELETE Screenshot:**  
![image](https://github.com/user-attachments/assets/4bb56307-7c3f-4f5b-94f2-2a3b2ab80d42)

---

### DELETE Query 3
**Description:**  

מחיקת שימוש במלאי שלא שייך לאף משימה


**Before DELETE – Screenshot of table:**  
![image](https://github.com/user-attachments/assets/458effd3-8575-4279-aaa2-c8b2c2c5f69c)


**Execution and After DELETE Screenshot:**  
![image](https://github.com/user-attachments/assets/ab1f6d6c-b7d8-4571-9299-f812da31ef9f)

---

## Part C: UPDATE Queries

### UPDATE Query 1
**Description:**  

עדכון סטטוס ניקיון לחדרים שבוצעה בהם משימת ניקיון בשלושה ימים האחרונים

**Before UPDATE – Screenshot:**  
![image](https://github.com/user-attachments/assets/827863cd-195b-49a3-b0a0-5aa62904f2db)


**Execution and After UPDATE Screenshot:**  
![image](https://github.com/user-attachments/assets/fc4fda66-b306-4322-9d70-f3addb2dcd7f)

---

### UPDATE Query 2
**Description:**  

עדכן חדרים ל-"Unavailable" אם יש להם בקשות תחזוקה בתהליך ב־7 הימים האחרונים


**Before UPDATE – Screenshot:**  
![image](https://github.com/user-attachments/assets/6e42f6e3-8a48-4f32-98b1-e651e8123bcc)


**Execution and After UPDATE Screenshot:**  
![image](https://github.com/user-attachments/assets/ce76dc23-b8ed-4434-a0e3-f1d685b5ac72)


---

### UPDATE Query 3
**Description:**  

סימון עובדים שלא בוצעה להם הקצאה בחודש האחרון כ"לא פעילים זמנית"


**Before UPDATE – Screenshot:**  
![image](https://github.com/user-attachments/assets/a3fb7faf-0063-4518-865b-a0ba47e949b1)


**Execution and After UPDATE Screenshot:**  
![image](https://github.com/user-attachments/assets/87f5d77b-4305-41de-b9b8-7670094b69d2)

---
## Part D: Rollback & Commit
---

### Rollback
---

**Before change:**
![image](https://github.com/user-attachments/assets/3fe57a29-6579-4fab-a7b4-b56137c27c39)

**After change:**
![image](https://github.com/user-attachments/assets/c9ec55dd-9ab3-49bf-a287-fab7f6cafd79)

**Rollback:**
![image](https://github.com/user-attachments/assets/1a9f68bf-f151-409c-a1ed-52914fbd8a62)

**After rollback:**
![image](https://github.com/user-attachments/assets/cc794dbb-9399-40ad-b71d-1c98c1411afc)
---

### Commit
---

**Before change:**
![image](https://github.com/user-attachments/assets/5fd73539-4974-411a-956e-6e0da64ace4d)

**After change:**
![image](https://github.com/user-attachments/assets/af89d41c-0aef-449b-8da2-17cb86d57c47)

**Commit:**
![image](https://github.com/user-attachments/assets/c4a710a3-9117-47a0-9561-39d2628f3328)

**After commit:**
![image](https://github.com/user-attachments/assets/c0a86627-2b93-45cd-b2ec-4e6209d5aad5)

---


## Part E: Constraints
---

### Constraint 1
**Description:**  

1.	אילוץ CHECK  על כמות בצריכת מלאי (שיהיה חיובי בלבד)
2.	

**Screenshot:**  
![image](https://github.com/user-attachments/assets/77d29c46-6c6a-4530-bd69-fec60cd2bcce)


**Insert invalid value:**  
![image](https://github.com/user-attachments/assets/6c7a719a-e0c9-4911-8926-aeed2e46abd9)
---


### Constraint 2
**Description:**  

אילוץ DEFAULT על עמודת Status בטבלת MaintenanceRequest


**Screenshot:**  
![image](https://github.com/user-attachments/assets/0b4550ba-9b87-4b46-a152-e8a94abdc3f3)


**Insert invalid value:**  
![image](https://github.com/user-attachments/assets/8877f55d-8b08-44bc-a746-a47183fb2a49)
---


### Constraint 3
**Description:**  

אילוץ DEFAULT על עמודת IsActive בטבלת Staff – ברירת מחדל לעובד חדש


**Screenshot:**  
![image](https://github.com/user-attachments/assets/5871ce72-2164-414e-b1e4-99e4ef6c5404)


**Insert invalid value:**  
![image](https://github.com/user-attachments/assets/0eda4514-1c72-4659-bfa8-5bc05f73e1c6)

---

## DSD and ERD Diagrams

### DSD and ERD before integration  
![secondDsd](https://github.com/user-attachments/assets/cddb8431-7d00-44b2-96b5-1d596bd60a61)
![secondErd](https://github.com/user-attachments/assets/e977b7ef-e678-480e-98d3-2397811fee27)

### ERD and DSD after integration  
![afterIntegration](https://github.com/user-attachments/assets/15552f2c-feb9-42ac-adbf-c57e8f55526a)
![dsdAterIntegration](https://github.com/user-attachments/assets/2e19ecf6-2ab2-4900-b0c7-93aeb2f77cdc)
---

## Integration Decisions

במהלך אינטגרציית בסיסי הנתונים, התקבלו ההחלטות הבאות:

- המרה של שמות עמודות כדי ליצור אחידות (`roomId` במקום `Room_Id`).
- ויתור על השדה capacity בטבלה Room של הdataBase השני מכיוון שבdataBase שלנו יש שדה זהה בטבלה roomType.
- מיזוג הנתונים על ידי עדכון מזהים (IDs) חופפים והסרת כפילויות.
- יצירת טבלאות foreign tables לקישור בין בסיסי הנתונים באמצעות `postgres_fdw`.

---

## Process and Commands Explanation

השלבים המרכזיים שבוצעו:
- חיבור בין בסיסי הנתונים באמצעות הפקודה:
  ```sql
  CREATE EXTENSION IF NOT EXISTS postgres_fdw;
  CREATE SERVER integration_server FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'localhost', dbname 'otherdb', port '5432');
  CREATE USER MAPPING FOR CURRENT_USER SERVER integration_server OPTIONS (user 'postgres', password 'password');

- מיזוג הטבלה Rooms לטבלה Romm:
INSERT INTO Room (RoomId, RoomNumber, PricePerNight, AvailabilityStatus, CleaningStatus, Floor, RoomTypeId)
SELECT 
    room_id,
    room_number::INTEGER,
    round((random() * (800 - 200) + 200)::numeric, 2) AS PricePerNight,
    (ARRAY['Available', 'Occupied', 'Maintenance'])[floor(random() * 3 + 1)] AS AvailabilityStatus,
    (ARRAY['Clean', 'Dirty', 'In Progress'])[floor(random() * 3 + 1)] AS CleaningStatus,
    floor,
    (
        SELECT RoomTypeId
        FROM RoomType
        ORDER BY random()
        LIMIT 1
    ) AS RoomTypeId
FROM  external_rooms
WHERE room_id NOT IN (SELECT RoomId FROM Room);

 - שינוי שם השדה room_id ל roomid בטבלה reservation:
ALTER TABLE reservation
RENAME COLUMN room_id TO roomid;


## Views

### View 1 – Original Department

מבט שמציג משימות ניקיון עם שם העובד והסטטוס:


![image](https://github.com/user-attachments/assets/8f3d6a8c-5ebc-4348-a1dd-f58ebff4e831)

![image](https://github.com/user-attachments/assets/45e2ae3b-5e39-4ef0-a30f-d29fb0481404)


### View 2 – Received Department

מבט המציג את שמות האורחים עם פרטי ההזמנה:


![image](https://github.com/user-attachments/assets/480baaf4-1048-4458-8ae8-2ab44b61ccb2)

![image](https://github.com/user-attachments/assets/cb2afd21-e471-4638-a9b8-b1cce19eaa0d)


## Queries on Views

### Queries on view 1
רשימת משימות ניקיון שטרם הושלמו, עם שם העובד והקומה


![image](https://github.com/user-attachments/assets/302b1087-6239-4a4d-bc63-441c68b11958)

כמה משימות ביצע כל עובד ניקיון פעיל


![image](https://github.com/user-attachments/assets/733fa852-89ca-4fbd-858c-5303a8a229ca)


### Queries on view 2

מספר הזמנות לפי סטטוס

![image](https://github.com/user-attachments/assets/39977c22-77f6-403a-bb7f-5b64a9a19b62)

הזמנות שצפויות להתחיל בשבוע הקרוב

![image](https://github.com/user-attachments/assets/8654a55d-f6a4-475a-b096-41fe971bbba6)

## Programs


### Procedures

הפרוצדורה סורקת חדרים שלא הוזמנו ב־60 הימים האחרונים. אם החדר מלוכלך או שאין לו קריאה פתוחה לאחזקה, היא יוצרת משימת ניקיון או בקשת אחזקה בהתאם, ומעדכנת הערה בטבלת החדרים.

```sql
CREATE OR REPLACE PROCEDURE public.analyze_and_schedule_maintenance()
LANGUAGE plpgsql
AS $$
DECLARE
    room_rec RECORD;
    has_open_issue BOOLEAN;
    task_id INT;
    new_request_id INT;
BEGIN
    FOR room_rec IN
        SELECT r.RoomId, r.RoomNumber, r.CleaningStatus
        FROM Room r
        WHERE NOT EXISTS (
            SELECT 1
            FROM Reservation res
            WHERE res.roomId = r.RoomId
              AND res.start_date > CURRENT_DATE - INTERVAL '60 days'
        )
    LOOP
        -- Check if there is already an open maintenance issue
        SELECT EXISTS (
            SELECT 1
            FROM MaintenanceRequest mr
            WHERE mr.RoomId = room_rec.RoomId AND mr.Status != 'closed'
        )
        INTO has_open_issue;

        -- If the room is dirty or has no bookings recently or needs attention
        IF room_rec.CleaningStatus != 'clean' OR NOT has_open_issue THEN

		            -- Schedule housekeeping task if the room is dirty
            IF room_rec.CleaningStatus != 'clean' THEN
                SELECT COALESCE(MAX(TaskID), 0) + 1 INTO task_id FROM Housekeeping;

				INSERT INTO Housekeeping(TaskID, TaskDate, Status, RoomId)
				VALUES (task_id, CURRENT_DATE, 'pending', room_rec.RoomId);


                RAISE NOTICE 'Housekeeping task scheduled for Room % (TaskID: %)', room_rec.RoomNumber, task_id;

            -- Create maintenance request if none exists
            ELSE
                -- Generate next available RequestId
                SELECT COALESCE(MAX(RequestId), 0) + 1
                INTO new_request_id
                FROM MaintenanceRequest;

                INSERT INTO MaintenanceRequest(RequestId, IssueDescription, RequestDate, Status, RoomId)
                VALUES (
                    new_request_id,
                    'Auto-detected unbooked room for over 60 days',
                    CURRENT_DATE,
                    'open',
                    room_rec.RoomId
                );

                RAISE NOTICE 'Maintenance request created for Room % (RequestID: %)', room_rec.RoomNumber, new_request_id;
            END IF;


            -- Update room note
            UPDATE Room
            SET MaintenanceNote = CONCAT(
                'Room unused for over 60 days. Auto-scheduled maintenance and cleaning on ',
                CURRENT_DATE
            )
            WHERE RoomId = room_rec.RoomId;

            RAISE NOTICE 'Room % marked for maintenance and/or cleaning.', room_rec.RoomNumber;
        END IF;
    END LOOP;

EXCEPTION
    WHEN OTHERS THEN
        RAISE WARNING 'Error during maintenance analysis: %', SQLERRM;
END;
$$;

ALTER PROCEDURE public.analyze_and_schedule_maintenance()
    OWNER TO postgres;
```
---

מכינה חדר לקראת הזמנה: אם החדר מלוכלך, נוצרת משימת ניקיון. אם יש תקלות פתוחות, מוצגת הודעה. בנוסף, הערת תחזוקה בטבלת החדרים מתעדכנת.


```sql
CREATE OR REPLACE PROCEDURE public.prepare_room_for_reservation(
	IN p_room_id integer)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    is_dirty BOOLEAN;
    has_open_issue BOOLEAN;
    task_id INTEGER;
    staff_id INTEGER;
BEGIN
    -- Check if the room needs cleaning
    SELECT (CleaningStatus != 'clean') INTO is_dirty
    FROM Room
    WHERE RoomId = p_room_id;

    -- Check if there are open maintenance issues
    SELECT EXISTS (
        SELECT 1 FROM MaintenanceRequest
        WHERE RoomId = p_room_id AND Status != 'closed'
    ) INTO has_open_issue;

    -- Create cleaning task if needed
    IF is_dirty THEN
        -- Find next TaskID
        SELECT COALESCE(MAX(TaskID), 0) + 1 INTO task_id FROM Housekeeping;

        -- Insert new housekeeping task with calculated TaskID
        INSERT INTO Housekeeping(TaskID, TaskDate, Status, RoomId)
        VALUES (task_id, CURRENT_DATE, 'pending', p_room_id);

        RAISE NOTICE 'Cleaning task created for room % (TaskID: %)', p_room_id, task_id;
    END IF;

    -- Notify about open issues
    IF has_open_issue THEN
        RAISE NOTICE 'Room % has an open maintenance issue. Action required before guest arrival.', p_room_id;
    END IF;

    -- Update room maintenance note
    IF is_dirty OR has_open_issue THEN
        UPDATE Room
        SET MaintenanceNote = CONCAT('Rebooked on ', CURRENT_DATE,
                                     CASE WHEN is_dirty THEN '. Cleaning required' ELSE '' END,
                                     CASE WHEN has_open_issue THEN '. Open maintenance issue' ELSE '' END)
        WHERE RoomId = p_room_id;
    END IF;
END;
$BODY$;
```
---
### Functions

פונקציה שמחזירה את מספר החדרים עם בעיה כלשהי: מצב ניקיון שאינו תקין או תקלה פתוחה.


```sql
CREATE OR REPLACE FUNCTION public.count_problematic_rooms(
	)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    total INTEGER;
BEGIN
    SELECT COUNT(*) INTO total
    FROM Room
    WHERE MaintenanceNote IS NOT NULL
      AND (CleaningStatus != 'clean'
           OR EXISTS (
                SELECT 1 FROM MaintenanceRequest
                WHERE RoomId = Room.RoomId AND Status != 'closed'
           ));

    RETURN total;
END;
$BODY$;

ALTER FUNCTION public.count_problematic_rooms()
    OWNER TO postgres;
```
---

מחזירה קורסור עם אנשי ניקיון זמינים – כלומר, עובדים פעילים שלא משובצים למשימות ניקיון פתוחות באותו היום.



```sql
CREATE OR REPLACE FUNCTION public.get_available_cleaners()
RETURNS refcursor
LANGUAGE plpgsql
AS $$
DECLARE
    cleaner_cursor REFCURSOR;
BEGIN
    OPEN cleaner_cursor FOR
        SELECT s.StaffId, s.FirstName, s.LastName,
               COUNT(hk.TaskID) AS pending_tasks
        FROM Staff s
        LEFT JOIN AssignKeepingStaff aks ON aks.StaffId = s.StaffId
        LEFT JOIN Housekeeping hk ON hk.TaskID = aks.TaskID
                                    AND hk.Status != 'Completed'
                                    AND hk.TaskDate = CURRENT_DATE
        WHERE s.Role = 'cleaner' AND s.IsActive = TRUE
        GROUP BY s.StaffId, s.FirstName, s.LastName
        HAVING COUNT(hk.TaskID) = 0 
        ORDER BY s.LastName, s.FirstName;

    RETURN cleaner_cursor;
END;
$$;
```
---

### Main Programs

מריצה את ניתוח האחזקה (כולל משימות ניקיון ובקשות תחזוקה), ומדפיסה את מספר החדרים הבעייתיים.


```sql
CREATE OR REPLACE PROCEDURE public.process_maintenance_and_report(
	)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    total_bad_rooms INTEGER;
BEGIN
    -- Call the maintenance analysis procedure
    CALL analyze_and_schedule_maintenance();

    -- Get the number of problematic rooms (assumes count_problematic_rooms() function exists and returns integer)
    total_bad_rooms := count_problematic_rooms();

    -- Output the number of problematic rooms
    RAISE NOTICE 'Current number of problematic rooms: %', total_bad_rooms;
END;
$BODY$;
ALTER PROCEDURE public.process_maintenance_and_report()
    OWNER TO postgres;
```
---

![image](https://github.com/user-attachments/assets/8302af82-a056-4693-9d1e-8b6bab30d92d)

---

מכינה חדר להזמנה וגם משייכת מנקה זמין למשימת הניקיון שנוצרה, אם נוצרה. אם אין מנקה פנוי – מתקבלת הודעה.




```sql
CREATE OR REPLACE PROCEDURE public.prepare_and_assign_cleaner(
	IN p_room_id integer)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    task_id INTEGER;
    staff_id INTEGER;
    cleaner_cursor REFCURSOR;
    cleaner_record RECORD;
BEGIN
    -- Step 1: Prepare the room (creates a cleaning task if needed)
    CALL prepare_room_for_reservation(p_room_id);

    -- Step 2: Check if a cleaning task was created today for the room
    SELECT hk.TaskID INTO task_id
    FROM Housekeeping hk
    WHERE hk.RoomId = p_room_id
      AND hk.TaskDate = CURRENT_DATE
      AND hk.Status = 'pending'
    ORDER BY hk.TaskID DESC
    LIMIT 1;

    IF task_id IS NULL THEN
        RAISE NOTICE 'No cleaning task created for room %. Nothing to assign.', p_room_id;
        RETURN;
    END IF;

    -- Step 3: Get the available cleaners (least number of pending tasks)
    cleaner_cursor := get_available_cleaners();

    -- Step 4: Fetch the first available cleaner
    FETCH cleaner_cursor INTO cleaner_record;

    IF FOUND THEN
        staff_id := cleaner_record.StaffId;

        -- Step 5: Assign the cleaner to the task
        INSERT INTO AssignKeepingStaff(TaskID, StaffId)
        VALUES (task_id, staff_id);

        RAISE NOTICE 'Assigned staff (ID: %) to cleaning task (TaskID: %).', staff_id, task_id;
    ELSE
        RAISE NOTICE 'No available cleaning staff. Manual assignment required for TaskID %.', task_id;
    END IF;

    -- Step 6: Close the cursor
    CLOSE cleaner_cursor;
END;
$BODY$;
ALTER PROCEDURE public.prepare_and_assign_cleaner(integer)
    OWNER TO postgres;
```
---

![image](https://github.com/user-attachments/assets/3204b213-c115-4e17-a6c4-00ff9179c2a2)

---
### Triggers

טריגר שמתעדכן אוטומטית את מצב ניקיון החדר ל־clean כאשר משימת ניקיון מתבצעת (Status='Completed').
```sql
CREATE OR REPLACE FUNCTION update_room_cleaning_status()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.Status = 'Completed' THEN
        UPDATE Room
        SET CleaningStatus = 'Clean'
        WHERE RoomId = NEW.RoomId;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_cleaning_status
AFTER UPDATE OF Status ON Housekeeping
FOR EACH ROW
WHEN (NEW.Status = 'Completed')
EXECUTE FUNCTION update_room_cleaning_status();
```
---

טריגר שמונע הזמנה כפולה של אותו חדר בטווח תאריכים חופף. מופעל לפני כל INSERT או UPDATE בטבלת Reservation.


```sql
CREATE OR REPLACE FUNCTION prevent_double_booking()
RETURNS TRIGGER AS $$
DECLARE
    overlapping_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO overlapping_count
    FROM Reservation
    WHERE roomId = NEW.roomId
      AND status = 'booked'
      AND NEW.start_date < end_date
      AND NEW.end_date > start_date
      AND (reservation_id IS DISTINCT FROM NEW.reservation_id);

    IF overlapping_count > 0 THEN
        RAISE EXCEPTION 'Room % is already booked in the selected date range.', NEW.roomId;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_double_booking
BEFORE INSERT OR UPDATE ON Reservation
FOR EACH ROW
EXECUTE FUNCTION prevent_double_booking();
```
---
