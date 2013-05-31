from gluon import *
import logging
import logging.handlers


def get_configured_logger(name):
    logger = logging.getLogger(name)
    if (len(logger.handlers) == 0):
        # This logger has no handlers, so we can assume it hasn't yet been configured
        # (Configure logger)

        # Create default handler
        if request.env.web2py_runtime_gae:
            # Create GAEHandler
            handler = GAEHandler()
        else:
            # Create RotatingFileHandler
            import os
            formatter = "%(funcName)s():%(lineno)d %(message)s \n"
            handler = logging.handlers.RotatingFileHandler(os.path.join(request.folder, 'private/app3.log'), maxBytes=10000000, backupCount=2)
            handler.setFormatter(logging.Formatter(formatter))

        handler.setLevel(logging.DEBUG)

        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger

# Assign application logger to a global var
logger = get_configured_logger("log")


def getLimit():
    if request.vars['iDisplayStart'] and request.vars['iDisplayLength'] != '-1':
        return (int(request.vars['iDisplayStart']), int(request.vars['iDisplayStart'])
                + int(request.vars['iDisplayLength']))


def getOrder(columns, db):
    orderby = None
    for i in range(int(request.vars['iSortingCols'])):
        if request.vars['bSortable_' + str(request.vars['iSortCol_' + str(i)])] == "true":
            idx = int(request.vars['iSortCol_' + str(i)])
            if request.vars['sSortDir_' + str(i)] == "asc":
                orderby = db[columns[idx][0]][columns[idx][1]]
            else:
                orderby = ~db[columns[idx][0]][columns[idx][1]]
    return orderby


def getFilter(columns, db):
    like = None
    for i in range(len(columns) + 1):
        if request.vars['bSearchable_' + str(i)] and request.vars['bSearchable_' + str(i)] == "true" and request.vars['sSearch_' + str(i)] != '':
            a = "%%%s%%" % request.vars['sSearch_' + str(i)]
            if like is None:
                like = db[columns[i][0]][columns[i][1]].like(a)
            else:
                like &= db[columns[i][0]][columns[i][1]].like(a)
    return like


def proccessTableQuery(query=None, countBeforeFilter=None, left=None, columns=None, selectcolumns=None, db=db):
    limitby = getLimit()
    orderby = getOrder(columns, db)
    filterby = getFilter(columns, db)
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
