import os

class Utils:
    @staticmethod
    def load_config(filename='config.txt'):
        try:
            with open(filename, 'r') as config_file:
                return config_file.read().strip()
        except FileNotFoundError:
            return "C:\\Path\\To\\AutoIt3.exe"

    @staticmethod
    def save_config(path, filename='config.txt'):
        with open(filename, 'w') as config_file:
            config_file.write(path)
