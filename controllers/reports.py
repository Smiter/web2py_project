## This is a sample controller
from gluon import *
import json
import logging
import local_settings


def view_reports():
    """
    Used for rendering views/reports/view_reports.html page
    """

    return dict()


def rpc_reports():
    """
    Fill reports datatable dynamically.\n
    Used also when you perform operations with datatable(search, pagination, etc.)

    :returns:  JSON with data from database.
    """
    labelColumns = {
    1: ('label', 'id'),
    2: ('label', 'releasecandidatename'),
    3: ('label', 'date'),
    4: ('label', 'user')}
    
    selectcolumns = (db.label.id, db.label.releasecandidatename, db.label.user, db.label.date)
    tableData = proccessTableQuery(query=db.label.id, countBeforeFilter=db.label.id,
     columns=labelColumns, selectcolumns=selectcolumns)
    return response.json(tableData)


def rpc_generate_report():
    """
    Generate report, it's a simple redirection to the Tomcat web server birt application.

    :param report_design_name: the name of report design for the eclipse birt app
    :type report_design_name: string
    :param report_id: report id
    :type report_id: int
    :returns:  string  -- URL to redirect to the tomcat web server
    """

    report_design_name = request.post_vars.report_design_name
    report_id = request.vars.report_id
    return local_settings.tomcat_web_server_birt_url % (report_design_name, report_id)


def rpc_check_if_report_analyzed():
    """
    Check if report is analyzed before allow to generate report.

    :param report_id: report id
    :type report_id: int
    :returns:  boolean  -- True if report is analyzed, else False.
    """

    report_id = request.vars.report_id
    rows= db((db.testsuite.id == db.labeltorun.testsuite_id) & (db.labeltorun.label_id == report_id)).select(db.testsuite.analyzed)
    for r in rows:
        if r.analyzed == 0:
            return False
    return True
