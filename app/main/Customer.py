from dataclasses import dataclass

from main.Entity import Entity
from main.constants import DB_Type

@dataclass 
class Customer(Entity):
    firstname: str = ""
    lastname: str = ""
    _DB_TYPE: str = DB_Type.CUSTOMER.value


