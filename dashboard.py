from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QFrame, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt
from db_config import DatabaseConnection
from PyQt5.QtGui import QFont

class StatCard(QFrame):
    def __init__(self, title, value, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #fff700;  /* bright yellow */
                border-radius: 10px;
                padding: 1px;
                min-width: 150px;
                min-height: 50px;
                border: 2px solid #00e6ff; /* bright cyan border */
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #222; font-size: 14px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Value
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet("color: #ff4cff; font-size: 28px; font-weight: bold;")
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)

    def set_value(self, value):
        # Always show a string, default to "0" if value is None or empty
        self.value_label.setText(str(value) if value not in (None, '', []) else "0")

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        print("DashboardWidget initialized")  # Debug
        self.db = DatabaseConnection()
        self.setup_ui()
        self.load_stats()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Dashboard")
        header.setStyleSheet("""
            QLabel {
                color: #222;
                font-size: 24px;
                padding: 10px;
                background-color: #ffb347;
                border-radius: 5px;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Stats Grid
        stats_layout = QGridLayout()
        self.stats_widgets = {
            'total_rooms': StatCard("Total Rooms", "0"),
            'available_rooms': StatCard("Available Rooms", "0"),
            'occupied_rooms': StatCard("Occupied Rooms", "0"),
            'maintenance_rooms': StatCard("Rooms in Maintenance", "0"),
            'total_staff': StatCard("Active Staff", "0"),
            'pending_tasks': StatCard("Pending Tasks", "0"),
            'today_checkins': StatCard("Today's Check-ins", "0"),
            'today_checkouts': StatCard("Today's Check-outs", "0")
        }
        
        positions = [(i, j) for i in range(2) for j in range(4)]
        for (key, widget), (row, col) in zip(self.stats_widgets.items(), positions):
            stats_layout.addWidget(widget, row, col)
        
        layout.addLayout(stats_layout)
        
        # Recent Activity Section
        activity_label = QLabel("Recent System Activity")
        activity_label.setStyleSheet("color: #222; font-size: 18px; padding: 10px;")
        layout.addWidget(activity_label)
        
        # Make activity list scrollable and limit height
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent; border: none;")
        self.activity_list = QLabel()
        self.activity_list.setStyleSheet("""
            QLabel {
                color: #222;
                background-color: #fff9c4;
                padding: 15px;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        self.activity_list.setWordWrap(True)
        scroll_area.setWidget(self.activity_list)
        scroll_area.setMaximumHeight(180)
        layout.addWidget(scroll_area)

        # Add stretch to push everything up
        layout.addStretch()
    
    def load_stats(self):
        conn = None
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            # Get total rooms and their status
            cur.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN AvailabilityStatus = 'Available' THEN 1 ELSE 0 END) as available,
                    SUM(CASE WHEN AvailabilityStatus = 'Occupied' THEN 1 ELSE 0 END) as occupied,
                    SUM(CASE WHEN AvailabilityStatus = 'Maintenance' THEN 1 ELSE 0 END) as maintenance
                FROM Room
            """)
            room_stats = cur.fetchone()
            print("Room stats:", room_stats)  # Debug
            # Ensure room_stats is a tuple of 4 integers (default 0)
            if not room_stats or len(room_stats) < 4:
                room_stats = (0, 0, 0, 0)
            else:
                room_stats = tuple(x if x is not None else 0 for x in room_stats)
            self.stats_widgets['total_rooms'].set_value(room_stats[0])
            self.stats_widgets['available_rooms'].set_value(room_stats[1])
            self.stats_widgets['occupied_rooms'].set_value(room_stats[2])
            self.stats_widgets['maintenance_rooms'].set_value(room_stats[3])

            # Get active staff count
            cur.execute("SELECT COUNT(*) FROM Staff WHERE IsActive = true")
            staff_count = cur.fetchone()
            print("Staff count:", staff_count)  # Debug
            staff_count = staff_count[0] if staff_count and staff_count[0] is not None else 0
            self.stats_widgets['total_staff'].set_value(staff_count)

            # Get pending tasks
            cur.execute("""
                SELECT COUNT(*)
                FROM (
                    SELECT TaskID FROM Housekeeping WHERE Status = 'Pending'
                    UNION ALL
                    SELECT RequestId FROM MaintenanceRequest WHERE Status = 'Pending'
                ) AS pending_tasks
            """)
            pending_tasks = cur.fetchone()
            print("Pending tasks:", pending_tasks)  # Debug
            pending_tasks = pending_tasks[0] if pending_tasks and pending_tasks[0] is not None else 0
            self.stats_widgets['pending_tasks'].set_value(pending_tasks)

            # Get today's check-ins and check-outs
            cur.execute("""
                SELECT 
                    SUM(CASE WHEN start_date = CURRENT_DATE THEN 1 ELSE 0 END) as checkins,
                    SUM(CASE WHEN end_date = CURRENT_DATE THEN 1 ELSE 0 END) as checkouts
                FROM reservation
                WHERE status = 'booked'
            """)
            reservation_stats = cur.fetchone()
            print("Reservation stats:", reservation_stats)  # Debug
            checkins = reservation_stats[0] if reservation_stats and reservation_stats[0] is not None else 0
            checkouts = reservation_stats[1] if reservation_stats and reservation_stats[1] is not None else 0
            self.stats_widgets['today_checkins'].set_value(checkins)
            self.stats_widgets['today_checkouts'].set_value(checkouts)

            # Get recent activity
            cur.execute("""
                SELECT r.RoomNumber, res.start_date, res.end_date, g.full_name
                FROM reservation res
                JOIN Room r ON res.roomId = r.RoomId
                JOIN Guests g ON res.guest_id = g.guest_id
                WHERE res.start_date >= CURRENT_DATE
                ORDER BY res.start_date ASC
                LIMIT 5
            """)
            recent_bookings = cur.fetchall()
            print("Recent bookings:", recent_bookings)  # Debug

            cur.execute("""
                SELECT r.RoomNumber, mr.IssueDescription, mr.Status, mr.RequestDate,
                       s.FirstName || ' ' || s.LastName as AssignedTo
                FROM MaintenanceRequest mr
                JOIN Room r ON mr.RoomId = r.RoomId
                LEFT JOIN AssignMaintenanceStaff ams ON mr.RequestId = ams.RequestId
                LEFT JOIN Staff s ON ams.StaffId = s.StaffId
                WHERE mr.Status != 'Completed'
                ORDER BY mr.RequestDate DESC
                LIMIT 5
            """)
            maintenance_requests = cur.fetchall()
            print("Maintenance requests:", maintenance_requests)  # Debug

            cur.execute("""
                SELECT r.RoomNumber, h.Status, h.TaskDate,
                       s.FirstName || ' ' || s.LastName as AssignedTo
                FROM Housekeeping h
                JOIN Room r ON h.RoomId = r.RoomId
                LEFT JOIN AssignKeepingStaff aks ON h.TaskID = aks.TaskID
                LEFT JOIN Staff s ON aks.StaffId = s.StaffId
                WHERE h.TaskDate = CURRENT_DATE
                ORDER BY h.TaskDate DESC
                LIMIT 5
            """)
            housekeeping_tasks = cur.fetchall()
            print("Housekeeping tasks:", housekeeping_tasks)  # Debug

            # Format activity text
            activity_text = "Recent Bookings:\n"
            for room, start, end, guest in recent_bookings:
                activity_text += f"🏨 Room {room}: {guest} ({start} to {end})\n"
            
            activity_text += "\nMaintenance Requests:\n"
            for room, issue, status, date, staff in maintenance_requests:
                activity_text += f"🔧 Room {room}: {issue[:50]}... ({status}) - {staff or 'Unassigned'}\n"
            
            activity_text += "\nToday's Housekeeping:\n"
            for room, status, date, staff in housekeeping_tasks:
                activity_text += f"🧹 Room {room}: {status} - {staff or 'Unassigned'}\n"
            
            if not (recent_bookings or maintenance_requests or housekeeping_tasks):
                print("No recent activity found.")  # Debug
                activity_text = "No recent activity"
            
            self.activity_list.setText(activity_text)
            
            # Schedule automatic refresh every 30 seconds
            if not hasattr(self, 'refresh_timer'):
                from PyQt5.QtCore import QTimer
                self.refresh_timer = QTimer()
                self.refresh_timer.timeout.connect(self.load_stats)
                self.refresh_timer.start(30000)  # 30 seconds
            
        except Exception as e:
            print("Dashboard error:", e)  # Debug
            self.activity_list.setText(f"Error loading dashboard data: {str(e)}")
            if conn:
                conn.rollback()
