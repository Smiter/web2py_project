## This is a sample controller
from gluon import *
import json


def runs():
    return dict(message=T(""))


def runsHandler():
    logger.error(request.post_vars)
    selectcolumns = (db.testsuite.id, db.testsuite.testsuitename, db.testsuite.starttime, db.testsuite.endtime, db.testsuite.analyzed, db.anaconda.name, db.anaconda.changelist)
    query = db.testsuite.anaconda_id == db.anaconda.id
    tableData = proccessTableQuery(query=query,
                                   countBeforeFilter=db.testsuite.id,
                                   columns=testsuiteColumns,selectcolumns = selectcolumns)
    return response.json(tableData)


def analyzeHandler():
    logger.error("analyze Handler")
    selectcolumns = (db.testdescription.name, db.analysis.id, db.testdescription.testdescription, db.testresult.testresult, db.testresult.failuredescription, db.analysis.errortype, db.analysis.elvis_id, db.analysis.comment,db.testresult.id)

    query = (db.testsuite.id == db.test.testsuite_id) & (
        db.testdescription.id == db.test.testdescription_id) & (
            db.testresult.id == db.test.testresult_id) & (
                db.testsuite.id == request.vars.testsuiteid)
    tableData = proccessTableQuery(
        query=query,
        countBeforeFilter=query,
        left=db.analysis.on(db.analysis.testresult_id == db.testresult.id),
        columns=analyzedColumns, selectcolumns = selectcolumns)

    return response.json(tableData)


def analysis():
    logger.error("analysis")
    result = json.loads(request.vars.testsuitelist)
    left = db.anaconda.on(db.anaconda.id == db.testsuite.anaconda_id)
    query = None
    for i in result:
        if query is None:
            query = db.testsuite.id == i
        else:
            query |= db.testsuite.id == i

    rows = db(query).select(left=left)
    return dict(testsuiteArray=rows.as_list())


def saveAnalyze():
    import time
    logger.error("saveAnalyze")

    
    # logger.error(request.vars.analysisMap)
    # logger.error(json.loads(request.vars.analysisMap))
    # logger.error(request.vars.testsuiteid)
    analysisListOfMaps = json.loads(request.vars.analysisMap)
    for map_item in analysisListOfMaps:
        logger.error(map_item)
        testresult_id = map_item["testresult_id"]
        analysis_id = map_item["analysis_id"]
        errortype = map_item["errortype"]
        comment = map_item["comment"]
        jira_id = map_item["jira_id"]
        if analysis_id is None:
            db.analysis.insert(
                            testresult_id=testresult_id,
                            errortype=errortype,
                            comment=comment,
                            elvis_id=jira_id)
        else:    
            db(db.analysis.id == analysis_id).update(
                            testresult_id=testresult_id,
                            errortype=errortype,
                            comment=comment,
                            elvis_id=jira_id)
    if request.vars.testsuiteid != -1:
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
    db.label.insert(releasecandidatename=request.post_vars.labelname, user=request.post_vars.username)
    row = db(db.label.id).select().last()

    for k in session.label_preview_list.keys():
        db(db.testsuite.id == k).update(
            label_id=row.id)
    session.label_preview_list = dict()

    redirect(URL('web2py_birt', 'labels', 'list'))


def checkifanalyzed():
    left = db.testsuite.on(db.label.id == db.testsuite.label_id)
    row = db(db.label.id == request.post_vars.labelid).select(db.testsuite.analyzed, left=left)
    for r in row:
        if r.analyzed == 0:
            return False
    return True