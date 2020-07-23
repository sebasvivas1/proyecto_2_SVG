from functions import *
from Crucero import *
from Food import *
from Alimento import *
from Drink import *
from Tour import *
import os

# Variables / listas
menu = {}
standar_menu = {}
combos = {}

tours = [
    {"name": 'Tour en Puerto',
    "price": 30,
    "group_cap": 4,
    "starting_hour": '7 AM',
    "max_capacity": 10},
    {"name": 'Degustación de comida local',
    "price": 100,
    "group_cap": 2,
    "starting_hour": '12 PM',
    "max_capacity": 100},
    {"name": 'Trotar por el pueblo/ciudad',
    "price": 0,
    "group_cap": 'Sin limite de',
    "starting_hour": '6 AM',
    "max_capacity": 'Sin limite'},
    {"name": 'Visita a lugares historicos',
    "price": 40,
    "group_cap": 4,
    "starting_hour": '10 AM',
    "max_capacity": 15}
]

cruises_list = []
option = 0
rest_menu_option = 0

# Repeat Message
repeat_program = 'Would you like to continue using the program?'

# Error Message
invalid_option = 'Invalid option.'
invalid_product = 'Producto no existente.'

# Welcome Message
print('---Welcome to Saman Cruise! We will guide you through some options to give you the best experience---')

# Other Messages
restaurant_menu_welcome = 'Bienivenido! Acá podrá añadir nuevos alimentos/bebidas al menu del restaurante!'
msg_remove_welcome = 'Acá podrá eliminar cualquier producto del Menú del Restaurante.'
msg_update_welcome = 'Acá podrá actualizar la información de alguno de los productos existentes en el menú.'
msg_intro_menu = 'Bienvenido al Modulo de Gestión de Comida de nuestro Restaurante!'
msg_combo_welcome = 'Acá podrá crear combos para nuestro Menú de Combos!'
msg_find_product_menu = 'Acá podrá buscar productos del Menú por nombre o rango de precio!'
msg_tour_info = 'En Saman Cruise tenemos los mejores Tours para que disfrutes con tus acompañantes!'
msg_tour = 'Acá podrá comprar el tour de su preferencia.'
msg_delete_combo = 'Aca podrá eliminar un combo del Menú de combos.'




# Option Menu
msg_option_menu = '''
1. Ver información de cruceros.
2. Vender boletos por nombre del crucero/destino.
3. Ver información de Tours.
4. Vender Tours.
5. Gestionar Menu del Restaurante.
6.
> '''

# Restaurant Option Menu
msg_restaurant_options = '''
1. Agregar Alimentos/Bebidas.
2. Eliminar Alimentos/Bebidas.
3. Modificar Alimentos.
4. Agregar Combo.
5. Eliminar Combo.
6. Buscar producto por nombre o rango de precio.
7. Buscar combo por nombre o rango de precio.
8. Volver al menu principal.
> '''


while True:       

    option = enter_option(option, msg_option_menu, invalid_option)
    print()

    # Option 1: Cruises Information (Name, Date, Route, Prices.)
    if option == 1:
        cruises_information = show_cruisers()

    # Option 2: Sell Cruise tickets
    elif option == 2:
        sell_tickets = sell_rooms()

    # Option 4: See Tours Info
    elif option == 3:
        show_tours(tours ,msg_tour_info, invalid_option)

    # Option 5: Sell Tours (destiny)
    elif option == 4:
        select_tour(tours, msg_tour, invalid_product)

    # Option 6: Update Restaurant's Menu.
    elif option == 5:

        # Restaurant's Menu Options
        print(msg_intro_menu)
        rest_menu_option = enter_option(rest_menu_option, msg_restaurant_options, invalid_option)

        # Agregar Alimentos / Bebidas
        if rest_menu_option == 1:
            add_product = gen_menu(menu, msg_restaurant_options, invalid_option)
            add_more_products(menu)

        # Eliminar Alimentos/Bebidas.
        elif rest_menu_option == 2:
            remove_menu_product = remove_product(menu, msg_remove_welcome, invalid_product)
        
        # Modificar Alimentos.
        elif rest_menu_option == 3:
            update_menu_product = update_product(menu, msg_update_welcome, invalid_product)
        
        # Agregar Combo.
        elif rest_menu_option == 4:
            add_combo = gen_combo(combos, msg_combo_welcome, invalid_product)

        # 5. Eliminar Combo.
        elif rest_menu_option == 5:
            gen_combo(combos, msg_delete_combo, invalid_product)

        # Buscar producto por nombre o rango de precio.
        elif rest_menu_option == 6:
            find_product_menu(menu, msg_find_product_menu, invalid_option)

        # Buscar combo por nombre o rango de precio.
        elif rest_menu_option == 7:
            find_combo(combos)
        
        # Regresar al menu principal.
        elif rest_menu_option == 8:
            pass

        # Error
        else:
            print(invalid_option)
    
    # Estadisticas del crucero.
    elif option == 6:
        statistics()

    # Mensaje de error
    else:
        print(invalid_option)











