import tkinter as tk
from tkinter import ttk
from pathlib import Path

class CreateFolderDialog(tk.Tk):
    def __init__(self, treeviewFrame):
        self._app = treeviewFrame.app
        self._window = treeviewFrame.window
        self._treeviewFrame = treeviewFrame
        self._parentFolder = treeviewFrame.currentSelectedItemID

        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Create Folder")
        self.winfo_toplevel().geometry("350x150+500+200")
        f = tk.Frame(self, bg='white')

        # Label
        self.label = tk.Label(f, bg='white', fg='black', text="Create New Folder:")
        self.label.place(x = 10, y = 10, anchor='nw')

        # Text Input
        self.entry = tk.Entry(f, bg='white', fg='black', borderwidth=2, width=53)
        self.entry.place(x = 10, y = 50, anchor='nw')

        # Error Line
        self.error_label = tk.Label(f, bg='white', fg='red', text="")
        self.error_label.place(x = 10, y=72, anchor='nw')

        # Button
        self.okButton = ttk.Button(f, text="OK", width=10, command= lambda: self.createFolder())
        self.okButton.place(x = 60, y = 100, anchor='nw')

        # Close Button
        self.closeButton = ttk.Button(f, text="Cancel", width=10, command= self.kill)
        self.closeButton.place(x = 200, y = 100, anchor='nw')

        f.pack(fill = 'both', expand=1)
        self.after(500, lambda: self.focus_force())
    
    def createFolder(self):
        newFolderName: str = self.entry.get()

        if not newFolderName.isalnum():
            self.error_label.config(text="Folder name must be alphanumeric.")
            return None
        
        # Convert folder ID to path structure: /__/__/
        parent = '/'
        if self._parentFolder == 'root':
            parent = '/'
        elif self._parentFolder.startswith('dir_'):
            split_path = self._parentFolder.split('_')
            parent = parent + split_path[1]

        # Create the Folder
        self._app.create_folder(newFolderName, parent)

        # Add Folder to Tree Frame
        if self._parentFolder == 'root':
            self._treeviewFrame.add_folder_to_tree(newFolderName, 'root')
        else:
            parent_iid = 'dir_' + parent[1:].replace('/', '_')
            self._treeviewFrame.add_folder_to_tree(newFolderName, parent_iid)

        self.kill()
        return None
        
    def kill(self):
        self.winfo_toplevel().destroy()




class DeleteFolderDialog(tk.Tk):
    def __init__(self, treeviewFrame):
        self._app = treeviewFrame.app
        self._window = treeviewFrame.window
        self._treeviewFrame = treeviewFrame
        self._currentFolder = treeviewFrame.currentSelectedItemID

        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Delete Folder")
        self.winfo_toplevel().geometry("350x150+500+200")
        f = tk.Frame(self, bg='white')

        # Label
        self.label = tk.Label(f, bg='white', fg='black', text="Would you like to move any existing files to the parent folder?")
        self.label.place(x = 10, y = 10, anchor='nw')

        # Error Line
        self.error_label = tk.Label(f, bg='white', fg='red', text="")
        self.error_label.place(x = 10, y=72, anchor='nw')

        # Checkbox Input
        self._keepfiles = tk.IntVar(f)
        self.checkButton = tk.Checkbutton(f, text="Keep Files", var=self._keepfiles)
        self.checkButton.place(x = 135, y = 45, anchor='nw')

        # Button
        self.okButton = ttk.Button(f, text="Delete", width=10, command= lambda: self.deleteFolder())
        self.okButton.place(x = 60, y = 100, anchor='nw')

        # Close Button
        self.closeButton = ttk.Button(f, text="Cancel", width=10, command= self.kill)
        self.closeButton.place(x = 200, y = 100, anchor='nw')

        f.pack(fill = 'both', expand=1)
        self.after(500, lambda: self.focus_force())
    
    def deleteFolder(self):
        if self._keepfiles.get() == 0:
            # Remove from project
            self._app.delete_folder(self._keepfiles.get(), self._currentFolder)

            # Remove folder from tree            
            self._treeviewFrame.remove_folder(self._currentFolder)
        
        elif self._keepfiles.get() == 1:
            # Remove from project
            removed = self._app.delete_folder(self._keepfiles.get(), self._currentFolder)

            # Move files
            for file in removed:
                folder_iid = ""
                if file['directory'] == 'root':
                    folder_iid = 'root'
                else:
                    folder_iid = 'dir_' + file['directory']

                self._treeviewFrame.add_drawing_to_tree(file, folder_iid)

            # Remove folder from tree
            self._treeviewFrame.remove_folder(self._currentFolder)
        
        self.kill()

        
    def kill(self):
        self.winfo_toplevel().destroy()





class RenameFolderDialog(tk.Tk):
    def __init__(self, treeviewFrame):
        self._app = treeviewFrame.app
        self._window = treeviewFrame.window
        self._treeviewFrame = treeviewFrame

        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Rename Folder")
        self.winfo_toplevel().geometry("350x150+500+200")
        f = tk.Frame(self, bg='white')

        # Label
        self.label = tk.Label(f, bg='white', fg='black', text="New Folder Name:")
        self.label.place(x = 10, y = 10, anchor='nw')

        # Text Input
        self.entry = tk.Entry(f, bg='white', fg='black', borderwidth=2, width=53)
        self.entry.place(x = 10, y = 50, anchor='nw')

        # Error Line
        self.error_label = tk.Label(f, bg='white', fg='red', text="")
        self.error_label.place(x = 10, y=72, anchor='nw')

        # Button
        self.okButton = ttk.Button(f, text="OK", width=10, command= lambda: self.renameFolder())
        self.okButton.place(x = 60, y = 100, anchor='nw')

        # Close Button
        self.closeButton = ttk.Button(f, text="Cancel", width=10, command= self.kill)
        self.closeButton.place(x = 200, y = 100, anchor='nw')

        f.pack(fill = 'both', expand=1)
        self.after(500, lambda: self.focus_force())
    
    def renameFolder(self):
        newFolderName: str = self.entry.get()

        if not newFolderName.isalnum():
            self.error_label.config(text="Folder name must be alphanumeric.")
            return None
        
        # Rename folder in project tree
        folder_path = self._treeviewFrame.currentSelectedItemID.replace('dir_', '')
        self._app.rename_folder(folder_path, newFolderName)
        
        # Rename folder in tree view and corresponding IDs for directory and subdirectory files
        parent_iid = ''
        if self._treeviewFrame.currentSelectedItemID.count("_") == 1:
            parent_iid = 'root'
        else: 
            parent_iid = 'dir_' + self._treeviewFrame.currentSelectedItemID.split('_')[1]
        
        self._treeviewFrame.rename_folder(parent_iid, newFolderName)

        self.kill()
        return None
        
    def kill(self):
        self.winfo_toplevel().destroy()









class DeleteFileDialog(tk.Tk):
    def __init__(self, treeviewFrame):
        self._app = treeviewFrame.app
        self._window = treeviewFrame.window
        self._treeviewFrame = treeviewFrame
        self._currentFile = treeviewFrame.currentSelectedItemID

        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Delete DWG")
        self.winfo_toplevel().geometry("350x150+500+200")
        f = tk.Frame(self, bg='white')

        # Label
        self.label = tk.Label(f, bg='white', fg='black', text="Are you sure you want to remove this DWG from the WDP configuration?")
        self.label.place(x = 10, y = 10, anchor='nw')

        # Button
        self.yesButton = ttk.Button(f, text="Yes, Delete", width=10, command= lambda: self.deleteFile())
        self.yesButton.place(x = 60, y = 100, anchor='nw')

        # Close Button
        self.closeButton = ttk.Button(f, text="No, Cancel", width=10, command= self.kill)
        self.closeButton.place(x = 200, y = 100, anchor='nw')

        f.pack(fill = 'both', expand=1)
        self.after(500, lambda: self.focus_force())
    
    def deleteFile(self):
        # Remove from project
        self._app.remove_dwg(self._currentFile)

        # Remove from TreeView
        self._treeviewFrame.remove_file(self._currentFile)

        self.kill()

        
    def kill(self):
        self.winfo_toplevel().destroy()






class EditAllDescription1Dialog(tk.Tk):
    def __init__(self, treeviewFrame):
        self._app = treeviewFrame.app
        self._window = treeviewFrame.window
        self._treeviewFrame = treeviewFrame
        self._selected_folder = treeviewFrame.currentSelectedItemID

        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Edit All Description 1")
        self.winfo_toplevel().geometry("350x150+500+200")
        f = tk.Frame(self, bg='white')

        # Label
        self.label = tk.Label(f, bg='white', fg='black', text="New Description 1:")
        self.label.place(x = 10, y = 10, anchor='nw')

        # Text Input
        self.entry = tk.Entry(f, bg='white', fg='black', borderwidth=2, width=53)
        self.entry.place(x = 10, y = 50, anchor='nw')

        # Error Line
        self.error_label = tk.Label(f, bg='white', fg='red', text="")
        self.error_label.place(x = 10, y=72, anchor='nw')

        # Button
        self.okButton = ttk.Button(f, text="OK", width=10, command= lambda: self.editDescription1())
        self.okButton.place(x = 60, y = 100, anchor='nw')

        # Close Button
        self.closeButton = ttk.Button(f, text="Cancel", width=10, command= self.kill)
        self.closeButton.place(x = 200, y = 100, anchor='nw')

        f.pack(fill = 'both', expand=1)
        self.after(500, lambda: self.focus_force())
    
    def editDescription1(self):
        newDescription1: str = self.entry.get()

        # Change Description 1 in the Model
        self._app.editAllDescription1(self._selected_folder, newDescription1)

        # Update the ModelView Treeview object
        self._window.refresh_folder_mode()


        self.kill()
        return None
        
    def kill(self):
        self.winfo_toplevel().destroy()



class EditAllDescription2Dialog(tk.Tk):
    def __init__(self, treeviewFrame):
        self._app = treeviewFrame.app
        self._window = treeviewFrame.window
        self._treeviewFrame = treeviewFrame
        self._selected_folder = treeviewFrame.currentSelectedItemID

        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Edit All Description 2")
        self.winfo_toplevel().geometry("350x150+500+200")
        f = tk.Frame(self, bg='white')

        # Label
        self.label = tk.Label(f, bg='white', fg='black', text="New Description 2:")
        self.label.place(x = 10, y = 10, anchor='nw')

        # Text Input
        self.entry = tk.Entry(f, bg='white', fg='black', borderwidth=2, width=53)
        self.entry.place(x = 10, y = 50, anchor='nw')

        # Error Line
        self.error_label = tk.Label(f, bg='white', fg='red', text="")
        self.error_label.place(x = 10, y=72, anchor='nw')

        # Button
        self.okButton = ttk.Button(f, text="OK", width=10, command= lambda: self.editDescription2())
        self.okButton.place(x = 60, y = 100, anchor='nw')

        # Close Button
        self.closeButton = ttk.Button(f, text="Cancel", width=10, command= self.kill)
        self.closeButton.place(x = 200, y = 100, anchor='nw')

        f.pack(fill = 'both', expand=1)
        self.after(500, lambda: self.focus_force())
    
    def editDescription2(self):
        newDescription2: str = self.entry.get()

        # Change Description 1 in the Model
        self._app.editAllDescription2(self._selected_folder, newDescription2)

        # Update the ModelView Treeview object
        self._window.refresh_folder_mode()


        self.kill()
        return None
        
    def kill(self):
        self.winfo_toplevel().destroy()





class CreateFileFromTemplateDialog(tk.Tk):
    def __init__(self, treeviewFrame):
        self._app = treeviewFrame.app
        self._window = treeviewFrame.window
        self._treeviewFrame = treeviewFrame
        self._currentFolder = treeviewFrame.currentSelectedItemID

        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Create File from Template")
        self.winfo_toplevel().geometry("350x150+500+200")
        f = tk.Frame(self, bg='white')

        # Label
        self.label = tk.Label(f, bg='white', fg='black', text="Choose Template:")
        self.label.place(x = 10, y = 10, anchor='nw')

        # Template selected
        options = [path.name for path in self._app.appModel.templateModel.possible_templates]
        self._string_var = tk.StringVar(f)
        if len(options) > 0: self._string_var.set(options[0])
        self.dropdown = tk.OptionMenu(f, self._string_var, *options)
        self.dropdown.place(x = 120, y= 10, width=140, anchor='nw')

        # New Name Label
        self.name_label = tk.Label(f, bg='white', fg='black', text="New Filename:")
        self.name_label.place(x = 10, y = 40, anchor='nw')

        self.entry = tk.Entry(f, bg='white', fg='black', borderwidth=2, width=53)
        self.entry.place(x = 10, y = 60, anchor='nw')
    
        # Error Line
        self.error_label = tk.Label(f, bg='white', fg='red', text="")
        self.error_label.place(x = 10, y=80, anchor='nw')

        # Button
        self.okButton = ttk.Button(f, text="Create", width=10, command= lambda: self.createDWG())
        self.okButton.place(x = 60, y = 100, anchor='nw')

        # Close Button
        self.closeButton = ttk.Button(f, text="Cancel", width=10, command= self.kill)
        self.closeButton.place(x = 200, y = 100, anchor='nw')

        f.pack(fill = 'both', expand=1)
        self.after(500, lambda: self.focus_force())
    
    def createDWG(self):
        newDWGName: str = self.entry.get()
        if newDWGName[-4:] != '.dwg':
            newDWGName += '.dwg'
        folder_iid = self._currentFolder
        file_iid = folder_iid + "_" + newDWGName

        template_file = self._string_var.get()
        template_path = self._app.appModel.templateModel.template_path / Path(template_file)

        
        # Update Model
        self._app.create_dwg(file_iid, template_path)

        # Update Tree
        splits = file_iid.split('_')
        directory = ""
        if splits[0] == 'root':
            directory = ''
        elif len(splits) == 3:
            directory = splits[1]
        elif len(splits) == 4:
            directory = splits[1] + "/" + splits[2]
        newDWG = {
            'name': newDWGName,
            'directory': directory,
            'description1': '',
            'description2': '',
            'description3': ''
        }
        self._treeviewFrame.add_drawing_to_tree(newDWG, folder_iid)

        self._window.refresh_folder_mode()

        self.kill()

        
    def kill(self):
        self.winfo_toplevel().destroy()



        