from flask import Flask, request, Response, render_template, send_from_directory, send_file, abort
from app import app
from db import db
from models import Beacon, Place, Visiter, Snap, Camera
import datetime
import json
import copy
from threading import Timer
import os
from werkzeug.utils import secure_filename
import requests
from io import BytesIO

live_views = {};

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

def validate_user(data):
    if "user" not in data:
        return False
    
    if not isinstance(data["user"], str) or len(data["user"]) > 255:
        return False
    
    return True

def validate_beacon(data):
    if "uuid" not in data or "major" not in data or "minor" not in data:
        return False
    
    if not isinstance(data["uuid"], str) or len(data["uuid"]) != 36:
        return False
    
    if not isinstance(data["major"], int):
        return False
    
    if not isinstance(data["minor"], int):
        return False
    
    return True

def validate_visiter(data):
    if "id" not in data or "user" not in data or "place" not in data or "pass_phrase" not in data or "snap" not in data or "date" not in data:
        return False
    
    if not isinstance(data["id"], int):
        return False
    
    if not isinstance(data["user"], str) or len(data["user"]) > 255:
        return False
    
    if not isinstance(data["place"], int):
        return False
    
    if not isinstance(data["pass_phrase"], str) or len(data["pass_phrase"]) != 32:
        return False
    
    if not isinstance(data["snap"], int):
        return False
    
    if not isinstance(data["date"], str):
        return False
    
    return True


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

def set_snap(snap):
    snap = db.session.query(Snap).filter_by(id=snap).one()
    
    if len(snap.visiters) != 0:
        camera = db.session.query(Place).filter_by(id=snap.visiters[0].place).one().camera[0]
        print("requesting snap...")
        payload = {"snap": snap.id, "interval": app.config["SNAP_TIME_LAG"]}
        print(requests.get(camera.endpoint, params=payload).text)


@app.route("/")
def show_all():
    if(not app.debug):
        return abort(404)
    
    return render_template("index.html")

@app.route("/get_place", methods=["POST"])
def get_place():
    params = get_json_params()

    if not validate_beacon(params):
        return abort(400)

    place = Beacon.query.filter_by(\
        uuid=params["uuid"],\
        major=params["major"],\
        minor=params["minor"]\
    ).one().place

    return Response(json.dumps(parse_serializable_obj(place), ensure_ascii=False), mimetype="application/json")

@app.route("/get_visiter", methods=["POST"])
def get_visiter():
    params = get_json_params()
    
    if not validate_user(params) or not validate_beacon(params["beacon"]):
        return abort(400)
    
    place = Beacon.query.filter_by(\
        uuid=params["beacon"]["uuid"],\
        major=params["beacon"]["major"],\
        minor=params["beacon"]["minor"]\
    ).one().place
    
    active_snaps = Snap.query.filter("date > :now").params(now=datetime.datetime.now()).all();
    
    for snap in active_snaps:
        if len(snap.visiters) != 0 and snap.visiters[0].place == place.id:
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
    
    set_snap(serializable_new_visiter["snap"])
    
    return Response(json.dumps(serializable_new_visiter), mimetype="application/json")

@app.route("/delete_visiter", methods=["POST"])
def delete_visiter():
    params = get_json_params()
    
    if not validate_visiter(params):
        return abort(400)
    
    visiter = get_valid_visiter(params)
    
    if visiter is None:
        return Response(status=204)
    
    db.session.delete(visiter)
    db.session.commit()
    return Response(json.dumps({"state": "done"}), mimetype="application/json")

@app.route("/get_image", methods=["GET", "POST"])
def get_image():
    if(request.method == "GET"):
        params = json.loads(request.args.get("visiter"));
    else:
        params = get_json_params()

    if not validate_visiter(params):
        return abort(400)
    
    snap = get_snap_from_visiter_json(params)
    
    if snap is None or snap.src is None:
        return Response(status=204)
    
    os.path.exists(app.config["SNAPS_DIRECTORY"] + snap.src)
    
    return send_from_directory(app.config["SNAPS_DIRECTORY"], snap.src)

@app.route("/get_thum", methods=["POST"])
def get_thum_image():
    params = get_json_params()
    
    if not validate_visiter(params):
        return abort(400)
    
    snap = get_snap_from_visiter_json(params)
    
    if snap is None or snap.thum_src is None:
        return Response(status=204)
    
    return send_from_directory(app.config["SNAPS_DIRECTORY"], snap.thum_src)

@app.route("/get_snap_state", methods=["POST"])
def get_snap_state():
    params = get_json_params()
    
    if not validate_visiter(params):
        return abort(400)
    
    snap = get_snap_from_visiter_json(params)
    
    if snap is None:
        return Response(status=204)
    
    response_data = {
        "visiter_length": len(snap.visiters),
        "snap_time": snap.date,
        "done": snap.src is not None
    }
    
    return Response(json.dumps(parse_serializable_obj(response_data)), mimetype="application/json")

@app.route("/add_camera", methods=["POST"])
def add_camera():
    params = get_json_params()
    
    cameras = db.session.query(Camera).filter_by(place=params["place"]).all()
    if len(cameras) != 0:
        cameras[0].endpoint = params["endpoint"]
        db.session.commit()
        return "update ok"
    
    new_camera = Camera(params["place"], params["endpoint"])
    db.session.add(new_camera)
    db.session.commit()
    
    return "ok"

@app.route("/post_image", methods=["POST"])
def post_image():
    if "image" not in request.files or "thum" not in request.files:
        return "No file"
    
    image = request.files["image"]
    thum = request.files["thum"]
    
    if image.filename == "" or thum.filename == "":
        return "No filename"
    
    image_filename = secure_filename(image.filename)
    thum_filename = secure_filename(thum.filename)
    
    image.save(os.path.join(app.config["SNAPS_DIRECTORY"], image_filename))
    thum.save(os.path.join(app.config["SNAPS_DIRECTORY"], thum_filename))
    
    snap = db.session.query(Snap).filter_by(id=request.form["snap"]).one()
    snap.src = image_filename
    snap.thum_src = thum_filename
    db.session.commit()
    
    return "ok"

@app.route("/post_live_view", methods=["POST"])
def post_live_view():
    if "place" not in request.form:
        abort(400)

    live_views[request.form["place"]] = BytesIO(request.files["live_view"].stream.read())
    return "ok"

@app.route("/get_live_view", methods=["POST"])
def get_live_view():
    params = get_json_params()

    if not validate_visiter(params):
        return abort(400)

    if live_views[str(params["place"])].closed:
        abort(404)

    return send_file(live_views[str(params["place"])], mimetype="image/jpeg");





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

