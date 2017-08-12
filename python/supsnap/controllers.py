from flask import Flask, request, flash, url_for, redirect, render_template
from app import app
from db import db
from models import Beacon, Place, Visiter, Snap

@app.route("/")
def show_all():
    return render_template("index.html")
