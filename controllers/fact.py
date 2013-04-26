## This is a sample controller
from gluon import *
import json


def runs():
    logger.error(request.application)
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
    selectcolumns = (db.testdescription.name, db.analysis.id, db.analysis.jira_id, db.testdescription.testdescription, db.testresult.testresult, db.testresult.failuredescription, db.analysis.errortype, db.analysis.comment, db.testresult.id, db.test.include_test)

    query = (db.testsuite.id == db.test.testsuite_id) & (
        db.testdescription.id == db.test.testdescription_id) & (
            db.testresult.id == db.test.testresult_id) & (
                db.testsuite.id == request.vars.testsuiteid) 

    if request.vars.testresult == 'NOK' or request.vars.testresult == 'OK':
        query &= db.testresult.testresult == request.vars.testresult
    else:
        query &= (db.testresult.testresult == 'NOK' ) | (db.testresult.testresult == 'OK')

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
    logger.error("saveAnalyze")
    analysisListOfMaps = json.loads(request.vars.analysisMap)
    for map_item in analysisListOfMaps:
        testresult_id = map_item["testresult_id"]
        analysis_id = map_item["analysis_id"]
        errortype = map_item["errortype"]
        comment = map_item["comment"]
        jira_id = map_item["jira_id"]
        include_test = map_item["include_test"]
        db(db.test.testresult_id == testresult_id).update(
                            include_test=include_test)
        if map_item["testresult"] == 'OK':
            continue
        logger.error(map_item["testresult"])
        if errortype == "OK in Context":
            db(db.testresult.id == testresult_id).update(
                            testresult='OK')
        if analysis_id is None:
            db.analysis.insert(
                            testresult_id=testresult_id,
                            errortype=errortype,
                            comment=comment,
                            jira_id=jira_id)
        else:    
            db(db.analysis.id == analysis_id).update(
                            testresult_id=testresult_id,
                            errortype=errortype,
                            comment=comment,
                            jira_id=jira_id)
    if request.vars.testsuiteid != -1:
        db(db.testsuite.id == request.vars.testsuiteid).update(analyzed=1)

    # redirect(URL('web2py_birt', 'fact', 'runs'))


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
    db.label.insert(releasecandidatename=request.post_vars.labelname, user=request.post_vars.username, releasecomment = request.post_vars.releasecomment, commentswqs = request.post_vars.commentswqs)
    row = db(db.label.id).select().last()
    for k in session.label_preview_list.keys():
        db.labeltorun.insert(label_id = row.id, testsuite_id = k)        
        idd = db(db.testsuite.id == k).select().last()
        if request.post_vars.changelist != "":
            db(db.anaconda.id ==int(idd.anaconda_id)).update(changelist=str(request.post_vars.changelist))
        if request.post_vars.branch != "":
            db(db.anaconda.id ==int(idd.anaconda_id)).update(name=request.post_vars.branch+"_"+request.post_vars.changelist)
        db(db.testsuite.id == k).update(
            label_id=row.id)
    session.label_preview_list = dict()

    redirect(URL(request.application, 'labels', 'list'))


def checkifanalyzed():
    row = db((db.testsuite.id == db.labeltorun.testsuite_id) & (db.labeltorun.label_id == request.post_vars.labelid)).select(db.testsuite.analyzed)
    for r in row:
        if r.analyzed == 1:
            return True
    return False

def edit_cell_value():
    logger.error(request.vars)
    value = request.vars.value
    column_name = request.vars.column_name
    testsuite_id = request.post_vars.testsuite_id
    if column_name == "testsuitename":
        db(db.testsuite.id == int(testsuite_id)).update(
                                testsuitename=value)
    if column_name == "changelist":
        row = db(db.testsuite.id == int(testsuite_id)).select(db.testsuite.anaconda_id).last()
        db(db.anaconda.id == int(row.anaconda_id)).update(
                                changelist=value)
    return value



def get_testsuite_by_name():
    if not request.vars.auto_testsuitename: return ''
    selected = db(db.testsuite.testsuitename.contains(request.vars.auto_testsuitename)).select(db.testsuite.testsuitename, db.testsuite.id)
    return ''.join([DIV(k.testsuitename,
                 _onclick="jQuery('#autocomplite_by_name_input%s').val('%s'); jQuery('#autocomplite_by_id_input%s').val('%s'); jQuery('#suggestions_name%s').empty();" % (request.vars.collapse_id, k.testsuitename, request.vars.collapse_id, k.id, request.vars.collapse_id),
                 _onmouseover="this.style.backgroundColor='yellow'",
                 _onmouseout="this.style.backgroundColor='white';"
                 ).xml() for k in selected])

def get_testsuite_by_id():
    if not request.vars.auto_testsuiteid: return ''
    pattern = request.vars.auto_testsuiteid + '%'
    selected = db(db.testsuite.id.like(pattern)).select(db.testsuite.id, db.testsuite.testsuitename)
    return ''.join([DIV(k.id,
                 _onclick="jQuery('#autocomplite_by_id_input%s').val('%s'); jQuery('#autocomplite_by_name_input%s').val('%s'); jQuery('#suggestions_id%s').empty();" % (request.vars.collapse_id, k.id, request.vars.collapse_id, k.testsuitename, request.vars.collapse_id),
                 _onmouseover="this.style.backgroundColor='yellow'",
                 _onmouseout="this.style.backgroundColor='white';"
                 ).xml() for k in selected])

def autocomplite_jiraids():
    logger.error(request.vars)
    s = "select vjira_id, ganalysis_id, gtestresult_id, verror, vcomment from (select testdescription.name as vname, analysis.jira_id as vjira_id,  analysis.errortype as verror, analysis.comment as vcomment from testsuite "
    s += "left join test on testsuite.id = test.testsuite_id "
    s += "left join testdescription on testdescription.id = test.testdescription_id "
    s += "left join testresult on testresult.id = test.testresult_id "
    s += "left join analysis on analysis.testresult_id = testresult.id "
    s += "where testresult.testresult = 'NOK' and testsuite.id = " + request.vars.testsuiteid_autocomplited + " ) v "
    s += "join (select testdescription.name as gname, analysis.id as ganalysis_id, analysis.jira_id as gjira_id, testresult.id as gtestresult_id from testsuite "
    s += "left join test on testsuite.id = test.testsuite_id "
    s += "left join testdescription on testdescription.id = test.testdescription_id "
    s += "left join testresult on testresult.id = test.testresult_id "
    s += "left join analysis on analysis.testresult_id = testresult.id "
    s += "where testresult.testresult = 'NOK' and testsuite.id = "+ request.vars.testsuiteid_origin +" ) g  on v.vname = g.gname " 
    results = db.executesql(s)
    for i in results:
        jira_id = i[0]
        analysis_id = i[1]
        testresult_id = i[2]
        errortype = i[3]
        comment = i[4]
        if analysis_id is None:
            db.analysis.insert(
                            testresult_id=int(testresult_id),
                            errortype=errortype,
                            comment=comment,
                            jira_id=jira_id)
        else: 
            db(db.analysis.id == analysis_id).update(
                            testresult_id=int(testresult_id),
                            errortype=errortype,
                            comment=comment,
                            jira_id=jira_id)


