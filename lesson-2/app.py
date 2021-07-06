from faker import Faker
from flask import Flask
import requests
import json
import csv

app = Flask(__name__)
fake = Faker()

@app.route('/requirements/')
def f():
    file = open("fedorchuk-homework/lesson-2/requirements.txt", "r")
    data = file.read()
    return(data)

@app.route('/generate-users/<int:num>')
def create_names_list(num):
    names = []
    for i in range(0,num):
        names.append(fake.first_name() + '  ' + fake.email())
    return str(names)

@app.route('/mean/')
def mean():
    height_list = []
    weight_list = []
    with open('fedorchuk-homework/lesson-2/hw.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            height = row[' "Height(Inches)"']
            weight = row[' "Weight(Pounds)"']
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




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)