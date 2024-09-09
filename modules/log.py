import os

def create_file(file_name, content):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    logs_dir = os.path.join(project_root, 'logs')
    
    os.makedirs(logs_dir, exist_ok=True)
    
    path = os.path.join(logs_dir, file_name)
    
    with open(path, 'w') as dosya:
        dosya.write(content)
    print(f"Log File Created at {path}")
    
def write_on_file(file_name, content):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    logs_dir = os.path.join(project_root, 'logs')
    path = os.path.join(logs_dir, file_name)
    
    with open(path, 'a') as dosya: 
        dosya.write(content)