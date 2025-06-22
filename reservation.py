from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                           QDialog, QFormLayout, QLineEdit, QMessageBox, QCalendarWidget,
                           QDateEdit)
from PyQt5.QtCore import Qt, QDate
from db_config import DatabaseConnection
import datetime

class ReservationDialog(QDialog):
    def __init__(self, parent=None, reservation_data=None):
        super().__init__(parent)
        self.reservation_data = reservation_data
        self.db = DatabaseConnection()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Add/Edit Reservation")
        self.setMinimumWidth(400)
        layout = QFormLayout(self)
        
        # Guest Information
        self.guest_name = QLineEdit()
        layout.addRow("Guest Name:", self.guest_name)
        
        self.guest_email = QLineEdit()
        layout.addRow("Email:", self.guest_email)
        
        self.guest_phone = QLineEdit()
        layout.addRow("Phone:", self.guest_phone)
        
        # Room Selection
        self.room_combo = QComboBox()
        self.load_available_rooms()
        layout.addRow("Room:", self.room_combo)
        
        # Dates
        self.check_in = QDateEdit()
        self.check_in.setCalendarPopup(True)
        self.check_in.setDate(QDate.currentDate())
        layout.addRow("Check-in Date:", self.check_in)
        
        self.check_out = QDateEdit()
        self.check_out.setCalendarPopup(True)
        self.check_out.setDate(QDate.currentDate().addDays(1))
        layout.addRow("Check-out Date:", self.check_out)
        
        # Status
        self.status = QComboBox()
        self.status.addItems(["booked", "checked-in", "checked-out", "cancelled"])
        layout.addRow("Status:", self.status)
        
        # Buttons
        buttons = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)
        
        if self.reservation_data:
            self.populate_data()
    
    def load_available_rooms(self):
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT r.RoomId, CONCAT(r.RoomNumber, ' - ', rt.TypeName, ' ($', r.PricePerNight, ')')
                FROM Room r
                JOIN RoomType rt ON r.RoomTypeId = rt.RoomTypeId
                WHERE r.AvailabilityStatus = 'Available'
                ORDER BY r.RoomNumber
            """)
            rooms = cur.fetchall()
            self.room_combo.clear()
            for room_id, room_desc in rooms:
                self.room_combo.addItem(room_desc, room_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load rooms: {str(e)}")
    
    def populate_data(self):
        self.guest_name.setText(self.reservation_data['guest_name'])
        self.guest_email.setText(self.reservation_data['guest_email'])
        self.guest_phone.setText(self.reservation_data['guest_phone'])
        
        index = self.room_combo.findData(self.reservation_data['room_id'])
        if index >= 0:
            self.room_combo.setCurrentIndex(index)
            
        self.check_in.setDate(QDate.fromString(self.reservation_data['check_in'], Qt.ISODate))
        self.check_out.setDate(QDate.fromString(self.reservation_data['check_out'], Qt.ISODate))
        self.status.setCurrentText(self.reservation_data['status'])

class ReservationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.setup_ui()
        self.load_reservation()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("New Reservation")
        self.edit_btn = QPushButton("Edit Reservation")
        self.delete_btn = QPushButton("Cancel Reservation")
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
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Reservation ID", "Guest Name", "Room", "Check-in", 
            "Check-out", "Status", "Email", "Phone"
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
        self.add_btn.clicked.connect(self.add_reservation)
        self.edit_btn.clicked.connect(self.edit_reservation)
        self.delete_btn.clicked.connect(self.cancel_reservation)
        self.refresh_btn.clicked.connect(self.load_reservation)
    
    def load_reservation(self):
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    r.reservation_id,
                    g.full_name,
                    rm.RoomNumber,
                    r.start_date,
                    r.end_date,
                    r.status,
                    g.email,
                    g.phone
                FROM reservation r
                JOIN Guests g ON r.guest_id = g.guest_id
                JOIN Room rm ON r.roomId = rm.RoomId
                ORDER BY r.start_date DESC
            """)
            reservation = cur.fetchall()
            
            self.table.setRowCount(len(reservation))
            for row, res in enumerate(reservation):
                for col, value in enumerate(res):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(row, col, item)
            
            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load reservation: {str(e)}")
    
    def add_reservation(self):
        dialog = ReservationDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            conn = None
            try:
                # Validate dates
                check_in = dialog.check_in.date()
                check_out = dialog.check_out.date()
                if check_in >= check_out:
                    QMessageBox.warning(self, "Warning", "Check-out date must be after check-in date!")
                    return
                
                conn = self.db.get_connection()
                cur = conn.cursor()
                
                # Begin transaction
                cur.execute("BEGIN")
                
                # First check if the guest already exists
                cur.execute("""
                    SELECT guest_id FROM Guests
                    WHERE email = %s
                """, (dialog.guest_email.text(),))
                
                result = cur.fetchone()
                if result:
                    guest_id = result[0]
                    # Update existing guest info
                    cur.execute("""
                        UPDATE Guests 
                        SET full_name = %s, phone = %s
                        WHERE guest_id = %s
                    """, (
                        dialog.guest_name.text(),
                        dialog.guest_phone.text(),
                        guest_id
                    ))
                else:
                    # Create new guest
                    cur.execute("""
                        INSERT INTO Guests (full_name, email, phone)
                        VALUES (%s, %s, %s)
                        RETURNING guest_id
                    """, (
                        dialog.guest_name.text(),
                        dialog.guest_email.text(),
                        dialog.guest_phone.text()
                    ))
                    guest_id = cur.fetchone()[0]
                
                # Check room availability for the selected dates
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM reservation
                    WHERE roomId = %s 
                    AND status = 'booked'
                    AND NOT (end_date <= %s OR start_date >= %s)
                """, (
                    dialog.room_combo.currentData(),
                    check_in.toString(Qt.ISODate),
                    check_out.toString(Qt.ISODate)
                ))
                
                if cur.fetchone()[0] > 0:
                    cur.execute("ROLLBACK")
                    QMessageBox.warning(self, "Warning", 
                                    "Room is not available for the selected dates!")
                    return
                
                # Get next reservation ID
                cur.execute("SELECT COALESCE(MAX(reservation_id), 0) + 1 FROM reservation")
                reservation_id = cur.fetchone()[0]
                
                # Create reservation
                cur.execute("""
                    INSERT INTO reservation (reservation_id, guest_id, roomId, start_date, end_date, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    reservation_id,
                    guest_id,
                    dialog.room_combo.currentData(),
                    check_in.toString(Qt.ISODate),
                    check_out.toString(Qt.ISODate),
                    dialog.status.currentText()
                ))
                
                conn.commit()
                self.load_reservation()
                QMessageBox.information(self, "Success", "Reservation created successfully!")
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Error", f"Failed to create reservation: {str(e)}")
    
    def edit_reservation(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a reservation to edit.")
            return

        try:
            reservation_id = int(self.table.item(current_row, 0).text())
            
            # Fetch current reservation data from database
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT r.reservation_id, g.full_name, g.email, g.phone,
                       r.roomId, r.start_date, r.end_date, r.status
                FROM reservation r
                JOIN Guests g ON r.guest_id = g.guest_id
                WHERE r.reservation_id = %s
            """, (reservation_id,))
            
            result = cur.fetchone()
            if not result:
                QMessageBox.warning(self, "Error", "Reservation not found in database!")
                return
                
            reservation_data = {
                'reservation_id': result[0],
                'guest_name': result[1],
                'guest_email': result[2],
                'guest_phone': result[3],
                'room_id': result[4],
                'check_in': str(result[5]),
                'check_out': str(result[6]),
                'status': result[7]
            }
            
            dialog = ReservationDialog(self, reservation_data)
            if dialog.exec_() == QDialog.Accepted:
                # Check room availability for the selected dates (excluding current reservation)
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM reservation
                    WHERE roomId = %s 
                    AND status = 'booked'
                    AND reservation_id != %s
                    AND (
                        (start_date <= %s AND end_date >= %s)
                        OR (start_date <= %s AND end_date >= %s)
                        OR (start_date >= %s AND end_date <= %s)
                    )
                """, (
                    dialog.room_combo.currentData(),
                    reservation_id,
                    dialog.check_in.date().toString(Qt.ISODate),
                    dialog.check_in.date().toString(Qt.ISODate),
                    dialog.check_out.date().toString(Qt.ISODate),
                    dialog.check_out.date().toString(Qt.ISODate),
                    dialog.check_in.date().toString(Qt.ISODate),
                    dialog.check_out.date().toString(Qt.ISODate)
                ))
                
                if cur.fetchone()[0] > 0:
                    QMessageBox.warning(self, "Warning", 
                                    "Room is not available for the selected dates!")
                    return
                
                # Update guest information
                cur.execute("""
                    UPDATE Guests 
                    SET full_name = %s, phone = %s
                    WHERE email = %s
                """, (
                    dialog.guest_name.text(),
                    dialog.guest_phone.text(),
                    dialog.guest_email.text()
                ))
                
                # Update reservation
                cur.execute("""
                    UPDATE reservation
                    SET roomId = %s, start_date = %s, end_date = %s, status = %s
                    WHERE reservation_id = %s
                """, (
                    dialog.room_combo.currentData(),
                    dialog.check_in.date().toString(Qt.ISODate),
                    dialog.check_out.date().toString(Qt.ISODate),
                    dialog.status.currentText(),
                    reservation_id
                ))
                
                conn.commit()
                self.load_reservation()
                QMessageBox.information(self, "Success", "Reservation updated successfully!")
                
        except Exception as e:
            if 'conn' in locals() and conn:
                conn.rollback()
            QMessageBox.critical(self, "Error", f"Failed to update reservation: {str(e)}")
        
    
    def cancel_reservation(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a reservation to cancel.")
            return
        
        reservation_id = self.table.item(current_row, 0).text()
        guest_name = self.table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirm Cancellation",
            f"Are you sure you want to cancel the reservation for {guest_name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                conn = self.db.get_connection()
                cur = conn.cursor()
                cur.execute("""
                    UPDATE reservation 
                    SET status = 'cancelled'
                    WHERE reservation_id = %s
                """, (reservation_id,))
                conn.commit()
                self.load_reservation()
                QMessageBox.information(self, "Success", "Reservation cancelled successfully!")
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Error", f"Failed to cancel reservation: {str(e)}")
