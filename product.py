class Product:
    def __init__(self, id, name, category, price, stock):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"Product(id={self.id}, name={self.name}, category={self.category}, price={self.price}, stock={self.stock})"