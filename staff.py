from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                           QDialog, QFormLayout, QLineEdit, QMessageBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from db_config import DatabaseConnection

class StaffDialog(QDialog):
    def __init__(self, parent=None, staff_data=None):
        super().__init__(parent)
        self.staff_data = staff_data
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Add/Edit Staff")
        layout = QFormLayout(self)
        
        # Staff ID display (read-only)
        self.staff_id_display = QLineEdit()
        self.staff_id_display.setReadOnly(True)
        layout.addRow("Staff ID:", self.staff_id_display)
        
        # First Name
        self.first_name = QLineEdit()
        layout.addRow("First Name:", self.first_name)
        
        # Last Name
        self.last_name = QLineEdit()
        layout.addRow("Last Name:", self.last_name)
        
        # Role
        self.role = QComboBox()
        self.role.addItems(["Manager", "Receptionist", "Housekeeping", "Maintenance"])
        layout.addRow("Role:", self.role)
        
        # Phone Number
        self.phone = QLineEdit()
        layout.addRow("Phone Number:", self.phone)
        
        # Employment Date
        self.employment_date = QDateEdit()
        self.employment_date.setCalendarPopup(True)
        self.employment_date.setDate(QDate.currentDate())
        layout.addRow("Employment Date:", self.employment_date)
        
        # Active Status
        self.is_active = QComboBox()
        self.is_active.addItems(["Active", "Inactive"])
        layout.addRow("Status:", self.is_active)
        
        # Buttons
        buttons = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)
        
        if self.staff_data:
            self.populate_data()
        else:
            # For new staff, get and display next available ID
            self.get_next_staff_id()
    
    def get_next_staff_id(self):
        try:
            conn = DatabaseConnection().get_connection()
            cur = conn.cursor()
            cur.execute("SELECT COALESCE(MAX(StaffId), 0) + 1 FROM Staff")
            next_id = cur.fetchone()[0]
            self.staff_id_display.setText(str(next_id))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate staff ID: {str(e)}")
    
    def populate_data(self):
        self.staff_id_display.setText(str(self.staff_data['staff_id']))
        self.first_name.setText(self.staff_data['first_name'])
        self.last_name.setText(self.staff_data['last_name'])
        self.role.setCurrentText(self.staff_data['role'])
        self.phone.setText(self.staff_data['phone'])
        self.employment_date.setDate(QDate.fromString(self.staff_data['employment_date'], Qt.ISODate))
        self.is_active.setCurrentText("Active" if self.staff_data['is_active'] else "Inactive")

class StaffWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.setup_ui()
        self.load_staff()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Staff")
        self.edit_btn = QPushButton("Edit Staff")
        self.delete_btn = QPushButton("Delete Staff")
        self.refresh_btn = QPushButton("Refresh")
        
        for btn in [self.add_btn, self.edit_btn, self.delete_btn, self.refresh_btn]:
            button_layout.addWidget(btn)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #34495e;
                    color: white;
                    padding: 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #3498db;
                }
            """)
        
        layout.addLayout(button_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Staff ID", "First Name", "Last Name", "Role", 
            "Phone", "Employment Date", "Status"
        ])
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #2c3e50;
                border: 1px solid #2c3e50;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 6px;
                border: 1px solid #2c3e50;
            }
        """)
        layout.addWidget(self.table)
        
        # Connect signals
        self.add_btn.clicked.connect(self.add_staff)
        self.edit_btn.clicked.connect(self.edit_staff)
        self.delete_btn.clicked.connect(self.delete_staff)
        self.refresh_btn.clicked.connect(self.load_staff)
    
    def load_staff(self):
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT StaffId, FirstName, LastName, Role, PhoneNumber, 
                       EmploymentDate, CASE WHEN IsActive THEN 'Active' ELSE 'Inactive' END
                FROM Staff
                ORDER BY LastName, FirstName
            """)
            staff = cur.fetchall()
            
            self.table.setRowCount(len(staff))
            for row, member in enumerate(staff):
                for col, value in enumerate(member):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(row, col, item)
            
            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load staff: {str(e)}")
    
    def add_staff(self):
        dialog = StaffDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            conn = None
            try:
                conn = self.db.get_connection()
                cur = conn.cursor()
                
                # Get the next staff ID from the display
                staff_id = int(dialog.staff_id_display.text())
                
                # Insert new staff member with the specified ID
                cur.execute("""
                    INSERT INTO Staff (StaffId, FirstName, LastName, Role, PhoneNumber, 
                                     EmploymentDate, IsActive)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    staff_id,
                    dialog.first_name.text(),
                    dialog.last_name.text(),
                    dialog.role.currentText(),
                    dialog.phone.text(),
                    dialog.employment_date.date().toString(Qt.ISODate),
                    dialog.is_active.currentText() == "Active"
                ))
                
                conn.commit()
                self.load_staff()
                QMessageBox.information(self, "Success", f"Staff member added successfully with ID: {staff_id}")
            except Exception as e:
                if conn:
                    conn.rollback()
                QMessageBox.critical(self, "Error", f"Failed to add staff member: {str(e)}")
    
    def edit_staff(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a staff member to edit.")
            return

        try:
            staff_id = int(self.table.item(current_row, 0).text())
            
            # Fetch current staff data from database
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT StaffId, FirstName, LastName, Role, PhoneNumber, 
                       EmploymentDate, IsActive
                FROM Staff
                WHERE StaffId = %s
            """, (staff_id,))
            
            result = cur.fetchone()
            if not result:
                QMessageBox.warning(self, "Error", "Staff member not found in database!")
                return
                
            staff_data = {
                'staff_id': result[0],
                'first_name': result[1],
                'last_name': result[2],
                'role': result[3],
                'phone': result[4],
                'employment_date': str(result[5]),
                'is_active': result[6]
            }
            
            dialog = StaffDialog(self, staff_data)
            if dialog.exec_() == QDialog.Accepted:
                cur.execute("""
                    UPDATE Staff 
                    SET FirstName = %s, LastName = %s, Role = %s,
                        PhoneNumber = %s, EmploymentDate = %s, IsActive = %s
                    WHERE StaffId = %s
                """, (
                    dialog.first_name.text(),
                    dialog.last_name.text(),
                    dialog.role.currentText(),
                    dialog.phone.text(),
                    dialog.employment_date.date().toString(Qt.ISODate),
                    dialog.is_active.currentText() == "Active",
                    staff_id
                ))
                conn.commit()
                self.load_staff()
                QMessageBox.information(self, "Success", "Staff member updated successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update staff member: {str(e)}")
        
    def delete_staff(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a staff member to delete.")
            return
        
        staff_id = self.table.item(current_row, 0).text()
        name = f"{self.table.item(current_row, 1).text()} {self.table.item(current_row, 2).text()}"
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete staff member {name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                conn = self.db.get_connection()
                cur = conn.cursor()
                
                # Begin transaction
                cur.execute("BEGIN")
                
                # Delete from AssignKeepingStaff
                cur.execute("""
                    DELETE FROM AssignKeepingStaff
                    WHERE StaffId = %s
                """, (staff_id,))
                
                # Delete from AssignMaintenanceStaff
                cur.execute("""
                    DELETE FROM AssignMaintenanceStaff
                    WHERE StaffId = %s
                """, (staff_id,))
                
                # Delete staff member
                cur.execute("""
                    DELETE FROM Staff
                    WHERE StaffId = %s
                """, (staff_id,))
                
                msg = "Staff member and all assignments deleted successfully!"
                cur.execute("COMMIT")
                
                conn.commit()
                self.load_staff()
                QMessageBox.information(self, "Success", msg)
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Error", f"Failed to delete staff member: {str(e)}")
