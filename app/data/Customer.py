from dataclasses import dataclass

from data.Entity import Entity
from data.constants import DB_Type

@dataclass 
class Customer(Entity):
    firstname: str = ""
    lastname: str = ""
    _DB_TYPE: str = DB_Type.CUSTOMER.value


