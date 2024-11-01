import sys
from PyQt5.QtWidgets import QApplication
from controllers.login_controller import LoginController

def main():
    app = QApplication(sys.argv)
    login_controller = LoginController()
    login_controller.login_view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
