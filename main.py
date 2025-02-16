import json
import logging
from flask import Flask, request, render_template
from markupsafe import escape
from kd_tree import KdTree
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
        nodes = kd_tree.nearest_neighbour(position.coordinates, 100)
        nearest = [node.data for node in nodes]
        distances = [position.distance(system) for system in nearest]
        return render_template('closest.html', position=position, rows=zip(nearest, distances)) 
    else:
        return render_template('closest.html')

def load_systems(filename):
    logging.info('Reading systems data')
    systems = []
    coords = []
    with open(filename, 'r') as file:
        systems_json = json.load(file)
        systems = [System(row['name'], sectors=sectors) for row in systems_json]
        coords = [system.coordinates for system in systems]
        logging.info('Number of systems read: %d', len(systems))
    return systems, coords

logging.basicConfig(level=logging.INFO)
sectors = Sectors()
systems, coordinates = load_systems('resources/systemsWithoutCoordinates.json')

logging.info('Creating tree')
kd_tree = KdTree(coordinates, systems)
logging.info('Tree created')
