import datetime
from flask import Flask, request
import requests
from flask import render_template
from data.Readings import Readings

from data.Entity import Entity
from data.Customer import Customer
from data.User import User
from data.constants import BASE_URL


##VARS
app = Flask(__name__)

##METHODS

def get_readings_json():
    s = requests.get(BASE_URL + 'rest/reading/get/all')
    print(f"GET_CUSTOMERS - JSON: \n {s.json()}")
    return s.json() 

#this just calls our rest-api and returns the json
def get_customers_json():
    s = requests.get(BASE_URL + 'rest/customer/get/all')
    print(f"GET_CUSTOMERS - JSON: \n {s.json()}")
    return s.json() 

#This doesnt have to be a route. @app.route('/customer/get/<id>/')
#returns a tuple. either (0, customer-json) or (1, error-message) idk why. I liked error-codes when i wrote this. 
def get_customer_with_id(id):
    response = requests.get(f'{BASE_URL}rest/customer/get/{id}')
    print(response.status_code)

    if (response.status_code == 200): #s.ok would theoretically work but 204 (no content) results in errors again that would need manual fixing.
        return (1, response.json()[0]) #this only should hold one element so we can delte the []-brackets 
    else:
        return (0, f"Error occured! Code: {response.status_code}; Reason: {response.reason}")
    #return s.json()   

def get_users_json():
    response = requests.get(BASE_URL + "rest/user/get/all")
    if (response.status_code == 200):
        print(f"GET_USERS - JSON: \n {response.json()}")
        return (1, response.json())
    else:
        return (0, f"Error occured! Code: {response.status_code}; Reason: {response.reason}")

def delete(o: Entity):
    s = f"{BASE_URL}rest/{o.get_db_type()}/delete/{o.id}"
    print(s)
    response = requests.get(s)
    print("RESPONSE:")
    print(response.content)

def edit(o: Entity):
    s = f"{BASE_URL}rest/{o.get_db_type()}/edit"
    response = requests.put(s, json=o.toDICT())

    print(response.status_code)
    print("RESPONSE:")
    print(response.content)

def create(o: Entity):
    print(o.__dict__)
    response = requests.post(f"{BASE_URL}rest/{o.get_db_type()}/create", json=o.toDICT())
    print("RESPONSE:")
    print(response.content)


##ROUTES
@app.route('/')
def index():
    return render_template("Home.html")

@app.route("/readings")
def route_readings():
    return render_template("Readings.html")

@app.route("/readings/create", methods=["POST"])
def route_readings_create():
    print("CREATE-REQ-FORM: " + str(request.form))
    #fake-customer for request:
    c  = Customer(id=request.form["customer"])
    #none is 'better' than -1 i gues butttt does it maaatter?
    r = Readings(id=None, comment=request.form["comment"], customer=c, dateofreading=request.form["dateofreading"], kindofmeter=request.form["kindofmeter"], metercount=request.form["metercount"], meterid=request.form["meterid"])
    print(str(r))
    create(r)
    return render_template("Readings.html")

@app.route("/readings/edit", methods=["POST"])
def route_readings_edit():
    print("EDIT-REQ: " + str((request.form)))
    
    c  = Customer(id=request.form["customer"])
    r = Readings(id=request.form["id"], comment=request.form["comment"], customer=c, dateofreading=request.form["dateofreading"], kindofmeter=request.form["kindofmeter"], metercount=request.form["metercount"], meterid=request.form["meterid"])
    print(str(r))
    edit(r)
    return render_template("Readings.html")

@app.route('/readings/delete/<id>')
def route_reading_delete(id):
    delete(Readings(id=id))
    #delete_customer(id)
    return render_template("Readings.html")

@app.route('/customers')
def route_customer():
    return render_template("Customers.html")

@app.route('/customers/create', methods=['POST'])
def route_customer_create():
    #this is the actual api-call. DELETE has to be post for some browser-related-reasons i guess. It COULD be a normal method/route with a variable but yeaaah. #TODO.
    print("CREATE-REQ-FORM: " + str(request.form))
    c = Customer(firstname=request.form["firstname"], lastname=request.form["lastname"], id=-1)
    create(c)
        
    return render_template("Customers.html")

@app.route('/customers/edit/', methods=['POST'])
def route_customer_edit():
    print("EDIT-REQ: " + str(request.form))

    c = Customer(firstname=request.form["firstname"], lastname=request.form["lastname"], id=request.form["id"])
    edit(c)

    return render_template("Customers.html")

@app.route('/customers/delete/<id>')
def route_customer_delete(id):
    delete(Customer(firstname="", lastname="", id=id))
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
    u = User(firstname=request.form["firstname"], lastname=request.form["lastname"], password=request.form["password"], token=request.form["token"], id=-1)
    create(u)
    return render_template("Users.html")

@app.route('/users/edit', methods=['POST'])
def route_users_edit():
    print("EDIT-REQ: " + str(request.form))
    u = User(firstname=request.form["firstname"], lastname=request.form["lastname"], token=request.form["token"], password=request.form["password"], id=request.form["id"])    
    edit(u)

    return render_template("Users.html")

@app.route('/users/delete/<id>')
def route_user_delete(id):
    delete(User(firstname="", lastname="", id=id))
    #delete_user(id)
    return render_template("Users.html")


@app.context_processor
def context_processors():
    def date_now(format="%d.%m.%Y %H:%M:%S"):
        """ returns the formated datetime """
        return datetime.datetime.now().strftime(format)

    def print_readings():
        cList = get_readings_json()
        str = """<table id='readings_table' class='object_table'>
            <tr><th>COMMENT</th><th>CUSTOMER</th><th>kind</th><th>count</th><th>meter_id</th><th>sub</th><th>date</th><th>id</th><th>action</th></tr>"""
        for r in cList:
            str += f"""<tr><td>{r['comment']}</td><td>{r['customer']['id']}</td><td>{r['kindofmeter']}</td>
            <td>{r['metercount']}</td><td>{r['meterid']}</td><td>{r['substitute']}</td><td>{r['dateofreading']}</td><td>{r['id']}</td>
            <td><a href='/readings/delete/{r['id']}'>[delete]</a></td></tr>"""
        str += "</table>"
        return str
    
    def print_customers():
        cList = get_customers_json()
        str = """<table id='customer_table' class='object_table'>
            <tr><th>LAST</th><th>FIRST</th><th>ID</th><th>action</th></tr>"""
        for c in cList:
            str += f"<tr><td>{c['lastname']}</td><td>{c['firstname']}</td><td>{c['id']}</td><td><a href='/customers/delete/{c['id']}'>[delete]</a></td></tr>"
        str += "</table>"
        return str

    def print_users():
        getUsers = get_users_json()
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

    return dict(date_now=date_now, print_customers=print_customers, print_users=print_users, print_readings=print_readings)


if __name__ == '__main__':
    app.run(debug=True)