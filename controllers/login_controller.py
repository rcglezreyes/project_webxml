from models.login_model import LoginModel
from views.login_view import LoginView
from views.main_view import MainView
from views.product_view import ProductView

from PyQt5.QtWidgets import QMessageBox

class LoginController:
    def __init__(self):
        self.login_view = LoginView()
        self.main_view = MainView()
        self.product_view = ProductView()
        self.model = LoginModel()
        
        self.login_view.login_button.clicked.connect(self.authenticate)
        

    def authenticate(self):
        username = self.login_view.username_input.text()
        password = self.login_view.password_input.text()
        if self.model.authenticate(username, password):
            self.main_view = MainView(username=username)
            self.main_view.logout_action.triggered.connect(self.logout)
            self.main_view.clients_action.triggered.connect(self.show_clients)
            self.main_view.products_action.triggered.connect(self.show_products)
            self.main_view.users_action.triggered.connect(self.show_users)
            self.main_view.invoices_action.triggered.connect(self.show_invoices)
            self.login_view.close()  
            self.main_view.show() 
        else:
            self.login_view.show_error("Invalid username or password")

    def logout(self):
        self.main_view.hide()
        self.login_view.show()
    
    def show_clients(self):
        QMessageBox.information(self.main_view, "Clients", "Clients Section")

    def show_products(self):
        self.product_view = ProductView(username=self.main_view.username)
        self.product_view.show()
        self.product_view.load_products()

    def show_users(self):
        QMessageBox.information(self.main_view, "Users", "Users Section")

    def show_invoices(self):
        QMessageBox.information(self.main_view, "Invoices", "Invoices Section")
