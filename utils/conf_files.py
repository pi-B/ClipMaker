import json

def add_current_project(projects: list, current_project_path : str) -> list:
    index = is_in_list(projects, current_project_path)
    if index == 0:
        return projects
    elif index is None :
        return [current_project_path] + projects
    else :
        projects.pop(index)
        replacement = [current_project_path] + projects
        return replacement
      
    
def is_in_list(search_list : list, value : str) -> int | None:
    try:
        i = search_list.index(value)
    except ValueError:
        return None
    
    for i in range(0,len(search_list)-1):
        if search_list[i] == value : 
            return i
        
def update_conf_file(conf : dict) :
    with open(".conf/state.json", "w") as conf_file:
        stringified = json.dumps(conf)
        conf_file.write(stringified)
        conf_file.close()        

def get_conf() -> dict :
    with open(".conf/state.json", "r") as conf_file:
        conf = json.loads(conf_file.read())       
        conf_file.close()
        return conf