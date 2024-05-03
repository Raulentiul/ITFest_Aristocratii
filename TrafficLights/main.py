from UserApp import UserApp
from AdminApp import MapManager
from simulation import MapApp

if __name__ == '__main__':
    input = (input("Admin True or False: "))
    if input == "y":
        app_instance = MapManager()
        app_instance.run()
    else:
        app_instance = MapApp()
        app_instance.run()

