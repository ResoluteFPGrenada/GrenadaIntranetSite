#Setup#
new-item -Path "$PSScriptRoot\log.txt" -type File -force
write-warning "creating log file"

# Create local git repo #
git init

# Check if Python is installed #
try{
    python --version
}catch{
    write-error "Please install python 3.6 or higher, before running this setup tool. Otherwise make sure python in setup in path"
    add-content "$PSScriptRoot\log.txt" -Value "Python not installed or path could not be found. Please install Python 3.6 or later." -force
    read-host "Press any button to stop program."
    break
}

# setup connection to github repo #
git remote add origin https://github.com/ResolutefpGrenada/GrenadaIntranetSite.git


# pull down repo #

git pull origin master


# check if virtualenv is installed #

try{
    virtualenv --version
}catch{
    pip install virtualenv 
    write-warning "installing virtualenv on local machine."
    add-content "$PSScriptRoot\log.txt" -Value "Installed virtualenv." -force
    read-host "Press any button to continue"
}


# setup virtual environment #

$TP = test-path .\venv
if($TP -ne $true){
    virtualenv venv
}

venv\scripts\activate


# run requirments.txt to install denpendencies #

pip install -r requirements.txt


# Ask user to create scheduled task to run python manage.py prod in directory folder. #
write-host ""
write-warning "Please create scheduled task to run python manage.py prod in project directory."
read-host "Press any button to continue"


# Deactivate venv and show setup was successful. # 
venv\scripts\deactivate.bat
write-warning "Setup of site was successful."
add-content "$PSScriptRoot\log.txt" -Value "Setup was completed successfully." -force
read-host "Press any button to complete this setup."