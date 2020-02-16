import csv
import heapq
from flask import Flask, render_template, g
from markupsafe import escape
from systems import System, Sectors

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/form')
def form():
    return '''
        <form method="get">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/system/<name>')
def get_coords(name):
    system = System(name, sectors=sectors)
    return render_template('system.html', system=system)

@app.route('/closest/<name>')
def get_closest(name):
    position = System(name)
    head = heapq.nsmallest(100, systems, key=lambda a : a.distance(position))
    distances = [round(position.distance(system), 2) for system in head]

    return render_template('closest.html', position=position, rows=zip(head, distances)) 


def load_systems(filename):
    print('Reading systems data')
    systems = []
    with open(filename, newline='') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        begin, end = 0, 30000
        for i, row in enumerate(csvreader):
            if begin <= i < end:
                systems.append(System(row[1], sectors=sectors))
            if i == end:
                break
        print('Number of systems:', i)
    return systems

sectors = Sectors()
systems = load_systems('resources/systems-without-coordinates.csv')
