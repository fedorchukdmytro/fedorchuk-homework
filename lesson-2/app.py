from faker import Faker
from flask import Flask
import requests
import csv
from flask_sqlalchemy import SQLAlchemy
from flask import request

app = Flask(__name__)
fake = Faker()


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homework3.db'
db = SQLAlchemy(app)


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    Transaction_date = db.Column(db.String, unique=False, nullable=False)
    Product = db.Column(db.String(80), unique=False, nullable=False)
    Price = db.Column(db.Integer, unique=False, nullable=False)
    Payment_type = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f'[{self.Transaction_date}, {self.Product}, {self.Price}]'                         

db.create_all()      


@app.route('//')
def indexPage():
    if len(Sales.query.all()) !=0:
        return "<h1>DATABASE ALREADY EXISTS<h1/>"
    else:
        with open ('homework3sales.csv', 'r') as csvfile:
                tbl_reader = csv.reader(csvfile, delimiter=';')
                next(tbl_reader)
                for row in tbl_reader:
                    ins = Sales(Transaction_date=row[0], Product=row[1], Price=row[2], Payment_type=row[3])
                    db.session.add(ins)
                db.session.commit()
        return "<h1>DATABASE WAS JUST CREATED<h1/>"

@app.route('/requirements/')
def f():
    file = open("requirements.txt","r")
    data = file.read()
    output = ''.join([f" {line} ;<br/>" for line in data.split()])
    return str(output)

@app.route('/generate-users/<int:num>')
def create_names_list(num): 
    output = ''.join([f" {fake.first_name()} {fake.email()};<br/>" for i in range(0,num)])
    return str(output)

@app.route('/mean/')
def mean():
    height_list = []
    weight_list = []
    with open('hw.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            height_list.append(float(row[' "Height(Inches)"']))
            weight_list.append(float(row[' "Weight(Pounds)"']))
            averageHeight = sum(height_list) / len(height_list)
            averageWeight = sum(weight_list) / len(weight_list)
            result = (' ave height is  ' + str(averageHeight) +
                      ' ave weight is  ' + str(averageWeight))
    return result                  

@app.route('/space/')
def space():
    r = requests.get('http://api.open-notify.org/astros.json')
    return(r.json())


@app.route("/summary/")
def summary():
    sales = Sales.query.all()
    summary_dict = {}
    for event in sales:
        date = event.Transaction_date.split()[0]
        if not date in summary_dict.keys():
            summary_dict[date] = float(event.Price)
        else:
            transitional_sum = summary_dict.get(date, 0.0)
            summary_dict[date] = transitional_sum + float(event.Price)
    
    output = ''.join([ f"{key} : {value}; <br/>" for key, value in summary_dict.items()])
    return str(output)    

@app.route('/sales/')
def query():
    
    args = request.args
    argsdict ={}
    for key, value in args.items():
        argsdict[key.capitalize()] = value.capitalize()
    query = Sales.query.filter_by(**argsdict).all()
    output = ''.join([ f" {x.Product},{x.Payment_type},{x.Price},{x.Transaction_date.split()[0]}<br/>" for x in query])
    return str(output)



if __name__ == '__main__':
    app.run()
    