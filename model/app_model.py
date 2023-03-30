from pathlib import Path

from wdp_util import get_wdp_lines, get_drawings_and_empty_subdirectories, get_project_directory_structure


class WDPModel:
    """
    Represents the WDP file
    """
    def __init__(self, wdp_filepath: Path):
        self._filepath: Path = wdp_filepath
        self._is_valid: bool = False

        # Drawings List
        self._drawings = []

        # Project Tree
        self._project_tree = {}
    
    @property
    def is_valid(self): 
        return self._is_valid
    
    @property
    def wdp_filename(self):
        return self._filepath.name

    def parse(self) -> int:
        """
        Parses the WDP file in WDPModel filepath variable.

        Successful parsing results in WDPModel setting is_valid.

        If no file is present, -1 is returned.
        Returns 0 on successful parsing.
        """

        try:
            # Step 1: Parse only the relevant lines of the WDP file
            relevant_lines= get_wdp_lines(self._filepath)

            # Step 2: Extract Project File Information into WDPModel object
            self._drawings, empty_subdirectories = get_drawings_and_empty_subdirectories(relevant_lines)

            # Step 3: Construct and populate the project file structure
            self._project_tree = get_project_directory_structure(self._drawings, empty_subdirectories)
        except Exception as e:
            print(e)
            print(e.args)
            self._is_valid = False
            return -1

        self._is_valid = True
        return 0
    
    @property
    def project_tree(self):
        return self._project_tree
    
    @property
    def drawings(self):
        return self._drawings
    
    def get_section(self, drawing_path, drawing_name):
        """
        Drawing Path given in format /__/__/ where the first __ is the first folder and the second __ is the second folder.

        Given a path and a drawing name, returns drawing section as string.
        """
        if drawing_path == '/':
            for file in self.project_tree['files']:
                if file['name'] == drawing_name:
                    return file['section']
        
        elif drawing_path.count('/') == 2:
            d = drawing_path[1:-1]
            for file in self.project_tree['dirs'][d]['files']:
                if file['name'] == drawing_name:
                    return file['section']
        
        elif drawing_path.count('/') == 3:
            d = drawing_path[1:-1]
            path_folders = d.split('/')
            first_folder = path_folders[0]
            second_folder = path_folders[1]

            for file in self.project_tree['dirs'][first_folder]['dirs'][second_folder]['files']:
                if file['name'] == drawing_name:
                    return file['section']
        
        return None
    
    def get_descriptions(self, drawing_path, drawing_name):
        """
        Drawing Path given in format /___/___/ where the first ___ is the first folder and the second ___ is the second folder.

        Given a path and a drawing naming, returns the drawing descriptions in a 3-tuple.
        """
        if drawing_path == '/':
            for file in self.project_tree['files']:
                if file['name'] == drawing_name:
                    return (file['description1'], file['description2'], file['description3'])
        
        elif drawing_path.count('/') == 2:
            d = drawing_path[1:-1]
            for file in self.project_tree['dirs'][d]['files']:
                if file['name'] == drawing_name:
                    return (file['description1'], file['description2'], file['description3'])
        
        elif drawing_path.count('/') == 3:
            d = drawing_path[1:-1]
            path_folders = d.split('/')
            first_folder = path_folders[0]
            second_folder = path_folders[1]

            for file in self.project_tree['dirs'][first_folder]['dirs'][second_folder]['files']:
                if file['name'] == drawing_name:
                    return (file['description1'], file['description2'], file['description3'])
        
        return None
    


    def edit_section(self, new_section, drawing_path, drawing_name):
        """
        Edits the section to <new_section> given the drawing_path and drawing_name.
        """
        # Root folder
        if drawing_path == '/':
            for file in self.project_tree['files']:
                if file['name'] == drawing_name:
                    file['section'] = new_section
                    return 0
            
        # One-level folder
        elif drawing_path.count('/') == 2:
            d = drawing_path[1:-1]
            for file in self.project_tree['dirs'][d]['files']:
                if file['name'] == drawing_name:
                    file['section'] = new_section
                    return 0
        
        # Two-Level folder
        elif drawing_path.count('/') == 3:
            d = drawing_path[1:-1]
            path_folders = d.split('/')
            first_folder = path_folders[0]
            second_folder = path_folders[1]

            for file in self.project_tree['dirs'][first_folder]['dirs'][second_folder]['files']:
                if file['name'] == drawing_name:
                    file['section'] = new_section
                    return 0

        return -1


    
    def edit_description(self, number, new_description, drawing_path, drawing_name):
        """
        Edits the description <number> to <new_description> given drawing_path and drawing_name.
        """
        # Root folder
        if drawing_path == '/':
            for file in self.project_tree['files']:
                if file['name'] == drawing_name:
                    if number == 1: file['description1'] = new_description
                    elif number == 2: file['description2'] = new_description
                    elif number == 3: file['description3'] = new_description
                    else: return -1
                    return 0
        
        # One-level folder
        elif drawing_path.count('/') == 2:
            d = drawing_path[1:-1]
            for file in self.project_tree['dirs'][d]['files']:
                if file['name'] == drawing_name:
                    if number == 1: file['description1'] = new_description
                    elif number == 2: file['description2'] = new_description
                    elif number == 3: file['description3'] = new_description
                    else: return -1
                    return 0
        
        # Two-Level folder
        elif drawing_path.count('/') == 3:
            d = drawing_path[1:-1]
            path_folders = d.split('/')
            first_folder = path_folders[0]
            second_folder = path_folders[1]

            for file in self.project_tree['dirs'][first_folder]['dirs'][second_folder]['files']:
                if file['name'] == drawing_name:
                    if number == 1: file['description1'] = new_description
                    elif number == 2: file['description2'] = new_description
                    elif number == 3: file['description3'] = new_description
                    else: return -1
                    return 0

        return -1
    
    def create_folder(self, newFolderName:str, folderPath:str):
        """
        Creates a new Folder in application Model.
        """
        if folderPath == '/':
            self.project_tree['dirs'][newFolderName] = {
                'dirs': {},
                'files': []
            }
            return 0

        self.project_tree['dirs'][folderPath[1:]]['dirs'][newFolderName] = {
            'dirs': {},
            'files': []
        }
        return 0
    
    def delete_folder(self, keep, folder_path):
        """
        Deletes a folder in the project.

        If keep = True, all drawings in the folder will be moved to the parent folder.
        """
        folder_path = folder_path.replace('dir_', '')
        folders_in_path = folder_path.split('_')
        
        # Delete files
        if keep == 0:
            if len(folders_in_path) == 1:
                del self._project_tree['dirs'][folder_path]

            elif len(folders_in_path) == 2:
                del self._project_tree['dirs'][folders_in_path[0]]['dirs'][folders_in_path[1]]
        
            return []
        
        files_to_add_to_tree = []

        # Keep files
        if keep == 1:
            if len(folders_in_path) == 1:
                # Files directly in the folder
                files_to_move = self._project_tree['dirs'][folder_path]['files']
                for file in files_to_move:
                    file['directory'] = 'root'
                    self._project_tree['files'].append(file)
                    files_to_add_to_tree.append(file)
                
                # Files in folders underneath the folder to be deleted
                if len(self._project_tree['dirs'][folder_path]['dirs']) != 0:
                    for key, value in self._project_tree['dirs'][folder_path]['dirs'].items():
                        for file in self._project_tree['dirs'][folder_path]['dirs'][key]['files']:
                            file['directory'] = 'root'
                            self._project_tree['files'].append(file)
                            files_to_add_to_tree.append(file)
                
                del self._project_tree['dirs'][folder_path]

            elif len(folders_in_path) == 2:
                # Files directly in the folder
                files_to_move = self._project_tree['dirs'][folders_in_path[0]]['dirs'][folders_in_path[1]]['files']
                for file in files_to_move:
                    file['directory'] = file['directory'].replace(f"/{folders_in_path[1]}", "")
                    self._project_tree['dirs'][folders_in_path[0]]['files'].append(file)
                    files_to_add_to_tree.append(file)
                
                del self._project_tree['dirs'][folders_in_path[0]]['dirs'][folders_in_path[1]]

        return files_to_add_to_tree
    
    def rename_folder(self, folder_path, new_folder_name):
        """
        Renames a folder in the Model, given the path and folder name
        """
        # Second level folder
        if "_" in folder_path:
            folders = folder_path.split('_')
            parent_folder = folders[0]
            current_folder = folders[1]

            copy_of_folder = self._project_tree['dirs'][parent_folder]['dirs'][current_folder]

            for file in copy_of_folder['files']:
                file['directory'] = file['directory'].replace(current_folder, new_folder_name)

            self._project_tree['dirs'][parent_folder]['dirs'][new_folder_name] = copy_of_folder
            removed = self._project_tree['dirs'][parent_folder]['dirs'][current_folder]
            del self._project_tree['dirs'][parent_folder]['dirs'][current_folder]

            return (removed, copy_of_folder)
        
        # First level folder
        elif '_' not in folder_path:
            current_folder = folder_path

            copy_of_folder = self._project_tree['dirs'][current_folder]

            # Files immediately in old folder need to have their path renamed
            for file in copy_of_folder['files']:
                file['directory'] = file['directory'].replace(current_folder, new_folder_name)
            
            # Each dir in old folder needs to be updated likewise
            for dir_key, dir in copy_of_folder['dirs'].items():
                for file in copy_of_folder['dirs'][dir_key]['files']:
                    file['directory'] = file['directory'].replace(current_folder, new_folder_name)
            
            
            self._project_tree['dirs'][new_folder_name] = copy_of_folder
            removed = self._project_tree['dirs'][current_folder]
            del self._project_tree['dirs'][current_folder]

            return (removed, copy_of_folder)

        return "",""
    
    def remove_file(self, dwg_iid):
        """
        Removes a file in the Model, given the DWG iid within the treeview structure.
        """
        iid_parts = dwg_iid.split('_')
        if iid_parts[0] == 'root':
            for file in self._project_tree['files']:
                if file['name'] == iid_parts[1]:
                    self._project_tree['files'].remove(file)
            return 0

        if iid_parts[0] == 'dir':
            if len(iid_parts) == 3:
                for file in self._project_tree['dirs'][iid_parts[1]]['files']:
                    if file['name'] == iid_parts[2]:
                        self._project_tree['dirs'][iid_parts[1]]['files'].remove(file)
                return 0
            if len(iid_parts) == 4:
                for file in self._project_tree['dirs'][iid_parts[1]]['dirs'][iid_parts[2]]['files']:
                    if file['name'] == iid_parts[3]:
                        self._project_tree['dirs'][iid_parts[1]]['dirs'][iid_parts[2]]['files'].remove(file)
                return 0

        return -1

    def editAllDescription1(self, folder_iid, newDescription):
        """
        Edits all description 1 fields of every DWG file in a folder identified by folder_iid to new_description.
        """
        folder_parts = folder_iid.split('_')
        
        # Root
        if folder_parts[0] == 'root':
            for file in self._project_tree['files']:
                file['description1'] = newDescription
            
            for dict_key, dict_val in self._project_tree['dirs'].items():
                for file in self._project_tree['dirs'][dict_key]['files']:
                    file['description1'] = newDescription
                
                for dict_key2, dict_val2 in self._project_tree['dirs'][dict_key]['dirs'].items():
                    for file in self._project_tree['dirs'][dict_key]['dirs'][dict_key2]['files']:
                        file['description1'] = newDescription
                
            return 0
        
        if folder_parts[0] == 'dir':
            if len(folder_parts) == 2:
                for file in self._project_tree['dirs'][folder_parts[1]]['files']:
                    file['description1'] = newDescription
                
                for dict_key, dict_val in self._project_tree['dirs'][folder_parts[1]]['dirs'].items():
                    for file in self._project_tree['dirs'][folder_parts[1]]['dirs'][dict_key]['files']:
                        file['description1'] = newDescription

                return 0

            elif len(folder_parts) == 3:
                for file in self._project_tree['dirs'][folder_parts[1]]['dirs'][folder_parts[2]]['files']:
                    file['description1'] = newDescription
                
                return 0

        return -1
    
    def editAllDescription2(self, folder_iid, newDescription):
        """
        Edits all description 2 fields of every DWG file in a folder identified by folder_iid to new_description.
        """
        folder_parts = folder_iid.split('_')
        
        # Root
        if folder_parts[0] == 'root':
            for file in self._project_tree['files']:
                file['description2'] = newDescription
            
            for dict_key, dict_val in self._project_tree['dirs'].items():
                for file in self._project_tree['dirs'][dict_key]['files']:
                    file['description2'] = newDescription
                
                for dict_key2, dict_val2 in self._project_tree['dirs'][dict_key]['dirs'].items():
                    for file in self._project_tree['dirs'][dict_key]['dirs'][dict_key2]['files']:
                        file['description2'] = newDescription
                
            return 0
        
        if folder_parts[0] == 'dir':
            if len(folder_parts) == 2:
                for file in self._project_tree['dirs'][folder_parts[1]]['files']:
                    file['description2'] = newDescription
                
                for dict_key, dict_val in self._project_tree['dirs'][folder_parts[1]]['dirs'].items():
                    for file in self._project_tree['dirs'][folder_parts[1]]['dirs'][dict_key]['files']:
                        file['description2'] = newDescription

                return 0

            elif len(folder_parts) == 3:
                for file in self._project_tree['dirs'][folder_parts[1]]['dirs'][folder_parts[2]]['files']:
                    file['description2'] = newDescription
                
                return 0

        return -1
    
    def add_dwg(self, dwg_iid):
        """
        Adds a DWG to the Model with identification dwg_iid
        """
        splits = dwg_iid.split('_')
        # Adding to the root
        if splits[0] == 'root':
            self._project_tree['files'].append(
                {
                    'name':splits[1],
                    'directory':'',
                    'section':'',
                    'description1':'',
                    'description2':'',
                    'description3':''
                }
            )
            return 0
        
        elif splits[0] == 'dir':
            if len(splits) == 3:
                self._project_tree['dirs'][splits[1]]['files'].append(
                    {
                    'name':splits[2],
                    'directory':f"{splits[1]}",
                    'section':'',
                    'description1':'',
                    'description2':'',
                    'description3':''
                }
                )
                return 0
            elif len(splits) == 4:
                self._project_tree['dirs'][splits[1]]['dirs'][splits[2]]['files'].append(
                    {
                    'name':splits[3],
                    'directory':f"{splits[1]}/{splits[2]}",
                    'section':'',
                    'description1':'',
                    'description2':'',
                    'description3':''
                }
                )
                return 0
        
        return -1





class TemplateModel:
    """
    Handles Template File and its properties.
    """
    def __init__(self, template_path: Path):
        self._template_path: Path = template_path
        self._possible_templates: list = []
        self._has_template = False

    @property
    def has_template(self):
        return self._has_template
    
    @property
    def template_path(self):
        return self._template_path
    
    @property
    def possible_templates(self):
        return self._possible_templates
    
    @possible_templates.setter
    def possible_templates(self, value: list):
        self._possible_templates = value
    
    def store_template_options(self):
        """
        Possible template files are stored in Template Model. 
        """
        p = sorted(self._template_path.glob('*.dwg'))
        self._possible_templates = [x for x in p if x.is_file()]
        self._has_template = True





class AppModel:
    """
    Represents Application Model

    Holds the WDP Model and Template Model references for Application object in run.py.
    """
    def __init__(self) -> None:
        self._wdpModel: WDPModel = None
        self._templateModel: TemplateModel = None
    
    def parse_wdp_file(self, wdp_filepath: Path):
        """
        Parses all WDP file contents and stores in WDP Model object
        Returns the WDP Model object
        """
        model = WDPModel(wdp_filepath)
        model.parse()

        if model.is_valid:
            self._wdpModel = model
            return model
        
        return None
    
    def store_possible_templates(self, template_filepath: Path):
        """
        Takes in the directory path where DWG template files are stored
        """
        model = TemplateModel(template_filepath)
        model.store_template_options()

        if model.has_template:
            self._templateModel = model
            return model
        
        return None
    
    @property
    def wdpModel(self):
        return self._wdpModel
    
    @property
    def templateModel(self):
        return self._templateModel