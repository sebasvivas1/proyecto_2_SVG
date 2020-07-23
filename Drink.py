from Food import *

class Drink(Food):
    def __init__(self, name, drink_size, price):
        super().__init__(name, price)
        # drink_size = Tamaño de la bebida (Pequeño, Mediano, Grande)
        self.drink_size = drink_size


    def show_name(self):
        return '{self.name}'

    def show_info(self):
        return '{self.name} - {self.drink_size} - ${self.price}'