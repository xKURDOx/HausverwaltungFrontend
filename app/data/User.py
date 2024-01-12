from dataclasses import dataclass
from data.Entity import Entity

from data.constants import DB_Type

@dataclass 
class User(Entity):
    firstname: str = ""
    lastname: str = ""
    password: str = ""
    token: str = ""
    _DB_TYPE: str = DB_Type.USER.value

   

