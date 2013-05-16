Code documentation for the web2py application
*********************************************

Database models definitions
===========================

* To define a model for the table the following syntax is used:

::

    #models/db.py

    db.define_table('labeltorun',
        Field('id', type='integer'),
        Field('label_id', type='integer'),
        Field('testsuite_id', type='integer'),
        primarykey=['id', 'id'],
        migrate=migrate)


Controllers on fact runs page
=============================

.. automodule:: controllers.fact_runs
    :members:

Controllers on analysis page
===================================

.. automodule:: controllers.report_analysis
    :members:

Controllers on reports page
===================================

.. automodule:: controllers.reports
    :members:
