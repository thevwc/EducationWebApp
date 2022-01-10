# routes.py

from flask import session, render_template, flash, redirect, url_for, request, jsonify, json, make_response, after_this_request
import pdfkit


from flask_bootstrap import Bootstrap
from werkzeug.urls import url_parse
from app.models import ShopName, Member, MemberActivity, MonitorSchedule, MonitorScheduleTransaction,\
MonitorWeekNote, CoordinatorsSchedule, ControlVariables, DuesPaidYears, Contact
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

@app.route('/')
@app.route('/index/')
@app.route('/index', methods=['GET'])
def index():
    # BUILD ARRAY OF NAMES FOR DROPDOWN LIST OF MEMBERS
    nameDict=[]
    nameItems=[]
    sqlSelect = "SELECT Last_Name, First_Name, Nickname, Member_ID FROM tblMember_Data "
    sqlSelect += "ORDER BY Last_Name, First_Name "

    nameList = db.engine.execute(sqlSelect)
    position = 0
    for n in nameList:
        position += 1
        if n.Last_Name != None and n.First_Name != None:
            lastFirst = n.Last_Name + ', ' + n.First_Name + ' (' + n.Member_ID + ')'
            if (n.Nickname != None and n.Nickname != ''):
                lastFirst += ' (' + n.Nickname + ')'
        else:
            lastFirst = ''

        nameItems = {
            'memberName':lastFirst,
            'memberID':n.Member_ID
        }
        
        nameDict.append(nameItems)

    return render_template("index.html",nameDict=nameDict)
   

# DISPLAY MEMBER CONTACT INFO
@app.route("/getMemberContactInfo",methods=['POST'])
def getMemberContactInfo():
    req = request.get_json()
    memberID = req["villageID"]

    # GET MEMBER NAME
    member = db.session.query(Member).filter(Member.Member_ID== memberID).first()
    if member == None:
        msg = "ERROR - Member not found"
        return jsonify(msg=msg)
    
    memberName = member.First_Name + ' ' + member.Last_Name
    if member.Nickname != '' and member.Nickname != None:
        memberName = member.First_Name + ' (' + member.Nickname + ') ' + member.Last_Name
    return jsonify(eMail=member.eMail,memberName=memberName,memberID=member.Member_ID,lightspeedID=member.LightspeedID, homePhone=member.Home_Phone,cellPhone=member.Cell_Phone)
    
