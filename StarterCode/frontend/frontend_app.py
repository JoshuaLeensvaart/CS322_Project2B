# Front End Full-Stack App
from flask import Flask, render_template, request, redirect, flash, url_for
import requests
# Note the two libraries:
#
# flask.request processes incoming requests to the frontend server
# (in other words, form submissions)
#
# the python requests library (plural!) sends requests to
# a different server:  the backend server
# need to execute in Terminal:    pip install requests

# create the frontend app, which talks to the user, receives
# user requests, and then approves them to be sent to the backend
frontend_app = Flask(__name__)
backend_url = "http://127.0.0.1:5001"

# ROUTES

# view all destinations on homepage
@frontend_app.route("/")
@frontend_app.route("/home")
def home():
    # send a request to the backend for all the destinations
    # NOTE: the response variable includes the entire HTTP response
    # NOTE: can use print(dest_list.json()) # can use for debugging
    try:
        response = requests.get(backend_url + "/api")
        dest_list = response.json()
    except Exception as e:
        dest_list = []
        print(f"Backend connection error: {e}")

    return render_template('bucketlist.html', places=dest_list)

    # now, pass the data returned from the backend to the template and
    # render it (send it to the client computer as an HTML file)
    return render_template('bucketlist.html', places=response.json())

# add a new destination
@frontend_app.route("/new_destination", methods=["GET", "POST"])
def new_destination():
    # if GET request, display the form
    if request.method == "GET":
        return render_template('new_destination.html')
    # process the submitted form on a POST request
    if request.method == "POST":
        # Retrieve data from the form using the 'name' attribute
        name = request.form.get('dest_name')
        notes = request.form.get('notes')
        cost = request.form.get('cost')
        if not name or len(name) > 20 or not notes or len(notes) > 100:
            flash("Error: Name and Notes must be 1-20 characters.")
            return redirect(url_for('new_destination'))

        try:
            cost_val = float(cost)
            if cost_val < 0 or cost_val >= 100000:
                flash("Error: Cost must be a positive number under 100,000.")
                return redirect(url_for('new_destination'))
        except (ValueError, TypeError):
            flash("Error: Cost must be a valid number.")
            return redirect(url_for('new_destination'))

        payload = {
            "name": name,
            "notes": notes,
            "cost": cost_val
        }

        response = requests.post(backend_url + "/api/new", json=payload)
        if response.status_code == 201:
            return redirect(url_for('home'))
        else:
            flash(f"Backend rejected request: {response.json().get('error')}")
            return redirect(url_for('new_destination'))
