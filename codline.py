import os

FILENAME = "password_manager.txt"
ADMIN_USERNAME = "aadmin"
ADMIN_PASSWORD = "admin"

def load_data():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as file:
        lines = file.readlines()
    data = []
    for i in range(0, len(lines), 4):  # Leemos cada bloque de 4 líneas
        site = lines[i].strip().replace("Sitio web / Aplicación: ", "")
        username = lines[i+1].strip().replace("Usuario / Correo: ", "")
        password = lines[i+2].strip().replace("Contraseña: ", "")
        data.append([site, username, password])
    return data

def save_data(data):
    with open(FILENAME, "w") as file:
        for item in data:
            file.write(f"Sitio web / Aplicación: {item[0]}\n")
            file.write(f"Usuario / Correo: {item[1]}\n")
            file.write(f"Contraseña: {item[2]}\n")
            file.write("----------------------------------------------------------------------\n")

def add_user():
    site = input("Ingrese el enlace o nombre del sitio: ")
    username = input("Ingrese el usuario o correo electrónico: ")
    password = input("Ingrese la contraseña: ")
    data = load_data()
    data.append([site, username, password])
    save_data(data)
    print("Usuario/Correo añadido correctamente.")

def authenticate_admin():
    username = input("Ingrese el nombre de usuario de admin: ")
    password = input("Ingrese la contraseña de admin: ")
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def view_users():
    if not authenticate_admin():
        print("¡Acceso denegado! Usuario o contraseña incorrectos.")
        return

    data = load_data()
    print("\nOpciones de filtro:")
    print("1. Orden alfabético por sitio")
    print("2. Orden alfabético por correo electrónico")
    print("3. Orden alfabético por usuario")
    print("4. Orden alfabético por aplicación")

    filter_option = input("Elija una opción de filtro (1-4): ")

    if filter_option == "1":
        data = sorted(data, key=lambda x: x[0])
    elif filter_option == "2":
        data = sorted(data, key=lambda x: x[1] if "@" in x[1] else "")
    elif filter_option == "3":
        data = sorted(data, key=lambda x: x[1])
    elif filter_option == "4":
        data = sorted(data, key=lambda x: x[0])
    else:
        print("Opción no válida.")
        return

    print("\nUsuarios / Correos y Contraseñas:")
    for entry in data:
        print(f"Sitio web / Aplicación: {entry[0]}")
        print(f"Usuario / Correo: {entry[1]}")
        print(f"Contraseña: {entry[2]}")
        print("----------------------------------------------------------------------")

def modify_or_delete_user():
    if not authenticate_admin():
        print("¡Acceso denegado! Usuario o contraseña incorrectos.")
        return

    data = load_data()
    print("\nUsuarios / Correos actuales:")
    for idx, entry in enumerate(data):
        print(f"{idx + 1}. Sitio web / Aplicación: {entry[0]}, Usuario/Correo: {entry[1]}, Contraseña: {entry[2]}")

    try:
        choice = int(input("\nElija el número del usuario que desea modificar/eliminar (0 para cancelar): "))
        if choice == 0:
            return
        if choice < 1 or choice > len(data):
            print("Número no válido.")
            return

        print("\nOpciones:")
        print("1. Modificar")
        print("2. Eliminar")
        action = input("Seleccione una acción (1-2): ")

        if action == "1":
            new_site = input("Ingrese el nuevo enlace/nombre del sitio (presione Enter para mantener el actual): ")
            new_username = input("Ingrese el nuevo usuario/correo (presione Enter para mantener el actual): ")
            new_password = input("Ingrese la nueva contraseña (presione Enter para mantener la actual): ")

            if new_site:
                data[choice - 1][0] = new_site
            if new_username:
                data[choice - 1][1] = new_username
            if new_password:
                data[choice - 1][2] = new_password

            save_data(data)
            print("Usuario/Correo modificado correctamente.")
        elif action == "2":
            data.pop(choice - 1)
            save_data(data)
            print("Usuario/Correo eliminado correctamente.")
        else:
            print("Opción no válida.")
    except ValueError:
        print("Entrada no válida.")

def main_menu():
    while True:
        print("\n--- Administrador de Contraseñas ---")
        print("1. Añadir usuario / correo electrónico y contraseña")
        print("2. Ver listado de usuarios / correos electrónicos y contraseñas")
        print("3. Modificar / Eliminar usuario / correo electrónico y contraseña")
        print("4. Salir")

        option = input("Seleccione una opción (1-4): ")

        if option == "1":
            add_user()
        elif option == "2":
            view_users()
        elif option == "3":
            modify_or_delete_user()
        elif option == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

if __name__ == "__main__":
    main_menu()
