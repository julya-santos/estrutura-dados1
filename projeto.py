import customtkinter as ctk
from tkinter import messagebox
import heapq
from datetime import datetime

# -----------------------------
# Estruturas de Dados
# -----------------------------
class Node:
    def __init__(self, task_id, due_date, task_desc, priority, created_at):
        self.task_id = task_id
        self.due_date = due_date
        self.task_desc = task_desc
        self.priority = priority
        self.created_at = created_at
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_task(self, task_id, due_date, task_desc, priority, created_at):
        new_node = Node(task_id, due_date, task_desc, priority, created_at)
        new_node.next = self.head
        self.head = new_node

    def remove_task(self, task_id):
        current = self.head
        prev = None
        while current:
            if current.task_id == task_id:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True, current
            prev = current
            current = current.next
        return False, None

    def get_all_tasks(self):
        tasks = []
        current = self.head
        while current:
            try:
                due_dt = datetime.strptime(current.due_date, "%d/%m")
            except ValueError:
                due_dt = datetime.max
            tasks.append((current.task_id, current.due_date, current.task_desc, current.priority, due_dt, current.created_at))
            current = current.next
        return sorted(tasks, key=lambda x: (x[3], x[4]))

class PriorityQueue:
    def __init__(self):
        self.heap = []
    def push(self, priority, task):
        heapq.heappush(self.heap, (priority, task))
    def pop(self):
        return heapq.heappop(self.heap)[1] if self.heap else None

class HashTable:
    def __init__(self):
        self.table = {}
    def add(self, key, value):
        self.table[key] = value
    def get(self, key):
        return self.table.get(key)
    def remove(self, key):
        if key in self.table:
            del self.table[key]

# -----------------------------
linked_list = LinkedList()
priority_queue = PriorityQueue()
hash_table = HashTable()

completed_tasks = []
removed_tasks = []

next_task_id = 1
selected_task_id = None

# -----------------------------
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Gerenciador de Tarefas")
root.geometry("700x800")
root.configure(fg_color="white")

font_task = ("Helvetica", 12)

lbl_title = ctk.CTkLabel(root, text="GERENCIADOR DE TAREFAS", font=("Helvetica", 24, "bold"), text_color="#222222")
lbl_title.pack(pady=(15, 0))

lbl_desc = ctk.CTkLabel(root, text="Organiza as atividades de acordo com a prioridade.\nPrioridade: 1=Alta, 2=Média ou 3=Baixa.", font=("Helvetica", 14), text_color="#555555")
lbl_desc.pack(pady=(2, 15))

entry_frame = ctk.CTkFrame(root, fg_color="white", border_width=0)
entry_frame.pack(padx=20, pady=10, fill="x")

lbl_desc_task = ctk.CTkLabel(entry_frame, text="Tarefa", width=90, anchor="w", font=font_task, text_color="#333333")
lbl_desc_task.grid(row=0, column=0, padx=(0,10), pady=8, sticky="w")
entry_task = ctk.CTkEntry(entry_frame, font=font_task)
entry_task.grid(row=0, column=1, sticky="ew", pady=8)

lbl_priority = ctk.CTkLabel(entry_frame, text="Prioridade (1, 2 ou 3)", width=90, anchor="w", font=font_task, text_color="#333333")
lbl_priority.grid(row=1, column=0, padx=(0,10), pady=8, sticky="w")
entry_priority = ctk.CTkEntry(entry_frame, font=font_task)
entry_priority.grid(row=1, column=1, sticky="ew", pady=8)

lbl_date = ctk.CTkLabel(entry_frame, text="Data (dd/mm)", width=90, anchor="w", font=font_task, text_color="#333333")
lbl_date.grid(row=2, column=0, padx=(0,10), pady=8, sticky="w")
entry_date = ctk.CTkEntry(entry_frame, font=font_task)
entry_date.grid(row=2, column=1, sticky="ew", pady=8)

entry_frame.grid_columnconfigure(1, weight=1)

# --------- SCROLLABLE FRAME FOR TASKS ----------
task_list_frame = ctk.CTkScrollableFrame(root, height=350, fg_color="#fafafa")
task_list_frame.pack(padx=20, pady=15, fill="both", expand=True)

# --------- FUNCTIONS ----------
def add_task():
    global next_task_id
    desc = entry_task.get().strip()
    due_date = entry_date.get().strip()
    try:
        priority = int(entry_priority.get())
    except ValueError:
        messagebox.showerror("Erro", "Prioridade deve ser número 1, 2 ou 3!")
        return
    if desc and due_date and priority in [1,2,3]:
        created_at = datetime.now().strftime("%d/%m %H:%M")
        linked_list.add_task(next_task_id, due_date, desc, priority, created_at)
        priority_queue.push(priority, (next_task_id, due_date, desc, priority, created_at))
        hash_table.add(next_task_id, desc)
        next_task_id += 1
        update_task_list()
        entry_task.delete(0, "end")
        entry_priority.delete(0, "end")
        entry_date.delete(0, "end")
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos corretamente!")

def complete_task():
    global selected_task_id
    if selected_task_id is None:
        messagebox.showwarning("Aviso", "Selecione uma tarefa ativa para concluir!")
        return
    removed, node = linked_list.remove_task(selected_task_id)
    if removed:
        completed_tasks.append((selected_task_id, node.due_date, node.task_desc, node.priority, datetime.now().strftime("%H:%M")))
        hash_table.remove(selected_task_id)
        selected_task_id = None
        update_task_list()

def remove_task():
    global selected_task_id
    if selected_task_id is None:
        messagebox.showwarning("Aviso", "Selecione uma tarefa ativa para cancelar!")
        return
    removed, node = linked_list.remove_task(selected_task_id)
    if removed:
        removed_tasks.append((selected_task_id, node.due_date, node.task_desc, node.priority, datetime.now().strftime("%H:%M")))
        hash_table.remove(selected_task_id)
        selected_task_id = None
        update_task_list()

def update_task_list():
    global selected_task_id
    for widget in task_list_frame.winfo_children():
        widget.destroy()
    selected_task_id = None

    # Active Tasks
    for task_id, due_date, desc, priority, _, created_at in linked_list.get_all_tasks():
        frame = ctk.CTkFrame(task_list_frame, fg_color="#ffffff")
        frame.pack(fill="x", pady=4, padx=5)

        label_text = f"ID {task_id} - {due_date} - {desc}. Prioridade {priority}. Adicionado em {created_at}."
        label = ctk.CTkLabel(frame, text=label_text, font=font_task, anchor="w", justify="left", wraplength=500, text_color="#000000")
        label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

        def on_select(tid=task_id):
            global selected_task_id
            selected_task_id = tid
            print(f"Selecionado: ID {selected_task_id}")

        label.bind("<Button-1>", lambda e, tid=task_id: on_select(tid))

    if completed_tasks or removed_tasks:
        sep = ctk.CTkLabel(task_list_frame, text="-" * 100)
        sep.pack(pady=5)

    for task_id, due_date, desc, priority, action_time in completed_tasks:
        text = f"✔ ID {task_id} - {due_date} - {desc}. Prioridade {priority}. Concluída em {action_time}."
        label = ctk.CTkLabel(task_list_frame, text=text, text_color="green", font=font_task, anchor="w", justify="left", wraplength=500)
        label.pack(fill="x", padx=10, pady=2)

    for task_id, due_date, desc, priority, action_time in removed_tasks:
        text = f"✘ ID {task_id} - {due_date} - {desc}. Prioridade {priority}. Cancelada em {action_time}."
        label = ctk.CTkLabel(task_list_frame, text=text, text_color="red", font=font_task, anchor="w", justify="left", wraplength=500)
        label.pack(fill="x", padx=10, pady=2)

# --------- BUTTONS ----------
button_frame = ctk.CTkFrame(root, fg_color="white", border_width=0)
button_frame.pack(pady=5)

def create_button(text, command, color):
    return ctk.CTkButton(button_frame, text=text, command=command, fg_color=color, text_color="white",
                         font=font_task, corner_radius=12, width=110, height=38)

btn_add = create_button("ADICIONAR", add_task, "#2196F3")
btn_add.pack(side="left", padx=10)

btn_complete = create_button("CONCLUIR ✓", complete_task, "#4CAF50")
btn_complete.pack(side="left", padx=10)

btn_remove = create_button("CANCELAR ✗", remove_task, "#F44336")
btn_remove.pack(side="left", padx=10)

update_task_list()
root.mainloop()
