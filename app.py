import datetime
import json
from flask import Flask
from markupsafe import escape
import requests
from flask import render_template

app = Flask(__name__)
@app.route('/')
def index():
    s = requests.get('http://localhost:8080/rest/customer/get/all')
    print(s.json())
    return customer()

@app.route('/customer', methods=['GET','POST', 'PUT', 'DELETE'])
def customer():
    if requests.methods == "GET": 
        
        s = requests.get('http://localhost:8080/rest/customer/get/all')
        print(s.json())
        return s.json()   

@app.route('/customer/get/<id>/')
def get_customer_with_id(id):
    s = requests.get(f'http://localhost:8080/rest/customer/get/{id}')
    print(s.status_code)

    if (s.status_code == 200): #s.ok would theoretically work but 204 (no content) results in errors again that would need manual fixing.
        return s.json()
    else:
        return f"Error occured! Code: {s.status_code}; Reason: {s.reason}"
    #return s.json()    

@app.route("/test")
def test():
    return render_template("base.html")

@app.context_processor
def context_processors():
    def date_now(format="%d.m.%Y %H:%M:%S"):
        """ returns the formated datetime """
        return datetime.datetime.now().strftime(format)

    def print_customers():
        cList = customer()
        str = """<table>
            <tr><th>LAST</th><th>FIRST</th><th>ID</th></tr>"""
        for c in cList:
            str += f"<tr><td>{c['lastname']}</td><td>{c['firstname']}</td><td>{c['id']}</td><tr>"
        str += "</table>"
        return str



    return dict(date_now=date_now, print_customers=print_customers)


if __name__ == '__main__':
    app.run(debug=True)