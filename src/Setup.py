import configparser
import os
import sys

cfg = configparser.ConfigParser()
exepath = os.path.dirname(sys.path[0])
print(exepath + "\src\static\config.cfg")
cfg.read(exepath + "\src\static\config.cfg")

class Settings(object):
    def __init__(self) -> None:
        pass

    def database(self):
        out = cfg.get("config","Data_Mode")
        if out == "True":
            reselt = {
                    "host": "frp-eye.top",
                    "port": 50334,
                    "user": "root",
                    "passwd": "root",
                    "db": "flaskdata"
                    }
        else:
            reselt = {
                    "host": "127.0.0.1",
                    "port": 3306,
                    "user": "root",
                    "passwd": "root",
                    "db": "flaskdata"
                    }
        return reselt

    def bg_path(self):
        out = cfg.get("config","Background_path")
        return out
    
    def keep_login(self):
        out = cfg.get("config","keep_login")
        if out == "True":
            reselt = cfg.get("Settings","acc")
        else:
            reselt = None
        return reselt

    def cfg_in(self, section, option, value):
        value = str(value)
        cfg.set(section,option,value)
        cfg.write(open('config.cfg', "w"))

    def dev_mode(self):
        out = cfg.get('config',"Dev_Mode")
        print(out)
        return out

    def rd(self, section, option):
        out = cfg.get(section,option)
        return out
    