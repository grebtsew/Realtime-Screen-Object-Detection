import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class MainWindow(QMainWindow):

    layout_main = None
    central_widget = None
    lbl_name = None
    lbl_value = None
    input_name = None
    input_value = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        #variables
        self.layout_main = QVBoxLayout()
        self.layout_labels = QHBoxLayout()
        self.layout_inputs = QHBoxLayout()
        self.central_widget = QWidget()
        self.lbl_name = QLabel("name")
        self.lbl_name.setFixedSize(100,50)
        self.lbl_value = QLabel("Value")
        self.lbl_value.setFixedSize(100, 50)
        self.input_name = QLineEdit()
        self.input_name.setFixedSize(100, 50)
        self.input_value = QLineEdit()
        self.input_value.setFixedSize(100, 50)
        #style
        self.layout_main.setContentsMargins(10, 10, 10, 10)
        self.setMinimumSize(250,100)
        #adding objects
        self.layout_labels.addWidget(self.lbl_name)
        self.layout_labels.addWidget(self.lbl_value)
        self.layout_main.addLayout(self.layout_labels)
        self.layout_inputs.addWidget(self.input_name)
        self.layout_inputs.addWidget(self.input_value)
        self.layout_main.addLayout(self.layout_inputs)

        self.central_widget.setLayout(self.layout_main)
        self.setCentralWidget(self.central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
