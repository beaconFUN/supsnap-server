from flask import Flask, request, Response, render_template, send_from_directory, abort
from app import app
from db import db
from models import Beacon, Place, Visiter, Snap
import datetime
import json
import copy
from threading import Timer

def parse_serializable_obj(data):
    data = copy.deepcopy(data)
    
    if hasattr(data, "__dict__"):
        data = vars(data)
    
    if "_sa_instance_state" in data:
        del data["_sa_instance_state"]
    
    for k, v in data.items():
        if isinstance(v, datetime.datetime):
            data[k] = v.strftime("%Y-%m-%dT%H:%M:%S")
        elif isinstance(v, bytes):
            data[k] = v.decode("utf-8")
    
    return data

def get_json_params():
    return json.loads(request.data)

def get_valid_visiter(data):
    visiter_query = Visiter.query.filter_by(\
        id=data["id"],\
        user=data["user"],\
        place=data["place"],\
        pass_phrase=data["pass_phrase"],\
        snap=data["snap"],\
        date=datetime.datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%S")\
    )
    
    if visiter_query.count() == 1:
        return visiter_query.one()
    else:
        return None

def get_snap_from_visiter_json(data):
    visiter = get_valid_visiter(data)
    
    if visiter is None:
        return None
    else:
        return Snap.query.filter_by(id=visiter.snap).one()


@app.route("/")
def show_all():
    if(not app.debug):
        return abort(404)
    
    return render_template("index.html")

@app.route("/get_visiter", methods=["POST"])
def get_visiter():
    params = get_json_params()
    
    place = Beacon.query.filter_by(\
        uuid=params["beacon"]["uuid"],\
        major=params["beacon"]["major"],\
        minor=params["beacon"]["minor"]\
    ).one().place;
    
    active_snaps = Snap.query.filter("date > :now").params(now=datetime.datetime.now()).all();
    
    for snap in active_snaps:
        if snap.visiters[0].place == place.id:
            for visiter in snap.visiters:
                if visiter.user == params["user"]:
                    return abort(409)
            
            new_visiter = Visiter(params["user"], place.id, snap.id)
            
            db.session.add(new_visiter)
            db.session.flush()
            serializable_new_visiter = copy.deepcopy(parse_serializable_obj(new_visiter))
            
            db.session.commit()
            
            return Response(json.dumps(serializable_new_visiter), mimetype="application/json")
    
    new_snap = Snap(datetime.datetime.now() + datetime.timedelta(seconds=app.config["SNAP_TIME_LAG"]))
    db.session.add(new_snap)
    db.session.flush()
    
    new_visiter = Visiter(params["user"], place.id, new_snap.id)
    db.session.add(new_visiter)
    db.session.flush()
    
    serializable_new_visiter = copy.deepcopy(parse_serializable_obj(new_visiter))
    
    db.session.commit()
    
    return Response(json.dumps(serializable_new_visiter), mimetype="application/json")

@app.route("/delete_visiter", methods=["POST"])
def delete_visiter():
    params = get_json_params()
    visiter = get_valid_visiter(params)
    
    if visiter is None:
        return abort(404)
    
    db.session.delete(visiter)
    db.session.commit()
    return Response(json.dumps({"state": "done"}), mimetype="application/json")

@app.route("/get_image", methods=["POST"])
def get_image():
    snap = get_snap_from_visiter_json(get_json_params())
    
    if snap is None:
        return abort(404)
    
    return send_from_directory(app.config["SNAPS_DIRECTORY"], snap.src)

@app.route("/get_thum", methods=["POST"])
def get_thum_image():
    snap = get_snap_from_visiter_json(get_json_params())
    
    if snap is None:
        return abort(404)
    
    return send_from_directory(app.config["SNAPS_DIRECTORY"], snap.thum_src)

@app.route("/get_snap_state", methods=["POST"])
def get_snap_state():
    snap = get_snap_from_visiter_json(get_json_params())
    
    if snap is None:
        return abort(404)
    
    response_data = {
        "visiter_length": len(snap.visiters),
        "snap_time": snap.date
    }
    
    return Response(json.dumps(parse_serializable_obj(response_data)), mimetype="application/json")


# debugging methods
@app.route("/models/<model>/<id>", methods=["GET"])
def get_model(model, id):
    if(not app.debug):
        return abort(404)
    
    model_class = eval("%s" % model)
    data = parse_serializable_obj(model_class.query.filter_by(id=id).first())
    
    return Response(json.dumps(data), mimetype="application/json")


@app.route("/models/<model>", methods=["GET"])
def get_models(model):
    if(not app.debug):
        return abort(404)
    
    model_class = eval("%s" % model)
    data = list(map(parse_serializable_obj, model_class.query.all()))
    
    return Response(json.dumps(data), mimetype="application/json")

