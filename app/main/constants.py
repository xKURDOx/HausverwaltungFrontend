#these variables are used for the call to the backend. it's still confusing that sometimes we use singular and sometimes plural... 
from enum import Enum


class DB_Type (Enum):
    CUSTOMER = "customer"
    USER = "user"
    READING = "reading"

BASE_URL = "http://localhost:8080/"