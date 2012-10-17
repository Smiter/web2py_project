## This is a sample controller
from gluon import *
import logging


def list():
    return dict(message=T(""))


def labelHandler():
    tableData = proccessTableQuery(query=db.label.id,countBeforeFilter=db.label.id, columns=labelColumns)
    return response.json(tableData)
