import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
import time
import threading
import winsound
from PIL import Image, ImageTk  # Asegúrate de tener Pillow instalado para manejar imágenes

# Variables globales para el almacenamiento de usuarios y alarmas
USER_DATA_FILE = 'user_data.json'
ALARM_DATA_FILE = 'alarm_data.json'


def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    return {}


def save_data(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file)


class AlarmApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alarm Dashboard")
        self.geometry("500x500")
        self.configure(bg="#01110e")  # Color de fondo oscuro principal

        self.users = load_data(USER_DATA_FILE)
        self.alarms = load_data(ALARM_DATA_FILE)
        self.current_user = None
        self.current_avatar = None

        self.show_login_screen()

    # Estilo de botones
    def create_styled_button(self, text, command, color, emoji):
        button = tk.Button(self, text=f"{emoji} {text}", command=command, bg=color, fg="white", borderwidth=0, width=30)
        button.config(font=("Arial", 12, "bold"), relief="flat")
        button.pack(pady=10, padx=20, fill=tk.X)
        button["highlightthickness"] = 0
        return button

    def show_login_screen(self):
        self.clear_window()

        # Pantalla de inicio de sesión
        tk.Label(self, text="Login", font=("Arial Bold", 24), bg="#01110e", fg="#edf365").pack(pady=20)

        tk.Label(self, text="Username:", bg="#01110e", fg="#edf365").pack()
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:", bg="#01110e", fg="#edf365").pack()
        self.password_entry = tk.Entry(self, show='*', width=30)
        self.password_entry.pack(pady=5)

        self.create_styled_button("Login", self.login_user, "#16928c", "🔓")
        self.create_styled_button("Register", self.show_registration_screen, "#16928c", "📝")

    def show_registration_screen(self):
        self.clear_window()

        # Pantalla de registro
        tk.Label(self, text="Register", font=("Arial Bold", 24), bg="#01110e", fg="#edf365").pack(pady=20)

        tk.Label(self, text="Username:", bg="#01110e", fg="#edf365").pack()
        self.reg_username_entry = tk.Entry(self, width=30)
        self.reg_username_entry.pack(pady=5)

        tk.Label(self, text="Password:", bg="#01110e", fg="#edf365").pack()
        self.reg_password_entry = tk.Entry(self, show='*', width=30)
        self.reg_password_entry.pack(pady=5)

        tk.Label(self, text="Email:", bg="#01110e", fg="#edf365").pack()
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.pack(pady=5)

        tk.Label(self, text="Select Avatar:", bg="#01110e", fg="#edf365").pack(pady=10)
        self.avatar_var = tk.StringVar(value="avatar1")
        self.create_avatar_selection()

        self.create_styled_button("Register", self.register_user, "#16928c", "✅")

    def create_avatar_selection(self):
        avatars_frame = tk.Frame(self)
        avatars_frame.pack()

        for i in range(1, 7):
            avatar_path = f"assets/images/avatar{i}.png"
            avatar_image = Image.open(avatar_path)
            avatar_image.thumbnail((50, 50))
            photo = ImageTk.PhotoImage(avatar_image)

            avatar_button = tk.Radiobutton(avatars_frame, image=photo, variable=self.avatar_var, value=f"avatar{i}", borderwidth=0)
            avatar_button.image = photo  # Mantener la referencia
            avatar_button.pack(side=tk.LEFT)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users and self.users[username]['password'] == password:
            self.current_user = username
            self.current_avatar = self.users[username]['avatar']
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register_user(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        email = self.email_entry.get()
        avatar = self.avatar_var.get()

        if username in self.users:
            messagebox.showerror("Error", "User already exists")
            return

        self.users[username] = {
            'password': password,
            'email': email,
            'avatar': avatar
        }
        save_data(USER_DATA_FILE, self.users)
        messagebox.showinfo("Success", "User registered successfully")
        self.show_login_screen()

    def show_dashboard(self):
        self.clear_window()

        tk.Label(self, text=f"Welcome, {self.current_user}", font=("Arial Bold", 24), bg="#01110e", fg="#edf365").pack(pady=20)

        # Mostrar el avatar
        avatar_path = f"assets/images/{self.current_avatar}.png"
        avatar_image = Image.open(avatar_path)
        avatar_image.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(avatar_image)

        avatar_label = tk.Label(self, image=photo, bg="#01110e")
        avatar_label.photo = photo  # Mantener la referencia
        avatar_label.pack()

        self.create_styled_button("Create Alarm", self.create_alarm, "#16928c", "⏰")
        self.create_styled_button("Edit Alarm", self.edit_alarm, "#16928c", "✏️")
        self.create_styled_button("Delete Alarm", self.delete_alarm, "#16928c", "🗑️")
        self.create_styled_button("View Alarms", self.view_alarms, "#16928c", "👁️")
        self.create_styled_button("Logout", self.logout, "#FF5733", "🚪")

    def create_alarm(self):
        alarm_window = tk.Toplevel(self)
        alarm_window.title("Create Alarm")
        alarm_window.geometry("400x350")
        alarm_window.configure(bg="#3ef7dd")  # Color de fondo de la ventana de alarma

        # Asunto de la alarma
        tk.Label(alarm_window, text="Alarm Subject:", font=("Arial", 14), bg="#3ef7dd", fg="#01110e").pack(pady=10)
        self.alarm_subject_entry = tk.Entry(alarm_window, width=30)
        self.alarm_subject_entry.pack(pady=5)

        # Selección de hora
        tk.Label(alarm_window, text="Set Alarm Time", font=("Arial", 14), bg="#3ef7dd", fg="#01110e").pack(pady=10)

        time_frame = tk.Frame(alarm_window, bg="#3ef7dd")
        time_frame.pack()

        self.hour_var = tk.StringVar(value="12")
        self.minute_var = tk.StringVar(value="00")
        self.am_pm_var = tk.StringVar(value="AM")

        hour_entry = ttk.Combobox(time_frame, textvariable=self.hour_var, values=[f"{i:02}" for i in range(1, 13)], width=3)
        hour_entry.grid(row=0, column=0, padx=5)

        minute_entry = ttk.Combobox(time_frame, textvariable=self.minute_var, values=[f"{i:02}" for i in range(60)], width=3)
        minute_entry.grid(row=0, column=1, padx=5)

        am_pm_entry = ttk.Combobox(time_frame, textvariable=self.am_pm_var, values=["AM", "PM"], width=5)
        am_pm_entry.grid(row=0, column=2, padx=5)

        # Selección de días
        tk.Label(alarm_window, text="Select Days:", font=("Arial", 14), bg="#3ef7dd", fg="#01110e").pack(pady=10)
        
        days_frame = tk.Frame(alarm_window, bg="#3ef7dd")
        days_frame.pack(pady=5)

        self.days_var = {day: tk.IntVar() for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
        for day in self.days_var:
            tk.Checkbutton(days_frame, text=day, variable=self.days_var[day], bg="#3ef7dd", fg="#01110e").pack(side=tk.LEFT)

        self.create_styled_button("Save Alarm", lambda: self.save_alarm(alarm_window), "#16928c", "💾")

    def save_alarm(self, alarm_window):
        subject = self.alarm_subject_entry.get()
        hour = self.hour_var.get()
        minute = self.minute_var.get()
        period = self.am_pm_var.get()
        days = [day for day, var in self.days_var.items() if var.get()]

        if not subject or not hour or not minute or not days:
            messagebox.showerror("Error", "All fields are required!")
            return

        alarm_time = f"{hour}:{minute} {period}"

        alarm_info = {
            'name': subject,
            'time': alarm_time,
            'days': days
        }

        if self.current_user not in self.alarms:
            self.alarms[self.current_user] = []

        self.alarms[self.current_user].append(alarm_info)
        save_data(ALARM_DATA_FILE, self.alarms)

        messagebox.showinfo("Success", "Alarm created successfully!")

        threading.Thread(target=self.check_alarms, daemon=True).start()
        alarm_window.destroy()  # Close the alarm creation window

    def edit_alarm(self):
        # Implementar la lógica para editar una alarma existente
        messagebox.showinfo("Info", "Edit Alarm feature not implemented yet.")

    def delete_alarm(self):
        # Implementar la lógica para eliminar una alarma
        messagebox.showinfo("Info", "Delete Alarm feature not implemented yet.")

    def view_alarms(self):
        alarms = self.alarms.get(self.current_user, [])
        alarm_list = "\n".join([f"{a['name']} at {a['time']} on {', '.join(a['days'])}" for a in alarms])

        if not alarm_list:
            alarm_list = "No alarms set."

        messagebox.showinfo("Your Alarms", alarm_list)

    def check_alarms(self):
        while True:
            current_time = time.strftime("%I:%M %p")  # Formato HH:MM AM/PM
            current_day = time.strftime("%a")

            for alarm in self.alarms.get(self.current_user, []):
                if current_time == alarm['time'] and current_day[:3] in alarm['days']:
                    self.activate_alarm(alarm['name'])
            
            time.sleep(60)

    def activate_alarm(self, alarm_name):
        messagebox.showinfo("Alarm", f"{alarm_name} is ringing!")
        winsound.Beep(1000, 1000)  # Sonido de alarma, ajusta la frecuencia y duración

    def logout(self):
        self.current_user = None
        self.show_login_screen()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = AlarmApp()
    app.mainloop()