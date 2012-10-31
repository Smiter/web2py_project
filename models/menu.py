from gluon import *

response.menu = [
    # (T('Home'), False, URL('default', 'index')),
    (T('Reports'), False, URL('labels', 'list')),
    (T('FACT runs'), False, URL('fact', 'runs')),
    (T('Validation suits'), False, URL('vs', 'runs')),
    (T('Report preview'), False, URL('reportprev', 'preview'))]

response.basket = (DIV(DIV('Short label preview', _class='dropdown-menu2'), _class='dropdown', _id="t5"))
