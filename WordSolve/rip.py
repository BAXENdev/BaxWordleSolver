import sys
from PyQt6.QtGui import QColor, QPalette, QPainter, QPen, QBrush
from PyQt6.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
import PyQt6.QtCore as Qt
    

# Create an instance of QApplication
app = QApplication(sys.argv)

# Create the main window and set its window title
window = QMainWindow()
window.setWindowTitle('My PyQt6 GUI')

# Create the sub-window widget and set its background color
sub_window = QWidget()
palette = QPalette()
# palette.setColor(QPalette.base, QColor('#373737'))
sub_window.setAutoFillBackground(True)
sub_window.setPalette(palette)

# Create the grid layout and add labels to it
layout = QGridLayout()

for i in range(6):
    for j in range(5):
        label = QLabel(parent=sub_window)
        label.setFixedSize(40, 40)
        label.setText('X')
        # label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('color: #240114; font-size: 24pt;')

        # Create a QPainter to draw the rounded corners and border
        painter = QPainter(label)
        # painter.setRenderHint(QPainter.Antialiasing)

        # Set the pen and brush to be used for drawing
        pen = QPen(QColor('#240114'))
        pen.setWidth(2)
        # pen.setStyle(Qt.SolidLine)
        brush = QBrush(QColor('#373737'))
        painter.setPen(pen)
        painter.setBrush(brush)

        # Draw the rounded corners and border
        rect = label.rect()
        radius = 10
        painter.drawRoundedRect(rect, radius, radius)

        layout.addWidget(label, i, j)

# Set the layout for the sub-window
sub_window.setLayout(layout)

# Add the sub-window to the main window
window.setCentralWidget(sub_window)

# Show the main window
window.show()

# Run the application's event loop
sys.exit(app.exec())
