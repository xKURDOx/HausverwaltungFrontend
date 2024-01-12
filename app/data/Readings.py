from dataclasses import dataclass
from data.Customer import Customer
from data.Entity import Entity

from data.constants import DB_Type

@dataclass 
class Readings(Entity):
    comment: str = ""
    customer: Customer = None
    dateofreading: int = 0
    kindofmeter: str = ""
    metercount: int = 0
    meterid: str = ""
    substitute = 0
    _DB_TYPE: str = DB_Type.READING.value

    def toDICT(self):
        v = vars(self)
        print(v)
        v.pop("_DB_TYPE") #we dont want this in our actual object, right.

        v["customer"] = self.customer.toDICT() #ithinkthiscouldbebetter
        print(v)
        return v

   

