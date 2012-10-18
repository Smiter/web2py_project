## This is a sample controller
from gluon import *


def list():
    return dict(message=T(""))


def labelHandler():
    tableData = proccessTableQuery(query=db.label.id, countBeforeFilter=db.label.id, columns=labelColumns)
    return response.json(tableData)


def showLabel():
    logger.error("showLabel")
    logger.error(request.post_vars.labelid)
    rows = db((db.testsuite.label_id == db.label.id ) & (db.label.id == request.post_vars.labelid)).select(db.testsuite.id)
    logger.error(rows.as_list())
    return dict(testsuiteArray=rows.as_list())
    
