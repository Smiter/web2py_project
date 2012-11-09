## This is a sample controller
from gluon import *
import json


def list():
    return dict(message=T(""))


def labelHandler():
    selectcolumns = (db.label.id, db.label.releasecandidatename, db.label.user, db.label.date)
    tableData = proccessTableQuery(query=db.label.id, countBeforeFilter=db.label.id, columns=labelColumns,selectcolumns = selectcolumns)
    return response.json(tableData)


def showlabel():
    logger.error("showLabel")
    rows = db((db.testsuite.id == db.labeltorun.testsuite_id) & (db.testsuite.anaconda_id == db.anaconda.id) & (db.labeltorun.label_id == request.post_vars.labelid)).select()
    return dict(testsuiteArray=rows.as_list())


def generateReport():
    logger.error("GENERATE REPORT")
    left = [db.testsuite.on(db.label.id == db.testsuite.label_id), db.anaconda.on(db.anaconda.id == db.testsuite.anaconda_id)]
    rows = db(db.label.id == request.post_vars.labelid).select(left=left)  

    return 'http://172.30.136.80:8080/birt2/frameset?__report=BirtReports/Designs/AnacondaTest/anaconda_limbo_report.rptdesign&Release Candidate=%s' % request.post_vars.labelid
