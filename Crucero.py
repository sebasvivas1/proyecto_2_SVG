class Crucero:
    
    def __init__(self, name, route, departure, room_price, rooms, room_capacity, sells):
        self.name = name
        self.route = route
        self.departure = departure
        self.room_price = room_price
        self.rooms = rooms
        self.room_capacity = room_capacity
        self.sells = sells
    
    def show_cruise_info(self):
        
        print(f'''
-----------------------------------------------------------------------------
||Crucero: {self.name}
||Ruta: {' ---> '.join(self.route)}
||Fecha de Salida: {self.departure}
-----------------------------------------------------------------------------
        ''')