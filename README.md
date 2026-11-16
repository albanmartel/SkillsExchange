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

####  Create a local Git repository

I have already created a Git repository on my online Git account.
I create a directory for the Django project. I navigate into it and initialise it as a local Git repository.

```bash
git init
```
I create a __README.md__ file and a __.gitignore__ file. I edit these files and then commit them to Git using ```git add``` and ```git commit```.

```bash
git branch -M main
git remote add origin https://github.com/albanmartel/SkillsExchange.git
git push -u origin main
```

####  Créer un environnement virtuel Python

```bash
python -m venv .venv
```

#### Activating the virtual environment

Open the terminal in your project’s root directory:

* **Windows (Command Prompt / `cmd.exe`)** :
```cmd
.venv\Scripts\activate.bat
```


* **Windows (PowerShell)** :
```powershell
.venv\Scripts\Activate.ps1
```

*(If a script execution error occurs, first run `Set-ExecutionPolicy Unrestricted -Scope Process` in your session).*
* **Linux / macOS** :
```bash
source .venv/bin/activate
```

*`(.venv)` appears at the start of the command line when the virtual environment is activated.*

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


__Note:__
1. I used a ‘requirements.txt’ file from a previous Git repository.
2. __tzdata__ was installed to avoid errors relating to the French date and time format

#### 5. Installing Django from the dependencies file

You must first have installed the virtual environment and activated it.

```bash
python -m pip install -r requirements.txt
```

### Creating the django basic site structure

```cmd
mkdir skillsexchange
django-admin startproject site_config skillsexchange
```

__Note:__
At this stage, the admin site is __site_config__ and the application site is __skills_exchange__

### Creating the __SkillsExchange__ application

```cmd
cd skillsexchange
python manage.py startapp skills_exchange
```

## Architecture

Project structure :
```powershell
────SkillsExchange
    └───.git
    └─── skillsexchange
        └─── site_config
        └─── skills_exchange
        └─── manage.py
    └───.venv
    └───.gitignore
    └─── README.md
    └─── requirements.txt
```

### Les réglages __site_config\settings.py__

Open the Python file __skills_exchange\apps.py__.
Take a look at the code. In my case, I have the following:
```python
from django.apps import AppConfig


class SkillsExchangeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skills_exchange'
```

I use this to write the following on the first line of the __INSTALLED_APPS__ table in the __site_config\settings.py__ file:

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

```python
ALLOWED_HOSTS = [
    '127.0.0.1',
]

In the TEMPLATES table, edit the following DIRS row as follows
```python
‘DIRS’: [BASE_DIR / ‘templates’],
```

Edit the ```LANGUAGE_CODE``` and ```TIME_ZONE``` variables so that they look like this:
```python
LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Europe/Paris'
```
Go to the line ```STATIC_URL = “static/”```. The code should look like this after you’ve made the changes:

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

In the __manage.py__ file, run the following commands
```PowerShell
mkdir templates
mkdir static
cd static
mkdir images
mkdir js
mkdir css
```

This allows parent templates to utilise JavaScript and CSS scripts.


### Launch of the development site

```python
python manage.py runserver
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
