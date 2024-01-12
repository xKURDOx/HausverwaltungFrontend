from dataclasses import dataclass
import dataclasses
import json

@dataclass
class Entity():
    firstname: str
    lastname: str
    id: int
    DB_TYPE: str

    @classmethod
    def from_instance(cls, instance):
        return cls(**dataclasses.asdict(instance))

    #the request doesnt work using toJSON (maybe because that still generates a str?) but dict works fine.
    def toDICT(self):
        v = vars(self)
        v.pop("DB_TYPE") #we dont want this in our actual object, right.
        return v

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)