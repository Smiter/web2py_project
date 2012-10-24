## This is a sample controller
from gluon import *
import json


def runs():
    return dict(message=T(""))


def runsHandler():
    logger.error(request.post_vars)
    query = db.testsuite.anaconda_id == db.anaconda.id
    tableData = proccessTableQuery(query=query,
                                   countBeforeFilter=db.testsuite.id,
                                   columns=testsuiteColumns)
    return response.json(tableData)


def analyzeHandler():
    logger.error("analyze Handler")
    logger.error(request.vars.testsuiteid)
    query = (db.testsuite.id == db.test.testsuite_id) & (
        db.testdescription.id == db.test.testdescription_id) & (
            db.testresult.id == db.test.testresult_id) & (
                db.testsuite.id == request.vars.testsuiteid)
    tableData = proccessTableQuery(
        query=query,
        countBeforeFilter=query,
        left=db.analysis.on(db.analysis.testresult_id == db.testresult.id),
        columns=analyzedColumns)

    return response.json(tableData)


def analysis():
    logger.error("analysis")
    logger.error(request.vars.testsuiteId)
    return dict(m=request.vars.testsuiteId)


def saveAnalyze():
    logger.error("saveAnalyze")
    logger.error(request.vars.analysisMap)
    logger.error(json.loads(request.vars.analysisMap))
    logger.error(request.vars.testsuiteid)
    analysisListOfMaps = json.loads(request.vars.analysisMap)
    for map_item in analysisListOfMaps:
        testresult_id = map_item["testresult_id"]
        errortype = map_item["errortype"]
        comment = map_item["comment"]
        jira_id = map_item["jira_id"]
        row = db(db.analysis.testresult_id == testresult_id).select().first()
        if row:
            db(db.analysis.testresult_id == testresult_id).update(
                id=row.id,
                testresult_id=testresult_id,
                errortype=errortype,
                comment=comment,
                elvis_id=jira_id)
        else:
            db.analysis.insert(
                testresult_id=testresult_id,
                errortype=errortype,
                comment=comment,
                elvis_id=jira_id)

    db(db.testsuite.id == request.vars.testsuiteid).update(analyzed=1)
    redirect(URL('web2py_birt', 'fact', 'runs'))


def saveLabelList():
    logging.error("AJAX CALL")
    labelList = json.loads(request.post_vars.array)
    resultList = dict()
    for k, v in labelList.items():
        if session.label_preview_list:
            if not k in session.label_preview_list:
                session.label_preview_list[k] = v
                resultList[k] = v
        else:
            session.label_preview_list = dict()
            session.label_preview_list[k] = v
            resultList[k] = v
    return response.json(resultList)


def removeLabelFromSession():
    logging.error("AJAX CALL2")
    del session.label_preview_list[request.post_vars.testsuiteid]
    return len(session.label_preview_list)

def saveLabel():
    db.label.insert(releasename=request.post_vars.labelname,user=request.post_vars.username)
    row = db(db.label.id).select().last()

    for k in session.label_preview_list.keys():
        db(db.testsuite.id == k).update(
                label_id=row.id)
    session.label_preview_list = dict()

    redirect(URL('web2py_birt', 'labels', 'list'))
