from flask import Flask, request, Response, render_template, send_from_directory, abort
from app import app
from db import db
from models import Beacon, Place, Visiter, Snap
import datetime
import json

def parse_serializable_obj(result):
    ans = vars(result)
    del ans["_sa_instance_state"]
    
    for k, v in ans.items():
        if(type(v) == datetime.datetime):
            ans[k] = v.isoformat()
    
    return ans

def get_json_params():
    return json.loads(request.data)

def get_snap_from_visiter_json(data):
    visiter = Visiter.query.filter_by(\
        id=data["id"],\
        user=data["user"],\
        place=data["place"],\
        pass_phrase=data["pass_phrase"],\
        snap=data["snap"],\
        date=datetime.datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%S")\
    ).first()
    
    if(visiter is None):
        return None
    
    return Snap.query.filter_by(id=visiter.snap).first()


@app.route("/")
def show_all():
    if(not app.debug):
        return abort(404)
    
    return render_template("index.html")

@app.route("/visiter", methods=["POST"])
def get_visiter():
    data = parse_serializable_obj(Visiter.query.filter_by(id=1).first())
    return Response(json.dumps(data), mimetype="application/json")

@app.route("/image", methods=["POST"])
def get_image():
    snap = get_snap_from_visiter_json(get_json_params())
    
    if snap is None:
        return abort(404)
    
    return send_from_directory(app.config["SNAPS_DIRECTORY"], snap.src)

@app.route("/thum", methods=["POST"])
def get_thum_image():
    snap = get_snap_from_visiter_json(get_json_params())
    
    if snap is None:
        return abort(404)
    
    return send_from_directory(app.config["SNAPS_DIRECTORY"], snap.thum_src)

@app.route("/snap_state", methods=["POST"])
def get_snap_state():
    return send_from_directory(app.config["SNAPS_DIRECTORY"], "1.jpg")


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

