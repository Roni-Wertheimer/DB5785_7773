from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                           QDialog, QFormLayout, QLineEdit, QMessageBox, QSpinBox,
                           QDoubleSpinBox)
from PyQt5.QtCore import Qt
from db_config import DatabaseConnection

class RoomDialog(QDialog):
    def __init__(self, parent=None, room_data=None):
        super().__init__(parent)
        self.room_data = room_data
        self.db = DatabaseConnection()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Add/Edit Room")
        layout = QFormLayout(self)
        
        # Room Number
        self.room_number = QSpinBox()
        self.room_number.setRange(1, 9999)
        layout.addRow("Room Number:", self.room_number)
        
        # Price Per Night
        self.price = QDoubleSpinBox()
        self.price.setRange(0, 99999.99)
        self.price.setDecimals(2)
        layout.addRow("Price per Night:", self.price)
        
        # Floor
        self.floor = QSpinBox()
        self.floor.setRange(1, 99)
        layout.addRow("Floor:", self.floor)
        
        # Room Type
        self.room_type = QComboBox()
        self.load_room_types()
        layout.addRow("Room Type:", self.room_type)
        
        # Status
        self.status = QComboBox()
        self.status.addItems(["Available", "Occupied", "Maintenance"])
        layout.addRow("Availability Status:", self.status)
        
        # Cleaning Status
        self.cleaning = QComboBox()
        self.cleaning.addItems(["Clean", "Dirty", "Being Cleaned"])
        layout.addRow("Cleaning Status:", self.cleaning)
        
        # Buttons
        buttons = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)
        
        if self.room_data:
            self.populate_data()

    def load_room_types(self):
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()

            # Get one RoomTypeId per distinct TypeName
            cur.execute("""
                SELECT DISTINCT ON (TypeName) RoomTypeId, TypeName
                FROM RoomType
                ORDER BY TypeName
            """)
            room_types = cur.fetchall()

            self.room_type.clear()
            for type_id, type_name in room_types:
                self.room_type.addItem(type_name, type_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load room types: {str(e)}")

    def populate_data(self):
        self.room_number.setValue(self.room_data['room_number'])
        self.price.setValue(float(self.room_data['price']))
        self.floor.setValue(self.room_data['floor'])
        index = self.room_type.findData(self.room_data['room_type_id'])
        if index >= 0:
            self.room_type.setCurrentIndex(index)
        self.status.setCurrentText(self.room_data['status'])
        self.cleaning.setCurrentText(self.room_data['cleaning'])

class RoomsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.setup_ui()
        self.load_rooms()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Room")
        self.edit_btn = QPushButton("Edit Room")
        self.delete_btn = QPushButton("Delete Room")
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
            "Room ID", "Room Number", "Floor", "Room Type", 
            "Price/Night", "Status", "Cleaning Status"
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
        self.add_btn.clicked.connect(self.add_room)
        self.edit_btn.clicked.connect(self.edit_room)
        self.delete_btn.clicked.connect(self.delete_room)
        self.refresh_btn.clicked.connect(self.load_rooms)
    
    def load_rooms(self):
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT r.RoomId, r.RoomNumber, r.Floor, rt.TypeName, 
                       r.PricePerNight, r.AvailabilityStatus, r.CleaningStatus
                FROM Room r
                JOIN RoomType rt ON r.RoomTypeId = rt.RoomTypeId
                ORDER BY r.RoomNumber
            """)
            rooms = cur.fetchall()
            
            self.table.setRowCount(len(rooms))
            for row, room in enumerate(rooms):
                for col, value in enumerate(room):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(row, col, item)
            
            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load rooms: {str(e)}")
    
    def add_room(self):
        dialog = RoomDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            conn = None
            try:
                conn = self.db.get_connection()
                cur = conn.cursor()
                
                # First check if room number already exists
                cur.execute("SELECT COUNT(*) FROM Room WHERE RoomNumber = %s", 
                          (dialog.room_number.value(),))
                if cur.fetchone()[0] > 0:
                    QMessageBox.warning(self, "Warning", 
                                      "A room with this number already exists!")
                    return
                
                # Get next room ID
                cur.execute("SELECT COALESCE(MAX(RoomId), 0) + 1 FROM Room")
                room_id = cur.fetchone()[0]
                
                cur.execute("""
                    INSERT INTO Room (RoomId, RoomNumber, PricePerNight, AvailabilityStatus, 
                                    CleaningStatus, Floor, RoomTypeId)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    room_id,
                    dialog.room_number.value(),
                    dialog.price.value(),
                    dialog.status.currentText(),
                    dialog.cleaning.currentText(),
                    dialog.floor.value(),
                    dialog.room_type.currentData()
                ))
                
                conn.commit()
                self.load_rooms()
                QMessageBox.information(self, "Success", "Room added successfully!")
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Error", f"Failed to add room: {str(e)}")
    
    def edit_room(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a room to edit.")
            return

        conn = None
        try:
            room_id = int(self.table.item(current_row, 0).text())
            
            # Fetch current room data from database
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT r.RoomId, r.RoomNumber, r.Floor, r.RoomTypeId,
                       r.PricePerNight, r.AvailabilityStatus, r.CleaningStatus
                FROM Room r
                WHERE r.RoomId = %s
            """, (room_id,))
            
            result = cur.fetchone()
            if not result:
                QMessageBox.warning(self, "Error", "Room not found in database!")
                return
                
            # Check if room is available for editing
            cur.execute("""
                SELECT COUNT(*) FROM reservation
                WHERE roomId = %s AND status = 'booked'
                AND CURRENT_DATE BETWEEN start_date AND end_date
            """, (room_id,))
            
            if cur.fetchone()[0] > 0:
                QMessageBox.warning(self, "Error", "Cannot edit room - currently occupied!")
                return
                
            room_data = {
                'room_id': result[0],
                'room_number': result[1],
                'floor': result[2],
                'room_type_id': result[3],
                'price': float(result[4]),
                'status': result[5],
                'cleaning': result[6]
            }
            
            dialog = RoomDialog(self, room_data)
            if dialog.exec_() == QDialog.Accepted:
                cur.execute("""
                    UPDATE Room 
                    SET RoomNumber = %s, PricePerNight = %s, AvailabilityStatus = %s,
                        CleaningStatus = %s, Floor = %s, RoomTypeId = %s
                    WHERE RoomId = %s
                """, (
                    dialog.room_number.value(),
                    dialog.price.value(),
                    dialog.status.currentText(),
                    dialog.cleaning.currentText(),
                    dialog.floor.value(),
                    dialog.room_type.currentData(),
                    room_data['room_id']
                ))
                conn.commit()
                self.load_rooms()
                QMessageBox.information(self, "Success", "Room updated successfully!")
            
        except Exception as e:
            if 'conn' in locals() and conn:
                conn.rollback()
            QMessageBox.critical(self, "Error", f"Failed to update room: {str(e)}")
        
    
    def delete_room(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a room to delete.")
            return
        
        room_id = self.table.item(current_row, 0).text()
        room_number = self.table.item(current_row, 1).text()
        
        reply = QMessageBox.question(self, "Confirm Delete",
                                   f"Are you sure you want to delete Room {room_number}?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = self.db.get_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM Room WHERE RoomId = %s", (room_id,))
                conn.commit()
                self.load_rooms()
                QMessageBox.information(self, "Success", "Room deleted successfully!")
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Error", f"Failed to delete room: {str(e)}")
