import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QStackedWidget, QLabel, QStyleFactory)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from db_config import DatabaseConnection
from rooms import RoomsWidget
from reservation import ReservationWidget
from staff import StaffWidget
from dashboard import DashboardWidget
from reports import ReportsWidget
from maintenance import MaintenanceWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hotel Management System")
        self.setMinimumSize(1200, 800)
        
        # Initialize database connection
        self.db = DatabaseConnection()
        self.db.connect()
        
        # Create the main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create header
        header = QLabel("Hotel Management System")
        header.setStyleSheet("""
            QLabel {
                color: #222;
                font-size: 24px;
                padding: 10px;
                background-color: #fff700;
                border-radius: 5px;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Create content area
        content = QWidget()
        content_layout = QVBoxLayout(content)
        
        # Navigation buttons
        nav_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Rooms", self.show_rooms),
            ("Reservation", self.show_reservation),
            ("Staff", self.show_staff),
            ("Maintenance", self.show_maintenance),
            ("Reports", self.show_reports),
            ("Settings", self.show_settings)
        ]
        
        button_style = """
            QPushButton {
                background-color: #00e6ff;
                color: #222;
                border: none;
                padding: 10px;
                margin: 5px;
                border-radius: 5px;
                font-size: 16px;
                min-width: 150px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffb347;
                color: #222;
            }
            QPushButton:pressed {
                background-color: #ff4cff;
                color: #fff;
            }
        """
        
        for text, slot in nav_buttons:
            button = QPushButton(text)
            button.setStyleSheet(button_style)
            button.clicked.connect(slot)
            content_layout.addWidget(button)
        
        # Add content to main layout
        layout.addWidget(content)
        
        # Create stacked widget for different screens
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # Add dashboard to stack and show it by default
        print("Creating DashboardWidget...")  # Debug
        self.dashboard = DashboardWidget()
        self.stack.addWidget(self.dashboard)
        self.stack.setCurrentWidget(self.dashboard)
        print("DashboardWidget added and set as current.")  # Debug

        # Set bright theme
        self.set_bright_theme()

    def set_bright_theme(self):
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        
        bright_palette = QPalette()
        bright_palette.setColor(QPalette.Window, QColor("#fffde7"))  # light yellow
        bright_palette.setColor(QPalette.WindowText, QColor("#222"))
        bright_palette.setColor(QPalette.Base, QColor("#ffffff"))    # white
        bright_palette.setColor(QPalette.AlternateBase, QColor("#fff9c4"))  # pale yellow
        bright_palette.setColor(QPalette.ToolTipBase, QColor("#fff700"))
        bright_palette.setColor(QPalette.ToolTipText, QColor("#222"))
        bright_palette.setColor(QPalette.Text, QColor("#222"))
        bright_palette.setColor(QPalette.Button, QColor("#00e6ff"))  # bright cyan
        bright_palette.setColor(QPalette.ButtonText, QColor("#222"))
        bright_palette.setColor(QPalette.BrightText, QColor("#ff4cff"))  # magenta
        bright_palette.setColor(QPalette.Link, QColor("#ffb347"))    # orange
        bright_palette.setColor(QPalette.Highlight, QColor("#ffb347"))
        bright_palette.setColor(QPalette.HighlightedText, QColor("#222"))

        app.setPalette(bright_palette)

    def show_dashboard(self):
        if not hasattr(self, 'dashboard'):
            self.dashboard = DashboardWidget()
            self.stack.addWidget(self.dashboard)
        self.stack.setCurrentWidget(self.dashboard)
        
    def show_rooms(self):
        if not hasattr(self, 'rooms'):
            self.rooms = RoomsWidget()
            self.stack.addWidget(self.rooms)
        self.stack.setCurrentWidget(self.rooms)
        
    def show_reservation(self):
        if not hasattr(self, 'reservation'):
            self.reservation = ReservationWidget()
            self.stack.addWidget(self.reservation)
        self.stack.setCurrentWidget(self.reservation)
        
    def show_staff(self):
        if not hasattr(self, 'staff'):
            self.staff = StaffWidget()
            self.stack.addWidget(self.staff)
        self.stack.setCurrentWidget(self.staff)
        
    def show_maintenance(self):
        if not hasattr(self, 'maintenance'):
            self.maintenance = MaintenanceWidget()
            self.stack.addWidget(self.maintenance)
        self.stack.setCurrentWidget(self.maintenance)
        
    def show_reports(self):
        if not hasattr(self, 'reports'):
            self.reports = ReportsWidget()
            self.stack.addWidget(self.reports)
        self.stack.setCurrentWidget(self.reports)
        
    def show_settings(self):
        if not hasattr(self, '_settings_widget'):
            self._settings_widget = QWidget()
            layout = QVBoxLayout(self._settings_widget)
            label = QLabel("Settings Feature Coming Soon")
            label.setStyleSheet("color: #222; font-size: 24px;")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            self.stack.addWidget(self._settings_widget)
        self.stack.setCurrentWidget(self._settings_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application-wide style sheet with bright colors
    app.setStyleSheet("""
        QMainWindow {
            background-color: #fffde7;
        }
        QWidget {
            background-color: #fffde7;
        }
        QMessageBox {
            background-color: #fff700;
        }
        QMessageBox QLabel {
            color: #222;
        }
        QMessageBox QPushButton {
            background-color: #00e6ff;
            color: #222;
            border: none;
            padding: 5px 15px;
            border-radius: 3px;
            font-weight: bold;
        }
        QMessageBox QPushButton:hover {
            background-color: #ffb347;
            color: #222;
        }
    """)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
