# Createfolio
![example workflow](https://github.com/NikOneZ1/createfolio/actions/workflows/django.yml/badge.svg)

Create your own portfolio. Add information about yourself, your best projects and share it with other people.
### [Demo](https://createfolio.herokuapp.com/portfolio/nikone)
![a](https://user-images.githubusercontent.com/48495591/137489586-8f98b747-606a-469c-82af-f6ff607063c7.png)
# How to install 
Install all dependencies
```
pip install -r requirements.txt
```
Set the settings in settings.py to run the project
```
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': "CLOUD_NAME of cloudinary storage",
    'API_KEY': "API_KEY of cloudinary storage",
    'API_SECRET': "API_SECRET of cloudinary storage"
}
EMAIL_HOST_USER = "Addres of the mail from which messages will be sent"
EMAIL_HOST_PASSWORD = "Password of the mail from which messages will be sent"
```