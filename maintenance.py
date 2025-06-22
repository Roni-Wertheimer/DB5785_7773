from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                           QDialog, QFormLayout, QLineEdit, QMessageBox, QTextEdit,
                           QDateEdit)
from PyQt5.QtCore import Qt, QDate
from db_config import DatabaseConnection
import datetime

class MaintenanceRequestDialog(QDialog):
    def __init__(self, parent=None, request_data=None):
        super().__init__(parent)
        self.request_data = request_data
        self.db = DatabaseConnection()
        self.setup_ui()
        if not self.request_data:
            self.get_next_request_id()
        
    def setup_ui(self):
        self.setWindowTitle("Add/Edit Maintenance Request")
        self.setMinimumWidth(400)
        layout = QFormLayout(self)
        
        # Request ID display (read-only)
        self.request_id_display = QLineEdit()
        self.request_id_display.setReadOnly(True)
        layout.addRow("Request ID:", self.request_id_display)
        
        # Room Selection
        self.room_combo = QComboBox()
        self.load_rooms()
        layout.addRow("Room:", self.room_combo)
        
        # Description
        self.description = QTextEdit()
        self.description.setMinimumHeight(100)
        layout.addRow("Issue Description:", self.description)
        
        # Status
        self.status = QComboBox()
        self.status.addItems(["Pending", "In Progress", "Completed", "Cancelled"])
        layout.addRow("Status:", self.status)
        
        # Staff Assignment
        self.staff_combo = QComboBox()
        self.load_maintenance_staff()
        layout.addRow("Assign To:", self.staff_combo)
        
        # Buttons
        buttons = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)
        
        if self.request_data:
            self.populate_data()
    
    def get_next_request_id(self):
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT COALESCE(MAX(RequestId), 0) + 1 FROM MaintenanceRequest")
            next_id = cur.fetchone()[0]
            self.request_id_display.setText(str(next_id))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate request ID: {str(e)}")
    
    def load_rooms(self):
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT r.RoomId, CONCAT(r.RoomNumber, ' - Floor ', r.Floor)
                FROM Room r
                ORDER BY r.RoomNumber
            """)
            rooms = cur.fetchall()
            self.room_combo.clear()
            for room_id, room_desc in rooms:
                self.room_combo.addItem(room_desc, room_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load rooms: {str(e)}")
    
    def load_maintenance_staff(self):
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            # Get current request ID if editing
            request_id = self.request_data['request_id'] if self.request_data else None

            # Get available maintenance staff (refcursor to record)
            cur.execute("""
                            SELECT get_available_cleaners();
                            FETCH ALL FROM cleaners_cursor;
            """)
            staff = cur.fetchall()
            cur.execute("CLOSE cleaners_cursor;")
            self.staff_combo.clear()
            self.staff_combo.addItem("-- Select Staff --", None)
            for staff_row in staff:
                staff_id = staff_row[0]
                staff_name = f"{staff_row[1]} {staff_row[2]}"  # Assuming columns: id, first_name, last_name
                self.staff_combo.addItem(staff_name, staff_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load staff: {str(e)}")
    
    def populate_data(self):
        self.request_id_display.setText(str(self.request_data['request_id']))
        self.description.setText(self.request_data['description'])
        self.status.setCurrentText(self.request_data['status'])
        
        room_index = self.room_combo.findData(self.request_data['room_id'])
        if room_index >= 0:
            self.room_combo.setCurrentIndex(room_index)
        
        staff_index = self.staff_combo.findData(self.request_data['staff_id'])
        if staff_index >= 0:
            self.staff_combo.setCurrentIndex(staff_index)
        else:
            self.staff_combo.setCurrentIndex(0)

class MaintenanceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.setup_ui()
        self.load_requests()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("New Request")
        self.edit_btn = QPushButton("Edit Request")
        self.complete_btn = QPushButton("Mark Complete")
        self.refresh_btn = QPushButton("Refresh")
        
        for btn in [self.add_btn, self.edit_btn, self.complete_btn, self.refresh_btn]:
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
            "Request ID", "Room", "Description", "Status", 
            "Request Date", "Assigned To", "Room ID"
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
        self.table.setColumnHidden(6, True)  # Hide Room ID column
        layout.addWidget(self.table)
        
        # Connect signals
        self.add_btn.clicked.connect(self.add_request)
        self.edit_btn.clicked.connect(self.edit_request)
        self.complete_btn.clicked.connect(self.complete_request)
        self.refresh_btn.clicked.connect(self.load_requests)
    
    def load_requests(self):
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    mr.RequestId,
                    r.RoomNumber,
                    mr.IssueDescription,
                    mr.Status,
                    mr.RequestDate,
                    COALESCE(s.FirstName || ' ' || s.LastName, 'Unassigned') as AssignedTo,
                    r.RoomId
                FROM MaintenanceRequest mr
                JOIN Room r ON mr.RoomId = r.RoomId
                LEFT JOIN AssignMaintenanceStaff ams ON mr.RequestId = ams.RequestId
                LEFT JOIN Staff s ON ams.StaffId = s.StaffId
                ORDER BY 
                    CASE 
                        WHEN mr.Status = 'Pending' THEN 1
                        WHEN mr.Status = 'In Progress' THEN 2
                        ELSE 3
                    END,
                    mr.RequestDate DESC
            """)
            requests = cur.fetchall()
            
            self.table.setRowCount(len(requests))
            for row, req in enumerate(requests):
                for col, value in enumerate(req):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(row, col, item)
            
            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load maintenance requests: {str(e)}")
    
    def add_request(self):
        dialog = MaintenanceRequestDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            conn = None
            try:
                conn = self.db.get_connection()
                cur = conn.cursor()
                
                # Begin transaction
                cur.execute("BEGIN")
                request_id = int(dialog.request_id_display.text())
                
                # Create maintenance request with specified ID
                cur.execute("""
                    INSERT INTO MaintenanceRequest (RequestId, RoomId, IssueDescription, RequestDate, Status)
                    VALUES (%s, %s, %s, CURRENT_DATE, %s)
                """, (
                    request_id,
                    dialog.room_combo.currentData(),
                    dialog.description.toPlainText(),
                    dialog.status.currentText()
                ))
                
                # Assign staff if selected
                if dialog.staff_combo.currentData():
                    cur.execute("""
                        INSERT INTO AssignMaintenanceStaff (RequestId, StaffId)
                        VALUES (%s, %s)
                    """, (request_id, dialog.staff_combo.currentData()))
                
                conn.commit()
                self.load_requests()
                QMessageBox.information(self, "Success", f"Maintenance request created successfully with ID: {request_id}")
            except Exception as e:
                if conn:
                    conn.rollback()
                QMessageBox.critical(self, "Error", f"Failed to create maintenance request: {str(e)}")
    
    def edit_request(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a request to edit.")
            return
        
        conn = None
        try:
            request_id = int(self.table.item(current_row, 0).text())
            room_id = int(self.table.item(current_row, 6).text())
            
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT mr.RequestId, mr.RoomId, mr.IssueDescription, mr.Status,
                       ams.StaffId
                FROM MaintenanceRequest mr
                LEFT JOIN AssignMaintenanceStaff ams ON mr.RequestId = ams.RequestId
                WHERE mr.RequestId = %s
            """, (request_id,))
            
            result = cur.fetchone()
            if not result:
                QMessageBox.warning(self, "Error", "Request not found in database!")
                return
            
            request_data = {
                'request_id': result[0],
                'room_id': result[1],
                'description': result[2],
                'status': result[3],
                'staff_id': result[4] if result[4] else None
            }
            
            dialog = MaintenanceRequestDialog(self, request_data)
            if dialog.exec_() == QDialog.Accepted:
                cur.execute("BEGIN")
                
                try:
                    # Update request status first
                    cur.execute("""
                        UPDATE MaintenanceRequest 
                        SET RoomId = %s, 
                            IssueDescription = %s, 
                            Status = %s
                        WHERE RequestId = %s
                        RETURNING RequestId
                    """, (
                        dialog.room_combo.currentData(),
                        dialog.description.toPlainText(),
                        dialog.status.currentText(),
                        request_id
                    ))
                    
                    if not cur.fetchone():
                        raise Exception("Request not found")
                    
                    # Handle staff assignment
                    if dialog.staff_combo.currentData():
                        cur.execute("""
                            INSERT INTO AssignMaintenanceStaff (RequestId, StaffId)
                            VALUES (%s, %s)
                            ON CONFLICT (RequestId) 
                            DO UPDATE SET StaffId = EXCLUDED.StaffId
                        """, (request_id, dialog.staff_combo.currentData()))
                    else:
                        # Only remove staff assignment if not completed
                        if dialog.status.currentText() != 'Completed':
                            cur.execute("""
                                DELETE FROM AssignMaintenanceStaff
                                WHERE RequestId = %s
                            """, (request_id,))
                    
                    conn.commit()
                    self.load_requests()
                    QMessageBox.information(self, "Success", "Maintenance request updated successfully!")
                    
                except Exception as e:
                    cur.execute("ROLLBACK")
                    raise e
                    
        except Exception as e:
            if conn:
                conn.rollback()
            QMessageBox.critical(self, "Error", f"Failed to update maintenance request: {str(e)}")
    
    def complete_request(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a request to mark as complete.")
            return
        
        request_id = self.table.item(current_row, 0).text()
        room_number = self.table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirm Completion",
            f"Mark maintenance request for Room {room_number} as completed?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                conn = self.db.get_connection()
                cur = conn.cursor()
                cur.execute("""
                    UPDATE MaintenanceRequest 
                    SET Status = 'Completed'
                    WHERE RequestId = %s
                """, (request_id,))
                conn.commit()
                self.load_requests()
                QMessageBox.information(self, "Success", "Request marked as completed!")
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Error", f"Failed to update request: {str(e)}")
