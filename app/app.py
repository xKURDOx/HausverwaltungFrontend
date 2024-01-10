import datetime
import json
from flask import Flask, request
from markupsafe import escape
import requests
from flask import render_template

app = Flask(__name__)
base_url = "http://localhost:8080/"

@app.route('/')
def index():
    '''s = requests.get('http://localhost:8080/rest/customer/get/all')
    print(s.json())
    return customer()'''
    return render_template("Home.html")

#this just calls our rest-api and returns the json
def get_customers():
    s = requests.get(base_url + 'rest/customer/get/all')
    print(f"GET_CUSTOMERS - JSON: \n {s.json}")
    return s.json() 

#This doesnt have to be a route. @app.route('/customer/get/<id>/')
#returns a tuplle. either (0, customer) or (1, error-message) idk why. I liked error-codes when i wrote this. 
def get_customer_with_id(id):
    response = requests.get(f'http://localhost:8080/rest/customer/get/{id}')
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

@app.route('/customers', methods=['GET','POST', 'PUT'])
def route_customer():
    print(request.method)
    if request.method == "GET": 
        return render_template("Customers.html")
    
    elif request.method == "POST":
        #this is the actual api-call. DELETE has to be post for some browser-related-reasons i guess. It COULD be a normal method/route with a variable but yeaaah. #TODO.
        print(request.form)
        print(request.form["type"])
        if (request.form["type"] == "create"):
            response = requests.post(base_url + "rest/customer/create", data={"firstname": request.form["firstname"], "lastname": request.form["lastname"]})
        elif (request.form["type"] == "delete"):
            response = requests.get(f"http://localhost:8080/rest/customer/delete/{request.form['id']}")
        elif (request.form["type"] == "edit"):
            response = requests.get(f"http://localhost:8080/rest/customer/edit/{request.form['id']}")
        else:
            print("thefuck?")
        return render_template("Customers.html")

@app.route('/users')
def route_users():
    print(request.method)
    if request.method == "GET": 
        return render_template("Users.html")


@app.context_processor
def context_processors():
    def date_now(format="%d.%m.%Y %H:%M:%S"):
        """ returns the formated datetime """
        return datetime.datetime.now().strftime(format)

    def print_customers():
        cList = get_customers()
        str = """<table id='customer_table'>
            <tr><th>LAST</th><th>FIRST</th><th>ID</th></tr>"""
        for c in cList:
            str += f"<tr><td>{c['lastname']}</td><td>{c['firstname']}</td><td>{c['id']}</td><tr>"
        str += "</table>"
        return str

    def print_users():
        getUsers = get_users()
        if (getUsers[0] == 0): 
            return """<table id='user_table'>
            <tr><th>LAST</th><th>FIRST</th><th>ID</th></tr>
            <tr><td></td><td></td><td></td><tr>"""
        else:
            uList = getUsers[1]
            str = """<table id='user_table'>
                <tr><th>LAST</th><th>FIRST</th><th>ID</th></tr>"""
            for u in uList:
                str += f"<tr><td>{u['lastname']}</td><td>{u['firstname']}</td><td>{u['id']}</td><tr>"
            str += "</table>"
            return str



    return dict(date_now=date_now, print_customers=print_customers, print_users=print_users)


if __name__ == '__main__':
    app.run(debug=True)