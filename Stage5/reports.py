from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                           QDateEdit, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from db_config import DatabaseConnection
import datetime

class ReportsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Report Selection
        selection_layout = QHBoxLayout()
        
        self.report_type = QComboBox()
        self.report_type.addItems([
            "Monthly Inventory Summary",
            "Open Maintenance Requests",
            "Rooms Due for Cleaning",
            "Recent Housekeeping Tasks",
            "Room Price Analysis",
            "Room Type Inventory Usage",
            "Run Maintenance Analysis",
            "Prepare Room"
        ])
        self.report_type.currentIndexChanged.connect(self.on_report_changed)
        selection_layout.addWidget(QLabel("Select Report:"))
        selection_layout.addWidget(self.report_type)
        
        # Room selection for prepare room procedure
        self.room_combo = QComboBox()
        self.room_combo.setVisible(False)
        self.load_rooms()
        selection_layout.addWidget(self.room_combo)
        
        # Date Range
        date_layout = QHBoxLayout()
        self.date_from = QDateEdit()
        self.date_to = QDateEdit()
        
        for date_edit in [self.date_from, self.date_to]:
            date_edit.setCalendarPopup(True)
        
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_to.setDate(QDate.currentDate())
        
        date_layout.addWidget(QLabel("From:"))
        date_layout.addWidget(self.date_from)
        date_layout.addWidget(QLabel("To:"))
        date_layout.addWidget(self.date_to)
        date_layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        self.generate_btn = QPushButton("Generate Report")
        self.export_btn = QPushButton("Export")
        
        for btn in [self.generate_btn, self.export_btn]:
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
            button_layout.addWidget(btn)
        
        # Table
        self.table = QTableWidget()
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
        
        # Add all layouts
        layout.addLayout(selection_layout)
        layout.addLayout(date_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        
        # Connect signals
        self.generate_btn.clicked.connect(self.generate_report)
        self.export_btn.clicked.connect(self.export_report)
        
        # Initialize first report
        self.on_report_changed()
    
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
    
    def on_report_changed(self):
        report_type = self.report_type.currentText()
        self.room_combo.setVisible(report_type == "Prepare Room")
        
        headers = {
            "Monthly Inventory Summary": ["Month", "Year", "Item Name", "Total Used"],
            "Open Maintenance Requests": ["Room Number", "Open Requests"],
            "Rooms Due for Cleaning": ["Room Number", "Floor"],
            "Recent Housekeeping Tasks": ["Task ID", "Task Date", "Month", "Year", "Room", "Floor", "Room Type", "Status", "Staff"],
            "Room Price Analysis": ["Room Number", "Current Price", "Base Price", "Room Type"],
            "Room Type Inventory Usage": ["Room Type", "Average Usage"]
        }
        
        if report_type in headers:
            self.table.setColumnCount(len(headers[report_type]))
            self.table.setHorizontalHeaderLabels(headers[report_type])
    
    def generate_report(self):
        try:
            report_type = self.report_type.currentText()
            conn = self.db.get_connection()
            cur = conn.cursor()


            if report_type == "Monthly Inventory Summary":
                cur.execute("""
                    SELECT 
                        EXTRACT(MONTH FROM H.TaskDate) AS Month,
                        EXTRACT(YEAR FROM H.TaskDate) AS Year,
                        IU.ItemName,
                        SUM(IU.Quantity) AS TotalUsed
                    FROM KeepingInventory KI
                    JOIN InventoryUsage IU ON KI.UsageId = IU.UsageId
                    JOIN Housekeeping H ON KI.TaskID = H.TaskID
                    GROUP BY Month, Year, IU.ItemName
                    ORDER BY Year, Month
                """)

            elif report_type == "Open Maintenance Requests":
                cur.execute("""
                    SELECT 
                        R.RoomNumber,
                        COUNT(M.RequestId) AS OpenRequests
                    FROM Room R
                    LEFT JOIN MaintenanceRequest M ON R.RoomId = M.RoomId 
                        AND (M.Status = 'Pending' OR M.Status = 'In Progress')
                    GROUP BY R.RoomNumber
                    ORDER BY OpenRequests DESC
                """)

            elif report_type == "Rooms Due for Cleaning":
                cur.execute("""
                    SELECT 
                        R.RoomNumber,
                        R.Floor
                    FROM Room R
                    LEFT JOIN Housekeeping H ON R.RoomId = H.RoomId 
                        AND H.TaskDate > CURRENT_DATE - INTERVAL '7 days'
                    WHERE H.TaskID IS NULL
                """)

            elif report_type == "Recent Housekeeping Tasks":
                cur.execute("""
                    SELECT 
                        H.TaskID,
                        H.TaskDate,
                        EXTRACT(MONTH FROM H.TaskDate) AS Month,
                        EXTRACT(YEAR FROM H.TaskDate) AS Year,
                        R.RoomNumber,
                        R.Floor,
                        RT.TypeName AS RoomType,
                        H.Status AS TaskStatus,
                        S.FirstName || ' ' || S.LastName AS StaffName
                    FROM Housekeeping H
                    JOIN Room R ON H.RoomId = R.RoomId
                    JOIN RoomType RT ON R.RoomTypeId = RT.RoomTypeId
                    JOIN AssignKeepingStaff AK ON H.TaskID = AK.TaskID
                    JOIN Staff S ON AK.StaffId = S.StaffId
                    WHERE H.TaskDate >= CURRENT_DATE - INTERVAL '3 months'
                    ORDER BY H.TaskDate DESC, R.RoomNumber
                """)

            elif report_type == "Room Price Analysis":
                cur.execute("""
                    SELECT 
                        R.RoomNumber,
                        R.PricePerNight,
                        RT.BasePrice,
                        RT.TypeName
                    FROM Room R
                    JOIN RoomType RT ON R.RoomTypeId = RT.RoomTypeId
                    WHERE R.PricePerNight > RT.BasePrice
                """)
                
            elif report_type == "Room Type Inventory Usage":
                cur.execute("""
                    SELECT 
                        RT.TypeName,
                        AVG(IU.Quantity) AS AvgUsage
                    FROM Room R
                    JOIN RoomType RT ON R.RoomTypeId = RT.RoomTypeId
                    JOIN Housekeeping H ON R.RoomId = H.RoomId
                    JOIN KeepingInventory KI ON H.TaskID = KI.TaskID
                    JOIN InventoryUsage IU ON KI.UsageId = IU.UsageId
                    GROUP BY RT.TypeName
                """)

            elif report_type == "Run Maintenance Analysis":
                cur.execute("CALL analyze_and_schedule_maintenance()")
                conn.commit()
                QMessageBox.information(self, "Success", "Maintenance analysis completed!")
                return
                
            elif report_type == "Prepare Room":
                room_id = self.room_combo.currentData()
                if not room_id:
                    QMessageBox.warning(self, "Warning", "Please select a room!")
                    return
                
                cur.execute("CALL prepare_room_for_reservation(%s)", (room_id,))
                conn.commit()
                QMessageBox.information(self, "Success", "Room preparation initiated!")
                return
            
            results = cur.fetchall()
            self.table.setRowCount(len(results))
            
            for row, data in enumerate(results):
                for col, value in enumerate(data):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(row, col, item)
            
            self.table.resizeColumnsToContents()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report: {str(e)}")
    
    def export_report(self):
        try:
            import csv
            from datetime import datetime
            from PyQt5.QtWidgets import QFileDialog
            
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Export Report",
                f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "CSV Files (*.csv)"
            )
            
            if filename:
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    
                    # Write headers
                    headers = []
                    for col in range(self.table.columnCount()):
                        headers.append(self.table.horizontalHeaderItem(col).text())
                    writer.writerow(headers)
                    
                    # Write data
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(self.table.columnCount()):
                            item = self.table.item(row, col)
                            row_data.append(item.text() if item else '')
                        writer.writerow(row_data)
                
                QMessageBox.information(self, "Success", "Report exported successfully!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export report: {str(e)}")
