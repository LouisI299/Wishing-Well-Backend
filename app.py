#Imports
from app import create_app

#Create the app (From init file)
app = create_app()

#Run the app
if __name__ == '__main__':
    app.run()