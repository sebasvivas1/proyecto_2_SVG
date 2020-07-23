class Food():
    def __init__(self, name, price):
        self.name = name
        # Food Type = Alimento / Bebida
        self.price = price

    def __str__(self):
        return f'{self.name} --- {self.price} ---\n'

