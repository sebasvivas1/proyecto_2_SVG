from Food import *

class Alimento(Food):
    def __init__(self, name, package, price):
        super().__init__(name, price)
        # Package = Empaque / Preparacion
        self.package = package
    

    def show_name(self):
        return '{self.name}'

    def show_info(self):
        return '{self.name} - {self.package} - ${self.price}'


