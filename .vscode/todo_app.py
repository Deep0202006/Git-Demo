import sys
import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem, Icon
from datetime import datetime, date
import threading
import time

class TodoItem:
    def __init__(self, description, priority='Medium', due_date=None, completed=False):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

    @staticmethod
    def from_dict(data):
        item = TodoItem(
            description=data.get('description', ''),
            priority=data.get('priority', 'Medium'),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            completed=data.get('completed', False)
        )
        item.created_at = datetime.fromisoformat(data.get('created_at', str(datetime.now())))
        return item

class TodoListApp:
    def __init__(self):
        # Initialize application
        self.todo_list = []
        self.todo_file = "todo_list.json"
        self.config_file = "app_config.json"
        
        # Load configurations
        self.load_config()
        
        # Load existing todo list
        self.load_todo_list()
        
        # Create root window
        self.root = tk.Tk()
        self.root.title("Todo List App")
        self.root.withdraw()  # Hide main window
        
        # Create system tray icon
        self.create_system_tray_icon()

    def load_config(self):
        """Load application configurations"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as file:
                    self.config = json.load(file)
            else:
                # Default configuration
                self.config = {
                    'dark_mode': False,
                    'notifications_enabled': True
                }
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {
                'dark_mode': False,
                'notifications_enabled': True
            }

    def load_todo_list(self):
        """Load todo list from JSON file"""
        try:
            if os.path.exists(self.todo_file):
                with open(self.todo_file, 'r') as file:
                    data = json.load(file)
                    # Ensure data is a list and handle potential dictionary input
                    if isinstance(data, dict):
                        data = [data]
                    self.todo_list = [TodoItem.from_dict(item) for item in data]
        except Exception as e:
            print(f"Error loading todo list: {e}")
            self.todo_list = []

    def save_todo_list(self):
        """Save todo list to JSON file"""
        try:
            with open(self.todo_file, 'w') as file:
                json.dump([item.to_dict() for item in self.todo_list], file)
        except Exception as e:
            print(f"Error saving todo list: {e}")

    def remove_todo_item(self):
        """Remove a todo item"""
        if not self.todo_list:
            messagebox.showwarning("Warning", "Todo list is empty!")
            return

        # Create a removal window
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Todo Item")
        remove_window.geometry("400x300")

        # Create Treeview for item selection
        columns = ("Description", "Priority", "Due Date")
        tree = ttk.Treeview(remove_window, columns=columns, show='headings', selectmode='browse')
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor='center')

        # Populate treeview
        for item in self.todo_list:
            due_date = item.due_date.strftime('%Y-%m-%d') if item.due_date else 'N/A'
            tree.insert('', 'end', values=(
                item.description, 
                item.priority, 
                due_date
            ))

        tree.pack(expand=True, fill='both', padx=10, pady=10)

        def confirm_removal():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select an item to remove")
                return

            # Get the index of the selected item
            index = tree.index(selected_item[0])
            
            # Remove the item
            removed_item = self.todo_list.pop(index)
            self.save_todo_list()
            
            messagebox.showinfo("Success", f"Removed: {removed_item.description}")
            remove_window.destroy()

        # Remove button
        remove_button = tk.Button(remove_window, text="Remove Selected Item", command=confirm_removal)
        remove_button.pack(pady=10)

    def create_system_tray_icon(self):
        """Create system tray icon"""
        image = self.create_image(64, 64)
        self.icon = pystray.Icon(
            "TodoList", 
            image, 
            "Todo List App", 
            menu=self.create_menu()
        )

    def create_image(self, width, height):
        """Create a simple icon image"""
        image = Image.new('RGB', (width, height), color='white')
        dc = ImageDraw.Draw(image)
        dc.rectangle([width//4, height//4, width*3//4, height*3//4], fill='black')
        return image

    def create_menu(self):
        """Create system tray menu"""
        return (
            MenuItem('Show Todo List', self.show_todo_list),
            MenuItem('Add Todo Item', self.add_todo_item),
            MenuItem('Remove Todo Item', self.remove_todo_item),
            MenuItem('Exit', self.exit_app)
        )

    def show_todo_list(self):
        """Display todo list"""
        if not self.todo_list:
            messagebox.showinfo("Todo List", "Your todo list is empty!")
            return

        todo_items = "\n".join([
            f"{i+1}. {item.description} (Priority: {item.priority}, "
            f"Due: {item.due_date.strftime('%Y-%m-%d') if item.due_date else 'N/A'})" 
            for i, item in enumerate(self.todo_list)
        ])
        messagebox.showinfo("Todo List", todo_items)

    def add_todo_item(self):
        """Add a new todo item"""
        description = simpledialog.askstring("Add Todo", "Enter todo item:")
        if description:
            priority = simpledialog.askstring("Priority", "Enter priority (High/Medium/Low):") or "Medium"
            due_date_str = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD) or leave blank:")
            
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
                new_item = TodoItem(description, priority, due_date)
                self.todo_list.append(new_item)
                self.save_todo_list()
                messagebox.showinfo("Success", f"Added: {description}")
            except (ValueError, TypeError):
                messagebox.showerror("Error", "Invalid date format!")

class TodoListApp:
    def __init__(self):
        # Initialize application
        self.todo_list = []
        self.todo_file = "todo_list.json"
        self.config_file = "app_config.json"
        
        # Load configurations
        self.load_config()
        
        self.load_list()
        # Load existing todo list
        self.load_todo_list()
        
        # Create root window
        self.root = tk.Tk()
        self.root.title("Todo List App")
        self.root.withdraw()  # Hide main window
        
        # Create system tray icon
        self.create_system_tray_icon()

    # ... [Previous methods remain the same] ...

    def exit_app(self, icon=None, item=None):
        """Exit the application"""
        # Save todo list before exiting
        self.save_todo_list()
        
        # Stop the system tray icon if it's running
        if icon:
            icon.stop()
        
        # Quit the Tkinter root window
        self.root.quit()
        
        # Exit the application
        sys.exit(0)

    def run(self):
        """Run the application"""
        try:
            # Start the system tray icon in a separate thread
            icon_thread = threading.Thread(target=self.icon.run, daemon=True)
            icon_thread.start()
            
            
            self.root.mainloop()
        except Exception as e:
            print(f"Error running application: {e}")
            sys.exit(1)


def main():
    app= TodoListApp()
    app.run()

if __name__ == "_main_":
    main()

def main():
    app= TodoListApp()
    app.run()

if __name__=="_main_":
    main()








