import os
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

FILENAME = "password_manager.txt"
ADMIN_USERNAME = "adminEMP"
ADMIN_PASSWORD = "123456abc987"

def load_data():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as file:
        lines = file.readlines()
    data = []
    for i in range(0, len(lines), 4):
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

def add_user_gui():
    site = simpledialog.askstring("Añadir Usuario", "Ingrese el enlace o nombre del sitio:")
    if not site:
        return
    username = simpledialog.askstring("Añadir Usuario", "Ingrese el usuario o correo electrónico:")
    if not username:
        return
    password = simpledialog.askstring("Añadir Usuario", "Ingrese la contraseña:")
    if not password:
        return

    data = load_data()
    data.append([site, username, password])
    save_data(data)
    messagebox.showinfo("Añadir Usuario", "Usuario/Correo añadido correctamente.")

def authenticate_admin():
    username = simpledialog.askstring("Autenticación", "Ingrese el nombre de usuario de admin:")
    password = simpledialog.askstring("Autenticación", "Ingrese la contraseña de admin:", show="*")
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def view_users_gui():
    if not authenticate_admin():
        messagebox.showerror("Error", "¡Acceso denegado! Usuario o contraseña incorrectos.")
        return

    data = load_data()
    
    view_window = tk.Toplevel()
    view_window.title("Ver Usuarios / Correos")

    text_area = scrolledtext.ScrolledText(view_window, width=80, height=20)
    text_area.pack()

    for entry in data:
        text_area.insert(tk.END, f"Sitio web / Aplicación: {entry[0]}\n")
        text_area.insert(tk.END, f"Usuario / Correo: {entry[1]}\n")
        text_area.insert(tk.END, f"Contraseña: {entry[2]}\n")
        text_area.insert(tk.END, "----------------------------------------------------------------------\n")

def modify_or_delete_user_gui():
    if not authenticate_admin():
        messagebox.showerror("Error", "¡Acceso denegado! Usuario o contraseña incorrectos.")
        return

    data = load_data()
    if not data:
        messagebox.showinfo("Modificar/Eliminar", "No hay usuarios para mostrar.")
        return

    modify_window = tk.Toplevel()
    modify_window.title("Modificar / Eliminar Usuarios")
    
    label = tk.Label(modify_window, text="Seleccione un usuario para modificar o eliminar:")
    label.pack()

    listbox = tk.Listbox(modify_window, width=100)
    for idx, entry in enumerate(data):
        listbox.insert(tk.END, f"{idx + 1}. Sitio web / Aplicación: {entry[0]}, Usuario/Correo: {entry[1]}")
    listbox.pack()

    def modify_selected():
        selection = listbox.curselection()
        if not selection:
            return
        index = selection[0]
        entry = data[index]

        new_site = simpledialog.askstring("Modificar Usuario", "Ingrese el nuevo enlace/nombre del sitio (presione Enter para mantener el actual):", initialvalue=entry[0])
        new_username = simpledialog.askstring("Modificar Usuario", "Ingrese el nuevo usuario/correo (presione Enter para mantener el actual):", initialvalue=entry[1])
        new_password = simpledialog.askstring("Modificar Usuario", "Ingrese la nueva contraseña (presione Enter para mantener la actual):", initialvalue=entry[2])

        if new_site:
            data[index][0] = new_site
        if new_username:
            data[index][1] = new_username
        if new_password:
            data[index][2] = new_password

        save_data(data)
        messagebox.showinfo("Modificar Usuario", "Usuario/Correo modificado correctamente.")
        modify_window.destroy()

    def delete_selected():
        selection = listbox.curselection()
        if not selection:
            return
        index = selection[0]
        del data[index]
        save_data(data)
        messagebox.showinfo("Eliminar Usuario", "Usuario/Correo eliminado correctamente.")
        modify_window.destroy()

    modify_button = tk.Button(modify_window, text="Modificar", command=modify_selected)
    modify_button.pack()

    delete_button = tk.Button(modify_window, text="Eliminar", command=delete_selected)
    delete_button.pack()

def main_gui():
    root = tk.Tk()
    root.title("Administrador de Contraseñas")

    label = tk.Label(root, text="--- Administrador de Contraseñas ---", font=("Arial", 14))
    label.pack(pady=10)

    add_button = tk.Button(root, text="Añadir usuario / correo electrónico y contraseña", command=add_user_gui)
    add_button.pack(pady=5)

    view_button = tk.Button(root, text="Ver listado de usuarios / correos electrónicos y contraseñas", command=view_users_gui)
    view_button.pack(pady=5)

    modify_button = tk.Button(root, text="Modificar / Eliminar usuario / correo electrónico y contraseña", command=modify_or_delete_user_gui)
    modify_button.pack(pady=5)

    exit_button = tk.Button(root, text="Salir", command=root.quit)
    exit_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
