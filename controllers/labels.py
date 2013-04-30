## This is a sample controller
from gluon import *
import json
import logging

def list():
    return dict(message=T(""))


def labelHandler():
    selectcolumns = (db.label.id, db.label.releasecandidatename, db.label.user, db.label.date)
    tableData = proccessTableQuery(query=db.label.id, countBeforeFilter=db.label.id, columns=labelColumns,selectcolumns = selectcolumns)
    return response.json(tableData)


def showlabel():
    logger.error("showLabel")
    rows = db((db.testsuite.id == db.labeltorun.testsuite_id) & (db.label.id == request.post_vars.labelid) & (db.testsuite.anaconda_id == db.anaconda.id) & (db.databaseundertest.id == db.testsuite.dut_id) & (db.testenviroment.id == db.testsuite.enviroment_id) & (db.labeltorun.label_id == request.post_vars.labelid)).select()
    label_id = request.post_vars.labelid
    tools_result = db(db.tools_analysis.label_id == label_id).select().last()
    techs_result = db(db.techs_analysis.label_id == label_id).select().last()
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
    return dict(testsuiteArray=rows, labelid=label_id, anaconda_id=anaconda_id, tools_result=tools_result, techs_result=techs_result)


def generateReport():
    logger.error("GENERATE REPORT")
    return 'http://172.30.136.225:8080/birt2/frameset?__report=BirtReports/Designs/AnacondaTest/%s.rptdesign&Release Candidate=%s&__format=pdf' % (request.post_vars.report_design_name, request.post_vars.labelid)


def save_edit_report():
    logging.error("save_edit_report")
    result = json.loads(request.post_vars.result)
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
