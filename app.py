from flask import Flask, jsonify, render_template, request
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt

#set up database

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#new model for database
Base = automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#references for tables 
Measurement = Base.classes.measurement

Station = Base.classes.station

#create a session
session = Session(engine)


#set up flask 
app = Flask(__name__)

#flask route 
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