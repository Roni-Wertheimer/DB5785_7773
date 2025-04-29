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






# 🧑‍💻 DB5785 - PostgreSQL and Docker Workshop 🗄️🐋

This workshop will guide you through setting up and managing a _PostgreSQL database_ using Docker.  
You will also explore how to use _pgAdmin_ GUI to interact with the database and perform various tasks.  

You will have to add to the [Workshop Files & Scripts](#workshop-id) section your own specific implementation  
- see: *[Markdown Guide](https://www.markdownguide.org)* and *[Writing and Formatting in Github](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github)* for modifying this Readme.md file accordingly. 

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (optional, but recommended): [Install Docker Compose](https://docs.docker.com/compose/install/)

---

## Setting Up PostgreSQL with Docker

### 1. **Pull the PostgreSQL Docker Image**
   Download the official PostgreSQL Docker image with the following command:

   ```bash
   docker pull postgres:latest
   ```

### 2. **Create a Docker Volume**
   Create a Docker volume to persist PostgreSQL data:

   ```bash
   docker volume create postgres_data
   ```

   This volume will ensure data persistence, even if the container is removed.

### 3. **Run the PostgreSQL Container**
   Start the PostgreSQL container using the following command:

   ```bash
   docker run --name postgres -e POSTGRES_PASSWORD=your_password -d -p 5432:5432 -v postgres_data:/var/lib/postgresql/data postgres
   ```

   Replace `your_password` with a secure password for the PostgreSQL superuser (`postgres`).

   - The `-v postgres_data:/var/lib/postgresql/data` flag mounts the `postgres_data` volume to the container's data directory, ensuring data persistence.

### 4. **Verify the Container**
   To confirm the container is running, use:

   ```bash
   docker ps
   ```

   You should see the `postgres` container listed.

---

## Setting Up pgAdmin with Docker

### 1. **Pull the pgAdmin Docker Image**
   Download the official PostgreSQL Docker image with the following command:

   ```bash
   docker pull dpage/pgadmin4:latest
   ```

### 2. **Run the pgAdmin Container**
   Start the pgAdmin container using the following command:

   ```bash
   docker run --name pgadmin -d -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=admin@example.com -e PGADMIN_DEFAULT_PASSWORD=admin dpage/pgadmin4:latest
   ```

   Replace `5050` with your desired port, and `admin@example.com` and `admin` with your preferred email and password for pgAdmin.

   - The `-p 5050:80` flag maps port `5050` on your host machine to port `80` inside the container (where pgAdmin runs).

### 3. **Access pgAdmin**
   Open your browser and go to:

   ```
   http://localhost:5050
   ```

   Log in using the email and password you set.

---

## Accessing PostgreSQL via pgAdmin

finding Host address: 
  ```bash
  docker inspect --format='{{.NetworkSettings.IPAddress}}' postgres
  ```

### 1. **Connect to the PostgreSQL Database**
   - After logging into pgAdmin, click on **Add New Server**.
   - In the **General** tab, provide a name for your server (e.g., `PostgreSQL Docker`).
   - In the **Connection** tab, enter the following details:
     - **Host name/address**: `postgres` (or the name of your PostgreSQL container). [usually  172.17.0.2 on windows]
     - **Port**: `5432` (default PostgreSQL port).
     - **Maintenance database**: `postgres` (default database).
     - **Username**: `postgres` (default superuser).
     - **Password**: The password you set for the PostgreSQL container (e.g., `your_password`).
   - Click **Save** to connect.

### 2. **Explore and Manage the Database**
   - Once connected, you can:
     - Create and manage databases.
     - Run SQL queries using the **Query Tool**.
     - View and edit tables, views, and stored procedures.
     - Monitor database activity and performance.

---

## Workshop Outcomes

By the end of this workshop, you will:

- Understand how to set up PostgreSQL and pgAdmin using Docker.
- Learn how to use Docker volumes to persist database data.
- Gain hands-on experience with basic and advanced database operations.

----
<a name="workshop-id"></a>
## 📝 Workshop Files & Scripts (to be modified by the students) 🧑‍🎓 

This workshop introduces key database concepts and provides hands-on practice in a controlled, containerized environment using PostgreSQL within Docker.

### Key Concepts Covered:

1. **Entity-Relationship Diagram (ERD)**:
   - Designed an ERD to model relationships and entities for the database structure.
   - Focused on normalizing the database and ensuring scalability.

   **[Add ERD Snapshot Here]**
   
 images/erd/addimagetoreadme.PNG  
> ![add_image_to readme_with_relative_path](images/erd/addimagetoreadme.PNG)

images/erd/one.jpg
> ![add_image_one.png](images/erd/one.jpg)

  
   *(Upload or link to the ERD image or file)*

3. **Creating Tables**:
   - Translated the ERD into actual tables, defining columns, data types, primary keys, and foreign keys.
   - Utilized SQL commands for table creation.

   **[Add Table Creation Code Here]**
   *(Provide or link to the SQL code used to create the tables)*

4. **Generating Sample Data**:
   - Generated sample data to simulate real-world scenarios using **SQL Insert Statements**.
   - Used scripts to automate bulk data insertion for large datasets.

   **[Add Sample Data Insert Script Here]**
   *(Upload or link to the sample data insert scripts)*

5. **Writing SQL Queries**:
   - Practiced writing **SELECT**, **JOIN**, **GROUP BY**, and **ORDER BY** queries.
   - Learned best practices for querying data efficiently, including indexing and optimization techniques.

   **[Add Example SQL Query Here]**
   *(Provide or link to example SQL queries)*

6. **Stored Procedures and Functions**:
   - Created reusable **stored procedures** and **functions** to handle common database tasks.
   - Used SQL to manage repetitive operations and improve performance.

   **[Add Stored Procedures/Function Code Here]**
   *(Upload or link to SQL code for stored procedures and functions)*

7. **Views**:
   - Created **views** to simplify complex queries and provide data abstraction.
   - Focused on security by limiting user access to certain columns or rows.

   **[Add View Code Here]**
   *(Provide or link to the SQL code for views)*

8. **PostgreSQL with Docker**:
   - Set up a Docker container to run **PostgreSQL**.
   - Configured database connections and managed data persistence within the containerized environment.

   **[Add Docker Configuration Code Here]**
   *(Link to or provide the Docker run command and any configuration files)*

---

## 💡 Workshop Outcomes

By the end of this workshop, you should be able to:

- Design and create a database schema based on an ERD.
- Perform CRUD (Create, Read, Update, Delete) operations with SQL.
- Write complex queries using joins, aggregations, and subqueries.
- Create and use stored functions and procedures for automation and performance.
- Work effectively with PostgreSQL inside a Docker container for development and testing.

---

## Additional Tasks for Students

### 1. **Database Backup and Restore**
   - Use `pg_dump` to back up your database and `pg_restore` or `psql` to restore it.

   ```bash
   # Backup the database
   pg_dump -U postgres -d your_database_name -f backup.sql

   # Restore the database
   psql -U postgres -d your_database_name -f backup.sql
   ```

### 2. **Indexing and Query Optimization**
   - Create indexes on frequently queried columns and analyze query performance.

   ```sql
   -- Create an index
   CREATE INDEX idx_your_column ON your_table(your_column);

   -- Analyze query performance
   EXPLAIN ANALYZE SELECT * FROM your_table WHERE your_column = 'value';
   ```

### 3. **User Roles and Permissions**
   - Create user roles and assign permissions to database objects.

   ```sql
   -- Create a user role
   CREATE ROLE read_only WITH LOGIN PASSWORD 'password';

   -- Grant read-only access to a table
   GRANT SELECT ON your_table TO read_only;
   ```

### 4. **Advanced SQL Queries**
   - Write advanced SQL queries using window functions, recursive queries, and CTEs.

   ```sql
   -- Example: Using a window function
   SELECT id, name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank
   FROM employees;
   ```

### 6. **Database Monitoring**
   - Use PostgreSQL's built-in tools to monitor database performance.

   ```sql
   -- View active queries
   SELECT * FROM pg_stat_activity;

   -- Analyze table statistics
   SELECT * FROM pg_stat_user_tables;
   ```

### 7. **Using Extensions**
   - Install and use PostgreSQL extensions like `pgcrypto` or `postgis`.

   ```sql
   -- Install the pgcrypto extension
   CREATE EXTENSION pgcrypto;

   -- Example: Encrypt data
   INSERT INTO users (username, password) VALUES ('alice', crypt('password', gen_salt('bf')));
   ```

### 8. **Automating Tasks with Cron Jobs**
   - Automate database maintenance tasks (e.g., backups) using cron jobs.

   ```bash
   # Example: Schedule a daily backup at 2 AM
   0 2 * * * pg_dump -U postgres -d your_database_name -f /backups/backup_$(date +\%F).sql
   ```

### 9. **Database Testing**
   - Write unit tests for your database using `pgTAP`.

   ```sql
   -- Example: Test if a table exists
   SELECT * FROM tap.plan(1);
   SELECT tap.has_table('public', 'your_table', 'Table should exist');
   SELECT * FROM tap.finish();
   ```

---

## Troubleshooting

### 1. **Connection Issues**
   - **Problem**: Unable to connect to the PostgreSQL or pgAdmin container.
   - **Solution**:  
     - Ensure both the PostgreSQL and pgAdmin containers are running. You can check their status by running:
       ```bash
       docker ps
       ```
     - Verify that you have the correct container names. If you are unsure of the names, you can list all containers (running and stopped) with:
       ```bash
       docker ps -a
       ```
     - Ensure that the correct ports are mapped (e.g., `5432:5432` for PostgreSQL and `5050:80` for pgAdmin).
     - Verify that the `postgres` container's name is used in pgAdmin's connection settings.
     - If using `localhost` and experiencing connection issues, try using the container name instead (e.g., `postgres`).
     - Check the logs for any error messages:
       ```bash
       docker logs postgres
       docker logs pgadmin
       ```
     - If you are still having trouble, try restarting the containers:
       ```bash
       docker restart postgres
       docker restart pgadmin
       ```

### 2. **Forgot Password**
   - **Problem**: You've forgotten the password for pgAdmin or PostgreSQL.
   - **Solution**:
     - For pgAdmin:
       1. Stop the pgAdmin container:
          ```bash
          docker stop pgadmin
          ```
       2. Restart the container with a new password:
          ```bash
          docker run --name pgadmin -d -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=admin@example.com -e PGADMIN_DEFAULT_PASSWORD=new_password dpage/pgadmin4:latest
          ```
     - For PostgreSQL:
       1. If you've forgotten the `POSTGRES_PASSWORD` for PostgreSQL, you’ll need to reset it. First, stop the container:
          ```bash
          docker stop postgres
          ```
       2. Restart it with a new password:
          ```bash
          docker run --name postgres -e POSTGRES_PASSWORD=new_password -d -p 5432:5432 -v postgres_data:/var/lib/postgresql/data postgres
          ```

### 3. **Port Conflicts**
   - **Problem**: Port is already in use on the host machine (e.g., port 5432 or 5050).
   - **Solution**:  
     - If a port conflict occurs (for example, PostgreSQL's default port `5432` is already in use), you can map a different host port to the container's port by changing the `-p` flag:
       ```bash
       docker run --name postgres -e POSTGRES_PASSWORD=your_password -d -p 5433:5432 -v postgres_data:/var/lib/postgresql/data postgres
       ```
       This would map PostgreSQL’s internal `5432` to the host’s `5433` port.
     - Similarly, for pgAdmin, you can use a different port:
       ```bash
       docker run --name pgadmin -d -p 5051:80 -e PGADMIN_DEFAULT_EMAIL=admin@example.com -e PGADMIN_DEFAULT_PASSWORD=admin dpage/pgadmin4:latest
       ```

### 4. **Unable to Access pgAdmin in Browser**
   - **Problem**: You cannot access pgAdmin through `http://localhost:5050` (or other port you have set).
   - **Solution**:
     - Ensure the pgAdmin container is running:
       ```bash
       docker ps
       ```
     - Double-check that the port mapping is correct and no firewall is blocking the port.
     - If using a non-default port (e.g., `5051` instead of `5050`), ensure you access it by visiting `http://localhost:5051` instead.

### 5. **Data Persistence Issue**
   - **Problem**: After stopping or removing the PostgreSQL container, the data is lost.
   - **Solution**:
     - Ensure that you are using a Docker volume for data persistence. When starting the container, use the `-v` flag to map the volume:
       ```bash
       docker run --name postgres -e POSTGRES_PASSWORD=your_password -d -p 5432:5432 -v postgres_data:/var/lib/postgresql/data postgres
       ```
     - To inspect or back up the volume:
       ```bash
       docker volume inspect postgres_data
       ```

### 6. **Accessing pgAdmin with Docker Network**
   - **Problem**: If you are trying to connect from pgAdmin to PostgreSQL and the connection is unsuccessful.
   - **Solution**:
     - Make sure both containers (PostgreSQL and pgAdmin) are on the same Docker network:
       ```bash
       docker network create pg_network
       docker run --name postgres --network pg_network -e POSTGRES_PASSWORD=your_password -d -p 5432:5432 -v postgres_data:/var/lib/postgresql/data postgres
       docker run --name pgadmin --network pg_network -d -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=admin@example.com -e PGADMIN_DEFAULT_PASSWORD=admin dpage/pgadmin4:latest
       ```
     - This ensures that both containers can communicate over the internal network created by Docker.

---


## 👇 Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

