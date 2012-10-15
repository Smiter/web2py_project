from gluon import *

response.menu = [
    (T('Home'), False, URL('default', 'index')),
    (T('Labels'), False, URL('labels', 'list')),
    (T('FACT runs'), False, URL('fact', 'runs')),
    (T('Validation suits'), False, URL('vs', 'runs')),
    (T('Report preview'), False, URL('reportprev', 'preview'))]
    # (T('Short label preview'), False, A('Short label preview', _class='labelpreview', _id='label_preview'))  ]


# response.menu += [
#     (SPAN('Short Label preview', _style='color:yellow;margin-left: 305px;',_id="t5"), False, '', [
#     (T('Report preview'), False, DIV('',_style='border-bottom:1px solid rgb(170, 170, 170);')),
#     (T('Report preview'), False, H4('FACT Runnings',_style='color:rgb(170, 170, 170);margin-left: 50px;')),
#     (T('Report preview'), False, A('Short label previsdsdsdsdsdsew', _class='labelpreview')),
#     (T('Report preview'), False, A('Short label previsdsdsdsdsdsew', _class='labelpreview')),
#     (T('Report preview'), False, A('Short label previsdsdsdsdsdsew', _class='labelpreview')),
#     (T('Report preview'), False, A('Short label previsdsdsdsdsdsew', _class='labelpreview')),
#     (T('Report preview'), False, A('Short label previsdsdsdsdsdsew', _class='labelpreview')),
#     (T('Report preview'), False, A('Short label previsdsdsdsdsdsew', _class='labelpreview')),
#     (T('Report preview'), False, DIV('',_style='border-bottom:1px solid rgb(170, 170, 170);')),
#     (T('Report preview'), False, H4('VS Runnings',_style='color:rgb(170, 170, 170);margin-left: 50px;')),
#     (T('Report preview'), False, H6('None',_style='color:rgb(170, 170, 170);margin-left: 20px;')),
#     (T(''), False, FORM(INPUT(_type='submit')))
#     ]
#     )]


# response.basket = [
#     (DIV('Short Label preview', _class='dropdown-menu2',_id="t5"), False, '', [
#     (T('Report preview'), False, DIV('',_style='border-bottom:1px solid rgb(170, 170, 170);')),
#     (T('Report preview'), False, H4('FACT Runnings',_style='color:rgb(170, 170, 170);margin-left: 50px;')),
#     (T('Report preview'), False, A('Short label previsdsdsdsdsdsew', _class='labelpreview')),
#     (T('Report preview'), False, A('Short label previsdsdsdsdsdsew', _class='labelpreview')),
#     (T('Report preview'), False, A('Short label previsdsdsdsdsdsew', _class='labelpreview')),
#     (T('Report preview'), False, A('Short label previsdsdsdsdsdsew', _class='labelpreview')),
#     (T('Report preview'), False, A('Short label previsdsdsdsdsdsew', _class='labelpreview')),
#     (T('Report preview'), False, A('Short label previsdsdsdsdsdsew', _class='labelpreview')),
#     (T('Report preview'), False, DIV('',_style='border-bottom:1px solid rgb(170, 170, 170);')),
#     (T('Report preview'), False, H4('VS Runnings',_style='color:rgb(170, 170, 170);margin-left: 50px;')),
#     (T('Report preview'), False, H6('None',_style='color:rgb(170, 170, 170);margin-left: 20px;')),
#     (T(''), False, FORM(INPUT(_type='submit')))
#     ]
#     )]


response.basket = (DIV(DIV('Short label preview', _class='dropdown-menu2'), _class='dropdown', _id="t5"))

