import tkinter as tk
from tkinter import ttk, messagebox
import json

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        # Intenta cargar tareas desde el archivo JSON existente
        try:
            with open("tasks.json", "r") as file:
                data = json.load(file)
                self.tasks = data.get("tasks", [])
                self.completed_tasks = data.get("completed_tasks", [])
        except FileNotFoundError:
            self.tasks = []
            self.completed_tasks = []

        # Configurar el tamaño de la ventana principal
        root.geometry("420x520")

        # Crear un marco para organizar los elementos de la interfaz
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.frame.columnconfigure(0, weight=1)  # Centrar en la columna

        # Elementos de la interfaz
        self.task_title_label = ttk.Label(self.frame, text="Título:")
        self.task_title_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.task_title_entry = ttk.Entry(self.frame, width=40)
        self.task_title_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.task_description_label = ttk.Label(self.frame, text="Descripción:")
        self.task_description_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.task_description_entry = ttk.Entry(self.frame, width=40)
        self.task_description_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.add_button = ttk.Button(self.frame, text="Agregar Tarea", command=self.add_task)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.task_listbox = tk.Listbox(self.frame, width=60, height=15)
        self.task_listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.complete_button = ttk.Button(self.frame, text="Marcar como Completada", command=self.complete_task)
        self.complete_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.delete_button = ttk.Button(self.frame, text="Eliminar Tarea", command=self.delete_task)
        self.delete_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.save_button = ttk.Button(self.frame, text="Guardar", command=self.save_tasks)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Llenar la lista de tareas
        self.show_tasks()

        # Guardar las tareas al cerrar la aplicación
        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Guardar tareas en el archivo JSON al cerrar la aplicación
        with open("tasks.json", "w") as file:
            data = {"tasks": self.tasks, "completed_tasks": self.completed_tasks}
            json.dump(data, file)

        self.root.destroy()

    def add_task(self):
        title = self.task_title_entry.get()
        description = self.task_description_entry.get()
        if title:
            self.tasks.append({"title": title, "description": description})
            self.show_tasks()
            self.task_title_entry.delete(0, tk.END)
            self.task_description_entry.delete(0, tk.END)

    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            self.completed_tasks.append(task)
            self.tasks.pop(selected_task_index[0])
            self.show_tasks()

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            if selected_task_index[0] < len(self.tasks):
                # Eliminar tarea pendiente
                self.tasks.pop(selected_task_index[0])
            else:
                # Eliminar tarea completada
                completed_index = selected_task_index[0] - len(self.tasks) - 1
                if completed_index < len(self.completed_tasks):
                    self.completed_tasks.pop(completed_index)

            self.show_tasks()

    def show_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, f"{task['title']} - {task['description']}")
        self.task_listbox.insert(tk.END, "------ Completed Tasks ------")
        for task in self.completed_tasks:
            self.task_listbox.insert(tk.END, f"{task['title']} - {task['description']}")

    def save_tasks(self):
        # Guardar tareas en el archivo JSON al hacer clic en el botón "Guardar"
        with open("tasks.json", "w") as file:
            data = {"tasks": self.tasks, "completed_tasks": self.completed_tasks}
            json.dump(data, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
