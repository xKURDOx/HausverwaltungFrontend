import datetime
import logging
from urllib import response
from flask import Flask, abort, request
import requests
from flask import render_template
from main.Readings import Readings

from main.Entity import Entity
from main.Customer import Customer
from main.User import User
from main.constants import BASE_URL


##VARS
app = Flask(__name__)

##METHODS

def get_readings_json():
    try:
        s = requests.get(BASE_URL + 'rest/reading/get/all')
        print(f"GET_READINGS - JSON: \n {s.json()}")
        return s.json() 
    except requests.exceptions.ConnectionError as e:
        #logging.critical(e, exc_info=True) 
        return None

def get_customers_json():
    """this just calls our rest-api and returns the json
        returns a list in the scheme of [json | None, (debug_message, debug_code, debug_headers)]
    """
    try: 
        s = requests.get(BASE_URL + 'rest/customer/get/all')
        print(f"GET_CUSTOMERS - JSON: \n {s.json()}")
        return [s.json(), ["Fetched customers.", s.status_code, s.headers.items()]]
    except requests.exceptions.ConnectionError as e:
        #logging.critical(e, exc_info=True) 
        return [None, ["Fetched customers.", "500", []]]


#This doesnt have to be a route. @app.route('/customer/get/<id>/')
#returns a list. Scheme: [json | None, (debug_message, debug_code, debug_headers)]
def get_customer_with_id(id):
    try: 
        response = requests.get(f'{BASE_URL}rest/customer/get/{id}')
        print(response.status_code)

        if (response.status_code == 200): #s.ok would theoretically work but 204 (no content) results in errors again that would need manual fixing.
            return [response.json()[0], (response.content, response.status_code, response.headers.items())] #this only should hold one element so we can delte the []-brackets 
        else:
            return [response.json()[0], (str(response.content), response.status_code, response.headers.items())]
    except requests.exceptions.ConnectionError as e:
        logging.critical(e, exc_info=True) 
        return [None, ("Fetched customer via ID.", "500", [])]
    #return s.json()   

def get_users_json():
    try: 
        s = requests.get(BASE_URL + 'rest/users/get/all')
        print(f"GET_USERS - JSON: \n {s.json()}")
        return s.json() 
    except requests.exceptions.ConnectionError as e:
        #logging.critical(e, exc_info=True) 
        return None

def delete(o: Entity):
    try:
        response = requests.get(f"{BASE_URL}rest/{o.get_db_type()}/delete/{o.id}")
        return [o, [response.content, response.status_code, response.headers.items()]]
    except requests.exceptions.ConnectionError as e:
        return [o, ["The server is unreachable.", 503, []]]

def edit(o: Entity):
    try:
        response = requests.put(f"{BASE_URL}rest/{o.get_db_type()}/edit", json=o.toDICT())
        return [o, [response.content, response.status_code, response.headers.items()]]

    except requests.exceptions.ConnectionError as e:
        return [o, ["The server is unreachable.", 503, []]]


def create(o: Entity):
    """
    Returns a list [entity, [repsonse-content, resp-code, resp-headers]]
    if the response shows no errors, the object shjould be created.
    """
    try:
        response = requests.post(f"{BASE_URL}rest/{o.get_db_type()}/create", json=o.toDICT())
        return [o, [response.content, response.status_code, response.headers.items()]]
    except requests.exceptions.ConnectionError as e:
        return [o, ["The server is unreachable.", 503, []]]


##ROUTES
@app.route('/')
def index():
    return render_template("Home.html")

@app.route("/readings")
def route_readings():

    return render_template("Readings.html", readings_list=get_readings_json())

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
def route_customer(*args):
    """
    routes to the customer page. Optionally takes a list of debug-messages [] in the first optional argument.
    if there are args, the debug-message of the fetch-all gets appended to that; otherwise just the fetch-all message gets returned as debug-message.
    """
    print("Args")
    print(args)
    if len(args) > 0:
        print(args[0])
    ###TODO: if this fails; redirect to error page instead of... well. running into an error.
    ###is now done by customers.html itself
    cList, debug_info = get_customers_json()
    print("DEBUG-INFO: ")
    print(debug_info)
    if len(args) > 0:
        args[0].append(debug_info)
        print(args[0])

    #this one is really ugly. Header is never used, either.
    #could be simplified by adding the other way around (no double-check on len(args))
    return render_template("Customers.html", customer_list=cList, debug_info=args[0] if len(args) > 0 else [debug_info])


    
@app.route('/customers/create', methods=['POST'])
def route_customer_create():
    #this is the actual api-call. DELETE has to be post for some browser-related-reasons i guess. It COULD be a normal method/route with a variable but yeaaah. #TODO.
    print("CREATE-REQ-FORM: " + str(request.form))
    c = Customer(firstname=request.form["firstname"], lastname=request.form["lastname"], id=-1)
    c, resp_val = create(c)
    
    return route_customer([resp_val])
 

@app.route('/customers/edit/', methods=['POST'])
def route_customer_edit():
    print("EDIT-REQ: " + str(request.form))

    c = Customer(firstname=request.form["firstname"], lastname=request.form["lastname"], id=request.form["id"])
    c, resp_val = edit(c)

    return route_customer([resp_val])


@app.route('/customers/delete/<id>')
def route_customer_delete(id):
    c, resp_val = delete(Customer(firstname="", lastname="", id=id))
    #delete_customer(id)
    return route_customer([resp_val])

@app.route('/users')
def route_users():
    return render_template("Users.html", users_list = get_users_json())

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

    @DeprecationWarning
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
    
    @DeprecationWarning
    def print_customers():
        cList = get_customers_json()
        str = """<table id='customer_table' class='object_table'>
            <tr><th>LAST</th><th>FIRST</th><th>ID</th><th>action</th></tr>"""
        for c in cList:
            str += f"<tr><td>{c['lastname']}</td><td>{c['firstname']}</td><td>{c['id']}</td><td><a href='/customers/delete/{c['id']}'>[delete]</a></td></tr>"
        str += "</table>"
        return str

    @DeprecationWarning
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