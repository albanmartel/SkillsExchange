# SkillsExchange

Projet web Django

## Objective

The application must enable people to exchange activities.
The person receiving support is not proficient in the activity being carried out.
The activity will take place when the carer has available slots.

## Clone the projet

```
git clone https://github.com/albanmartel/SkillsExchange.git
```

### Create a Django project

#### Create a local Git repository

I have already created a Git repository on my online Git account.
I create a directory for the Django project. I navigate into it and initialise it as a local Git repository.

```bash
git init
```

I create a **README.md** file and a **.gitignore** file. I edit these files and then commit them to Git using `git add` and `git commit`.

```bash
git branch -M main
git remote add origin https://github.com/albanmartel/SkillsExchange.git
git push -u origin main
```

#### Créer un environnement virtuel Python

```bash
python -m venv .venv
```

#### Activating the virtual environment

Open the terminal in your project’s root directory:

- **Windows (Command Prompt / `cmd.exe`)** :

```cmd
.venv\Scripts\activate.bat
```

- **Windows (PowerShell)** :

```powershell
.venv\Scripts\Activate.ps1
```

_(If a script execution error occurs, first run `Set-ExecutionPolicy Unrestricted -Scope Process` in your session)._

- **Linux / macOS** :

```bash
source .venv/bin/activate
```

_`(.venv)` appears at the start of the command line when the virtual environment is activated._

The **.env** file must be saved in the project root directory

#### 3. Installing Django

```bash
pip install Django==5.2.12
```

#### 4. Saving dependencies to a requirements.txt file

```bash
pip freeze > requirements.txt
```

From now on, the ‘requirements.txt’ file can be used to install dependencies for a Django project.

**Note:**

1. I used a ‘requirements.txt’ file from a previous Git repository.
2. **tzdata** was installed to avoid errors relating to the French date and time format

#### 5. Installing Django from the dependencies file

You must first have installed the virtual environment and activated it.

```bash
python -m pip install -r requirements.txt
```

### Creating the django basic site structure

```cmd
mkdir helpexchanges
django-admin startproject config helpexchanges
```

### Creating the **Skills** application

```cmd
cd skillsexchange
python .\manage.py startapp skills
```

**Note:**
At this stage, the admin site is **config** and the application site is **skills**

## Architecture

Project structure :

```powershell
────SkillsExchange
    └───.git
    └─── helpexchanges
        └─── config
        └─── skills
        └─── manage.py
    └───.venv
    └───.gitignore
    └─── README.md
    └─── requirements.txt
```

### Les réglages **site_config\settings.py**

Open the Python file **skills_exchange\apps.py**.
Take a look at the code. In my case, I have the following:

```python
from django.apps import AppConfig


class SkillsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skills'
```

I use this to write the following on the first line of the **INSTALLED_APPS** table in the **site_config\settings.py** file:

starting with the name ‘skills_exchange’, followed by ‘apps’, followed by the class name ‘SkillsExchangeConfig’.

```python
INSTALLED_APPS = [
    'skills_exchange.apps.AppConfig'
    'django.contrib.admin',
    ...
```

```python
ALLOWED_HOSTS = [
    '127.0.0.1',
]
```

In the TEMPLATES table, edit the following DIRS row as follows

```python
'DIRS': [BASE_DIR / 'templates'],
```

Edit the `LANGUAGE_CODE` and `TIME_ZONE` variables so that they look like this:

```python
LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Europe/Paris'
```

Go to the line `STATIC_URL = “static/”`. The code should look like this after you’ve made the changes:

```python
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

This allows you to create a static directory at the root of the Django site and use local CSS and JavaScript files.

The following settings will not be changed in order to use an SQLite database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

To include the debugging tools in Django, you need to add the following:

```python
# Source - https://stackoverflow.com/a/70224986
# Posted by Mohamed tourky
# Retrieved 2026-11-09, License - CC BY-SA 4.0

if DEBUG:

    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
```

### Creating utility directories

In the **manage.py** file, run the following commands

```PowerShell
mkdir templates
mkdir static
cd static
mkdir images
mkdir js
mkdir css
```

This allows parent templates to utilise JavaScript and CSS scripts.

### creates all the necessary tables

```python
python manage.py migrate
```

If your database doesn't exist yet, migrate creates all the necessary tables to match your model definitions. Otherwise if the database already exists, migrate updates the existing table definitions to match the model definitions. Maybe you added a field to one of your models, so migrate would add that column to the database table.

### Launch of the development site

```python
python manage.py runserver
```

### Creating a custom Django user model

__models.py__ :
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass
```

__settings.py__
```python
# Définition ajoutée
AUTH_USER_MODEL = 'users.CustomUser'
```
Note: _users_ est le nom de l'application django dans ce cas

__form.py__
```python
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('email', 'username',)


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('email', 'username',)
```

__admin.py__ :
```python
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]

admin.site.register(CustomUser, CustomUserAdmin)
```

### How to reset your Django migrations?
After completing the implementation steps outlined above, I encountered problems when trying to implement my new models in the database

If you encounter any problems with the migration.
My custom user model wasn’t created at the start of the project. As a result, I’ve run into some problems.

__Windows__
```PowerShell
bash
```
puis 
```bash
 find skills/migrations -type f ! -name "__init__.py" -delete
 rm -f db.sqlite3 ../db.sqlite3
```

__Notes:__ 

_The first command searches for and deletes old migration files._

_The second command deletes SQLite database files_

and after that, the usual commands :

```python
python manage.py makemigrations
python manage.py migrate
```

### Ressources

1. Use the help provided by <https://github.com>. When creating a repository, GitHub offers to help you link a local repository to the remote repository.

1. Link a local repository to the Git remote repository:
   <https://labex.io/fr/tutorials/git-step-by-step-instructions-for-linking-a-git-repository-to-a-remote-398369>

1. Add debugging tools to Django: <https://stackoverflow.com/a/70224986>

1. Suppress latest commit in git <https://sebastien-gandossi.fr/blog/git-supprimer-un-commit-local-ou-distant>

```PowerShell
git reset HEAD~
```

1. Update and avoid include warning <https://global.php.cn/fr/faq/1796912830.html>

```Python
from django.conf import settings

settings.configure(DEBUG=True)
```

1. what does " python manage.py migrate " in django do exactly ? <https://stackoverflow.com/questions/62311073/what-does-python-manage-py-migrate-in-django-do-exactly>

```Python
python manage.py migrate
```
### Create a superuser

```python
python manage.py createsuperuser
```

### Enregistrer les nouveaux modèles en base de données : 

```Python
python manage.py makemigrations
python manage.py migrate
```

1. List activities related to specific skills <https://www.davidfraisse.fr/competences-a-mettre-sur-un-cv/>

| Secteur / Domaine             | Compétences techniques                                                                           |
| ----------------------------- | ------------------------------------------------------------------------------------------------ |
| **Commercial / Vente**        | CRM Salesforce, négociation B2B, prospection outbound, gestion de pipeline, reporting commercial |
| **Ressources Humaines**       | SIRH (Workday, SAP HR), conduite d’entretiens, gestion de la paie, droit du travail, recrutement |
| **Informatique / Dev**        | Python, JavaScript, React, SQL, Git, Docker, CI/CD, AWS, méthodes Agile/Scrum                    |
| **Marketing / Communication** | Google Analytics, SEO/SEA, Meta Ads, gestion de campagnes email, Canva, Adobe Suite              |
| **Finance / Comptabilité**    | Sage, SAP FI, contrôle de gestion, consolidation, normes IFRS, reporting financier               |
| **Logistique / Supply Chain** | ERP (SAP WM), gestion des stocks, Lean management, planification, transport multimodal           |
| **Santé / Médico-social**     | Soins infirmiers, logiciel de dossier patient (DMP), gestion de plannings, protocoles médicaux   |
| **Enseignement / Formation**  | Ingénierie pédagogique, LMS (Moodle, Talentsoft), conception de modules e-learning, évaluation   |
| **BTP / Technique**           | AutoCAD, lecture de plans, gestion de chantier, normes NF, conduite d’engins (CACES)             |
| **Créatif / Design**          | Adobe Illustrator, Figma, direction artistique, UX/UI design, gestion de projets créatifs        |

1. Create super user <https://django.wiki/tutorials/manage-py-explained/>

1. Use a simple view <https://pytutorial.com/django-templateview-example/>

1. To see how to make abstract classe and use Class Meta abstract= true. Read Django Abstract classes <https://medium.com/@dharmateja.k/django-abstract-classes-f0928b2c9127>

1. Create dictionary of durations, broken down into days, hours and minutes in python <https://stackoverflow.com/a/10981895>

1. Creating a custom Django user model <https://openclassrooms.com/fr/courses/7192426-allez-plus-loin-avec-le-framework-django/7386368-personnalisez-le-modele-utilisateur>

1. How to reset your Django migrations? <https://medium.com/django-unleashed/how-to-reset-your-django-migrations-3717228054a0>

1. Examples of model relationship API usage¶<https://docs.djangoproject.com/fr/5.2/topics/db/examples/>

1. Create a date that is null by default <https://stackoverflow.com/a/53721823>

1. Ensure when the record is created, the date used is today’s date <https://stackoverflow.com/a/2771701>

1. The Enum types in Django 5.2 <https://docs.djangoproject.com/fr/5.2/ref/models/fields/#enumeration-types>