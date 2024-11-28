import os
import subprocess
import sys
from colorama import Fore, init
init()
import django
from django.contrib.auth import get_user_model
from django.core.management import call_command

# Project name and directory paths
PROJECT_NAME = "my_project"
BASE_DIR = os.path.join(os.getcwd(), PROJECT_NAME)
CORE_DIR = os.path.join(BASE_DIR, "core")
VENV_DIR = os.path.join(BASE_DIR, '.venv')
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
POSTS_DIR = os.path.join(BASE_DIR, 'posts')
FILES_DIR = os.path.join(os.getcwd(), 'files')

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
        'posts_list': 'posts_list.html',
        'post_page': 'post_page.html'
    }

    if templates_type not in templates_files:
        raise ValueError(f"Type de template non valide: {templates_type}")

    full_path = os.path.join(os.getcwd(), templates_path, templates_files[templates_type])
    print(f"Looking for template at: {full_path}")

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Le fichier template {full_path} n'existe pas")

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

    os.makedirs(target_dir, exist_ok=True)
    print(f"Directory ensured: {target_dir}")

    templates_files = {
        'home': 'home.html',
        'about': 'about.html',
        'layout': 'layout.html',
        'posts_list': 'posts_list.html',
        'post_page': 'post_page.html'
    }

    file_name = templates_files.get(templates_type)
    if not file_name:
        print(f"Type de template inconnu: {templates_type}")
        return

    file_path = os.path.join(target_dir, file_name)
    print(f"Creating template file at: {file_path}")

    try:
        templates_content = load_external_templates(templates_type, templates_path='files/templates.posts' if sub_dir == 'posts' else 'files/')
    except Exception as e:
        print(f"Erreur lors du chargement du template {templates_type}: {e}")
        return

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(templates_content)

    print(f"Le fichier {file_name} a été créé dans {target_dir}")

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

def create_posts_app():
    django_admin_path = os.path.join(VENV_DIR, 'bin', 'django-admin')
    posts_dir = os.path.join(BASE_DIR, 'posts')
    create_directory(posts_dir)  # Créez le répertoire posts avant d'exécuter startapp
    subprocess.check_call([django_admin_path, 'startapp', 'posts', posts_dir])
    print(f"Django app 'posts' created at {posts_dir}.")

def create_models_py(posts_dir, file_name):
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
    file_path = os.path.join(posts_dir, file_name)

    default_content = """
from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
"""
    with open(file_path, 'w') as file:
        file.write(default_content)

def create_posts_views_py(posts_dir, file_name):
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
    file_path = os.path.join(posts_dir, file_name)

    default_content = """
from django.shortcuts import render


# Create your views here.


def posts_list(request):
    return render(request, 'posts/posts_list.html')

"""
    with open(file_path, 'w') as file:
        file.write(default_content)

def create_posts_admin_py(posts_dir, file_name):
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
    file_path = os.path.join(posts_dir, file_name)

    default_content = """
from django.contrib import admin
from .models import Post

# Register your models here.
admin.site.register(Post)
"""
    with open(file_path, 'w') as file:
        file.write(default_content)

def create_posts_urls_py(posts_dir, file_name):
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
    file_path = os.path.join(posts_dir, file_name)

    default_content = """

from django.urls import path
from . import views


urlpatterns = [
    path('', views.posts_list),
]
"""
    with open(file_path, 'w') as file:
        file.write(default_content)

def create_core_views_py(core_dir, file_name):
    if not os.path.exists(core_dir):
        os.makedirs(core_dir)
    file_path = os.path.join(core_dir, file_name)

    default_content = """
# from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
    # return HttpResponse("Hello World! I'm Home.")
    return render(request, 'home.html')


def about(request):
    # return HttpResponse("My About page.")
    return render(request, 'about.html')
"""
    with open(file_path, 'w') as file:
        file.write(default_content)

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

def update_installed_apps(settings_file):
    with open(settings_file, 'r') as file:
        content = file.readlines()

    for i, line in enumerate(content):
        if line.strip().startswith("INSTALLED_APPS"):
            content.insert(i + 1, "    'posts',\n")
            break

    with open(settings_file, 'w') as file:
        file.writelines(content)

    print("Updated INSTALLED_APPS to include 'posts' in settings.py")

def update_urls_py(core_dir, file_name):
    new_content = """
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('about/', views.about),
    path('posts/', include('posts.urls'))
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
            new_lines[i] = "            'DIRS': [os.path.join(BASE_DIR, 'templates')],\n"
        elif "'DIRS':" in line and "templates" not in line:
            new_lines[i] = "            'DIRS': [os.path.join(BASE_DIR, 'templates')],\n"

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

def create_gitignore():
    gitignore_path = os.path.join(BASE_DIR, ".gitignore")
    with open(gitignore_path, "w") as f:
        f.write(GITIGNORE_CONTENT)
    print(".gitignore file created with the specified rules.")
    
def add_css_file(static_dir, css_source_path='files/static/style.css'):
    """
    Copie un fichier CSS vers le répertoire static de Django.
    """
    # Vérifie si le répertoire static existe, sinon le crée
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        print(f"Static directory created: {static_dir}")
    
    # Chemin de destination pour le fichier CSS
    css_dest_path = os.path.join(static_dir, 'style.css')

    if not os.path.exists(css_source_path):
        print(f"CSS source file '{css_source_path}' not found. Ensure the path is correct.")
        return

    # Copie le fichier CSS
    with open(css_source_path, 'r', encoding='utf-8') as source_file:
        css_content = source_file.read()
    
    with open(css_dest_path, 'w', encoding='utf-8') as dest_file:
        dest_file.write(css_content)

def load_migration_file(posts_dir, source_path='files/migrations/0001_initial.py'):
    """
    Charge le fichier de migration depuis un chemin source et le copie dans le dossier migrations de l'application.
    
    :param posts_dir: Répertoire de l'application posts
    :param source_path: Chemin source du fichier de migration
    """
    # Créer le dossier migrations s'il n'existe pas
    migrations_dir = os.path.join(posts_dir, 'migrations')
    os.makedirs(migrations_dir, exist_ok=True)

    # Chemin de destination du fichier de migration
    destination_path = os.path.join(migrations_dir, '0001_initial.py')

    # Copier le fichier de migration
    try:
        with open(source_path, 'r') as source_file:
            migration_content = source_file.read()
        
        with open(destination_path, 'w') as dest_file:
            dest_file.write(migration_content)
        
        print(f"Migration file copied from {source_path} to {destination_path}")
    except FileNotFoundError:
        print(f"Source migration file not found at {source_path}")
    except Exception as e:
        print(f"Error copying migration file: {e}")
        
def execute_django_migrations(base_dir):
    """
    Exécute les commandes makemigrations et migrate pour tous les apps.
    
    :param base_dir: Répertoire de base du projet Django
    """
    # Chemin vers manage.py
    manage_py_path = os.path.join(base_dir, 'manage.py')
    
    try:
        # Exécute makemigrations
        subprocess.run([sys.executable, manage_py_path, 'makemigrations'], 
                       check=True, 
                       cwd=base_dir)
        print(Fore.BLUE+ "Migrations created successfully ✅")
        
        # Exécute migrate
        subprocess.run([sys.executable, manage_py_path, 'migrate'], 
                       check=True, 
                       cwd=base_dir)
        print(Fore.BLUE + "Migrations applied successfully 🚀")
        
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error during migrations: {e}")
    except Exception as e:
        print
        
 

def create_superuser(username='admin', password='19854', email='admin@example.com'):
    """
    Crée un superutilisateur Django automatiquement avec gestion d'erreurs améliorée.
    """
    # Configuration explicite de l'environnement Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    try:
        # Configurer explicitement Django
        django.setup()

        # Vérifier si le superutilisateur existe déjà
        User = get_user_model()

        if User.objects.filter(username=username).exists():
            print(f"Le superutilisateur {username} existe déjà")
            return
        
        # Créer un superutilisateur via la commande Django sans interaction
        call_command('createsuperuser', username=username, password=password, email=email, interactive=False)
        print(f"Superutilisateur {username} créé avec succès ✅")

    except Exception as e:
        print(f"Erreur lors de la création du superutilisateur : {e}")



def install_compressor():
    """Installe django-compressor dans l'environnement virtuel."""
    pip_path = os.path.join(VENV_DIR, 'bin', 'pip')
    subprocess.check_call([pip_path, 'install', 'django-compressor'])
    print("django-compressor installé dans l'environnement virtuel.")

def install_tailwind():
    """Installe Tailwind CSS via npm."""
    try:
        # Vérifier si npm est installé
        subprocess.check_call(['npm', '--version'])
        print("npm trouvé, installation de Tailwind CSS...")

        # Installer tailwind CSS via npm
        subprocess.check_call(['npm', 'install', 'tailwindcss'])
        print("Tailwind CSS installé avec succès.")
    except subprocess.CalledProcessError as e:
        print("Erreur lors de l'installation de Tailwind CSS. Assurez-vous que npm est installé.")
    except Exception as e:
        print(f"Erreur lors de l'installation de Tailwind CSS : {e}")

def add_compressor_to_settings(settings_file):
    """Ajoute django-compressor aux paramètres de settings.py."""
    with open(settings_file, 'r') as file:
        content = file.readlines()

    for i, line in enumerate(content):
        if line.strip().startswith("INSTALLED_APPS"):
            content.insert(i + 1, "    'compressor',\n")
            break

    with open(settings_file, 'w') as file:
        file.writelines(content)

    print("django-compressor ajouté à INSTALLED_APPS dans settings.py.")

def configure_tailwind_in_settings(settings_file):
    """Configure Tailwind CSS dans le settings.py de Django."""
    with open(settings_file, 'r') as file:
        content = file.readlines()

    for i, line in enumerate(content):
        if line.strip().startswith("STATICFILES_DIRS"):
            content.insert(i + 1, "    os.path.join(BASE_DIR, 'static'),\n")
            break

    with open(settings_file, 'w') as file:
        file.writelines(content)

    print("Configuration de Tailwind CSS ajoutée dans settings.py.")
    
def create_project_structure(project_name):
    os.makedirs(f'{project_name}/static/css', exist_ok=True)
    os.makedirs(f'{project_name}/templates', exist_ok=True)
    print(f"[INFO] Project structure created for: {project_name}")

def initialize_tailwind(static_dir):
    try:
        print("[INFO] Initializing Tailwind CSS configuration...")
        subprocess.check_call(['npx', 'tailwindcss', 'init'])
        print("[SUCCESS] tailwind.config.js created.")

        input_css_path = os.path.join(static_dir, 'css', 'input.css')
        os.makedirs(os.path.dirname(input_css_path), exist_ok=True)
        with open(input_css_path, 'w') as css_file:
            css_file.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n")
        print(f"[INFO] Tailwind CSS input file created at: {input_css_path}")

        output_css_path = os.path.join(static_dir, 'css', 'output.css')
        print(f"[INFO] Compiling Tailwind CSS into {output_css_path}...")
        subprocess.check_call(['npx', 'tailwindcss', '-i', input_css_path, '-o', output_css_path, '--watch'])
        print(f"[SUCCESS] Tailwind CSS output file generated at: {output_css_path}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] An error occurred: {e}")
        
# Fonction pour charger un fichier à partir du répertoire 'files'
def load_file(file_name, default_content=None):
    file_path = os.path.join(FILES_DIR, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif default_content:
        # Si le fichier n'existe pas, utiliser le contenu par défaut
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(default_content)
        return default_content
    else:
        raise FileNotFoundError(f"Le fichier {file_name} n'a pas été trouvé et aucun contenu par défaut n'est spécifié.")

# Contenu par défaut pour les fichiers si ils sont absents
DEFAULT_TAILWIND_CONFIG = """
module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""

DEFAULT_POSTCSS_CONFIG = """
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""

DEFAULT_CSS = """
@tailwind base;
@tailwind components;
@tailwind utilities;
"""

# Fonction pour installer Tailwind CSS et ses dépendances
def install_tailwind():
    subprocess.run(["npm", "install", "tailwindcss", "autoprefixer", "postcss-cli"], check=True)
    subprocess.run(["npx", "tailwindcss", "init"], check=True)
    print("Tailwind CSS a été installé et configuré.")

# Fonction pour ajouter le fichier de configuration Tailwind
def add_tailwind_config():
    # Vérifier si le fichier de configuration Tailwind existe dans le répertoire 'files'
    tailwind_config_content = load_file('tailwind.config.js', DEFAULT_TAILWIND_CONFIG)
    with open(os.path.join(BASE_DIR, 'tailwind.config.js'), 'w', encoding='utf-8') as file:
        file.write(tailwind_config_content)
    print("Le fichier de configuration tailwind.config.js a été créé ou mis à jour.")

    # Vérifier si le fichier postcss.config.js existe dans le répertoire 'files'
    postcss_config_content = load_file('postcss.config.js', DEFAULT_POSTCSS_CONFIG)
    with open(os.path.join(BASE_DIR, 'postcss.config.js'), 'w', encoding='utf-8') as file:
        file.write(postcss_config_content)
    print("Le fichier de configuration postcss.config.js a été créé ou mis à jour.")

# Fonction pour mettre à jour le fichier CSS avec Tailwind
def update_css_with_tailwind():
    # Créer un fichier CSS pour utiliser Tailwind
    css_content = load_file('style.css', DEFAULT_CSS)
    with open(os.path.join(STATIC_DIR, 'style.css'), 'w', encoding='utf-8') as file:
        file.write(css_content)
    print("Le fichier CSS a été mis à jour avec Tailwind.")

        

def main():
    project_name = 'my_project'
    create_project_structure(project_name)
    
    static_dir = os.path.join(project_name, 'static')
    initialize_tailwind(static_dir)
    print(f"[INFO] Project '{project_name}' set up successfully!")

# Fonction d'installation qui appelle toutes les autres
def setup_project():
    """
    Fonction principale pour configurer un projet Django.
    Inclut l'installation de Django, la création de l'application 'posts', la création des migrations,
    l'ajout des fichiers essentiels, et la création du superutilisateur.
    """
    print(f"Setting up the '{PROJECT_NAME}' project...")

    # Création des répertoires de base
    create_directory(PROJECT_NAME)
    create_directory(CORE_DIR)

    # Création de l'environnement virtuel et activation
    create_virtual_environment()
    activate_virtual_environment()

    # Installation de Django et démarrage du projet
    install_django()
    start_django_project()

    # Création de l'application 'posts' et ajout de ses fichiers
    create_posts_app()
    load_migration_file(POSTS_DIR)
    execute_django_migrations(BASE_DIR)

    create_models_py(POSTS_DIR, "models.py")
    create_posts_views_py(POSTS_DIR, "views.py")
    create_posts_admin_py(POSTS_DIR, "admin.py")
    create_posts_urls_py(POSTS_DIR, "urls.py")
    create_core_views_py(CORE_DIR, "views.py")

    # Mise à jour des paramètres dans 'settings.py'
    settings_file = os.path.join(CORE_DIR, "settings.py")
    update_allowed_hosts(settings_file)
    update_installed_apps(settings_file)

    # Création des templates
    create_directory(TEMPLATES_DIR)
    create_templates(TEMPLATES_DIR, 'layout')
    create_templates(TEMPLATES_DIR, 'home')
    create_templates(TEMPLATES_DIR, 'about')
    create_templates(TEMPLATES_DIR, 'posts_list', sub_dir='posts')
    create_templates(TEMPLATES_DIR, 'post_page', sub_dir='posts')

    # Création du dossier 'static' et ajout du fichier CSS
    create_directory(STATIC_DIR)
    add_css_file(STATIC_DIR, css_source_path='files/static/style.css')

    # Mise à jour des fichiers 'urls.py' et 'settings.py'
    update_urls_py(CORE_DIR, "urls.py")
    update_settings(CORE_DIR, "settings.py")

    # Création du fichier '.gitignore'
    create_gitignore()

    # Créer le superutilisateur après avoir exécuté les migrations
    create_superuser()

    # Installer django-compressor et Tailwind CSS si nécessaire
    install_compressor_and_tailwind()

    # Mise à jour de 'settings.py' pour ajouter les configurations de compressor et tailwind
    add_compressor_to_settings(settings_file)
    configure_tailwind_in_settings(settings_file)

    print(Fore.YELLOW + f"'{PROJECT_NAME}' project successfully set up! 🙌🏻 🎉")
    print(Fore.CYAN + f"'{PROJECT_NAME}' now type, cd {PROJECT_NAME} 📂 📂")
    print(Fore.MAGENTA + f"'{PROJECT_NAME}' and run the server with py manage.py runserver 👀 🔍")

def install_compressor_and_tailwind():
    """
    Installe django-compressor et django-tailwind dans l'environnement virtuel.
    """
    install_compressor()
    install_tailwind()

if __name__ == "__main__":
    setup_project()






