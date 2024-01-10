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
    s = requests.get(f'http://localhost:8080/rest/customer/get/{id}')
    print(s.status_code)

    if (s.status_code == 200): #s.ok would theoretically work but 204 (no content) results in errors again that would need manual fixing.
        return (1, s.json())
    else:
        return (0, f"Error occured! Code: {s.status_code}; Reason: {s.reason}")
    #return s.json()   

@app.route('/customer', methods=['GET','POST', 'PUT'])
def route_customer():
    print(request.method)
    if request.method == "GET": 
        return render_template("Customer.html")
    
    elif request.method == "POST":
        #this is the actual api-call. DELETE has to be post for some browser-related-reasons i guess. It COULD be a normal method/route with a variable but yeaaah. #TODO.
        print(request.form)
        print(request.form["post"])
        if (request.form["post"] == "create"):
            response = requests.post(base_url + "rest/customer/create", data={"firstname": request.form["firstname"], "lastname": request.form["lastname"]})
        elif (request.form["post"] == "delete"):
            response = requests.get(f"http://localhost:8080/rest/customer/delete/{request.form['id']}")
        else:
            print("thefuck?")
        return render_template("Customer.html")


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



    return dict(date_now=date_now, print_customers=print_customers)


if __name__ == '__main__':
    app.run(debug=True)