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
    rows = db((db.testsuite.id == db.labeltorun.testsuite_id) & (db.testsuite.anaconda_id == db.anaconda.id) & (db.labeltorun.label_id == request.post_vars.labelid)).select()
    label_id = request.post_vars.labelid
    tools_result = db(db.tools_analysis.label_id == label_id).select().last()
    techs_result = db(db.techs_analysis.label_id == label_id).select().last()
    if not tools_result:
        tools_result = {
            'fact_tool': 1,
            'nds_validation_tool': 1,
            'anaconda_wb_tool': 1,
            'mapviewer_tool': 1,
            'nds_validation_suite_tool': 1
        }
    if techs_result:
        techs_result = techs_result.as_dict()
    else:
        techs_result = {}
    return dict(testsuiteArray=rows.as_list(), labelid=label_id, tools_result=tools_result, techs_result=techs_result)


def generateReport():
    logger.error("GENERATE REPORT")
    logger.error(request.post_vars)
    return 'http://172.30.136.225:8080/birt2/frameset?__report=BirtReports/Designs/AnacondaTest/%s.rptdesign&Release Candidate=%s' % (request.post_vars.report_design_name, request.post_vars.labelid)


def save_tools_analysis():
    logging.error("save_tools_analysis")
    tool_result = request.post_vars['tool_result[]']
    techs_result = request.post_vars['techs_result[]']
    label_id = request.post_vars['labelid']
    tools_analysis_row = db(db.tools_analysis.label_id == label_id).select().last()
    techs_analysis_row = db(db.techs_analysis.label_id == label_id).select().last()
    if tools_analysis_row is None:
        logging.error("tools_analysis_row INSERT")
        db.tools_analysis.insert(
                            label_id=int(label_id),
                            fact_tool=int(tool_result[0]),
                            nds_validation_tool=int(tool_result[1]),
                            anaconda_wb_tool=int(tool_result[2]),
                            mapviewer_tool=int(tool_result[3]),
                            nds_validation_suite_tool=int(tool_result[4]))
    else:
        logging.error("tools_analysis_row UPDATE")
        db(db.tools_analysis.label_id == label_id).update(
                        fact_tool=int(tool_result[0]),
                        nds_validation_tool=int(tool_result[1]),
                        anaconda_wb_tool=int(tool_result[2]),
                        mapviewer_tool=int(tool_result[3]),
                        nds_validation_suite_tool=int(tool_result[4]))
    if techs_analysis_row is None:
        logging.error("techs_analysis_row INSERT")
        db.techs_analysis.insert(
                            label_id=int(label_id),
                            raw_data_inspection=int(techs_result[0]),
                            nds_specification=int(techs_result[1]),
                            structure_and_content=int(techs_result[2]),
                            comparision=int(techs_result[3]),
                            visual=int(techs_result[4]),
                            regression=int(techs_result[5]))
    else:
        logging.error("techs_analysis_row UPDATE")
        db(db.techs_analysis.label_id == label_id).update(
                        raw_data_inspection=int(techs_result[0]),
                        nds_specification=int(techs_result[1]),
                        structure_and_content=int(techs_result[2]),
                        comparision=int(techs_result[3]),
                        visual=int(techs_result[4]),
                        regression=int(techs_result[5]))
