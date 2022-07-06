# routes.py

from flask import session, render_template, flash, redirect, url_for, request, jsonify, json, make_response, after_this_request
import pdfkit


from flask_bootstrap import Bootstrap
from werkzeug.urls import url_parse
from app.models import *
from app import app
from app import db
from sqlalchemy import func, case, desc, extract, select, update, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DBAPIError
from sqlalchemy.orm import aliased

import datetime as dt
from datetime import date, datetime, timedelta

import os.path
from os import path

from flask_mail import Mail, Message
mail=Mail(app)
import requests


CodeVersion = GetAppVersion().get("version","UNKNOWN VERSION")


# Dump a Python object's non underscored members, for debug
def dump(obj):
    for attr in dir(obj):
        if hasattr( obj, attr ):
            if not attr.startswith("_"):
                print( "obj.%s = %s" % (attr, getattr(obj, attr)))


@app.route('/')
@app.route('/index')
def index():
    logging.debug("GetMemberList index entry")
    memberList = [ {"id":n.Member_ID, "first":n.First_Name, "last":n.Last_Name, "nick":n.Nickname} for n in GetMemberList()]
    logging.debug("GetMemberList index exit")

    return render_template("index.html", memberList=memberList, version=CodeVersion)


@app.route("/v1/webAppVersion", methods=["GET"])
def webAppVersion():
    return CodeVersion


# DISPLAY MEMBER CONTACT INFO
@app.route("/getMemberContactInfo", methods=['POST'])
def getMemberContactInfo():
    req = request.get_json()
    memberID = req["villageID"]

    member = GetMemberRecord(memberID)

    if member == None:
        msg = "ERROR - Member not found"
        return jsonify(msg=msg)
    # dump(member)
    memberName = member.First_Name + ' ' + member.Last_Name
    if member.Nickname != '' and member.Nickname != None:
        memberName = member.First_Name + ' (' + member.Nickname + ') ' + member.Last_Name
    return jsonify(mobilePhone=member.Cell_Phone,eMail=member.eMail,memberName=memberName,memberID=member.Member_ID,lightspeedID=member.LightspeedID, homePhone=member.Home_Phone,cellPhone=member.Cell_Phone)

