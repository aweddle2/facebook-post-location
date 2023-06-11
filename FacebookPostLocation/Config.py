import configparser
import os

class Config:
    def __init__(self): 
        self.Config = configparser.ConfigParser()
        self.Config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))