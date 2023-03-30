import tkinter as tk
from tkinter import ttk
import os
import sys

frames_dir = os.path.dirname(__file__)
dialogDir = os.path.join(frames_dir, 'dialogs')

sys.path.append(dialogDir)

from EditDescriptionDialogs import EditSectionDialog
from EditDescriptionDialogs import EditDescription1Dialog
from EditDescriptionDialogs import EditDescription2Dialog
from EditDescriptionDialogs import EditDescription3Dialog

sys.path.remove(dialogDir)

class MainFrame(tk.Frame):
    def __init__(self, app, window):
        self._app = app
        self._window = window

        tk.Frame.__init__(self, self._window, bg='WHITE', width=500)

        # Descriptive Labels
        self.drawings_title_label = tk.Label(self, text="DRAWING INFORMATION:", bg='white', fg='black', font='Helvetica 10 bold')
        self.name_label = tk.Label(self, text="FILENAME: ", bg='white', fg='black', font='Helvetica 10')
        self.path_label = tk.Label(self, text="PATH: ", bg='white', fg='black', font='Helvetica 10')
        self.section_label = tk.Label(self, text="SECTION: ", bg='white', fg='black', font='Helvetica 10')
        self.description1_label = tk.Label(self, text="DESCRIPTION 1: ", bg='white', fg='black', font='Helvetica 10')
        self.description2_label = tk.Label(self, text="DESCRIPTION 2: ", bg='white', fg='black', font='Helvetica 10')
        self.description3_label = tk.Label(self, text="DESCRIPTION 3: ", bg='white', fg='black', font='Helvetica 10')

        # Change Descriptions Buttons
        self.change_description1_button = ttk.Button(self, text="Edit Description 1..", width=25, command = lambda: self.show_dialog(EditDescription1Dialog))
        self.change_description2_button = ttk.Button(self, text="Edit Description 2..", width=25, command = lambda: self.show_dialog(EditDescription2Dialog))
        self.change_description3_button = ttk.Button(self, text="Edit Description 3..", width=25, command = lambda: self.show_dialog(EditDescription3Dialog))
        self.change_section_button = ttk.Button(self, text="Edit Section..", width=25, command = lambda: self.show_dialog(EditSectionDialog))
        self.change_description1_button.state(["disabled"])
        self.change_description2_button.state(["disabled"])
        self.change_description3_button.state(["disabled"])
        self.change_section_button.state(["disabled"])

        # Folder View
        self.folder_title_label = tk.Label(self, text="FOLDER ITEMS:", bg='white', fg='black', font='Helvetica 10 bold')
        self.folder_items_tree = ttk.Treeview(self, selectmode='browse', columns=['Filename', 'Section', 'Description1', 'Description2', 'Description3'])
        self.folder_items_tree.bind('<<TreeviewSelect>>', self.folder_tree_listener)
        self.folder_items_tree.heading('Filename', text='File Name')
        self.folder_items_tree.column('Filename', width=150, minwidth=10)
        self.folder_items_tree.heading('Section', text='Section')
        self.folder_items_tree.column('Section', width=60, minwidth=10)
        self.folder_items_tree.heading('Description1', text='Description 1')
        self.folder_items_tree.column('Description1', width=180, minwidth=10)
        self.folder_items_tree.heading('Description2', text='Description 2')
        self.folder_items_tree.column('Description2', width=180, minwidth=10)
        self.folder_items_tree.heading('Description3', text='Description 3')
        self.folder_items_tree.column('Description3', width=180, minwidth=10)
        self.folder_items_tree.configure(show="headings")


        # Descriptive Labels Placement
        self.drawings_title_label.place(x=5, y=10, anchor='nw')
        self.name_label.place(x=20, y=30, anchor='nw')
        self.section_label.place(x=20, y=50, anchor='nw')
        self.path_label.place(x=20, y=70, anchor='nw')
        self.description1_label.place(x=20, y=90, anchor='nw')
        self.description2_label.place(x=20, y=110, anchor='nw')
        self.description3_label.place(x=20, y=130, anchor='nw')

        # Change Description Buttons Placement
        self.change_description1_button.place(x=500, y=20, anchor='nw')
        self.change_description2_button.place(x=500, y=50, anchor='nw')
        self.change_description3_button.place(x=500, y=80, anchor='nw')
        self.change_section_button.place(x=500, y=110, anchor='nw')

        # Folder View Placement
        self.folder_title_label.place(x=5, y=170, anchor='nw')
        self.folder_items_tree.place(x=10, y=200, anchor='nw')
        
    
    @property
    def app(self):
        return self._app
    
    @property
    def window(self):
        return self._window
    
    def file_mode(self):
        # Enable description buttons
        self.change_description1_button.state(["!disabled"])
        self.change_description2_button.state(["!disabled"])
        self.change_description3_button.state(["!disabled"])
        self.change_section_button.state(["!disabled"])

        # Clear folder items tree
        for item in self.folder_items_tree.get_children():
            self.folder_items_tree.delete(item)
    
    def folder_mode(self):
        # Disable description buttons
        self.change_description1_button.state(["disabled"])
        self.change_description2_button.state(["disabled"])
        self.change_description3_button.state(["disabled"])
        self.change_section_button.state(["disabled"])

        # Populate folder items tree
        self.populate_folder_items_tree()
    
    def get_current_item_name(self):
        return self._window.get_current_item_name()
    
    def get_current_item_path(self):
        return self._window.get_current_item_path()
        
    def update_name_label(self, new_name):
        self.name_label.config(text=f"FILENAME:\t{new_name}")
    
    def update_section_label(self, new_section):
        self.section_label.config(text=f"SECTION:\t{new_section}")
    
    def update_path_label(self, new_path):
        self.path_label.config(text=f"PATH:\t\t{new_path}")
    
    def update_decsription1_label(self, new_d1):
        self.description1_label.config(text=f"DESCRIPTION 1:\t{new_d1}")
    
    def update_description2_label(self, new_d2):
        self.description2_label.config(text=f"DESCRIPTION 2:\t{new_d2}")
    
    def update_description3_label(self, new_d3):
        self.description3_label.config(text=f"DESCRIPTION 3:\t{new_d3}")
    
    def show_dialog(self, function):
        dialog = function(self)
        dialog.mainloop()
    
    def folder_tree_listener(self, event):
        pass

    def populate_folder_items_tree(self):
        """
        Populates the folder items tree with the items in the currently selected folder.
        """
        for item in self.folder_items_tree.get_children():
            self.folder_items_tree.delete(item)
            
        current_folder = self._window.get_current_folder()
        tree = self._app.get_project_tree()

        if current_folder == []:
            for file in tree['files']:
                self.folder_items_tree.insert("", "end", iid=f"{file['name']}", text=f"{file['name']}", values=(file['name'], file['section'], file['description1'], file['description2'], file['description3']))
                
        elif len(current_folder) == 1:
            for file in tree['dirs'][current_folder[0]]['files']:
                self.folder_items_tree.insert("", "end", iid=f"{file['name']}", text=f"{file['name']}", values=(file['name'], file['section'], file['description1'], file['description2'], file['description3']))
                
        else:
            for file in tree['dirs'][current_folder[0]]['dirs'][current_folder[1]]['files']:
                self.folder_items_tree.insert("", "end", iid=f"{file['name']}", text=f"{file['name']}", values=(file['name'], file['section'], file['description1'], file['description2'], file['description3']))
                
        
