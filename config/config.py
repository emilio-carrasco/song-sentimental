
import os
import platform
from sqlalchemy import create_engine
from dotenv import load_dotenv

plataforma=platform.system()
if plataforma == 'Linux':
    print(" - - - Levantar el servidor requiere de contraseña")    
    os.system("sudo /etc/init.d/mysql start") 
elif plataforma == 'OS X':
    os.system("sudo /usr/local/mysql/support-files/mysql.server start")
elif plataforma == 'Windows':
    os.system("/etc/init.d/mysql start")
else:
    pass
    #2do: levantar error de O

load_dotenv()
passw = os.getenv("pass_sql")
dbName = os.getenv("db")

print(" - - - Base de datos: ", dbName)

connectionData=f"mysql+pymysql://root:{passw}@localhost/{dbName}"
engine = create_engine(connectionData)
