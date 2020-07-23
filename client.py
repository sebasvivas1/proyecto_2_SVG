class Client:
    
    def __init__(self, name, dni, age, condition, selected_cruise, room_bought, price, tours):
        self.name = name
        self.dni = dni
        self.age = age
        self.condition = condition
        self.selected_cruise = selected_cruise
        self.room_bought = room_bought
        self.price = price
        self.tours = tours

    def show_client_info(self):

        if self.condition == True:
            client_condition = 'Si'
        
        else:
            client_condition = 'No'
        
        return f'''
Nombre: {self.name}
ID: {self.dni}
Edad: {self.age}
Discapacidad: {client_condition}
        '''


    def money_spend(self, dollars):
        self.price += dollars


    