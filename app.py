from flask import Flask, jsonify, render_template, request
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt

# set up database

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# new model for database
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# references for tables
Measurement = Base.classes.measurement

Station = Base.classes.station

# create a session
session = Session(engine)


# set up flask
app = Flask(__name__)

# flask route


@app.route("/")
def Home():
    return render_template("index.html")


def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.

    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d

    Returns:
        TMIN, TAVE, and TMAX
    """
    session = Session(engine)

    return (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start_date)
        .filter(Measurement.date <= end_date)
        .all()
    )


# Calculate the date 1 year ago from the last data point in the database
last_date = session.query(Measurement.date).order_by(
    Measurement.date.desc()).first()[0]
last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
last_year = last_date - dt.timedelta(days=365)


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary in JSON format where the date is the key and the value is 
    the precipitation data"""

    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    precip_results = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date > last_year)
        .order_by(Measurement.date)
        .all()
    )
    # Save the query results as a dictionary
    # Return the valid JSON response object
    return jsonify(precip_results)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""

    session = Session(engine)

    stations_results = session.query(Station.station, Station.name).all()

    return jsonify(stations_results)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year"""

    session = Session(engine)

    temp_results = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.date > last_year)
        .order_by(Measurement.date)
        .all()
    )
    return jsonify(temp_results)


@app.route("/api/v1.0/<start>")
def start(start):
    """Returns the JSON list of the minimum, average and the maximum temperatures for a given start date (YYYY-MM-DD)"""

    temps = calc_temps(start, last_date)

    # list to store the temperature records
    temp_list = []
    date_dict = {"Start Date": start, "End Date": last_date}
    temp_list.append(date_dict)
    temp_list.append(
        {"Observation": "Minimum Temperature", "Temperature(F)": temps[0][0]}
    )
    temp_list.append(
        {"Observation": "Average Temperature", "Temperature(F)": temps[0][1]}
    )
    temp_list.append(
        {"Observation": "Maximum Temperature", "Temperature(F)": temps[0][2]}
    )

    return jsonify(temp_list)


@app.route("/api/v1.0")
def start_end():
    """Returns the JSON list of the minimum, average and the maximum temperatures for a given start date and end date(YYYY-MM-DD)"""
    start = request.args.get("Start Date")
    end = request.args.get("End Date")

    temps = calc_temps(start, end)

    # list to store the temperature records

    temp_list = []
    date_dict = {"Start Date": start, "End Date": end}
    temp_list.append(date_dict)
    temp_list.append(
        {"Observation": "Minimum Temperature", "Temperature(F)": temps[0][0]}
    )
    temp_list.append(
        {"Observation": "Average Temperature", "Temperature(F)": temps[0][1]}
    )
    temp_list.append(
        {"Observation": "Maximum Temperature", "Temperature(F)": temps[0][2]}
    )
    return jsonify(temp_list)

    # run app
    if __name__ == "__main__":
    app.run(debug=True)
