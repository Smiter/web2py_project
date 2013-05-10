from gluon import *
import json


def analyse_testsuite():
    """
    Used for rendering views/report_analysis/analyse_testsuite.html page. Called when clicked on Analyze button.

    :param testsuitelist: list of testsuites from report preview window.
    :type testsuitelist: array
    :returns:  resultset of test runs from database.
    """

    result = json.loads(request.vars.testsuitelist)
    left = db.anaconda.on(db.anaconda.id == db.testsuite.anaconda_id)
    query = None
    for i in result:
        if query is None:
            query = db.testsuite.id == i
        else:
            query |= db.testsuite.id == i

    rows = db(query).select(left=left)
    return dict(testsuiteArray=rows)


def analyse_report():
    """
    Used for rendering views/report_analysis/analyse_report.html page. Called when clicked on Analyze button.

    :param report_id: id of report.
    :type report_id: int
    :returns:  resultset of test runs from database attached to the report, report_id, anaconda_id, tools_result, techs_result
    """
    
    report_id = request.vars.report_id
    rows = db((db.testsuite.id == db.labeltorun.testsuite_id) & (db.label.id == report_id) & (db.testsuite.anaconda_id == db.anaconda.id) & (db.databaseundertest.id == db.testsuite.dut_id) & (db.testenviroment.id == db.testsuite.enviroment_id) & (db.labeltorun.label_id == report_id)).select()
    tools_result = db(db.tools_analysis.label_id == report_id).select().last()
    techs_result = db(db.techs_analysis.label_id == report_id).select().last()
    if techs_result:
        techs_result = techs_result.as_dict()
    else:
        techs_result = {}
    if tools_result:
        tools_result = tools_result.as_dict()
    else:
        tools_result = {}
    if len(rows) > 0:
        anaconda_id = rows[0]['anaconda']['id']
    return dict(testsuiteArray=rows, labelid=report_id, anaconda_id=anaconda_id, tools_result=tools_result, techs_result=techs_result)



def rpc_analysis():
    """
    Fill analysis datatables dynamically.\n
    Used also when you perform operations with datatable(search, pagination, etc.)

    :param testresult: value can be one from list ['OK', 'NOK', 'Skipped', 'ALL'].
    :type testresult: string
    :returns:  JSON with data from database.
    """

    testresult = request.vars.testresult

    analyzedColumns = {
    0: ('testdescription', 'name'),
    1: ('testresult', 'testresult')
    }
    

    selectcolumns = (db.testdescription.name, db.analysis.id, db.analysis.jira_id,
     db.testdescription.testdescription, db.testresult.testresult,
     db.testresult.failuredescription, db.analysis.errortype,
     db.analysis.comment, db.testresult.id, db.test.include_test)

    query = (db.testsuite.id == db.test.testsuite_id) & (
        db.testdescription.id == db.test.testdescription_id) & (
            db.testresult.id == db.test.testresult_id) & (
                db.testsuite.id == request.vars.testsuiteid) 

    if testresult == 'NOK' or testresult == 'OK' or testresult == 'Skipped':
        query &= db.testresult.testresult == testresult
    else:
        query &= (db.testresult.testresult == 'NOK' ) | (db.testresult.testresult == 'OK') | (db.testresult.testresult == 'Skipped')

    tableData = proccessTableQuery(
        query=query,
        countBeforeFilter=query,
        left=db.analysis.on(db.analysis.testresult_id == db.testresult.id),
        columns=analyzedColumns, selectcolumns = selectcolumns)

    return response.json(tableData)


def rpc_save_analysis():
    """
    Save analysed data when click on button 'Save'

    :param analysisMap: list of maps with analyzed data.
    :type analysisMap: list of maps
    :param testsuite_id: testsuite_id of analyzed test run.
    :type testsuite_id: int
    :returns:  JSON with data from database.
    """
    testsuite_id = request.vars.testsuiteid

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
            if errortype in ["Known Error", "New Error", "Testcase Problem"]:
                db(db.testresult.id == testresult_id).update(
                            testresult='NOK')
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
    if testsuite_id != -1:
        db(db.testsuite.id == testsuite_id).update(analyzed=1)


def rpc_get_testsuite_by_name():
    """
    Used for autocomplete analysis data to fill window with elements (test run names)

    :param auto_testsuitename: value from text box to search testsuites in database by name.
    :type auto_testsuitename: string
    :param collapse_div_id: collapse dom element id.
    :type collapse_div_id: string
    :returns:  list of clickable DIV's to fill autocomplete window .
    """

    testsuitename = request.vars.auto_testsuitename
    collapse_div_id = request.vars.collapse_id
    if not testsuitename: return ''
    selected = db(db.testsuite.testsuitename.contains(testsuitename)).select(db.testsuite.testsuitename, db.testsuite.id)
    return ''.join([DIV(k.testsuitename,
                 _onclick="jQuery('#autocomplite_by_name_input%s').val('%s'); jQuery('#autocomplite_by_id_input%s').val('%s'); jQuery('#suggestions_name%s').empty();" % (collapse_div_id, k.testsuitename, collapse_div_id, k.id, collapse_div_id),
                 _onmouseover="this.style.backgroundColor='yellow'",
                 _onmouseout="this.style.backgroundColor='white';"
                 ).xml() for k in selected])


def rpc_get_testsuite_by_id():
    """
    Used for autocomplete analysis data to fill window with elements (test run id)

    :param auto_testsuiteid: value from text box to search testsuites in database by id.
    :type auto_testsuiteid: int
    :param collapse_div_id: collapse dom element id.
    :type collapse_div_id: string
    :returns:  list of clickable DIV's to fill autocomplete window .
    """

    testsuite_id = request.vars.auto_testsuiteid
    collapse_div_id = request.vars.collapse_id
    if not testsuite_id: return ''
    pattern = testsuite_id + '%'
    selected = db(db.testsuite.id.like(pattern)).select(db.testsuite.id, db.testsuite.testsuitename)
    return ''.join([DIV(k.id,
                 _onclick="jQuery('#autocomplite_by_id_input%s').val('%s'); jQuery('#autocomplite_by_name_input%s').val('%s'); jQuery('#suggestions_id%s').empty();" % (collapse_div_id, k.id, collapse_div_id, k.testsuitename, collapse_div_id),
                 _onmouseover="this.style.backgroundColor='yellow'",
                 _onmouseout="this.style.backgroundColor='white';"
                 ).xml() for k in selected])


def rpc_autocomplite_analysis():
    """
    Auto complete data for the analysis of the current run from the analyzed previous run.

    :param previous_testsuiteid: test suite id of previous analyzed test suite.
    :type previous_testsuiteid: int
    :param current_testsuiteid: test suite id of current test suite.
    :type current_testsuiteid: int
    """

    previous_testsuiteid = request.vars.previous_testsuiteid
    current_testsuiteid = request.vars.current_testsuiteid


    query = """
        select vjira_id, ganalysis_id, gtestresult_id, verror, vcomment 
            from (select testdescription.name as vname, analysis.jira_id as vjira_id, 
                  analysis.errortype as verror, analysis.comment as vcomment 
                  from testsuite 
                    left join test on testsuite.id = test.testsuite_id 
                    left join testdescription on testdescription.id = test.testdescription_id 
                    left join testresult on testresult.id = test.testresult_id 
                    left join analysis on analysis.testresult_id = testresult.id 
                        where testresult.testresult = 'NOK' and analysis.errortype IS NOT NULL 
                        and testsuite.id = %s
                 ) v 
            join (select testdescription.name as gname, analysis.id as ganalysis_id, 
                 analysis.jira_id as gjira_id, testresult.id as gtestresult_id 
                 from testsuite 
                    left join test on testsuite.id = test.testsuite_id 
                    left join testdescription on testdescription.id = test.testdescription_id  
                    left join testresult on testresult.id = test.testresult_id 
                    left join analysis on analysis.testresult_id = testresult.id 
                         where testresult.testresult = 'NOK' and testsuite.id = %s 
                 ) g 
            on v.vname = g.gname 
    """ % (previous_testsuiteid, current_testsuiteid)
    results = db.executesql(query)
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


def rpc_save_edit_report():
    """
    Used for save editing report when we click on 'Save' on analysis_report page.

    :param result: map with values from edit boxes
    :type result: map
    """

    result = json.loads(request.vars.result)
    tool_result = result["tool_result"]
    techs_result = result['techs_result']
    label_id = result['labelid']
    anaconda_id = result['anaconda_id']
    db(db.label.id == label_id).update(
        title=result['title'],
        releasecomment=result['comment_release'],
        commentswqs=result['comment_incident'],
        user=result['analysed_by']
    )
    db(db.anaconda.id == anaconda_id).update(
        name=result['version_name'],
        changelist=result['changelist'],
        branch=result['branch']
    )
    
    tools_analysis_row = db(db.tools_analysis.label_id == label_id).select().last()
    techs_analysis_row = db(db.techs_analysis.label_id == label_id).select().last()
    if tools_analysis_row is None:
        db.tools_analysis.insert(
                            label_id=int(label_id),
                            nds_validation_tool=int(tool_result[0]),
                            anaconda_wb_tool=int(tool_result[1]),
                            mapviewer_tool=int(tool_result[2]),
                            nds_validation_suite_tool=int(tool_result[3]))
    else:
        db(db.tools_analysis.label_id == label_id).update(
                        nds_validation_tool=int(tool_result[0]),
                        anaconda_wb_tool=int(tool_result[1]),
                        mapviewer_tool=int(tool_result[2]),
                        nds_validation_suite_tool=int(tool_result[3]))
    if techs_analysis_row is None:
        db.techs_analysis.insert(
                            label_id=int(label_id),
                            raw_data_inspection=int(techs_result[0]),
                            nds_specification=int(techs_result[1]),
                            structure_and_content=int(techs_result[2]),
                            comparision=int(techs_result[3]),
                            visual=int(techs_result[4]),
                            regression=int(techs_result[5]))
    else:
        db(db.techs_analysis.label_id == label_id).update(
                        raw_data_inspection=int(techs_result[0]),
                        nds_specification=int(techs_result[1]),
                        structure_and_content=int(techs_result[2]),
                        comparision=int(techs_result[3]),
                        visual=int(techs_result[4]),
                        regression=int(techs_result[5]))