import csv
import heapq
import logging
import random
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

def nth_element_util(list, n, begin, end, keys=None):
    if begin + 1 >= end:
        return
    # partition
    pivot_index = random.randint(begin, end - 1)
    pivot = keys[pivot_index]
    i, j = begin - 1, end
    while i < j:
        i += 1
        j -= 1
        while keys[i] < pivot:
            i += 1
        while keys[j] > pivot:
            j -= 1
        if i < j:
            list[i], list[j] = list[j], list[i]
            keys[i], keys[j] = keys[j], keys[i]
    if n <= j:
        nth_element_util(list, n, begin, j + 1, keys=keys)
    else:
        nth_element_util(list, n, j + 1, end, keys=keys)

def nth_element(list, n, key=None):
    if key is None:
        key = lambda a : a
    keys = [key(e) for e in list]
    nth_element_util(list, n, 0, len(list), keys=keys)

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
