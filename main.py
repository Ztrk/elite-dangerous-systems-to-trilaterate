import csv
import heapq
import logging
from flask import Flask, request, render_template
from markupsafe import escape
from systems import System, Sectors

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/system')
def get_coords():
    name = request.args.get('system', None)
    if name is not None:
        system = System(name, sectors=sectors)
        return render_template('system.html', system=system)
    else:
        return render_template('system.html')

@app.route('/closest')
def get_closest():
    name = request.args.get('system', None)
    if name is not None:
        position = System(name)
        head = heapq.nsmallest(100, systems, key=lambda a : a.distance2(position))
        distances = [position.distance(system) for system in head]
        return render_template('closest.html', position=position, rows=zip(head, distances)) 
    else:
        return render_template('closest.html')

def load_systems(filename):
    logging.info('Reading systems data')
    systems = []
    with open(filename, newline='') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for i, row in enumerate(csvreader):
            systems.append(System(row[1], sectors=sectors))
        logging.info('Number of systems read: %d', i)
    return systems

logging.basicConfig(level=logging.INFO)
sectors = Sectors()
systems = load_systems('resources/systems-without-coordinates.csv')
