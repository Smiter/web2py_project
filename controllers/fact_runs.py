from gluon import *
import json


def runs():
    """
    Used for rendering views/fact_runs/runs.html page
    """

    return dict()


def rpc_testruns():
    """
    fill test runs datatable dynamically.\n
    Used also when you perform operations with datatable(search, pagination, etc.)

    :returns:  JSON with data from database.
    """
    testsuiteColumns = {
    1: ('testsuite', 'id'),
    2: ('testsuite', 'testsuitename'),
    3: ('testsuite', 'starttime'),
    4: ('testsuite', 'endtime'),
    5: ('anaconda', 'name'),
    6: ('anaconda', 'changelist'),
    7: ('testsuite', 'analyzed')}

    selectcolumns = (db.testsuite.id, db.testsuite.testsuitename, db.testsuite.starttime,
     db.testsuite.endtime, db.testsuite.analyzed, db.anaconda.name, db.anaconda.changelist)
    query = db.testsuite.anaconda_id == db.anaconda.id
    tableData = proccessTableQuery(query=query, countBeforeFilter=db.testsuite.id,
                                   columns=testsuiteColumns, selectcolumns=selectcolumns)
    return response.json(tableData)


def rpc_add_runs_to_session():
    """
    add test runs to session when click on Add report.\n
    :param testruns: map of testsuite.id and testsuite name.
    :type testruns: JSON
    :returns:  JSON  -- map of testsuite.id and testsuite name.
    """

    testruns = json.loads(request.post_vars.testruns)
    resultList = dict()
    for k, v in testruns.items():
        if session.label_preview_list:
            if not k in session.label_preview_list:
                session.label_preview_list[k] = v
                resultList[k] = v
        else:
            session.label_preview_list = dict()
            session.label_preview_list[k] = v
            resultList[k] = v
    return response.json(resultList)


def rpc_remove_report_from_session():
    """
    delete test runs from session when click on remove button.\n
    :param testsuiteid: map of testsuite.id and testsuite name.
    :type testsuiteid: int
    :returns:  size of report preview map stored in session.
    """

    del session.label_preview_list[request.post_vars.testsuiteid]
    return len(session.label_preview_list)


def rpc_save_report():
    """
    Create new report in database when click on Save report.
    Also clear session map with test runs.

    :param report_name: name of new report
    :type report_name: string
    :param user_name: user who create report
    :type user_name: string
    :param releasecomment: release comment 
    :type releasecomment: string
    :param commentswqs: swqs comment
    :type commentswqs: string
    :param changelist: changelist of anaconda(not requered)
    :type changelist: string
    :param branch: branch of anaconda(not requered)
    :type branch: string
    """

    report_name = request.post_vars.labelname
    user_name = request.post_vars.username
    releasecomment = request.post_vars.releasecomment
    commentswqs = request.post_vars.commentswqs
    changelist = request.post_vars.changelist
    branch = request.post_vars.branch
    db.label.insert(releasecandidatename=report_name, user=user_name,
     releasecomment=releasecomment, commentswqs=commentswqs)
    last_report = db(db.label.id).select().last()
    for testsuite_id in session.label_preview_list.keys():
        db.labeltorun.insert(label_id=last_report.id, testsuite_id=testsuite_id)
        testsuite = db(db.testsuite.id == testsuite_id).select().last()
        if changelist != "":
            db(db.anaconda.id == int(testsuite.anaconda_id)).update(changelist=str(changelist))
        if branch != "":
            db(db.anaconda.id == int(testsuite.anaconda_id)).update(name=branch + "_" + changelist)
        db(db.testsuite.id == testsuite_id).update(label_id=last_report.id)
    session.label_preview_list = dict()
    redirect(URL(request.application, 'reports', 'view_reports'))


def rpc_edit_cell_value():
    """
    Edit cell values for test runs datatable

    :param value: edited value from cell
    :type value: string
    :param column_name: column name of edited cell
    :type column_name: string
    :param testsuite_id: test run id of edited row
    :type testsuite_id: int
    :returns:  edited value saved to database.
    """

    value = request.vars.value
    column_name = request.vars.column_name
    testsuite_id = request.post_vars.testsuite_id
    if column_name == "testsuitename":
        db(db.testsuite.id == int(testsuite_id)).update(testsuitename=value)
    if column_name == "changelist":
        row = db(db.testsuite.id == int(testsuite_id)).select(db.testsuite.anaconda_id).last()
        db(db.anaconda.id == int(row.anaconda_id)).update(changelist=value)
    return value
