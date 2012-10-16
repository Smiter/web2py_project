## This is a sample controller
from gluon import *
import json


def runs():
    return dict(message=T(""))


def runsHandler():
    query = db.testsuite.anaconda_id == db.anaconda.id
    tableData = proccessTableQuery(query=query,
                                   countBeforeFilter=db.testsuite.id,
                                   columns=testsuiteColumns)
    return response.json(tableData)


def analyzeHandler():
    logging.error("analyze Handler")
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
    logging.error("analysis")
    return dict(m=request.vars.testsuiteId, )


def saveAnalyze():
    logging.error("saveAnalyze")
    logging.error(json.loads(request.vars.analysisMap))
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

    logging.error(request.vars.testsuiteid)
    db(db.testsuite.id == request.vars.testsuiteid).update(analyzed=1)
    redirect(URL('web2py_birt', 'fact', 'runs'))


def saveLabelList():
    logging.error("AJAX CALL")
    labelList = json.loads(request.post_vars.array)
    resultList=dict()
    for k, v in labelList.items():
        if session.vasea:
            if not k in session.vasea:
                session.vasea[k] = v
                resultList[k]=v
        else:
            session.vasea = dict()
            session.vasea[k]=v
            resultList[k]=v
    return response.json(resultList)


def removeLabelFromSession():
    logging.error("AJAX CALL2")
    del session.vasea[request.post_vars.testsuiteid]
    return len(session.vasea)


def saveLabel():
    logging.error("saveLabel")
    logging.error(request.post_vars.username)
    logging.error(request.post_vars.labelname)
    logging.error(session.vasea.keys())
    # db.label.insert(     
        # releasename=request.post_vars.labelname,
        # user=request.post_vars.username )

    #  analysisListOfMaps = json.loads(request.vars.analysisMap)
    # for map_item in analysisListOfMaps:
    #     testresult_id = map_item["testresult_id"]
    #     errortype = map_item["errortype"]
    #     comment = map_item["comment"]
    #     jira_id = map_item["jira_id"]
    #     row = db(db.analysis.testresult_id == testresult_id).select().first()
    #     if row:
    #         db(db.analysis.testresult_id == testresult_id).update(
    #             id=row.id,
    #             testresult_id=testresult_id,
    #             errortype=errortype,
    #             comment=comment,
    #             elvis_id=jira_id)
    #     else:
    #         db.analysis.insert(
    #             testresult_id=testresult_id,
    #             errortype=errortype,
    #             comment=comment,
    #             elvis_id=jira_id)

    # logging.error(request.vars.testsuiteid)
    # db(db.testsuite.id == request.vars.testsuiteid).update(analyzed=1)


    # redirect(URL('web2py_birt', 'labels', 'list'))
