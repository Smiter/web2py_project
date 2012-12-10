testsuiteColumns = {
    1: ('testsuite', 'id'),
    2: ('testsuite', 'testsuitename'),
    3: ('testsuite', 'starttime'),
    4: ('testsuite', 'endtime'),
    5: ('anaconda', 'name'),
    6: ('anaconda', 'changelist'),
    7: ('testsuite', 'analyzed')}

analyzedColumns = {
    0: ('testdescription', 'name'),
    1: ('testresult', 'testresult')
    }

labelColumns = {
    1: ('label', 'id'),
    2: ('label', 'releasecandidatename'),
    3: ('label', 'date'),
    4: ('label', 'user')}


ANALYZED_IMAGE_NO = '<img height="22" width="22" src="../static/images/no1.jpg">'
ANALYZED_IMAGE_YES = '<img height="22" width="22" src="../static/images/yes2.jpg">'
BUG_TYPE = """<select name="combobox" id="errortype" style="width : 105px">
                           <option value="1" %s>Unknown</option>
                           <option value="2" %s>Known Error</option>
                           <option value="3" %s>OK in Context</option>
                           <option value="4" %s>New Error</option>
                           <option value="5" %s>Testcase Problem</option>
                           </select>"""
JIRA_ID = '<input type="text" name="jira_id" id="jira_id" value="%s" style="width : 60px">'
COMMENT = '<textarea id="comment_id" style="width : 100px">%s</textarea>'
