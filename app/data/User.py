from dataclasses import dataclass
from data.Entity import Entity

from data.constants import DB_Type

@dataclass 
class User(Entity):
    password: str = ""
    token: str = ""
    DB_TYPE: str = DB_Type.USER.value

   

