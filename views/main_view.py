from PyQt5 import QtWidgets
from views.utils.center_window import center_window

import os

class MainView(QtWidgets.QMainWindow):
    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Dashboard")
        self.setFixedSize(1000, 600)
        center_window(self)
        
        background_image_path = os.path.join("views/assets", "background.png")
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-image: url({background_image_path});
                background-repeat: no-repeat;
                background-position: center;
            }}
        """)
        
        toolbar = self.addToolBar("Operations")
        
        clients_action = QtWidgets.QAction("Clients", self)
        products_action = QtWidgets.QAction("Products", self)
        users_action = QtWidgets.QAction("Users", self)
        invoices_action = QtWidgets.QAction("Invoices", self)
        
        toolbar.addAction(clients_action)
        toolbar.addAction(products_action)
        toolbar.addAction(users_action)
        toolbar.addAction(invoices_action)
        
        logout_action = QtWidgets.QAction("Logout", self)
        toolbar.addAction(logout_action)
        
        self.clients_action = clients_action
        self.products_action = products_action
        self.users_action = users_action
        self.invoices_action = invoices_action
        self.logout_action = logout_action
