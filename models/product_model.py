import xml.etree.ElementTree as ET
from models.connection_model import ConnectionModel

class ProductModel(ConnectionModel):
    def __init__(self):
        super().__init__()

    def product_code_exists(self, code):
        """Check if a product code already exists in the database."""
        query = "SELECT 1 FROM product WHERE code = %s"
        connection = self.connect_postgres()
        cursor = connection.cursor()
        cursor.execute(query, (code,))
        exists = cursor.fetchone() is not None
        cursor.close()
        connection.close()
        return exists

    def add_product(self, product_data, username):
        """Add a new product to the database."""
        if self.product_code_exists(product_data["code"]):
            return False

        query = """
        INSERT INTO product (name, code, description, price, tax_rate)
        VALUES (%s, %s, %s, %s, %s)
        """
        connection = self.connect_postgres()
        cursor = connection.cursor()
        cursor.execute(query, (
            product_data["name"],
            product_data["code"],
            product_data["description"],
            product_data["price"],
            product_data["tax_rate"],
        ))
        connection.commit()
        user = self.select_user(username)
        query = """
        INSERT INTO track ("user", action, created_at, ip_4_number, mac_address, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user[0],
            "add_product",
            "NOW()",
            self.get_ip(),
            self.get_mac(),
            f'Add product with info (CODE: {product_data["code"]}, NAME: {product_data["name"]}, DESCRIPTION: {product_data["description"]}, PRICE: {product_data["price"]}, TAX RATE: {product_data["tax_rate"]})',
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    def update_product(self, product_id, product_data, username):
        """Update an existing product in the database."""
        if self.product_code_exists(product_data["code"]):
            existing_product = self.get_product_by_id(product_id)
            if existing_product and existing_product["code"] != product_data["code"]:
                return False

        query = """
        UPDATE product
        SET name = %s, code = %s, description = %s, price = %s, tax_rate = %s, updated_at = NOW()
        WHERE id = %s
        """
        connection = self.connect_postgres()
        cursor = connection.cursor()
        cursor.execute(query, (
            product_data["name"],
            product_data["code"],
            product_data["description"],
            product_data["price"],
            product_data["tax_rate"],
            product_id,
        ))
        connection.commit()
        user = self.select_user(username)
        query = """
        INSERT INTO track ("user", action, created_at, ip_4_number, mac_address, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user[0],
            "update_product",
            "NOW()",
            self.get_ip(),
            self.get_mac(),
            f'Update product with info (CODE: {product_data["code"]}, NAME: {product_data["name"]}, DESCRIPTION: {product_data["description"]}, PRICE: {product_data["price"]}, TAX RATE: {product_data["tax_rate"]})',
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    def delete_product(self, product_id, username):
        query = "SELECT * FROM product WHERE id = %s"
        connection = self.connect_postgres()
        cursor = connection.cursor()
        cursor.execute(query, (product_id,))
        connection.commit()
        product_data = cursor.fetchone()
        """Delete a product from the database."""
        query = "DELETE FROM product WHERE id = %s"
        cursor.execute(query, (product_id,))
        connection.commit()
        user = self.select_user(username)
        query = """
        INSERT INTO track ("user", action, created_at, ip_4_number, mac_address, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user[0],
            "delete_product",
            "NOW()",
            self.get_ip(),
            self.get_mac(),
            f'Delete product with info (CODE: {product_data[8]}, NAME: {product_data[2]}, DESCRIPTION: {product_data[3]}, PRICE: {product_data[4]}, TAX RATE: {product_data[5]})',
        ))
        connection.commit()
        cursor.close()
        connection.close()

    def get_all_products(self):
        """Fetch all products from the database."""
        query = "SELECT id, name, code, description, price, tax_rate FROM product"
        connection = self.connect_postgres()
        cursor = connection.cursor()
        cursor.execute(query)
        products = cursor.fetchall()
        cursor.close()
        connection.close()

        # Return products as a list of dictionaries
        return [
            {
                "id": row[0],
                "name": row[1],
                "code": row[2],
                "description": row[3],
                "price": row[4],
                "tax_rate": row[5],
            }
            for row in products
        ]

    def get_product_by_id(self, product_id):
        """Fetch a specific product by ID from the database."""
        query = "SELECT id, name, code, description, price, tax_rate FROM product WHERE id = %s"
        connection = self.connect_postgres()
        cursor = connection.cursor()
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()
        cursor.close()
        connection.close()

        if product:
            return {
                "id": product[0],
                "name": product[1],
                "code": product[2],
                "description": product[3],
                "price": product[4],
                "tax_rate": product[5],
            }
        return None
