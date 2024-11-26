import os
import subprocess
import sys
from colorama import Fore, init

init()

# Project name and directory paths
PROJECT_NAME = "my_project"
BASE_DIR = os.path.join(os.getcwd(), PROJECT_NAME)
CORE_DIR = os.path.join(BASE_DIR, "core")
VENV_DIR = os.path.join(BASE_DIR, '.venv')
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Content for the .gitignore file
GITIGNORE_CONTENT = """
.DS_Store
core/.venv
*.sqlite3
__pycache__
"""

def load_external_templates(templates_type='home', templates_path='files/'):
    """
    Charge un template HTML depuis un fichier externe.
    """
    templates_files = {
        'home': 'home.html',
        'about': 'about.html',
        'layout': 'layout.html',
        'post_list': 'post_list.html',  # Added
        'post_page': 'post_page.html'   # Added
    }

    if templates_type not in templates_files:
        raise ValueError(f"Type de template non valide: {templates_type}")
    
    full_path = os.path.join(os.getcwd(), templates_path, templates_files[templates_type])
    print(f"Looking for template at: {full_path}")  # Debugging

    # Vérifier si le fichier existe
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Le fichier template {full_path} n'existe pas")
    
    # Lire le contenu du fichier
    with open(full_path, 'r', encoding='utf-8') as file:
        templates_content = file.read()
    
    return templates_content

def create_templates(templates_dir, templates_type='home', sub_dir=None):
    """
    Crée un fichier de template dans le dossier templates (y compris les sous-dossiers).
    """
    target_dir = templates_dir
    if sub_dir:
        target_dir = os.path.join(templates_dir, sub_dir)
    
    # Ensure the directory exists
    os.makedirs(target_dir, exist_ok=True)
    print(f"Directory ensured: {target_dir}")  # Debugging



def create_directory(path):
    os.makedirs(path, exist_ok=True)
    print(f"Directory created: {path}")

def create_virtual_environment():
    subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
    print(f"Virtual environment created at {VENV_DIR}")

def activate_virtual_environment():
    activate_script = os.path.join(VENV_DIR, 'bin', 'activate')
    if not os.path.isfile(activate_script):
        print(f"The activation script was not found at {activate_script}")
        return
    subprocess.run(f"source {activate_script} && echo 'Virtual environment activated'", shell=True, executable='/bin/bash')
    print("The virtual environment has been activated.")

def install_django():
    pip_path = os.path.join(VENV_DIR, 'bin', 'pip')
    subprocess.check_call([pip_path, 'install', 'django'])
    print("Django installed in the virtual environment.")

def start_django_project():
    django_admin_path = os.path.join(VENV_DIR, 'bin', 'django-admin')
    subprocess.check_call([django_admin_path, 'startproject', "core", BASE_DIR])
    print(f"Django project '{PROJECT_NAME}' initialized with `manage.py`.")

def update_allowed_hosts(settings_file):
    with open(settings_file, 'r') as file:
        content = file.readlines()

    for i, line in enumerate(content):
        if line.strip().startswith("ALLOWED_HOSTS"):
            content[i] = "ALLOWED_HOSTS = ['127.0.0.1']\n"
            break

    with open(settings_file, 'w') as file:
        file.writelines(content)
    
    print("Updated ALLOWED_HOSTS to include '127.0.0.1' in settings.py")

def create_templates(templates_dir, templates_type='home', sub_dir=None):
    """
    Crée un fichier de template dans le dossier templates (y compris les sous-dossiers).
    """
    # Resolve subdirectory path
    target_dir = templates_dir
    if sub_dir:
        target_dir = os.path.join(templates_dir, sub_dir)
    
    # Ensure the directory exists
    os.makedirs(target_dir, exist_ok=True)
    print(f"Directory ensured: {target_dir}")
    
    # Map template types to filenames
    templates_files = {
        'home': 'home.html',
        'about': 'about.html',
        'layout': 'layout.html',
        'post_list': 'post_list.html',
        'post_page': 'post_page.html',
    }
    
    file_name = templates_files.get(templates_type)
    if not file_name:
        print(f"Type de template inconnu: {templates_type}")
        return
    
    file_path = os.path.join(target_dir, file_name)
    print(f"Creating template file at: {file_path}")
    
    # Load template content
    try:
        # Use appropriate path for posts templates
        templates_content = load_external_templates(templates_type, templates_path='files/templates.posts' if sub_dir == 'posts' else 'files/')
    except Exception as e:
        print(f"Erreur lors du chargement du template {templates_type}: {e}")
        return
    
    # Write the template content to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(templates_content)
    
    print(f"Le fichier {file_name} a été créé dans {target_dir}")

    

def create_gitignore():
    gitignore_path = os.path.join(BASE_DIR, ".gitignore")
    with open(gitignore_path, "w") as f:
        f.write(GITIGNORE_CONTENT)
    print(".gitignore file created with the specified rules.")

def create_views_py(core_dir, file_name):
    if not os.path.exists(core_dir):
        os.makedirs(core_dir)
    file_path = os.path.join(core_dir, file_name)

    default_content = """
from django.shortcuts import render

def homepage(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
"""
    with open(file_path, 'w') as file:
        file.write(default_content)

def update_urls_py(core_dir, file_name):
    new_content = """
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('about/', views.about),
]
"""
    file_path = os.path.join(core_dir, file_name)

    if os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write(new_content)
        print(f"Le fichier '{file_name}' dans le dossier '{core_dir}' a été mis à jour.")

def update_settings(core_dir, file_name):
    settings_file_path = os.path.join(core_dir, file_name)
    
    if not os.path.exists(settings_file_path):
        print(f"Le fichier '{settings_file_path}' n'existe pas.")
        return

    with open(settings_file_path, 'r') as file:
        content = file.readlines()

    import_os_present = False
    new_lines = []

    for line in content:
        if line.strip() == "import os":
            import_os_present = True
        
        if not import_os_present and line.startswith("import"):
            new_lines.append("import os\n")  
            import_os_present = True
        
        new_lines.append(line)

    if not import_os_present:
        new_lines.insert(0, "import os\n")

    for i, line in enumerate(new_lines):
        if "'DIRS': []" in line:
            new_lines[i] = "            'DIRS': ['templates'],\n"
        elif "'DIRS':" in line and "templates" not in line:
            new_lines[i] = "            'DIRS': ['templates'],\n"
    
    staticfiles_found = False
    for i, line in enumerate(new_lines):
        if "STATICFILES_DIRS" in line:
            staticfiles_found = True
            break

    if not staticfiles_found:
        staticfiles_config = "\nSTATICFILES_DIRS = [\n    os.path.join(BASE_DIR, 'static')\n]\n"
        new_lines.append(staticfiles_config)
    
    with open(settings_file_path, 'w') as file:
        file.writelines(new_lines)


def setup_project():
    print(f"Setting up the '{PROJECT_NAME}' project...")
    create_directory(PROJECT_NAME)
    create_directory(CORE_DIR)
    create_virtual_environment()
    activate_virtual_environment()
    install_django()
    start_django_project()
    settings_file = os.path.join(CORE_DIR, "settings.py")
    update_allowed_hosts(settings_file) 
    create_directory(TEMPLATES_DIR)
    create_templates(TEMPLATES_DIR, 'layout')
    create_templates(TEMPLATES_DIR, 'home')
    create_templates(TEMPLATES_DIR, 'about')
    
    # Create templates for posts in the 'posts' subdirectory
    create_templates(TEMPLATES_DIR, 'post_list', sub_dir='posts')
    create_templates(TEMPLATES_DIR, 'post_page', sub_dir='posts')
    
    create_directory(STATIC_DIR)
    create_views_py(CORE_DIR, "views.py")
    update_urls_py(CORE_DIR, "urls.py")
    update_settings(CORE_DIR, "settings.py")
    create_gitignore()
    print(Fore.GREEN + f"'{PROJECT_NAME}' project successfully set up! 🎉")
    print(Fore.CYAN + f"'{PROJECT_NAME}' now type, cd my_project 📂")
    print(Fore.MAGENTA + f"'{PROJECT_NAME}' and run the server with py manage.py runserver 🔍")


if __name__ == "__main__":
    setup_project()