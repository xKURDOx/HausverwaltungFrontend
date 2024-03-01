from dataclasses import dataclass
from main.Entity import Entity

from main.constants import DB_Type

@dataclass 
class User(Entity):
    firstname: str = ""
    lastname: str = ""
    password: str = ""
    token: str = ""
    _DB_TYPE: str = DB_Type.USER.value

   

