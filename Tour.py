class Tour():
    def __init__(self, tour_name, tour_price, tour_group_cap, tour_starting_time, tour_capacity, tour_space_available):
        self.tour_name = tour_name
        self.tour_price = tour_price
        self.tour_group_cap = tour_group_cap
        self.tour_starting_time = tour_starting_time
        self.tour_capacity = tour_capacity
        self.tour_space_available = tour_space_available
    
    def __str__(self):
        return f'{self.tour_name} tiene un precio de ${self.tour_price} por persona. Cupo maximo de personas por grupo: {self.tour_group_cap} y comienza a las {self.tour_starting_time} tiene una capacidad maxima de {self.tour_capacity} personas.'
