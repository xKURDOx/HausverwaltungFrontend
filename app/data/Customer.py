from dataclasses import dataclass

from data.Entity import Entity
from data.constants import DB_Type

@dataclass 
class Customer(Entity):
    DB_TYPE: str = DB_Type.CUSTOMER.value


