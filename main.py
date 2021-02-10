from traceback import print_exc
from uuid import uuid4
from flask import Flask, request, send_from_directory
from function_plot import *

app = Flask(__name__)

max_simultaneous_requests = 8
simultaneous_requests = 0


@app.route('/generate/')
def generate():
    global simultaneous_requests
    simultaneous_requests += 1
    try:
        if simultaneous_requests >= max_simultaneous_requests:
            raise Exception("Too many simultaneous requests")

        fn = request.args.get("fn")

        x_min = float(request.args.get("x_min", -8))
        x_max = float(request.args.get("x_max", 8))
        y_min = float(request.args.get("y_min", -5))
        y_max = float(request.args.get("y_max", 5))

        filename = str(uuid4()) + ".mp4"

        return plot(fn, filename, x_min, x_max, y_min, y_max)
    except:
        print_exc()
        return ""
    finally:
        simultaneous_requests -= 1


@app.route('/videos/<path:filename>')
def download_file(filename):
    return send_from_directory(path, filename, mimetype="video/mp4", as_attachment=True)
