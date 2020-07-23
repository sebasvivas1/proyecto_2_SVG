class Room:
    def __init__(self, room_type, letter, number, code, description, capacity, price, information, available):
        self.room_type = room_type
        self.letter = letter
        self.number = number
        self.code = code
        self.description = description
        self.capacity = capacity
        self.price = price
        self.information = information
        self.available = available

    def show_room_info(self):
        return f''' 
Tipo de habitacion: {self.room_type}
Codigo de habitacion: {self.letter}{self.number}
Capacidad: {self.capacity}
Referencia: {self.description}
Precio de habitacion: {self.price}
Informacion de la habitacion: {self.information}
Disponibile: {self.available}
        '''

    def room_available(self):
        if self.available == True:
            self.available = True
        else:
            self.available = False
        
    def family_description(self):
        if not self.available:
            self.description = input('Descripción de la familia:\n===> ')
        else:
            self.available = None
