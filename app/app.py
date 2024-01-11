import datetime
from enum import Enum
import json
from flask import Flask, request
from markupsafe import escape
import requests
from flask import render_template

app = Flask(__name__)

#these variables are used for the call to the backend. it's still confusing that sometimes we use singular and sometimes plural... 
class TYPE (Enum):
    CUSTOMER = "customer"
    USER = "user"

base_url = "http://localhost:8080/"

@app.route('/')
def index():
    return render_template("Home.html")

#this just calls our rest-api and returns the json
def get_customers():
    s = requests.get(base_url + 'rest/customer/get/all')
    print(f"GET_CUSTOMERS - JSON: \n {s.json}")
    return s.json() 

#This doesnt have to be a route. @app.route('/customer/get/<id>/')
#returns a tuplle. either (0, customer) or (1, error-message) idk why. I liked error-codes when i wrote this. 
def get_customer_with_id(id):
    response = requests.get(f'{base_url}rest/customer/get/{id}')
    print(response.status_code)

    if (response.status_code == 200): #s.ok would theoretically work but 204 (no content) results in errors again that would need manual fixing.
        return (1, response.json())
    else:
        return (0, f"Error occured! Code: {response.status_code}; Reason: {response.reason}")
    #return s.json()   

def get_users():
    response = requests.get(base_url + "rest/user/get/all")
    if (response.status_code == 200):
        print(f"GET_USERS - JSON: \n {response.json()}")
        return (1, response.json())
    else:
        return (0, f"Error occured! Code: {response.status_code}; Reason: {response.reason}")

def delete(type: TYPE, id):
    s = f"{base_url}rest/{type}/delete/{id}"
    print(s)
    response = requests.get(s)
    print("deleted.")
    print(response.raw)

def edit(type: str, data):
    print(data)
    s = f"{base_url}rest/{type}/edit"
    print(s)
    response = requests.put(s, json=data)
    print(response.status_code)
    print("edited.")
    print(response.content)

def create(type: str, data):
    print(data)
    #print("0:" + request.form[0])
    #print("type:" +  request.form["type"])
    response = requests.post(f"{base_url}rest/{type}/create", json=data)
    print(response.content)

#def delete_customer(id):
#    response = requests.get(f"http://localhost:8080/rest/customer/delete/{id}")

#def delete_user(id):
#    response=requests.get(f"http://localhost:8080/rest/user/delete/{id}")


@app.route('/customers', methods=['GET','POST'])
def route_customer():
    return render_template("Customers.html")

@app.route('/customers/create', methods=['POST'])
def route_customer_create():
    #this is the actual api-call. DELETE has to be post for some browser-related-reasons i guess. It COULD be a normal method/route with a variable but yeaaah. #TODO.
    print("CREATE-REQ-FORM: " + str(request.form))
    #print("0:" + request.form[0])
    #print("type:" +  request.form["type"])
    j = {"firstname": request.form["firstname"], "lastname": request.form["lastname"], "id": -1}
    create(TYPE.CUSTOMER.value, j)
        
    return render_template("Customers.html")

@app.route('/customers/edit/', methods=['POST'])
def route_customer_edit():
    print("EDIT-REQ: " + str(request.form))

    json={"firstname": request.form["firstname"], "lastname": request.form["lastname"], "id": request.form["id"]}
    edit(TYPE.CUSTOMER.value, json)

    return render_template("Customers.html")

@app.route('/customers/delete/<id>')
def route_customer_delete(id):
    delete(TYPE.CUSTOMER.value, id)
    #delete_customer(id)
    return render_template("Customers.html")

@app.route('/users')
def route_users():
    return render_template("Users.html")

@app.route('/users/create', methods=["POST"])
def route_users_create():
    print("CREATE-REQ-FORM: " + str(request.form))
    #print("0:" + request.form[0])
    #print("type:" +  request.form["type"])
    j = {"firstname": request.form["firstname"], "lastname": request.form["lastname"], "password": request.form["password"], "token": request.form["token"], "id": -1}
    create(TYPE.USER.value, j)
    return render_template("Users.html")

@app.route('/users/edit', methods=['POST'])
def route_users_edit():
    print("EDIT-REQ: " + str(request.form))
    #TODO: why do we need json here but data works fine for the create-endpoint? makes sense but also doesn't.
    
    j = f'''{{ "firstname": "{request.form["firstname"]}", "lastname": "{request.form["lastname"]}", "password": "{request.form["password"]}",
        "token": "{request.form["token"]}", "id": "{request.form["id"]}" }}'''
    edit(TYPE.USER.value, json.loads(j))
    return render_template("Users.html")

@app.route('/users/delete/<id>')
def route_user_delete(id):
    delete(TYPE.USER.value, id)
    #delete_user(id)
    return render_template("Users.html")


@app.context_processor
def context_processors():
    def date_now(format="%d.%m.%Y %H:%M:%S"):
        """ returns the formated datetime """
        return datetime.datetime.now().strftime(format)

    def print_customers():
        cList = get_customers()
        str = """<table id='customer_table' class='object_table'>
            <tr><th>LAST</th><th>FIRST</th><th>ID</th><th>action</th></tr>"""
        for c in cList:
            str += f"<tr><td>{c['lastname']}</td><td>{c['firstname']}</td><td>{c['id']}</td><td><a href='/customers/delete/{c['id']}'>[delete]</a></td></tr>"
        str += "</table>"
        return str

    def print_users():
        getUsers = get_users()
        if (getUsers[0] == 0): 
            return """<table id='user_table', class='object_table'>
            <tr><th>LAST</th><th>FIRST</th><th>ID</th></tr>
            <tr><td></td><td></td><td></td><tr>"""
        else:
            uList = getUsers[1]
            str = """<table id='user_table', class='object_table'>
                <tr><th>LAST</th><th>FIRST</th><th>PASS</th><th>TOKEN</th><th>ID</th><th>action</th></tr>"""
            for u in uList:
                str += f"""<tr><td>{u['lastname']}</td><td>{u['firstname']}</td><td>{u['password']}</td><td>{u['token']}</td><td>{u['id']}</td>
                <td><a href='/users/delete/{u['id']}'>[x]</a></td></tr>"""
            str += "</table>"
            return str

    return dict(date_now=date_now, print_customers=print_customers, print_users=print_users)


if __name__ == '__main__':
    app.run(debug=True)