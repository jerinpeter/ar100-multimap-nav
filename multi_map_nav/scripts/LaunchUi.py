#!/usr/bin/env python3
import sys
import subprocess
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QFormLayout, QLineEdit, QDoubleSpinBox, QPushButton,
    QLabel, QMessageBox
)

class GoalPublisher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 NavigateToGoal Sender")
        self.setWindowIcon(QIcon("icons/rocket.png"))
        self.setMinimumSize(450, 360)
        self._apply_stylesheet()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # ─── Header with Icon ────────────────────────────────────────────────
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        ico = QLabel()
        ico.setPixmap(QPixmap("icons/rocket.png").scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        title = QLabel("Navigate To Goal")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header_layout.addWidget(ico)
        header_layout.addSpacing(10)
        header_layout.addWidget(title)
        main_layout.addLayout(header_layout)
        
        # ─── Parameters Group ───────────────────────────────────────────────
        form_group = QGroupBox("Goal Parameters")
        form_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #555;
                border-radius: 6px;
                margin-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 6px;
            }
        """)
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignCenter)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(12)
        
        # target_map with icon action
        self.map_edit = QLineEdit()
        self.map_edit.setPlaceholderText("e.g. map2")
        self.map_edit.addAction(QIcon("icons/map.png"), QLineEdit.LeadingPosition)
        
        # target_x with inline icon
        self.x_spin = QDoubleSpinBox()
        self._decorate_spin(self.x_spin, "icons/x_axis.png")
        self.x_spin.setRange(-1000.0, 1000.0)
        self.x_spin.setDecimals(2)
        self.x_spin.setSingleStep(0.1)
        
        # target_y with inline icon
        self.y_spin = QDoubleSpinBox()
        self._decorate_spin(self.y_spin, "icons/y_axis.png")
        self.y_spin.setRange(-1000.0, 1000.0)
        self.y_spin.setDecimals(2)
        self.y_spin.setSingleStep(0.1)
        
        form_layout.addRow("Target Map:", self.map_edit)
        form_layout.addRow("Target X:",   self.x_spin)
        form_layout.addRow("Target Y:",   self.y_spin)
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)
        
        # ─── Send Button ───────────────────────────────────────────────────
        send_btn = QPushButton(" Send Goal")
        send_btn.setFixedHeight(44)
        send_btn.setCursor(Qt.PointingHandCursor)
        send_btn.setIcon(QIcon("icons/send.png"))
        send_btn.setIconSize(QSize(24,24))
        send_btn.clicked.connect(self.send_goal)
        main_layout.addWidget(send_btn)

    def _decorate_spin(self, spinbox, icon_path):
        """Put a small icon inside the spinbox’s leading edge."""
        action = spinbox.lineEdit().addAction(
            QIcon(icon_path), QLineEdit.LeadingPosition
        )
        # shrink right padding so the icon sits nicely
        spinbox.setStyleSheet("QDoubleSpinBox { padding-left: 26px; }")
    
    def _apply_stylesheet(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
                font-family: "Segoe UI";
                font-size: 13px;
            }
            QLineEdit, QDoubleSpinBox {
                background-color: #3c3c3c;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
    
    def send_goal(self):
        m = self.map_edit.text().strip()
        x = self.x_spin.value()
        y = self.y_spin.value()

        if not m:
            QMessageBox.warning(self, "Missing Map", "Please enter a target_map.")
            return

        payload = f"""header:
  seq: 0
  stamp: {{secs: 0, nsecs: 0}}
  frame_id: ''
goal_id:
  stamp: {{secs: 0, nsecs: 0}}
  id: ''
goal:
  target_x: {x}
  target_y: {y}
  target_map: '{m}'"""

        cmd = [
            "rostopic", "pub", "-1",
            "/navigate_to_goal/goal",
            "multi_map_nav/NavigateToGoalActionGoal",
            payload
        ]

        try:
            subprocess.Popen(cmd)
            QMessageBox.information(self, "Sent", "✅ Goal published!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to publish:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = GoalPublisher()
    win.show()
    sys.exit(app.exec_())
