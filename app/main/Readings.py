from dataclasses import dataclass
from main.Customer import Customer
from main.Entity import Entity

from main.constants import DB_Type

@dataclass 
class Readings(Entity):
    comment: str = ""
    customer: Customer | None = None
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

        if (self.customer is not None):
            v["customer"] = self.customer.toDICT() #ithinkthiscouldbebetter
            print(v)
        return v

   

