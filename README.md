# DreamApp

### About the Dream App:
Built as part of the [Udacity's Full Stack Nanodegree](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/262a84d7-86dc-487d-98f9-648aa7ca5a0f/concepts/079be127-2d22-4c62-91a8-aa031e760eb0) this is a RESTful web application utilizing the Flask framework which accesses a SQL database that populates dream categories and their items. OAuth2 provides authentication for further CRUD functionality on the application. 

### Getting Set Up:

### System Requirements:
1. [Python3](https://www.python.org/)
2. [Vagrant](https://www.vagrantup.com/)
  * This is the software that configures the Virtual machine
3. [Virtual Box](https://www.virtualbox.org/)
  * This is the software that actually runs the virtual machine
  * Allows you to share files between the VM filesystem and your host computer
  * Install the platform package for your OS
  * Don't launch after installing, Vagrant handles this for you
 4. [Udacity Vagrant Machine](https://github.com/udacity/fullstack-nanodegree-vm)

### Project Setup:
1. Install Python3 
2. Install Vagrant
3. Install Virtual Box
4. Download or clone the Udacity Vagrant Machine repository and place it in the vagrant directory

### Launch the VM:
1. Inside the Vagrant directory downloaded from the full-stack-nanodegree-vm run this command in your terminal
   `vagrant up`
2. Log in to the VM 
   `vagrant ssh`
3. Change directory to the files and look around
   `cd /vagrant' 'ls' `
   
### Set Up the Database:
1. Load the data in the local database
   `python database_setup.py`
2. Populate the database
   `python dreamFiles.py `

### Set up Google Login:
1. Log in to [Google Dev Console](https://console.developers.google.com/)
2. Go to Credentials
3. Select Create Crendentials > OAuth Client ID
4. Select Web Application
5. Enter name 'Dream Catalog'
6. Under 'Authorized Javascript Origins add' `http://localhost:5000/`
7. Authorized redirect URIs = 'http://localhost:5000/login' && 'http://localhost:5000/gconnect'
8. Click create client ID
9. Download JSON and save it as "client_secret.json" in the root directory (replace the existing)
10. In main.html replace the line "data-clientid="#####.apps.googleusercontent.com" so that it uses your Client ID from the web applciation.

### Set up Facebook Login:
1. Log in to [Facebook Dev Console](https://developers.facebook.com/)
2. Go to Dashboard
3. Click `Add Product` on the bottom left of the page
4. Add `facebook login`
5. Click Client OAuth
6. Add `http://localhost:5000/` to the Valid OAuth redirect URIs section
7. Replace app_id and app_secret in fb_client_secrets.json file

### Run the Application:
1. From the vagrant direcotry inside the VM
   `python project.py`
2. Navigate to [http://localhost:5000/](http://localhost:5000/) in your browser

### Exiting the VM
To exit type `control + D`