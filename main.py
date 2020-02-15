import csv
from flask import Flask, render_template
from markupsafe import escape
from systems import System, get_systems

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/form')
def form():
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/system/<name>')
def get_coords(name):
    system = System(name)
    return '%s' % escape(system.name) + ' ' + str(system.coordinates) + ' ' + str(system.error)

@app.route('/closest/<name>')
def get_closest(name):
    position = System(name, use_edsm=True)
    systems.sort(key=lambda a : a.distance(position))
    response = '%s' % escape(position.name) + ' ' + str(position.coordinates) + '<br> <br>'
    for system in systems[:100]:
        response += '{} {} {} {}<br>'.format(escape(system.name), str(system.coordinates), str(system.error), str(round(position.distance(system), 2)))
    return response


def load_systems(filename):
    print('Reading systems data')
    systems = []
    with open(filename, newline='') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        begin, end = 0, 300000
        for i, row in enumerate(csvreader):
            if begin <= i < end:
                systems.append(System(row[1]))
            if i == end:
                break
    return systems

systems = load_systems('resources/systems-without-coordinates.csv')

