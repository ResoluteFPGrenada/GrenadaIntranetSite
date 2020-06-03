# GrenadaIntranetSite
A intranet site used to centralize data and applications in one local location at Resolute Forest Products Grenada office.

# Setup
1. download setup.ps1 file from this repo.

2. download and install Python 3.6 or later on the machine where you want the site to run.

3. move setup.ps1 file to a directory where the site should be built.

4. open command prompt as administrator and cd to project folder

5. run powershell .\setup.ps1 executionpolicy bypass

6. add databases from backup directory to PROJECTFOLDER\WebApp\databases

7. run venv\scripts\activate

8. run python manage.py runserver prod to run server in production environment. otherwise python manage.py runserver dev in testing/dev environment.
