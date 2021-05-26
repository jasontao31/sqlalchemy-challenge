import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine  = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    first_date = last_date - timedelta(days = 365)
    Prcp = (session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= first_date).order_by(Measurement.date).all())
    return jsonify(Prcp)

@app.route("/api/v1.0/stations")
def stations():
  session  = Session(engine)
  stations = session.query(Station.station, Station.name).all()
  return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    first_date = last_date - timedelta(days = 365)
    station_count = (session.query(Measurement.station, func.count).filter(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    active_station = (station_count[0])
    active_station = (active_station[0])
    session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.station == active_station).all()
    active_station_year = session.query(Measurement.tobs).\
    filter(Measurement.station == active_station).filter(Measurement.date >= first_date).all()
    return jsonify(active_station_year)

@app.route("/api/v1.0/<start>")
def TempStartDate(start):
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(temp_results)

@app.route("/api/v1.0/<start>/<end>")
def TempStartEndDate(start,end):
    temp_results_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(temp_results_end)
    


if __name__ == '__main__':
   app.run()
