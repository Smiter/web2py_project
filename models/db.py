# -*- coding: utf-8 -*-
from gluon import *


#db = DAL("mysql://nds:test@172.30.136.176/ndsreport_new", pool_size=10)
#db = DAL("mysql://root:111@localhost/test", pool_size=10)
db = DAL("mysql://nds:test@oekalxap68/ndsreport", pool_size=10)

migrate = False

db.define_table('labeltorun',
                Field('id', type='integer'),
                Field('label_id', type='integer'),
                Field('testsuite_id', type='integer'),
                 primarykey=['id', 'id'],
                migrate=migrate)
db.define_table('anaconda',
                Field('id', type='integer'),
                Field('name', type='text'),
                Field('version', type='text'),
                Field('branch', type='text'),
                Field('calendarweek', type='integer'),
                Field('year', type='integer'),
                Field('changelist', type='text'),
                Field('hudsonjobname', type='text'),
                Field('hudsonbuildnumber', type='text'),
                Field('creationdate', type='text'),
                Field('md5checksum', type='text', unique=True),
                primarykey=['id', 'id'],
                migrate=migrate)

#logging.error(db().select(db.anaconda.ALL))
#    logging.error(row.id)

db.define_table('analysis',
                Field('id', type='integer'),
                Field('testresult_id', type='reference analysis.testresult_id', unique=True),
                Field('errortype', type='text'),
                Field('comment', type='text'),
                Field('elvis_id', type='reference analysis'),
                Field('jira_id', type='text'),
                primarykey=['id', 'id'],
                migrate=migrate)

db.define_table('databaseundertest',
                Field('id', type='integer'),
                Field('postgresdatabasename', type='text'),
                Field('postgreshost', type='text'),
                Field('postgresport', type='text'),
                Field('nndbprovider', type='text'),
                Field('rdfbuildversion', type='text'),
                Field('rdfdatareleasedate', type='text'),
                Field('rdfproductcreationdate', type='text'),
                Field('rdfproductversion', type='text'),
                Field('rdfschemaversion', type='text'),
                Field('nndbversion', type='text'),
                Field('indsversion', type='text'),
                Field('ndsversion', type='text'),
                Field('ndscreationdate', type='text'),
                Field('md5checksum', type='text', unique=True),
                primarykey=['id', 'id'],
                migrate=migrate)

db.define_table('label',
                Field('id', type='integer'),
                Field('releasename', type='text'),
                Field('releasecandidatename', type='text'),
                Field('scope', type='text'),
                Field('year', type='integer'),
                Field('calendarweek', type='integer'),
                Field('releaseversion', type='text'),
                Field('status', type='text'),
                Field('commentswqs', type='text'),
                Field('releasecomment', type='text'),
                Field('user', type='text'),
                Field('releaserecommendationswqs', type='text'),
                Field('ctrssnapshotid', type='integer'),
                Field('date', type='text'),
                primarykey=['id', 'id'],
                migrate=migrate)

db.define_table('newtestsuites',
                Field('id', type='integer', default=0),
                Field('anaconda_id', type='integer', default=0),
                primarykey=['id', 'anaconda_id', 'id', 'anaconda_id'],
                migrate=migrate)

db.define_table('origin',
                Field('id', type='integer'),
                Field('idstring', type='text'),
                Field('link', type='text'),
                Field('type', type='text', default='DOORS'),
                Field('md5checksum', type='text', unique=True),
                primarykey=['id', 'id'],
                migrate=migrate)

db.define_table('test',
                Field('id', type='integer'),
                Field('testsuite_id', type='reference test'),
                Field('testresult_id', type='reference test'),
                Field('testdescription_id', type='reference test'),
                primarykey=['id', 'id'],
                migrate=migrate)

db.define_table('testdescription',
                Field('id', type='integer'),
                Field('testcreationdate', type='text'),
                Field('name', type='text'),
                Field('testdescription', type='text'),
                Field('author', type='text'),
                Field('testclass', type='text'),
                Field('testeddbformat', type='text'),
                Field('testedbuildingblocks', type='text'),
                Field('testcaseversion', type='text'),
                Field('testcasestatus', type='text'),
                Field('expectation', type='text'),
                Field('testedattributes', type='text'),
                Field('md5checksum', type='text', unique=True),
                Field('componentundertest', type='text'),
                Field('moduleundertest', type='text'),
                Field('functionundertest', type='text'),
                Field('interfaceundertest', type='text'),
                Field('precondition', type='text'),
                Field('maxdeviation', type='integer', default=0),
                Field('workpackage', type='integer', default=-1),
                primarykey=['id', 'id'],
                migrate=migrate)

db.define_table('testdescription_has_origin',
                Field('testdescription_id', type='reference testdescription_has_origin'),
                Field('origin_id', type='reference testdescription_has_origin'),
                Field('marker', type='integer'),
                migrate=migrate)

db.define_table('testenviroment',
                Field('id', type='integer'),
                Field('osversion', type='text'),
                Field('jvmversion', type='text'),
                Field('testframeworkversion', type='text'),
                Field('testrunmachine', type='text'),
                Field('hudsonbuildnumber', type='text'),
                Field('hudsonjobname', type='text'),
                Field('hudsonbuildid', type='text'),
                Field('perforceclient', type='text'),
                Field('testframeworkchangelist', type='text'),
                Field('md5checksum', type='text', unique=True),
                primarykey=['id', 'id'],
                migrate=migrate)

db.define_table('testresult',
                Field('id', type='integer'),
                Field('testresult', type='text'),
                Field('starttime', type='text'),
                Field('endtime', type='text'),
                Field('failuredescription', type='text'),
                Field('executedtests', type='integer'),
                Field('incidents', type='integer'),
                primarykey=['id', 'id'],
                migrate=migrate)

db.define_table('testsuite',
                Field('id', type='integer'),
                Field('label_id', type='reference testsuite'),
                Field('testsuitename', type='text'),
                Field('dut_id', type='reference testsuite'),
                Field('anaconda_id', type='reference testsuite'),
                Field('enviroment_id', type='reference testsuite'),
                Field('playlistfile', type='text'),
                Field('autoChecked', type='text', default='N'),
                Field('factconfig', type='text'),
                Field('inclusionpattern', type='text'),
                Field('exclusionpattern', type='text'),
                Field('analyzed', type='integer', default=0),
                Field('user', type='text'),
                Field('starttime', type='text'),
                Field('endtime', type='text'),
                primarykey=['id', 'id'],
                migrate=migrate)


db.anaconda.name.filter_out = lambda txt: txt[: txt.rfind('_')][txt.rfind('-')+1:] if txt != "__" else "unknown"
#db.testsuite.timestamp.filter_out = lambda number: "unknown" if number == 0 else datetime.datetime.fromtimestamp(number / 1000).strftime('%d/%m/%Y, %H:%M:%S')
db.testsuite.endtime.filter_out = lambda number: "" if number is None else number
db.anaconda.changelist.filter_out = lambda changelist: "unknown" if not changelist else changelist
#db.testsuite.analyzed.filter_out = lambda analyzed: ANALYZED_IMAGE_NO if analyzed == 0 else ANALYZED_IMAGE_YES
db.analysis.errortype.filter_out = lambda errortype: {'Unknown': BUG_TYPE % ("selected", "", "", "", ""),
                                                      'Known Error': BUG_TYPE % ("", "selected", "", "", ""),
                                                      'OK in Context': BUG_TYPE % ("", "", "selected", "", ""),
                                                      'New Error': BUG_TYPE % ("", "", "", "selected", ""),
                                                      'Testcase Problem': BUG_TYPE % ("", "", "", "", "selected"),
                                                      None: BUG_TYPE % ("selected", "", "", "", "")}.get(errortype)
db.analysis.jira_id.filter_out = lambda jira_id: JIRA_ID % "" if jira_id is None else JIRA_ID % jira_id
# db.analysis.comment.filter_out = lambda comment: COMMENT % "" if comment is None else COMMENT % comment


