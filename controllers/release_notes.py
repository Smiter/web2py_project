## This is a sample controller
from gluon import *
import json
from datetime import datetime
# import logging
def create_edit_report():
    """
    Used for rendering views/report_analysis/analyse_note_report.html page. Called when clicked on Create New Release Note button.
    """
    note = None
    check_result = None
    if request.vars.note_id:
        
        row = release_note_db((release_note_db.release_note.id == int(request.vars.note_id)) & 
            (release_note_db.database_info.note_id == int(request.vars.note_id)) & 
            (release_note_db.nds_file_structure.note_id == int(request.vars.note_id)) & 
            (release_note_db.features_info.note_id == int(request.vars.note_id)) & 
            (release_note_db.known_issues.note_id == int(request.vars.note_id)) ).select().last()
        check_result_row = release_note_db(release_note_db.features_info.note_id == int(request.vars.note_id)).select().last()
        if check_result_row:
            check_result = check_result_row.as_dict()
        else:
            check_result = {}

        note = row.as_dict()
        note["release_note"]["date"] = datetime.strptime(str(note["release_note"]["date"]), '%Y-%m-%d').strftime('%d.%m.%Y')
    return dict(note_result=note, check_res=check_result)



def view_notes():
    return dict()

def rpc_release_notes():
    """
    Fill release_notes datatable dynamically.\n
    Used also when you perform operations with datatable(search, pagination, etc.)

    :returns:  JSON with data from database.
    """
    labelColumns = {
    1: ('release_note', 'id'),
    2: ('release_note', 'release_note_name'),
    3: ('release_note', 'date'),
    4: ('release_note', 'user_name')}
    
    selectcolumns = (release_note_db.release_note.id, release_note_db.release_note.release_note_name, release_note_db.release_note.date, release_note_db.release_note.user_name)
    tableData = proccessTableQuery(query=release_note_db.release_note.id, countBeforeFilter=release_note_db.release_note.id,
     columns=labelColumns, selectcolumns=selectcolumns, db=release_note_db)
    return response.json(tableData)


def rpc_add_new_note():
    """
    Used for creating and saving new release note when we click on 'Add new Release Note' on 
    modal window releasenotesubmitform.

    :param result: map with values from edit boxes
    :type result: map
    :returns:  id of new release_note
    """
    result = json.loads(request.vars.res)
    release_note_db.release_note.insert(
        release_note_name=result['release_note_name'], 
        user_name=result['release_note_user_name'], 
        date=datetime.strptime(result['release_note_date'], '%d.%m.%Y'))
    row = release_note_db(release_note_db.release_note.id).select().last()
    return row.id

def rpc_save_cover_note():
    """
    Used for save "Cover" tab, when we click on 'Save' on analysis_report page.

    :param result: map with values from edit boxes
    :type result: map
    """
    result = json.loads(request.vars.result)
    note_id = result['note_id']

    release_note_db(release_note_db.release_note.id == int(note_id)).update(
        date=datetime.strptime(result['release_note_date'], '%d.%m.%Y'),
        version=result['version'],
        owner=result['owner'],
        approved_by=result['approved_by']
    )

def rpc_save_note():
    """
    Used for save information from tab OEM when we click on 'Save' on create_report page.

    :param result: map with values from edit boxes
    :type result: map
    """
    result = json.loads(request.vars.result)
    note_id = result['note_id']    

    for key, value in result.items():
        if isinstance(result[key], dict):
            row = release_note_db[key](note_id=int(note_id))
            if row:
                release_note_db(release_note_db[key].note_id == int(note_id)).update(
                  **result[key]
                )
            else:
                release_note_db[key].insert(**result[key])

       
def generate_report():
    logging.error(request.vars)
    response.headers['Content-Type']='application/pdf'
    return generate_pdf_report_for_test_summary(db)


def ssh_connect():
    from pysqlite2 import dbapi2 as sqlite3
    
    import paramiko, base64
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.connect('172.16.20.73', username='smikhaylenko', password='anaconda1')
    ftp = client.open_sftp()
    ftp.get('/data/0ME_2681.NDS', 'applications/'+request.application+'/databases/0ME_2681.NDS')
    ftp.close() 
    conn = sqlite3.connect('applications/'+request.application+'/databases/0ME_2681.NDS')
    cur = conn.cursor()
    cur.execute("select * from versionTable")
    for r in cur:
        logging.error(r)
    # stdin, stdout, stderr = client.exec_command('ls')
    # for line in stdout:
    #     return '... ' + line.strip('\n')
    # client.close()