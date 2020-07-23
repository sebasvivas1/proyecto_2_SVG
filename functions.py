from Crucero import *
from client import *
from Alimento import *
from Food import *
from Drink import *
from Tour import *
from Room import *
import string
import requests
import pickle
import datetime

def enter_option(option, msg1, msg2):
    """Recibe una opcion introducida por el usuario y valida si es o no una opcion valida (ints)

    Args:
        option ([int]): [Seleccion del usuario.]
        msg1 ([string]): [Mensaje de bienvenida]
        msg2 ([string]): [Mensaje de error.]

    Returns:
        [int]: [Devuelve la opcion seleccionada por el usuario despues de haber sido validada.]
    """
    valid_option = False
    while not(valid_option):
        try:
            option = int(input(msg1))
            valid_option = True
        except:
            print(msg2)

    return option

def enter_input(word, msg1, msg2):
    """Recibe un string introducido por el usuario.

    Args:
        option ([str]): [Seleccion del usuario.]
        msg1 ([string]): [Mensaje de bienvenida]
        msg2 ([string]): [Mensaje de error.]

    Returns:
        [str]: [Devuelve la cadena de texto introducida por el usuario.]
    """
    word = input(msg1)
    while word.isnumeric():
        print(msg2)
        word = input(msg1)

    return word

def check_file(file):
    """Verifica si un archivo existe o no.

    Args:
        file ([str]): [NOmbre del archivo]

    Returns:
        [bool]: [True si el archivo existe, False si no.]
    """
    try:
        with open(file) as file:
            return True
    except:
        return False

def save_api_info():
    """[Importa la informacion de la API provista.]

    Returns:
        [dict]: [Retorna la informacion de la API en forma de diccionario]
    """
    response = requests.get('https://saman-caribbean.vercel.app/api/cruise-ships')

    saman_caribbean_api = response.json()

    return saman_caribbean_api

def save_cruisers_info():
    """[Recorre la API y guarda la informacion importante.]

    Returns:
        [list]: [Lista con la informacion extraida del API.]
    """

    cruisers_api = save_api_info()

    cruisers = []

    for cruise in cruisers_api:
            
            name = cruise["name"]
            route = cruise["route"]
            departure = cruise["departure"]
            room_price = cruise["cost"]
            rooms = cruise["rooms"]
            room_capacity = cruise["capacity"]
            sells = cruise["sells"]

            crucero = Crucero(name, route, departure, room_price, rooms, room_capacity, sells)

            cruisers.append(crucero)

    return cruisers

def show_cruisers():
    """Muestra al usuario la informacion de los cruceros disponibles. Dicha informacion proviene de la API.
    """

    information = save_cruisers_info()

    # Mensajes
    msg1 = 'Estos son los barcos disponibles:'

    print(msg1)

    for cruise in information:
        cruise.show_cruise_info()

def choose_cruise():
    """Permite al usuario ver la informacion acerca de los cruceros de dos maneras: segun el destino del crucero, o segun el nombre del barco.

    Returns:
        [int]: [Opcion elegida por el usuario]
    """
    # Variables
    option = 0
    option1 = 0

    # Mensajes 
    msg1 = 'Quisiera vender boletos por nombre del barco (1), o por destino (2)?\n===> '
    msg2 = 'Seleccione su opcion de preferencia.\n===> '
    invalid_option = 'Error. Introduzca una opcion valida.'

    option = enter_option(option, msg1, invalid_option)
    cruise_info = save_cruisers_info()

    if option == 1:
        for i, cruise_info in (enumerate(cruise_info)):
            print(f'{i+1}. {cruise_info.name}')
    
    elif option == 2:
        for i, cruise_info in (enumerate(cruise_info)):
            print(f'{i+1}. {cruise_info.route[-1]}')

    option1 = enter_option(option1, msg2, invalid_option)

    return option1

def register_client(people, cruise, room, room_letter, clients, cruise_info):
    """Registra al cliente en la base de datos (txt)

    Args:
        people ([int]): [Cantidad de personas]
        cruise ([int]): [Crucero elegido por la persona.]
        room ([int]): [Habitacion escogida por el usuario.]
        room_letter ([str]): [Letra inicial de la habitacion (S, V, P)]
        clients ([list]): [Lista con los clientes]
        cruise_info ([list]): [Lista con informacion de los cruceros]

    Returns:
        [list]: [Lista de clientes con la informacion de registros actualizada.]
    """
    
    # Mensajes
    msg_clients_registration = 'Ingrese la siguiente informacion de los clientes: '
    msg_name = 'Ingrese el nombre completo: '
    msg_dni = '\nDNI: '
    msg_age = '\nEdad: '
    msg_condition = '\nTiene alguna discapacidad?(1/2)\n1. Si\n2. No\n===> '
    invalid_option = '\nError.'
    invalid_option2 = 'Error2'
    invalid_option3 = 'Error3'
    invalid_dni = '\nDebe contener al menos 5 numeros.'
    msg_halls = '\nLetra de la habitacion en la que se quiere hospedar.\n===> '
    msg_number = '\nNumero de habitación: \n===> '

    # Variables
    first_name = ''
    last_name = ''
    full_name = ''
    dni = 0
    discount = 0
    special_discount = 0
    age = 0
    condition = 0
    halls = ''
    number = 0
    room_bought = ''
    

    cruise_info = save_cruisers_info()

    if not check_file("floors.txt"):
        gen_rooms(cruise_info)


    with open("floors.txt", "rb") as data:
        floors = pickle.load(data)

    while True:
        try:
            halls = enter_input(halls, msg_halls, invalid_option3).capitalize()
            if halls not in (floors[cruise][room]).keys():
                raise
            else:
                break
        except:
            print(invalid_option3)
            break

    while True:
        try:
            number = enter_option(number, msg_number, invalid_option2)
            if str(number) not in floors[cruise][room][halls]:
                raise
            else:
                break
        except:
            print(invalid_option)
            break
    
    
    room_bought = room_letter + halls + str(number)
    floors[cruise][room][halls].remove(str(number))

    with open("floors.txt", "wb") as data:
        pickle.dump(floors, data)
    
    with open("rooms.txt", "rb") as a:
        rooms = pickle.load(a)


    for room in rooms[cruise]:
        if room.code == room_bought:
            room.room_available()
            room.family_description()
            client_room = room


    print(msg_clients_registration)

    # if check_file("clients.txt"):
    #     with open("clients.txt", "rb") as ci:
    #         registered_clients = pickle.load

    for i in range(people):

        
        full_name = enter_input(full_name, msg_name, invalid_option)

        while True:
            try:
                dni = enter_option(dni, msg_dni, invalid_option)
                if len(str(dni)) < 5:
                    raise
                else:
                    break
            except:
                print(invalid_dni)

        if prime_number(dni):
            discount = 0.10
        elif abundant_number(dni):
            discount = 0.15
        
        while True:
            try:
                age = enter_option(age, msg_age, invalid_option)
                break
                
            except:
                print(invalid_option)
        
        while True:
            try:
                condition = enter_option(condition, msg_condition, invalid_option)
                if condition == 1:
                    condition = True
                    special_discount = 0.3
                    break

                elif condition == 2:
                    condition = False
                    break
                
                else:
                    raise
            except:
                print(invalid_option)


        price = (client_room.price) * (1 - special_discount - discount)
        selected_cruise = cruise_info[cruise].name

        client = Client(full_name, dni, age, condition, selected_cruise, room_bought, price, False)

        clients.append(client)

        with open("rooms.txt", "wb") as a:
            pickle.dump(rooms, a)

    return clients

def prime_number(dni):
    """Verifica si el numero del DNI del cliente es un numero primo.

    Args:
        dni ([int]): [DNI del cliente.]

    Returns:
        [bool]: [Devuelve True si el numero es primo, falso si el numero no es primo.]
    """
    prime = False

    for number in range(2, dni+1):
        if (dni%number) == 0:
            prime = False
            break
        else:
            prime = True
    
    return prime

def abundant_number(dni):
    """Verifica si el DNI del cliente es un numero abundante.

    Args:
        dni ([int]): [DNI del cliente.]

    Returns:
        [bool]: [Retorna True si el numero es abundante, False si no es.]
    """
    abundant = False
    divisores = 0

    for i in range(1,dni):
        if dni % i == 0:
            divisores += i
    if divisores > dni:
        abundant = True
    else:
        abundant = False
    return abundant

def gen_rooms():
    """[Funcion que genera las habitaciones de los cruceros en forma matricial con la letra de habitacion, la letra del pasillo y el numero de habitacion.]
    """
    cruisers_info = save_cruisers_info()

    letters = string.ascii_uppercase
    alphabet = list(letters)
    all_rooms = []
    all_floors = []
    cruise_rooms = []
    cruise_floors = []

    room_type = ['simple', 'premium', 'vip']
    room_letters = ['S', 'P', 'P']
    room_info = ['Room Service', 'Vista al mar', 'Fiestas privadas']

    for cruise in cruisers_info:
        for i in range(len(room_type)):
            type_of_room = room_type[i]
            hall_repr = {(alphabet[i]): [str(x+1) for x in range(cruise.rooms[type_of_room][1])] for i in range(cruise.rooms[type_of_room][0])}

            room_capacity = cruise.room_capacity[type_of_room]
            room_price = cruise.room_price[type_of_room]
            room_information = room_info[i]
            aux_letter = room_letters[i]
            for key in hall_repr.keys():
                letter = key
                for u in hall_repr[key]:
                    number = str(u)
                    code = aux_letter + letter + number

                    room = Room(type_of_room, letter, number, code, '', room_capacity, room_price, room_information, True)

                    cruise_rooms.append(room)

            cruise_floors.append(hall_repr)

        all_rooms.append(cruise_rooms)
        all_floors.append(cruise_floors)
    
    print(all_floors)
    print(all_rooms)

        

    with open("floors.txt", "wb") as data:
            pickle.dump(all_floors, data)
        
    with open("rooms.txt", "wb") as data:
            pickle.dump(all_rooms, data)

def print_rooms(cruise, room):
    """Muestra al usuario las habitaciones en forma de matriz.

    Args:
        cruise: Crucero elegido por el cliente.
        room: habitacion elegida por el cliente.
    """
    # Mensajes
    msg1 = 'Habitaciones disponibles:\n'
    
    with open("floors.txt", "rb") as data:
        floors = pickle.load(data)
    
    print(msg1)

    for letter, number in floors[cruise][room].items():
        for x in range(len(number)):
            print(f"{letter}{number[x]}" , end = " ")
        print()

def sell_rooms():
    """[Recopila la informacion necesaria para proceder a la venta de habitaciones del crucero.]
    """

    # Mensajes
    msg1 = 'Como desea ver las opciones de crucero?\n1. Segun su nombre (1) \n2. Segun el destino del crucero (2)\n===> '
    msg_select_cruisers = 'Seleccione el numero del crucero de su eleccion.\n===> '
    msg2 = 'Que tipo de habitacion desea? (1/2/3)\n1. Simple\n2. Premium\n3. VIP.\n===> '
    msg3 = 'Cuantas personas viajan?\n===> '
    msg4 = 'El numero de personas que viajan excede la capacidad maxima de la habitacion. Deberá comprar mas de una habitacion.'
    invalid_option = 'Error. Introduzca una opcion valida.'

    # Variables
    see_cruise_option = 0
    select_cruisers = 0
    room_option = 0
    people = 0
    room_name = ''
    room_letter = ''
    clients = []

    cruise_info = save_cruisers_info()

    if not check_file("floors.txt"):
        gen_rooms(cruise_info)
    

    # see_cruise_option = enter_option(see_cruise_option, msg1, invalid_option)

    while True:
        try:

            see_cruise_option = enter_option(see_cruise_option, msg1, invalid_option)

            if see_cruise_option == 1:
                for i, cruise_info in (enumerate(cruise_info)):
                    print(f'{i+1}. {cruise_info.name}')
                break    

            elif see_cruise_option == 2:
                for i, cruise_info in (enumerate(cruise_info)):
                    print(f'{i+1}. {cruise_info.route[-1]}')
                break 
            else:
                raise
        
        except:
            print(invalid_option)

    
    while True:
        try:
            
            select_cruisers = enter_option(select_cruisers, msg_select_cruisers, invalid_option)

            if select_cruisers not in range(1,5):
                raise
            else:
                break
        
        except:
            print(invalid_option)
            

    
    while True:
        try:
            room_option = enter_option(room_option, msg2, invalid_option)
            if room_option == 1:
                room_name = 'simple'
                room_letter = 'S'
                break
            elif room_option == 2:
                room_name = 'premium'
                room_letter = 'P'
                break
            elif room_option == 3:
                room_name = 'vip'
                room_letter = 'V'
                break  
            else:
                raise
        except:
            print(invalid_option)
    

    while True:
        try:
            people = enter_option(people, msg3, invalid_option)
            if people < 1:
                raise
                
            else:
                break
        except:
            print(invalid_option)

    
    with open("floors.txt", "rb") as data:
        floors = pickle.load(data)

    selected_cruise = cruise_info.name[select_cruisers - 1]
    room_capacity = cruise_info.room_capacity[room_name]
    cruise = (select_cruisers) - 1
    room = (room_option) - 1 

    if people > room_capacity:
        print(msg4)

        while people > room_capacity:
            print_rooms(cruise, room)
            register_client(room_capacity, cruise, room, room_letter, clients, cruise_info)
            people = people - room_capacity
        print_rooms(cruise, room)
        register_client(people, cruise, room, room_letter, clients, cruise_info)

    else:
        print_rooms(cruise, room)
        register_client(people, cruise, room, room_letter, clients, cruise_info)

    occupied_rooms = []
    total_payment = []

    print('Clientes:')
    for client in clients:
        print(client.show_client_info())
        occupied_rooms.append(client.room_bought)
        total_payment.append(client.price)
    total = sum(total_payment)
    sold_rooms = set(occupied_rooms)
    info_occupied_rooms = ',' .join(sold_rooms)

    print(f'Habitaciones: {info_occupied_rooms}')
    room_price = cruise_info.room_price[room_name]*len(clients)
    iva = room_price * 0.16
    print(f'''
-------------------------------------
||Precio: ${room_price}
||IVA: ${iva}
||Total a pagar: ${room_price+iva}
-------------------------------------
''')

    if not check_file("clients.txt"):
        with open("clients.txt", "wb") as ci:
            pickle.dump(clients, ci)
    
    else:
        with open("clients.txt", "rb") as rc:
            new_clients = pickle.load(rc)
            for client in clients:
                new_clients.append(client)

    with open("clients.txt", "wb") as ci:
        pickle.dump(clients, ci)

def enter_price(price, msg_product_price, invalid_text):
    """Recibe un input y verifica que sea de tipo float/int para generar el precio de cada producto.

    Args:
        price ([float]): [Precio del producto]
        msg_product_price ([string]): ['Indique el precio del articulo']
        invalid_text ([string]): [Error: Introduzca un texto/una opcion valid@.]

    Returns:
        [float]: [Retorna el precio del producto en forma de float.]
    """

    product_price = float(input(msg_product_price))
    while not(product_price):
        print(invalid_text)
        product_price = float(input(msg_product_price))
    
    return product_price

def gen_menu(menu, msg1, msg2):
    """[Añade los productos a un diccionario llamado "Menu".]

    Args:
        menu ([dict]): [Estructura de datos utilizada para almacenar la informacion de los productos del restaurante.]
        msg1 ([string]): [El menú de opciones a escoger por el usuario para seleccionar la tarea a realizar.]
        msg2 ([string]): [Error: Introduzca una opcion valida.]

    Returns:
        [dict]: [Regresa el diccionario con el producto añadido.]
    """
    # Mensajes
    msg_welcome_menu_rest = '\nAcá podrá agregar productos a nuestro asombroso Menu!'
    # Productos / Creacion / Eliminar
    msg_create_product = 'Para introducir un nuevo articulo al menu introduzca los siguientes datos:'
    msg_product_name = 'Nombre del articulo que desea añadir.\n===> '
    msg_food_type = 'Indique el tipo de producto (Alimento (1) / Bebida (2)).\n===> '
    msg_food_package = 'Indique el empaquetado del producto (Listo para consumir (1) / Para preparar (2).\n===> '
    msg_drink_size = 'Indique el tamaño de la bebida (Pequeño (P) / Mediano (M) / Grande (G).\n===> '
    msg_product_price = 'Indique el precio del producto.\n===> '
    msg_update_product = 'Indique el nombre del producto que desea modificar del menu.\n===> '
    msg_find_product_name_price = 'Indique el nombre o el precio del producto que desea buscar.\n===> '
    msg_add_more_products = 'Quisiera añadir otro articulo al menú? (Si (1)/ No (2))\n===> '
    msg_added_succesfully = 'Producto añadido satisfactoriamente!'

    # Mensajes Error
    invalid_text = 'Introduzca un texto/una opcion valid@.'

    # Variables
    product_name = ''
    food_type = 0
    food_package = 0
    drink_size = ''
    price = 0
    add_more = 0
    iva = 0.16
    flag = True
   
    # Option 1 Msg
    print(msg_welcome_menu_rest)
    print()
    print(msg_create_product)
        # Inputs

        # Nombre del producto
    product_name = enter_input(product_name, msg_product_name,invalid_text).title()

    while product_name == "":
        print('No puede dejar el nombre del producto vacio.')
        product_name = enter_input(product_name, msg_product_name,invalid_text).title()
        
        
    # Tipo de producto (Bebida o Alimento)
    food_type = enter_option(food_type, msg_food_type,invalid_text)
    # Opcion 1: Alimento

    if food_type == 1:
        # 1) Listo para consumir / 2) Para preparar.

        food_package = enter_option(food_package,msg_food_package, invalid_text)

        if food_package == 1:
            food_package = 'Listo para consumir.'
        elif food_package == 2:
            food_package = 'Para preparar.'
        else:
            print(invalid_text)

        # Precio del alimento.
        price = enter_price(price, msg_product_price, invalid_text)
        price = price + (price * iva)

        # Se crea el objeto de alimento.
        alimento = Alimento(product_name, food_package, price)
        menu[product_name] = [food_package, ' $'+str(price)]

    # Opcion 2: Bebida
    elif food_type == 2:

        # Tamaño de la bebida (Pequeño, Mediano, Grande)
        drink_size = enter_input(drink_size, msg_drink_size,invalid_text).capitalize()

        while drink_size == "":
            print('Por favor introduzca el tamaño de la bebida.')
            drink_size = enter_input(drink_size, msg_drink_size,invalid_text).capitalize()

        if drink_size == 'P':
            drink_size = 'Pequeña'
        elif drink_size == 'M':
            drink_size = 'Mediana'
        elif drink_size == 'G':
            drink_size = 'Grande'
        else:
            print(invalid_text)
            
        # Precio de la bebida.
        price = enter_price(price, msg_product_price, invalid_text)

        price = price + (price * iva)

        # Se crea el objeto de bebida.
        drink = Drink(product_name, drink_size, price)
        menu[product_name] = [drink_size + ' $'+str(price)]


    else:
        print(invalid_text)

    print(msg_added_succesfully)
    
    with open("menu_data.txt", "wb") as file:
        pickle.dump(menu, file)

    return menu

def add_more_products(menu):
    """Funcion que permite al usuario ingresar mas productos al menu de forma mas rapida y eficiente.

    Args:
        menu ([dict]): [Menu de comida existente.]
    """
    flag = True
    msg_add_more = 'Desea añadir otro producto al menu? (Si (1)/ No (Cualquier num))\n===> '
    invalid_option = 'Error! Invalid Option, please try again.'
    msg_thanks = 'Gracias! Hasta pronto.'
    msg_welcome_menu_rest = 'Acá podrá agregar productos a nuestro asombroso Menu!'
    option = 0

    while flag:
        option = enter_option(option, msg_add_more, invalid_option)

        if option == 1:
            gen_menu(menu, msg_welcome_menu_rest, invalid_option)
        else:
            print(msg_thanks)
            flag = False

def remove_product(menu, msg_remove_welcome, error_message):
    """[Elimina un producto del menú del restaurante (lista) siempre y cuando este artículo exista.]

    Args:
        menu ([list]): [Menu del restaurante que contiene los articulos]
        msg_remove_welcome ([string]): ['Acá podrá eliminar cualquier producto del Menú del Restaurante.']
        invalid_product ([string]): ['Producto no existente.']

    Returns:
        [list]: [Retorna el Menu del restaurante (list) actualizado.]
    """

    # Mensajes
    msg_remove_welcome = 'Acá podrá eliminar cualquier producto del Menú del Restaurante.'
    msg_delete_succesfully = 'Producto eliminado correctamente.'

    # Productos
    msg_delete_product = 'Indique el nombre del producto que desea eliminar del menu.\n===> '

    # Mensajes Error
    invalid_text = 'Introduzca un producto existente.'

    # Variables
    product_name = ''

    # Inputs
    product_name = enter_input(product_name, msg_delete_product, invalid_text)

    for products in menu:
        if product_name == menu.product_name:
            pass
    
    else:
        print(invalid_text)

    return menu

def update_product(menu, msg_update_welcome, error_message):
    """Funcion que pide al usuario el nombre de un producto existente del menú. Si este producto existe, su informacion podra ser actualizada.

    Returns:
        [dict]: [Retorna el diccionario de menu actualizado.]
    """
    # Productos
    msg_update_product = 'Introduzca el nombre del producto que desea actualizar.\n===> '

    # Mensaje Error
    invalid_text = 'Introduzca un producto existente.'
    invalid_input = 'Intentelo de nuevo.'

    # Variables
    product_name = ''

    # Inputs
    product_name = enter_input(product_name, msg_update_product, invalid_input).title()

    if product_name in menu.keys():
        del menu[product_name]
        gen_menu(menu, msg_update_product, invalid_input)
    
    else:
        print(invalid_text)

def gen_combo(combos, msg_combo_welcome, msg2):
    """Funcion que genera combos y los añade a un menu de combos.

    Args:
        combos ([dict]): [es un diccionario donde se agrupan todos los combos.]
        msg_combo_welcome ([string]): ['Acá podrá crear combos para nuestro Menú de Combos!']
        msg2 ([string]): [Mensaje de error si el usuario introduce un input invalido.]

    Returns:
        [dict]: [retorna el Menú de combos (diccionario) actualizado. ]
    """
    # Mensajes
    msg_combo_welcome = '\nAcá podrá crear combos para nuestro Menú de Combos!\n'
    msg_create_combo = 'Para crear un combo, introduzca la siguiente información:'
    msg_product_name = 'Introduzca el nombre del producto.\n===> '
    msg_combo_name = 'Nombre del combo:\n===> '
    msg_combo_items = 'Productos que contendrá el combo (minimo 2). '
    msg_combo_price = 'Precio del combo:\n===> '
    msg_find_combo_name_price = 'Indique el nombre o el precio del combo que desea buscar.\n===> '
    msg_another_product = 'Quisiera añadir otro producto a su combo? (Si) / (No)'
    msg_combo_succesfully = 'Combo creado correctamente!'
    # Error
    invalid_option = 'Error!'

    # Variables 
    product_name_1 = ''
    product_name_2 = ''
    another_product = ''
    combo_name = ''
    combo_price = 0
    iva = 0.16

    # Inputs
    print(msg_combo_welcome)
    print(msg_create_combo)

    combo_name = enter_input(combo_name, msg_combo_name, invalid_option).title()
    product_name_1 = enter_input(product_name_1, msg_product_name, invalid_option).title()
    product_name_2 = enter_input(product_name_2, msg_product_name, invalid_option).title()
    combo_price = enter_price(combo_price, msg_combo_price, invalid_option)
    combo_price = combo_price + (combo_price * iva)

    combos[combo_name] = [product_name_1, product_name_2, '$'+str(combo_price)]
    print(msg_combo_succesfully)
    return combos

def remove_combo(combos):
    """ Permite al usuario eliminar un combo existente en el menu de combos, si este no existe, da un mensaje de error.

    Args:
        combos ([dict]): [Diccionario ("menú") de combos.]

    Returns:
        [dict]: [Retorna el diccionario actualizado.]
    """
    # Variables
    combo_name = ''

    # Mensajes
    msg_delete_combo = 'Introduzca el nombre del combo que desea eliminar.\n===> '
    msg_combo_error = 'El combo no existe.'

    # Inputs
    combo_name = enter_input(combo_name, msg1, msg2)
    if combo_name in combos.keys():
        del combos[combo_name]

    return combos

def find_product_menu(menu, msg_find_product_menu, invalid_option):
    """[Permite al usuario buscar productos en el menu de comida segun su nombre o precio.]

    Args:
        menu ([dict]): [menu de comida]
        msg_find_product_menu ([str]): ['Acá podrá buscar productos del Menú por nombre o rango de precio!']
        invalid_option ([type]): [description]
    """
    # Mensajes
    msg_find_product_menu = 'Acá podrá buscar productos del Menú por nombre o rango de precio!'
    msg_product_name = 'Introduzca el nombre del producto que desea buscar.\n===> '
    msg_product_min_price = 'Introduzca el precio minimo que desea filtrar.\n===> '
    msg_product_max_price = 'Introduzca el precio maximo que desea filtrar.\n===> '
    invalid_option = 'Ha introducido un nombre invalido. Por favor introduzca solo caracteres alfabeticos.'
    invalid_price = 'Ha introducido un numero invalido. Por favor introduzca solo caracteres numericos.'
    msg_find_options = 'Desea buscar el producto por nombre (1) o por rango de precio (2)?\n===> '
    msg_product_not_found = 'El producto no existe.'

    # Variables
    product_name = ''
    find_options = 0
    product_min_price = 0
    product_max_price = 0
    prueba = 0

    # Inputs
    find_options = enter_option(find_options, msg_find_options, invalid_price)

    if find_options == 1:
        product_name = enter_input(product_name, msg_product_name, invalid_option).title()
        for product in menu.keys():
            if product_name in product:
                print(product_name+':', ', '.join(menu[product_name]))
                break
        else:
            print(msg_product_not_found)
    
    elif find_options == 2:
        product_min_price = enter_price(product_min_price, msg_product_min_price, invalid_price)

        product_max_price = enter_price(product_max_price, msg_product_max_price, invalid_price)

        for product_price in menu.values():
            if product_price[1] >= product_min_price and product_price[1] <= product_max_price:
                print(menu)
        

    else:
        print(msg_product_not_found)
  
def find_combo(combos):
    """Permite al usuario buscar combos en el menu de combos segun el nombre o el precio.

    Args:
        combos ([type]): [description]
    """
    # Mensajes
    msg_find_combo_welcome = 'Acá podrá buscar combos ya existentes!'
    msg_find_combo = 'Introduzca su forma de busqueda preferida: nombre (1), o rango de precio (2).\n===> '
    msg_combo_not_found = 'El combo no existe.'
    invalid_option = 'Error, intente de nuevo.'
    msg_combo_name = 'Introduzca el nombre del combo que desea buscar:\n===> '

    # Variables
    option = 0
    combo_name = ''

    # Input
    print(msg_find_combo_welcome+'\n')
    option = enter_option(option, msg_find_combo, invalid_option)

    if option == 1:
        combo_name = enter_input(combo_name, msg_combo_name, invalid_option).title()

        if combo_name in combos.keys():
            print(combo_name+' incluye:', ', '.join(combos[combo_name]))
    
    elif option == 2:
        sorted_combos = sorted(combos.items(), key=lambda kv: kv[2])
        combos = sorted_combos
        print(combos)
    
    else:
        print(invalid_option)

def show_tours(tours, msg1, ms2):
    """Muestra toda la informacion de los tours disponibles.

    Args:
        tours ([list]): [Lista de diccionarios que contiene la informacion de cada tour.]

        msg1 ([str]): ['En Saman Cruise tenemos los mejores Tours para que disfrutes con tus acompañantes!']

        ms2 ([str]): [Invalid Option.]
    
    Returns:
        Devuelve al usuario toda la informacion de cada tour disponible.
    """

    tours_list = []
    for tour in tours:
        tour_name = tour["name"]
        tour_price = tour["price"]
        tour_group_capacity = tour["group_cap"]
        tour_starting_hour = tour["starting_hour"]
        tour_max_capacity = tour["max_capacity"]
        tour = Tour(tour_name, tour_price, tour_group_capacity, tour_starting_hour, tour_max_capacity)
        tours_list.append(tour)
    
    for tour in tours_list:
        print(tour, '\n')
        
def select_tour(tours, msg_tour_welcome, invalid_option):

    """Permite al usuario seleccionar el Tour que desea vender y calcula toda la informacion necesaria correspondiente a los cupos y la disponibilidad del tour.

    Args:
        tours ([list]): [Lista de diccionarios que contiene la informacion de cada tour.]

        msg_tour_welcome ([str]): ['En Saman Cruise tenemos los mejores Tours para que disfrutes con tus acompañantes!']

        invalid_option ([str]): ['Invalid option.']

    Returns:
        Imprime al usuario la factua del cliente con toda la informacion incluida. (DNI del cliente, fecha de compra, cantidad de tickets, precio total.)
    """
    
    # Mensajes
    msg1 = '\nPor favor seleccione el tour que desea vender.\n===> '
    msg2 = 'Introduzca el DNI del cliente.\n===> '
    msg_error = 'Error!'
    msg3 = 'Cuantos tickets desea comprar?\n===> '
    msg_error_too_much_people = 'Su selección excede el cupo maximo por grupo.'
    msg_not_enough_cupos = 'No quedan suficientes cupos para el tour que ha seleccionado.'

    # Variables
    client_dni = 0
    option = 0
    cupos_max_group = 0
    cupos_max_tour = 0
    limits_group = []
    limits_tour = []
    price_list = []
    tour_name = []
    tour_tickets = 0
    discount = 0
    price = 0
    total_price = 0
    availability = 0
    name = ''
    hour_sold = datetime.datetime.now()

    with open("clients.txt", "rb") as ci:
        clients = pickle.load(ci)

    # Inputs
    client_dni = enter_option(client_dni, msg2, msg_error)
    
    for i, tour in enumerate(tours, 1):
        print(i, '. ' + tour["name"] + ', precio por persona: $' + str(tour["price"]) + '. Capacidad maxima por grupo: ' + str(tour["group_cap"])+' personas.' + ' Cupo total del tour: ' + str(tour["max_capacity"]) + ' personas.\n', sep='',end='\n')
    
    # Opcion para elegir el numero del tour que desea comprar.
    option = enter_option(option, msg1, invalid_option)

    # Se añade el limite de cada tickets que puede comprar un mismo grupo en una lista aparte.
    for x in range(len(tours)):
        limits_group.append(tours[x]["group_cap"])

    # Se añade el limite de cada tour en una lista aparte.
    for i in range(len(tours)):
        limits_tour.append(tours[i]["max_capacity"])
    
    # Se añade el precio de cada tour en una lista aparte.
    for z in range(len(tours)):
        price_list.append(tours[z]["price"])
    
    # Se añade el nombre de cada tour en una lista aparte.
    for y in range(len(tours)):
        tour_name.append(tours[y]["name"])
    
    # Tour #1
    if option == 1:

        name = tour_name[0]
        cupos_max_group = limits_group[0]
        cupos_max_tour = limits_tour[0]
        price = price_list[0]

    # Tour #2
    elif option == 2:
        name = tour_name[1]
        cupos_max_group = limits_group[1]
        cupos_max_tour = limits_tour[1]
        price = price_list[1]

    # Tour #3
    elif option == 3:
        name = tour_name[2]
        cupos_max_group = limits_group[2]
        cupos_max_tour = limits_tour[2]
        price = price_list[2]

        if str(cupos_max_group):
            name = tour_name[2]
            cupos_max_group = 999999999999999999999
            cupos_max_tour = 999999999999999999999
            price = 0

    # Tour #4
    elif option == 4:
        name = tour_name[3]
        cupos_max_group = limits_group[3]
        cupos_max_tour = limits_tour[3]
        price = price_list[3]

    # Opcion invalida
    else:
        print(msg_error)

    
    tour_tickets = enter_option(tour_tickets, msg3, invalid_option)

    # Se valida que el usuario no compre mas boletos de los que se ofrecen por grupo.
    if tour_tickets > cupos_max_group:
        print(msg_error_too_much_people)
    
    # Se calcula el precio del tour. (precio de tickes * personas y se aplica el descuento correspondiente si se cumple la condicion dada.)
    if option == 1 and tour_tickets >= 3:
        discount = 0.1
        total_price = (price * tour_tickets) - (discount * (price * tour_tickets))
        availability = cupos_max_tour - tour_tickets


    # Se calcula el precio del tour. (precio de tickes * personas)
    elif option == 1 and tour_tickets < 3:
        total_price = price * tour_tickets
        availability = cupos_max_tour - tour_tickets
    
    # Se calcula el precio del tour. (precio de tickes * personas)
    if option == 2:
        total_price = price * tour_tickets
        availability = cupos_max_tour - tour_tickets
    
    # Se calcula el precio del tour. (gratis)
    if option == 3:
        total_price = 0
    
    # Se calcula el precio del tour. (precio de tickes * personas y se aplica el descuento correspondiente si se cunple la condicion dada.)
    if option == 4 and tour_tickets >= 3:
        discount = 0.1
        total_price = (price * tour_tickets) - (discount * (price*tour_tickets))

    # Se imprime un mensaje que indica que se han acabado los cupos para un tour especifico.
    if availability == 0:
        print(f'Se han acabado los cupos del tour "{name}".')
    
    # Se valida que la cantidad de tickets pedida por el cliente no exceda la disponibilidad en el momento.
    if tour_tickets > availability:
        print(msg_not_enough_cupos)

    # Formato de factura para el cliente.
    else:
        print(f''' 
--------------------------------------------------------------
|| Felicidades por su compra! Los detalles son los siguientes: 
|| Cliente: {client_dni}
|| Fecha de compra: {hour_sold}
|| Tickets comprados: {tour_tickets}
|| Precio total: ${total_price}
--------------------------------------------------------------

''')

    for client_info in clients:
        if client_dni == client_info.dni:
            price += total_price

    # with open("clients.txt", "wb") as ci:
    #     pickle.dump(price, ci)

def statistics():
    """Permite al usuario ver las estadisticas de la empresa de cruceros.
    """
    # Variables
    option = 0
    top_sellers = []
    
    # Mensajes
    msg_statistics = '''Que estadisticas desea ver?
1. Promedio de gastos por cliente.
2. Porcentaje de clientes que no compran tours.
3. Clientes de mayor fidelidad.
4. Top cruceros con ventas en tickets.
5. Top 5 productos de nuestros restaurantes.
===> '''
    invalid_option = 'Error. Opcion invalida.'

    option = enter_option(option, msg_statistics, invalid_option)
    cruise_info = save_api_info()

    if option == 1:
        pass

    elif option == 2:
        pass

    elif option == 3:
        with open("clients.txt", "rb") as ci:
            clients = pickle.load(ci)
        for i, client_info in enumerate(clients):
            print(f'''
-----------------------------------
{i+1}. Cliente: {client_info.name}   
DNI: {client_info.dni}
Ha pagado: ${client_info.price}   
-----------------------------------
        ''')

    elif option == 4:
        pass

    elif option == 5:
        for x in range(len(cruise_info)):
            for food in cruise_info[x]["sells"]:
                food_list = [food["name"], food["amount"]]
                top_sellers.append(food_list)
        
        top_sellers_sorted = sorted(top_sellers, key = lambda k: k[1], reverse = True)
        for y in range(5):
            print(top_sellers_sorted[y])
        
        
        # for x, item in enumerate(top_sellers_sorted):
        #     my_print = (f'{x+1}. {item[0]} - Precio: {item[1]} - Vendidos: {item[2]}')
        #     print(my_print)

    elif option == 7:
        pass

    else:
        print(invalid_option)


    


        

