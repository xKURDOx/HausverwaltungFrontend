from dataclasses import dataclass
import json

from data.constants import DB_Type

@dataclass 
class User():
    firstname: str
    lastname: str
    password: str
    token: str
    id: int
    DB_TYPE: str = DB_Type.USER.value

    #the request doesnt work using toJSON but dict works fine.
    def toDICT(self):
        v = vars(self)
        v.pop("DB_TYPE")
        return v

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

