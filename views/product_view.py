from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtGui import QDoubleValidator
import xml.etree.ElementTree as ET
from models.product_model import ProductModel  
from views.utils.center_window import center_window

class ProductView(QtWidgets.QWidget):
    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.init_ui()
        self.model = ProductModel()  
        self.edit_mode = False  
        self.current_product_id = None  
        self.load_products()  

    def init_ui(self):
        self.setWindowTitle("Products Management")
        self.setFixedSize(1000, 600)
        center_window(self)
        
        form_layout = QtWidgets.QFormLayout()
        
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setFixedWidth(300)
        self.description_input = QtWidgets.QLineEdit()
        self.description_input.setFixedWidth(300)
        self.price_input = QtWidgets.QLineEdit()
        self.price_input.setFixedWidth(300)
        self.tax_rate_input = QtWidgets.QLineEdit()
        self.tax_rate_input.setFixedWidth(300)
        self.code_input = QtWidgets.QLineEdit()
        self.code_input.setFixedWidth(300)
        float_validator = QDoubleValidator(0.0, 999999.99, 2)
        float_validator.setNotation(QDoubleValidator.StandardNotation)
        self.price_input.setValidator(float_validator)
        
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Code:", self.code_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Price:", self.price_input)
        form_layout.addRow("Tax Rate:", self.tax_rate_input)
        
        self.submit_button = QtWidgets.QPushButton("Save")
        self.submit_button.clicked.connect(self.save_product)
        self.load_xml_button = QtWidgets.QPushButton("Load XML")
        self.load_xml_button.clicked.connect(self.load_xml)
        self.clear_button = QtWidgets.QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_form)
        
        button_widget = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_widget)
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.load_xml_button)
        button_layout.addWidget(self.clear_button)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        container_layout = QtWidgets.QHBoxLayout()
        container_layout.addStretch(1)
        container_layout.addWidget(button_widget)
        container_layout.addStretch(1)

        form_layout.addRow(container_layout)
        
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Code", "Description", "Price", "Tax Rate", "Actions"])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  
        
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    def load_products(self):
        """Load all products from the database and populate the table."""
        products = self.model.get_all_products()  

        self.table.setRowCount(len(products))  
        for row, product in enumerate(products):
            self.add_product_to_table(row, product)

    def add_product_to_table(self, row, product):
        """Add a product row to the table."""
        self.table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
        self.table.setItem(row, 1, QTableWidgetItem(product['name']))
        self.table.setItem(row, 2, QTableWidgetItem(product['code']))
        self.table.setItem(row, 3, QTableWidgetItem(product['description']))
        self.table.setItem(row, 4, QTableWidgetItem(str(product['price'])))
        self.table.setItem(row, 5, QTableWidgetItem(str(product['tax_rate'])))
        
        self.table.setRowHeight(row, 40)
        
        edit_button = QtWidgets.QPushButton("Edit")
        edit_button.setFixedSize(60, 30)
        edit_button.clicked.connect(lambda _, prod_id=product['id']: self.load_product_for_edit(prod_id))

        delete_button = QtWidgets.QPushButton("Delete")
        delete_button.setFixedSize(60, 30)
        delete_button.clicked.connect(lambda _, prod_id=product['id']: self.confirm_delete_product(prod_id))

        action_layout = QtWidgets.QHBoxLayout()
        action_layout.addWidget(edit_button)
        action_layout.addWidget(delete_button)
        action_layout.setContentsMargins(0, 0, 0, 0)

        action_widget = QtWidgets.QWidget()
        action_widget.setLayout(action_layout)
        self.table.setCellWidget(row, 6, action_widget)
        
        self.table.setColumnWidth(6, 150)

    def save_product(self):
        """Save or update product in the database."""
        if not all([
            self.name_input.text(), 
            self.code_input.text(),
            self.price_input.text(), 
            self.tax_rate_input.text()
        ]):
            QMessageBox.warning(self, "Validation Error", "All fields are required.")
            return
        if not self.price_input.hasAcceptableInput():
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Please enter a valid float value for the price.")
            return
        
        product_data = {
            'name': self.name_input.text(),
            'code': self.code_input.text(),
            'description': self.description_input.text(),
            'price': float(self.price_input.text()),
            'tax_rate': float(self.tax_rate_input.text())
        }

        if self.edit_mode:
            self.model.update_product(self.current_product_id, product_data, self.username)
            QMessageBox.information(self, "Updated", "Product updated successfully.")
            self.edit_mode = False
            self.submit_button.setText("Save")
        else:
            self.model.add_product(product_data, self.username)
            QMessageBox.information(self, "Saved", "Product saved successfully.")
        
        self.clear_form()
        self.refresh_table()

    def load_product_for_edit(self, product_id):
        """Load product data into form for editing."""
        product = self.model.get_product_by_id(product_id)
        if product:
            self.name_input.setText(product['name'])
            self.code_input.setText(product['code'])
            self.description_input.setText(product['description'])
            self.price_input.setText(str(product['price']))
            self.tax_rate_input.setText(str(product['tax_rate']))
            
            self.edit_mode = True
            self.current_product_id = product_id
            self.submit_button.setText("Update")

    def confirm_delete_product(self, product_id):
        """Show confirmation dialog for deletion."""
        reply = QMessageBox.question(self, "Delete Confirmation", "Are you sure you want to delete this product?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.model.delete_product(product_id, self.username)
            QMessageBox.information(self, "Deleted", "Product deleted successfully.")
            self.refresh_table()
            
            
    def load_xml(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open XML File", "", "XML Files (*.xml)")

        if not file_path:
            return

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            for elem in root.iter():
                print(f'Tag: {elem.tag}, Text: {elem.text}, Attributes: {elem.attrib}')

            if root.tag.lower() != 'products':
                QMessageBox.warning(self, "Error", "The selected XML is not a valid products file.")
                return
            
            total = len(root.findall('product'))
            print('total', total)
            count = 0
            errors = ''

            for product in root.findall('product'):
                product_data = {}
                
                for key, value in product.attrib.items():
                    product_data[key.lower()] = value.strip() if value else None
                
                for child in product:
                    product_data[child.tag.lower()] = child.text.strip() if child.text else None
                
                if not product_data:
                    QMessageBox.warning(self, "Error", "XML Product is empty or incompleted data provided.")
                    continue
                
                try:
                    if 'price' in product_data:
                        product_data['price'] = float(product_data['price'])
                    if 'tax_rate' in product_data:
                        product_data['tax_rate'] = float(product_data['tax_rate'])
                except ValueError:
                    QMessageBox.warning(self, "Error", "Invalid numeric data in XML product.")
                    continue

                if self.model.add_product(product_data, self.username):
                    count += 1
                else:
                    errors += f"Failed to save product: {product_data['code']} - {product_data['name']}\n"
            
            message = f"Loaded {count} of {total} products from XML file."
            
            if errors:
                message += f"\n\nErrors:\n{errors}"

            QMessageBox.information(self, "Success", message)
            self.refresh_table()

        except ET.ParseError:
            QMessageBox.warning(self, "Error", "Failed to parse XML file. Ensure it is well-formed and correct.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")


    def clear_form(self):
        """Clear the form inputs."""
        self.name_input.clear()
        self.code_input.clear()
        self.description_input.clear()
        self.price_input.clear()
        self.tax_rate_input.clear()
        self.edit_mode = False
        self.submit_button.setText("Save")

    def refresh_table(self):
        """Refresh the table data."""
        self.table.setRowCount(0)
        self.load_products()
