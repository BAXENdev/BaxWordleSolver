
# import PyQt6.QtDesigner as qtd
import PyQt6.QtCore as qtc
import PyQt6.QtWidgets as qtw

import sys

import random
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class PALETTE():
    WINDOW_STYLE = "QWidget { background-color: #373737 }"
    GAME_FRAME_STYLE = "QLabel { font: 24pt #060077; border: 2px solid #4b4b4b; border-radius: 10px; }".format()
    GAME_FRAME_STYLE2 = "QLabel { font-color: #060077; font-size: 24pt; border: 2px solid #4b4b4b; border-radius: 10px; }"

def init():
    app = qtw.QApplication([])

    window = qtw.QWidget()
    window.setStyleSheet(PALETTE.WINDOW_STYLE)
    horizontalLayout = qtw.QHBoxLayout()
    window.setLayout(horizontalLayout)

    gameFrame = qtw.QWidget()
    horizontalLayout.addWidget(gameFrame)
    gameFrameLayout = qtw.QGridLayout()
    gameFrame.setStyleSheet(PALETTE.GAME_FRAME_STYLE)
    gameFrame.setLayout(gameFrameLayout)

    for row in range(6):
        for col in range(5):
            input_box = qtw.QLabel(text=random.choice(letters))
            input_box.setFixedSize(40, 40)
            input_box.setAlignment(qtc.Qt.AlignmentFlag.AlignHCenter)
            gameFrameLayout.addWidget(input_box, row, col)
    
    window.show()

    sys.exit(app.exec())

init()


