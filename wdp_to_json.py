
def get_directory_lines(project_file: str):
    """
    Reads the AutoCAD WDP file and returns a list of relevant lines project directory information.
    """
    if project_file[-4:] != ".wdp":
        return None
    
    relevant_lines = []
    with open(project_file, 'r') as fd:
        lines = fd.readlines()
        
        for line in lines:
            if line.startswith('=') or line.endswith('.dwg\n'):
                relevant_lines.append(line.strip())

    fd.close()
    return relevant_lines

class Drawing:
    """
    Class: Drawing

    Describes a drawing within the WDP project file.
    """
    def __init__(self) -> None:
        self._name: str = None
        self._description1: str = None
        self._description2: str = None
        self._description3: str = None
        self._directory: str = None

    def name(self, set=False, name=None) -> str:
        if set: self._name = name
        return self._name
    
    def description(self, number=1, set=False, description=None) -> str:
        if number == 1:
            if set:
                self._description1 = description
            return self._description1
        elif number == 2:
            if set:
                self._description2 = description
            return self._description2
        elif number == 3:
            if set:
                self._description3 = description
            return self._description3
        else:
            raise ValueError()
    
    def directory(self, set=False, directory=None) -> str:
        if set:
            self._directory = directory
        return self._directory
    
    def clear(self):
        self._name = None
        self._description1 = None
        self._description2 = None
        self._description3 = None
        self._directory = None
    
    def to_json(self):
        return {
            "description1": self._description1, 
            "description2": self._description2, 
            "description3": self._description3, 
            "path":         self._directory
        }


def extract_project_info(contents: list):
    '''
    Extract Project Information

    Arguments:
        contents = list of relevant lines extracted from WDP file

    Returns:
        drawings = Extracted information from all drawings contained in WDP file (dict format)
        empty_subdirectories = All empty subdirectories (list format)
    '''
    drawings = {}
    empty_subdirectories = []

    dwg_obj = Drawing()
    description_number = 1
    for line in contents:
        # Project Path Directory Line
        if line[:9] == "=====SUB=":
            if "[Empty]" in line:
                empty_subdirectories.append(line[9:-7])
                dwg_obj.clear()
                description_number = 1

            dwg_obj.directory(set=True, directory=line[9:])
        # Description Line
        elif line[:3] == "===":
            dwg_obj.description(number=description_number, set=True, description=line[3:])
            description_number += 1
        # .dwg Line
        elif line[-4:] == '.dwg':
            dwg_obj.name(set = True, name=line)

            # DWG file is the last thing to be read
            #   save drawing object
            drawings[dwg_obj.name()] = dwg_obj.to_json()
            
            #   clear the dwg object
            dwg_obj.clear()
            description_number = 1

    return drawings, empty_subdirectories

def construct_project_structure(drawings, empty_directories):
    '''
    Construct Project Stucture

    Constructs the folder structure of WDP project in JSON format.
    '''
    
    root:dict = {
        'dirs':{},
        'files':[]
    }

    def path_exists(path_str, tree):
        '''
        Checks if we already added the path to the ROOT dictionary
        '''
        if path_str == None:
            return True
        
        current = tree['dirs']
        if path_str.count('/') == 0:
            try:
                current[path_str]
            except KeyError as e:
                return False

        if path_str.count('/') == 1:
            folders = path_str.split('/')
            try:
                current[folders[0]]['dirs'][folders[1]]
            except KeyError as e:
                return False

        return True
    
    for file in drawings:
        file_information = drawings[file]
        file_path = file_information['path']

        if not path_exists(file_path, root):
            # Single-level folder
            if file_path.count('/') == 0:
                root['dirs'][file_path] = {
                    'dirs':{},
                    'files':[]
                }
            
            # Two-level folder
            else:
                folders = file_path.split('/')
                # First level does not exists
                if not path_exists(folders[0], root):
                    # Add first level
                    root['dirs'][folders[0]] = {
                        'dirs': {},
                        'files': []
                    }
                    # Add second level
                    root['dirs'][folders[0]]['dirs'][folders[1]] = {
                        'dirs': {},
                        'files': []
                    }
                else:
                    # Add second level
                    root['dirs'][folders[0]]['dirs'][folders[1]] = {
                        'dirs': {},
                        'files': []
                    }

    # Empty Directories - empty_directories
    for path in empty_directories:
        # Path is only first level
        if path.count('/') == 0:
            root['dirs'][path] = {
                'dirs': {},
                'files': []
            }
        # Path is two-level
        elif path.count('/') == 1:
            folders = path.split('/')

            # The first level doesn't exist yet
            if not path_exists(folders[0], root):
                # Add first level
                root['dirs'][folders[0]] = {
                    'dirs': {},
                    'files': []
                }
                # Add second level
                root['dirs'][folders[0]]['dirs'][folders[1]] = {
                    'dirs': {},
                    'files': []
                }
            else:
                # Add second level
                root['dirs'][folders[0]]['dirs'][folders[1]] = {
                    'dirs': {},
                    'files': []
                }
    
    return root
    
def populate_folder_structure(drawings, root):
    '''
    Populate Folder Structure

    Inserts DWG files and information where they belong in the folder structure.
    '''
    for dwg in drawings:
        file_path = drawings[dwg]['path']

        d = {
            'name':dwg,
            'description1': drawings[dwg]['description1'],
            'description2': drawings[dwg]['description2'],
            'description3': drawings[dwg]['description3']
        }

        # Root
        if file_path == None:
            root['files'].append(d)


        # Single-Level
        elif file_path.count('/') == 0:
            root['dirs'][folders[0]]['files'].append(d)

        # Two-Level
        elif file_path.count('/') == 1:
            folders = file_path.split('/')
            root['dirs'][folders[0]]['dirs'][folders[1]]['files'].append(d)



def wdp_to_json(project_file: str):
    # Get relevant project structure/directory information
    contents: list = get_directory_lines(project_file)

    """
    PHASE 1:
        - Extract information for all drawings contained in WDP file (Python Dictionary format)
        - Extract all empty directories (list of empty subdirectories)
    """
    drawings, empty_directories = extract_project_info(contents)
    
    """
    PHASE 2:
        - Create a JSON object that resembles the folder structure
    """
    root = construct_project_structure(drawings, empty_directories)
    

    """
    PHASE 3:
        - Populate files into directory structure
    """
    populate_folder_structure(drawings, root)
    
    return root



project_file = "project.wdp"
wdp_json = wdp_to_json(project_file)