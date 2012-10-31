from gluon import *


def getLimit():
    if request.vars['iDisplayStart'] and request.vars['iDisplayLength'] != '-1':
        return (int(request.vars['iDisplayStart']), int(request.vars['iDisplayStart'])
                + int(request.vars['iDisplayLength']))


def getOrder(columns):
    orderby = None
    for i in range(int(request.vars['iSortingCols'])):
        if request.vars['bSortable_' + str(request.vars['iSortCol_' + str(i)])] == "true":
            idx = int(request.vars['iSortCol_' + str(i)])
            if request.vars['sSortDir_' + str(i)] == "asc":
                orderby = db[columns[idx][0]][columns[idx][1]]
            else:
                orderby = ~db[columns[idx][0]][columns[idx][1]]
    return orderby


def getFilter(columns):
    like = None
    for i in range(len(columns) + 1):
        if request.vars['bSearchable_' + str(i)] and request.vars['bSearchable_' + str(i)] == "true" and request.vars['sSearch_' + str(i)] != '':
            a = "%%%s%%" % request.vars['sSearch_' + str(i)]
            if like is None:
                like = db[columns[i][0]][columns[i][1]].like(a)
            else:
                like &= db[columns[i][0]][columns[i][1]].like(a)
    return like


def proccessTableQuery(query=None, countBeforeFilter=None, left=None, columns=None,selectcolumns=None):
    # selectcolumns = (db.testsuite.id, db.testsuite.testsuitename, db.testsuite.starttime, db.testsuite.endtime, db.testsuite.analyzed, db.anaconda.name, db.anaconda.changelist)
    logger.error(selectcolumns)
    limitby = getLimit()
    orderby = getOrder(columns)
    filterby = getFilter(columns)
    rows = db(filterby)(query).select(*selectcolumns,limitby=limitby, orderby=orderby, left=left)
    beforeFilter = db(countBeforeFilter).count()
    if filterby is None:
        afterFilter = beforeFilter
    else:
        afterFilter = db(filterby).count()

    tableData = {
        "sEcho": int(request.vars['sEcho']),
        "iTotalRecords": beforeFilter,
        "iTotalDisplayRecords": afterFilter,
        "aaData": rows.as_list()
    }

    return tableData
