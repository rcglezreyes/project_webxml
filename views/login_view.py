from PyQt5 import QtWidgets, QtCore
from views.utils.center_window import center_window

class LoginView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)
        center_window(self)

        self.username_label = QtWidgets.QLabel("Username:", self)
        self.username_label.move(20, 20)
        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.move(100, 20)

        self.password_label = QtWidgets.QLabel("Password:", self)
        self.password_label.move(20, 60)
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.move(100, 60)

        self.login_button = QtWidgets.QPushButton("Login", self)
        self.login_button.move(100, 100)

        self.status_label = QtWidgets.QLabel("", self)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.move(20, 130)
        self.status_label.resize(260, 20)

    def show_error(self, message):
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: red;")
