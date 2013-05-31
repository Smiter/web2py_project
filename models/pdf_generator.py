from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.platypus import *
from reportlab.lib import pagesizes, styles, colors
from reportlab.lib.fonts import addMapping
from reportlab.lib.units import *
from reportlab.lib.sequencer import Sequencer
from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import tan, black
from reportlab.lib.styles import ParagraphStyle
from cStringIO import StringIO
import os.path
import logging
import textwrap

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'static'))


BASE_FONT_DIR = os.path.join(PROJECT_ROOT, 'fonts')

pdfmetrics.registerFont(ttfonts.TTFont('ArialN', os.path.join(BASE_FONT_DIR,
    'arial.ttf')))
pdfmetrics.registerFont(ttfonts.TTFont('ArialI', os.path.join(BASE_FONT_DIR,
    'ariali.ttf')))
pdfmetrics.registerFont(ttfonts.TTFont('ArialB', os.path.join(BASE_FONT_DIR,
    'arialbd.ttf')))
pdfmetrics.registerFont(ttfonts.TTFont('ArialIB', os.path.join(BASE_FONT_DIR,
    'arialbdi.ttf')))

pdfmetrics.registerFont(ttfonts.TTFont('TimesN', os.path.join(BASE_FONT_DIR,
    'times.ttf')))
pdfmetrics.registerFont(ttfonts.TTFont('TimesI', os.path.join(BASE_FONT_DIR,
    'timesi.ttf')))
pdfmetrics.registerFont(ttfonts.TTFont('TimesB', os.path.join(BASE_FONT_DIR,
    'timesbd.ttf')))
pdfmetrics.registerFont(ttfonts.TTFont('TimesIB', os.path.join(BASE_FONT_DIR,
    'timesbi.ttf')))
pdfmetrics.registerFont(ttfonts.TTFont('Verdana', os.path.join(BASE_FONT_DIR,
    'verdana.ttf')))

PAGE_WIDTH = pagesizes.A4[0]
PAGE_HEIGHT = pagesizes.A4[1]

styles = styles.getSampleStyleSheet()

checkbox_path = os.path.join(MEDIA_ROOT, 'images', 'checkbox_cell.png')
checked_checkbox_path = os.path.join(MEDIA_ROOT, 'images', 'checked_checkbox_cell.png')

harman_logo_header_path = os.path.join(MEDIA_ROOT, 'images', 'harman_logo_header.jpg')

styles.add(ParagraphStyle(name='ArialNormal', fontName="ArialN", fontSize=12, leading=12))
styles.add(ParagraphStyle(name='ArialBold', fontName="ArialB", fontSize=12, leading=12))
styles.add(ParagraphStyle(name='ArialItalic', fontName="ArialI", fontSize=12, leading=12))
styles.add(ParagraphStyle(name='ArialItalicBold', fontName="ArialIB", fontSize=12, leading=12))
styles.add(ParagraphStyle(name='ArialTitle', fontName="ArialB", fontSize=12, leading=22, alignment=1))
styles.add(ParagraphStyle(name='Center', fontName="ArialN", fontSize=12, leading=22, alignment=1))



class Pdf(object):
    TITLE = ""
    _PDF_LEFT_COLUMN = 4*cm
    _PDF_MIDDLE_COLUMN = 6*cm
    _PDF_RIGHT_COLUMN = 13*cm
    _PDF_TABLE_TOP = 26*cm
    _LINK_COLOR = colors.HexColor("#2e2eff")

    def __init__(self, heading_line=None):
        arial = ttfonts.TTFont('Arial',
            os.path.join(PROJECT_ROOT, 'fonts', 'arial.ttf'))
        pdfmetrics.registerFont(arial)

        arial_bold = ttfonts.TTFont('Arial-Bold',
            os.path.join(PROJECT_ROOT, 'fonts', 'arialbd.ttf'))
        pdfmetrics.registerFont(arial_bold)

        arial_bold_italic = ttfonts.TTFont('Arial-Bold-Italic',
            os.path.join(PROJECT_ROOT, 'fonts', 'arialbdi.ttf'))
        pdfmetrics.registerFont(arial_bold_italic)

        palatino = ttfonts.TTFont('Palatino',
            os.path.join(PROJECT_ROOT, 'fonts', 'Palatino.ttc'))
        pdfmetrics.registerFont(palatino)

        self.heading_line = heading_line
        self.buffer = StringIO()
        self.pagesize=pagesizes.A4
        if heading_line:
            self.TITLE = heading_line

        self.page_seq = Sequencer()
        self.line_seq = Sequencer()
        self.page_number = 0
        self.line_number = self.line_seq.next()

    def _pdf_draw_strings(self, canvas, x, y, *lines):
        step = 0.5*cm
        for line in lines:
            if isinstance(line, int):
                if line < 0:
                    canvas.setFont('Arial', abs(line))
                else:
                    canvas.setFont('Palatino', abs(line)) # bold
                step = abs(line) / 24.0 * cm
                continue
            if line == 'checkbox_cell':
                canvas.drawInlineImage(checkbox_path, x, y,
                    width=3.44*mm, height=3.44*mm)
            elif line == 'checked_checkbox_cell':
                canvas.drawInlineImage(checked_checkbox_path, x, y,
                    width=3.44*mm, height=3.44*mm)
            else:
                canvas.drawString(x, y, line)
            y -= step
        return step

    def _draw_header(self, canvas, title=None):
        if self.page_number == 0:
            return
        canvas.drawInlineImage(harman_logo_header_path, 270, 800,
                width=20*mm, height=8*mm)

        if self.heading_line:
            self._pdf_draw_strings(canvas, self._PDF_LEFT_COLUMN-2.8*cm,
                27*cm, 12, self.heading_line)

        if title:
            canvas.setFont('ArialB', 16)
            canvas.drawString(self._PDF_MIDDLE_COLUMN+2.5*cm, 27*cm, title)

    def _draw_footer(self, canvas):
        width = canvas._pagesize[0]
        t_pos = ((width - self._PDF_LEFT_COLUMN + 2.8*cm) / 2)
        bottom_space = 0.5*cm

        canvas.setStrokeColor(colors.HexColor("#e5ecf5"))
        canvas.line(
            self._PDF_LEFT_COLUMN - 2.8*cm, bottom_space,
            t_pos, bottom_space
        )

        canvas.setStrokeColor(colors.HexColor("#b4cae3"))
        canvas.line(
            self._PDF_LEFT_COLUMN - 2.8*cm, bottom_space + 0.4*mm,
            t_pos, bottom_space + 0.4*mm
        )

        canvas.setFont('Arial-Bold', 12)
        page_number = self.page_number

        if not page_number:
            self.increment_page_number()
            page_number = self.page_number
        self._pdf_draw_strings(canvas, t_pos + 3*mm, bottom_space - 1*mm,
            12, "Page %s"%self.page_number)

        f_pos = t_pos + 1.8*cm

        canvas.setStrokeColor(colors.HexColor("#e5ecf5"))
        canvas.line(
            f_pos, bottom_space,
            width - self._PDF_LEFT_COLUMN + 2.8*cm, bottom_space
        )
        canvas.setStrokeColor(colors.HexColor("#b4cae3"))
        canvas.line(
            f_pos, bottom_space + 0.4*mm,
            width - self._PDF_LEFT_COLUMN + 2.8*cm, bottom_space + 0.4*mm
        )

        canvas.setFont('Palatino', 16)

    def _increment_line_number(self, times=1):
        for i in xrange(times):
            self.line_number = self.line_seq.next()

    def _reset_line_number(self):
        self.line_number = 0
        self.line_seq.reset()

    def _draw_page_break(self, canvas):
        """
        Puts page break by consiming all the space left
        """
        self.increment_page_number()
        self._reset_line_number()
        canvas.showPage()

    def increment_page_number(self):
        self.page_number = self.page_seq.next()


class CheckBox(Flowable):
    def __init__(self, xoffset=23, size=None, fillcolor=tan, strokecolor=black, line='checkbox_cell'):
        self.line = line
        if size is None:
            size = 0.4 * cm
        self.xoffset = xoffset
        self.size = size

    def wrap(self, *args):
        return (self.xoffset, self.size)

    def draw(self):
        canvas = self.canv
        if self.line == 'checkbox_cell':
            canvas.drawInlineImage(checkbox_path, 0, 0,
                width=4*mm, height=4*mm)
        elif self.line == 'checked_checkbox_cell':
            canvas.drawInlineImage(checked_checkbox_path, 0, 0,
                width=4*mm, height=4*mm)


class PdfPlatypus(Pdf):
    """
    Helper, which builds PDF using Platypus library
    """

    def _element(self, txt, style=styles['ArialNormal'], tags="<para>%s</para>",
        sep=0.3, bulletText='', fontSize=10, leading=12, fontname=None, boolToStr=None):
        style.fontSize = fontSize
        style.leading = leading
        if fontname:
            style.fontName = fontname
        
        if txt is not None:
            txt = str(txt)
            if boolToStr is None:
                if not isinstance(txt, tuple):
                    txt = txt.strip('\r')
            else:
                txt = "True" if txt =="1" else "False"
        else:
            txt=""
        return Paragraph(tags % txt, style=style,
            bulletText=bulletText)

    def p(self, **args):        
        return self._element(**args)

    def p_center(self, **args):       
        args['style'] = styles['Center']
        return self._element(**args)

    def image(self, image_path):    
        tags="<img width=560 height=30 src='%s'/>"      
        return self._element(image_path, tags=tags)

    def pre(self, txt, sep=0.1):
        s = Spacer(0.2*inch, sep*inch)
        p = Preformatted(txt.strip('\r'), styles['Code'])
        precomps = [s,p]
        result = KeepTogether(precomps)
        return result

    def title(self, **args):
        args['style'] = styles['ArialTitle']
        args['leading'] = 22
        return self._element(**args)

    def i(self, **args):
        args['style'] = styles['ArialItalic']
        return self._element(**args)

    def b(self, **args):
        args['style'] = styles['ArialBold']
        return self._element(**args)

    def u(self, **args):
        args['tags'] = '<para><u>%s</u></para>'
        return self._element(**args)

    def br(self, width=8, height=8):
        return Spacer(width, height)

    def checkbox(self, line='checkbox_cell', xoffset=23):
        return CheckBox(line=line, xoffset=xoffset)

    def bullet(self, txt):
        style=styles['Normal']
        style.leading=24
        return self._element(txt, style=style, bulletText=u'\N{BULLET}')

    def page_break(self):
        return PageBreak()

    def save(self, elements):
        """
        Renders PDF with header and footer.
        Returns PDF as text.
        """
        doc = SimpleDocTemplate(self.buffer, pagesize=self.pagesize)

        doc.leftMargin = 0.2 * inch
        doc.rightMargin = 0.5 * inch
        doc.topMargin = 0.8 * inch
        doc.bottomMargin = 0.3 * inch
        doc.width = PAGE_WIDTH - doc.leftMargin - doc.rightMargin
        doc.height = PAGE_WIDTH - doc.topMargin - doc.bottomMargin
        doc.author = 'SITE_NAME'
        doc.title = self.TITLE

        def _draw_header_and_footer(canvas, doc):
            self._draw_header(canvas)
            self._draw_footer(canvas)
            self.increment_page_number()

        doc.build(elements, onFirstPage=_draw_header_and_footer,
            onLaterPages=_draw_header_and_footer)

        self._draw_header(doc.canv)
        self._draw_footer(doc.canv)

        result = self.buffer.getvalue()
        self.buffer.close()
        return result




def generate_pdf_report_for_test_summary(db):
    bold_style = 'Heading5'
    logo_pdf_path = os.path.join(MEDIA_ROOT, 'images', 'harman_logo.jpg')

    details_query = """
    select
    labeltorun.label_id,
    testsuite.anaconda_id,
    testsuite.id as testsuite_id,
    testsuite.testsuitename,
    testsuite.dut_id,
    testsuite.enviroment_id,
    testsuite.playlistfile,
    databaseundertest.postgresdatabasename,
    databaseundertest.rdfbuildversion,
    databaseundertest.rdfdatareleasedate,
    databaseundertest.rdfproductcreationdate,
    databaseundertest.rdfproductversion,
    databaseundertest.rdfschemaversion,
    databaseundertest.nndbversion,
    databaseundertest.indsversion,
    databaseundertest.ndsversion,
    anaconda.name,
    anaconda.version,
    anaconda.branch,
    anaconda.changelist,
    anaconda.hudsonjobname,
    testenviroment.osversion,
    testenviroment.jvmversion,
    testenviroment.testframeworkversion,
    testenviroment.testrunmachine,
    testenviroment.hudsonbuildnumber,
    testenviroment.hudsonbuildid,
    testenviroment.perforceclient,
    label.year,
    label.calendarweek,
    label.releaseversion,
    label.status,
    label.commentswqs,
    label.releasecomment,
    label.user,
    label.date,     
    techs_analysis.raw_data_inspection,
    techs_analysis.nds_specification,
    techs_analysis.structure_and_content,
    techs_analysis.comparision,
    techs_analysis.visual,
    techs_analysis.regression,
    tools_analysis.nds_validation_tool,
    tools_analysis.anaconda_wb_tool,
    tools_analysis.mapviewer_tool,
    tools_analysis.nds_validation_suite_tool,
    CASE label.title
       WHEN label.title THEN label.title
       ELSE databaseundertest.ndsversion
    END AS title
from
    testsuite
    inner join databaseundertest
        on databaseundertest.id = testsuite.dut_id
    inner join anaconda
        on anaconda.id = testsuite.anaconda_id
        
    inner join testenviroment
        on testenviroment.id = testsuite.enviroment_id
        
    left outer join labeltorun
        on labeltorun.testsuite_id = testsuite.id

    inner join test
     on test.testsuite_id = testsuite.id
        
    left outer join label
        on label.id = labeltorun.label_id

    inner join testdescription_has_origin
        on testdescription_has_origin.testdescription_id = test.testdescription_id
    left outer join origin
        on origin.id = testdescription_has_origin.origin_id
    and origin.idstring != "SWQS internal"
    and origin.type = "DOORS"

    inner join techs_analysis
     on techs_analysis.label_id = labeltorun.label_id

     inner join tools_analysis
     on tools_analysis.label_id = labeltorun.label_id

where
    labeltorun.label_id = %s
    """

    result_statistic_query = """

    select
    labeltorun.label_id,
    testsuite.anaconda_id,
    databaseundertest.postgresdatabasename, 
    testsuite.id as testsuite_id,
    testsuite.testsuitename,
    testdescription.name,
    count(distinct testsuite.id) as CountTestSuites,
    count(distinct testresult.id) as CountTestsExecuted,
    count(distinct testfailed.id) as CountTestsFailed,
    count(distinct testsuccess.id) as CountTestsSuccess,
    count(distinct TR_NOK.id) as CountTestsNOK,
    count(distinct TR_Skippped.id) as CountTestsSkipped,
    count(distinct TR_PercentFailure.id) as CountTestsPercentFailure,
    count(NE_Errors.id) as CountNewErrors,
    count(KE_Errors.id) as CountKnownErrors,
    count(TCP_Errors.id) as CountTestCaseProblemErrors,
    count(A_Errors.id) as CountAftereffectErrors,
    count(NT_Errors.id) as CountNotTestableErrors,
    count(U_Errors.id) as CountUnknownErrors,
    count(OiC_Errors.id) as CountOKinContextErrors
from 
    testsuite
    inner join anaconda
        on
            anaconda_id = anaconda.id
            
inner join test 
    on test.testsuite_id=testsuite.id
inner join testdescription 
    on testdescription.id = test.testdescription_id
inner join databaseundertest 
    on databaseundertest.id = testsuite.dut_id
left outer join testresult 
    on  test.testresult_id=testresult.id
left outer join testresult testfailed 
    on test.testresult_id=testfailed.id
    and testfailed.testresult != "OK"
left outer join testresult testsuccess 
    on test.testresult_id=testsuccess.id
    and testsuccess.testresult = "OK"
left outer join testresult TR_NOK
    on test.testresult_id=TR_NOK.id
    and TR_NOK.testresult = "NOK"
left outer join testresult TR_Skippped
    on test.testresult_id=TR_Skippped.id
    and TR_Skippped.testresult = "Skipped"
left outer join testresult TR_PercentFailure
    on test.testresult_id=TR_PercentFailure.id
    and TR_PercentFailure.testresult = "SuccessPercentageFailure"
left outer join analysis NE_Errors
    on TR_NOK.id = NE_Errors.testresult_id
    and NE_Errors.errortype = "New Error"
left outer join analysis KE_Errors
    on TR_NOK.id = KE_Errors.testresult_id
    and KE_Errors.errortype = "Known Error"
left outer join analysis TCP_Errors
    on TR_NOK.id = TCP_Errors.testresult_id
    and TCP_Errors.errortype = "Testcase Problem"
left outer join analysis A_Errors
    on TR_NOK.id = A_Errors.testresult_id
    and A_Errors.errortype = "Aftereffects"
left outer join analysis NT_Errors
    on TR_NOK.id = NT_Errors.testresult_id
    and NT_Errors.errortype = "Not Testable"
left outer join analysis U_Errors
    on TR_NOK.id = U_Errors.testresult_id
    and U_Errors.errortype = "Unknown"
left outer join analysis OiC_Errors
    on TR_NOK.id = OiC_Errors.testresult_id
    and OiC_Errors.errortype = "OK in Context" 
left outer join labeltorun
        on labeltorun.testsuite_id = testsuite.id
    
left outer join analysis
        on analysis.testresult_id = testresult.id
        
where
    labeltorun.label_id = %s and test.include_test = 1 
group by
    databaseundertest.id,
    testsuite.id
    """

    details = db.executesql(details_query % 1879, as_dict = True)[0]
    result_set_statistic = db.executesql(result_statistic_query % 1879, as_dict = True)
    test_success_sum = 0
    test_nok_sum = 0
    test_skipped_sum = 0
    test_failure_sum = 0
    test_executed_sum = 0
    test_testsuites_sum = 0
    test_new_sum = 0
    test_known_sum = 0
    test_testcaseproblem_sum = 0
    test_unknown_sum = 0
    ok_per_testsuite = []
    nok_per_testsuite = []
    skipped_per_testsuite = []
    testsuite_names = []

    new_errors_per_testsuite = []
    known_per_testsuite = []
    testcaseproblem_per_testsuite = []
    unknown_per_testsuite = []
    

    for i in result_set_statistic:
        ok = i['CountTestsSuccess'] + i['CountOKinContextErrors']
        nok = i['CountTestsNOK'] - i['CountOKinContextErrors']
        new = i['CountNewErrors']
        known = i['CountKnownErrors'] 
        testcaseproblem = i['CountTestCaseProblemErrors'] 
        unknown = i['CountUnknownErrors']
        
        skipped = i["CountTestsSkipped"]
        test_success_sum += ok
        test_nok_sum += nok
        test_skipped_sum += skipped
        test_failure_sum += i["CountTestsFailed"] - i["CountOKinContextErrors"]
        test_executed_sum += i["CountTestsExecuted"]
        test_testsuites_sum += i["CountTestSuites"]
        test_new_sum += new if new is not None else 0
        test_known_sum += known if known is not None else 0
        test_testcaseproblem_sum += testcaseproblem if testcaseproblem is not None else 0
        test_unknown_sum += unknown if unknown is not None else 0

        ok_per_testsuite.append(None if ok == 0 else ok)
        nok_per_testsuite.append(None if nok == 0 else nok)
        skipped_per_testsuite.append(None if skipped == 0 else skipped)
        testsuite_names.append(i['testsuitename'])
        new_errors_per_testsuite.append(None if new == 0 else new)
        known_per_testsuite.append(None if known == 0 else known)
        testcaseproblem_per_testsuite.append(None if testcaseproblem == 0 else testcaseproblem)
        unknown_per_testsuite.append(None if unknown == 0 else unknown)

    logging.error(new_errors_per_testsuite)

    pdf = PdfPlatypus()
    elements = []
    elements.append(pdf.br(width=28, height=28))
    elements.append(pdf.image(logo_pdf_path))
    elements.append(pdf.br(width=108, height=108))

    elements.append(pdf.title(txt="Test summary for:"))
    elements.append(pdf.title(txt=details['title'], fontSize=14))
    elements.append(pdf.page_break())

    elements.append(pdf.b(txt="1. Details", fontSize=14))
    elements.append(pdf.br())

    table_data = [
            [
                [pdf.p(txt="Comment of Release Manager")],
                [pdf.p(txt=": " + details["releasecomment"])],
            ],
            [
                [pdf.p(txt="Comment of Incident Manager")],
                [pdf.p(txt=": " +details["commentswqs"])],
            ]
    ]
    cells_width = [180, 420]

    table = Table(table_data, cells_width,
        style=[('VALIGN',(0,0),(-1,-1), 'CENTER'),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('LEFTPADDING', (0,0),(0,-1), 34),
            ('TOPPADDING', (1,0),(1,-1), 8),
        ])
    elements.append(table)
    elements.append(pdf.br())
    elements.append(pdf.u(txt="1.1 Testee", fontSize=13))
    elements.append(pdf.br())
    table_data = [
            [
                [pdf.p(txt="Version Name")],
                [pdf.p(txt=": " + details["name"])],
            ],
            [
                [pdf.p(txt="P4 Changelist")],
                [pdf.p(txt=": " +details["changelist"])],
            ],
            [
                [pdf.p(txt="Branch")],
                [pdf.p(txt=": " +details["branch"])],
            ]
    ]

    cells_width = [180, 420]

    table = Table(table_data, cells_width,
        style=[('VALIGN',(0,0),(-1,-1), 'CENTER'),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('LEFTPADDING', (0,0),(0,-1), 34),
        ])
    elements.append(table)
    elements.append(pdf.br())
    elements.append(pdf.u(txt="1.2 Test Run", fontSize=13))
    elements.append(pdf.br())

    table_data = [
            [
                [pdf.p(txt="Date")],
                [pdf.p(txt=": " + str(details["date"]) )],
            ],
            [
                [pdf.p(txt="Analysed by")],
                [pdf.p(txt=": " +details["user"])],
            ],
    ]

    cells_width = [180, 420]

    table = Table(table_data, cells_width,
        style=[('VALIGN',(0,0),(-1,-1), 'CENTER'),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('LEFTPADDING', (0,0),(0,-1), 34),
        ])
    elements.append(table)
    elements.append(pdf.br())
    elements.append(pdf.u(txt="1.3 Variances", fontSize=13))
    elements.append(pdf.br())
    elements.append(pdf.p(txt="1.3.1. Test Item(s) Variances from Test Plan: None"))
    elements.append(pdf.p(txt="1.3.2. Test Procedures Variances: None"))
    elements.append(pdf.p(txt="1.3.3. Test Case Variances: None"))
    elements.append(pdf.br())

    elements.append(pdf.page_break())

    elements.append(pdf.b(txt="2. Test Stage / Test Tools", fontSize=14))
    elements.append(pdf.br(width=16, height=16))
    elements.append(pdf.p(txt="This chapter provides an overview about the stage of testing within the NAV2010 Projects. Most notable tools, which are used as test frameowork are listed"))
    elements.append(pdf.br())
    elements.append(pdf.u(txt="2.1 Test stage", fontSize=13))
    elements.append(pdf.br(width=16, height=16))

    elements.append(pdf.p(txt="NDS Data Base Qualification"))
    elements.append(pdf.br())
    elements.append(pdf.u(txt="2.2 Test Techniques", fontSize=13))
    elements.append(pdf.br(width=16, height=16))
    table_data = []
    row = [pdf.p_center(txt="Raw Data Inspection")]
    if details["raw_data_inspection"]:
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))
    else:
        row.append(pdf.checkbox(line='checkbox_cell', xoffset=12))
    table_data.append(row)

    row = [pdf.p_center(txt="Structure & Content")]
    if details["structure_and_content"]:
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))
    else:
        row.append(pdf.checkbox(line='checkbox_cell', xoffset=12))
    table_data.append(row)

    row = [pdf.p_center(txt="NDS Specification")]
    if details["nds_specification"]:
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))
    else:
        row.append(pdf.checkbox(line='checkbox_cell', xoffset=12))
    table_data.append(row)

    row = [pdf.p_center(txt="Visual")]
    if details["visual"]:
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))
    else:
        row.append(pdf.checkbox(line='checkbox_cell'))
    table_data.append(row)

    row = [pdf.p_center(txt="Comparision (old vs. new)")]
    if details["comparision"]:
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))
    else:
        row.append(pdf.checkbox(line='checkbox_cell', xoffset=12))
    table_data.append(row)

    row = [pdf.p_center(txt="Regression")]
    if details["regression"]:
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))
    else:
        row.append(pdf.checkbox(line='checkbox_cell', xoffset=12))
    table_data.append(row)

    cells_width = [150, 50]

    table = Table(table_data, cells_width,
        style=[('VALIGN',(0,0),(-1,-1), 'CENTER'),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ],hAlign='LEFT')
    elements.append(table)
    elements.append(pdf.br())
    elements.append(pdf.u(txt="2.3 Other test/tools", fontSize=13))
    elements.append(pdf.br(width=16, height=16))

    cells_width = [150, 50, 50, 70]

    table_data = []
    row = [pdf.p_center(txt="Tool"), pdf.p_center(txt="Passed"), pdf.p_center(txt="Failed"), pdf.p_center(txt="Test count")]
    table_data.append(row)

    row = [pdf.p_center(txt="NDS Validation Tool")]
    if details["nds_validation_tool"]:
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))
        row.append(pdf.checkbox(line='checkbox_cell', xoffset=12))
    else:
        row.append(pdf.checkbox(line='checkbox_cell', xoffset=12))
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))

    row.append(pdf.p_center(txt='1/1'))

    table_data.append(row)

    row = [pdf.p_center(txt="Anaconda Workbench")]
    if details["anaconda_wb_tool"]:
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))
        row.append(pdf.checkbox(line='checkbox_cell', xoffset=12))
    else:
        row.append(pdf.checkbox(line='checkbox_cell', xoffset=12))
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))
    row.append(pdf.p_center(txt='93/93'))
    table_data.append(row)

    row = [pdf.p_center(txt="MapViewer Simulation")]
    if details["mapviewer_tool"]:
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))
        row.append(pdf.checkbox(line='checkbox_cell', xoffset=12))
    else:
        row.append(pdf.checkbox(line='checkbox_cell', xoffset=12))
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))
    row.append(pdf.p_center(txt='363/363'))
    table_data.append(row)

    row = [pdf.p_center(txt="NDS Validation Suite")]
    if details["nds_validation_suite_tool"]:
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))
        row.append(pdf.checkbox(line='checkbox_cell', xoffset=12))
    else:
        row.append(pdf.checkbox(line='checkbox_cell', xoffset=12))
        row.append(pdf.checkbox(line='checked_checkbox_cell', xoffset=12))
    row.append(pdf.p_center(txt='4621/4621'))

    table_data.append(row)

    table = Table(table_data, cells_width,
        style=[('VALIGN',(0,0),(-1,-1), 'CENTER'),
            ('ALIGN',(0,0),(-1,-1), 'CENTER'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#99FF66")),
            ('BACKGROUND', (2, 0), (2, 0), colors.HexColor("#FF6666"))

        ],hAlign='LEFT')
    elements.append(table)
    elements.append(pdf.br())
    elements.append(pdf.u(txt="2.4 Not tested", fontSize=13))
    elements.append(pdf.br(width=16, height=16))
    elements.append(pdf.p(txt="""Depending on the content and the possiblity to conduct tests for specific building blocks, not all meseuarements can be taken to fullfill an appropriate coverage of features. The following
features have not been checked in full scope, but as much as possbile e.g."""))
    elements.append(pdf.p(txt="- Rounting"))
    elements.append(pdf.p(txt="- Speech"))
    elements.append(pdf.p(txt="- Traffict Information"))

    elements.append(pdf.page_break())
    elements.append(pdf.b(txt="3. Test Cases", fontSize=14))
    elements.append(pdf.br(width=16, height=16))
    elements.append(pdf.p(txt="The following table lists all successfully passed test cases run during test execution. All failed test cases were listed and analyzed in section 'Incident Overview'."))
    elements.append(pdf.br())
    elements.append(pdf.p_center(txt="Test Result State"))
    elements.append(pdf.br())

    table_data = [
            [
                [pdf.p(txt="Executed Test Suites")],
                [pdf.p(txt=str(test_testsuites_sum))],
            ],
            [
                [pdf.p(txt="Executed Test Cases")],
                [pdf.p(txt=str(test_executed_sum))],
            ],
            [
                [pdf.p(txt="Failed Test Cases")],
                [pdf.p(txt=str(test_failure_sum))],
            ],
            [
                [pdf.p(txt="OK")],
                [pdf.p(txt=str(test_success_sum))],
            ],
            [
                [pdf.p(txt="NOK")],
                [pdf.p(txt=str(test_nok_sum))],
            ],
            [
                [pdf.p(txt="Skipped")],
                [pdf.p(txt=str(test_skipped_sum))],
            ],
    ]

    cells_width = [180, 50]
    table = Table(table_data, cells_width,
        style=[('VALIGN',(0,0),(-1,-1), 'CENTER'),
            ('ALIGN',(0,0),(-1,-1), 'CENTER'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 3), (1, 3), colors.HexColor("#99FF66")),
            ('BACKGROUND', (0, 4), (1, 4), colors.HexColor("#FF6666")),
            ('BACKGROUND', (0, 5), (1, 5), colors.HexColor("#C6DEF3"))

        ],hAlign='CENTER')
    elements.append(table)

    from reportlab.lib.colors import Color, blue, red  
    from reportlab.graphics.charts.legends import Legend, TotalAnnotator  
    from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin 
    from reportlab.lib.validators import Auto  
    from reportlab.graphics.charts.barcharts import VerticalBarChart  , VerticalBarChart3D
    
    from reportlab.lib.colors import Color, blue, red , grey, green
    from reportlab.graphics.charts.legends import Legend, TotalAnnotator  
    from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin  
    from reportlab.lib.validators import Auto  
    from reportlab.lib.colors import HexColor
    from reportlab.graphics.charts.textlabels import Label

    class FactSheetHoldingsVBar(_DrawingEditorMixin,Drawing):  
        def __init__(self,width=400,height=200, x=10, y=-250, bar_width=550, bar_height=350, num_bars=3, bars_colors=None, data=[], *args,**kw):  
            apply(Drawing.__init__,(self,width,height)+args,kw)  
            
            self._add(self,VerticalBarChart3D(),name='bar',validate=None,desc=None)  
            self.bar.data             = data  
            self.bar.categoryAxis.categoryNames = testsuite_names  
            self.bar.width                      = bar_width  
            self.bar.height                     = bar_height  
            self.bar.x                          = x  
            self.bar.y                          = y  
            self.bar.useAbsolute = 0
            self.bar.barSpacing                 = 0  
            self.bar.groupSpacing               = 0.7  
            self.bar.barWidth               = 1  
            self.bar.valueAxis.labels.fontName  = 'ArialN'  
            self.bar.valueAxis.rangeRound       = 'both'  
            self.bar.valueAxis.valueMax         = None#10#  
            self.bar.categoryAxis.visible       = 1  
            self.bar.categoryAxis.visibleTicks  = 0
            self.bar.categoryAxis.labels.fontSize = 8
            self.bar.categoryAxis.labels.angle = -35
            self.bar.categoryAxis.labels.dy = -15
            self.bar.categoryAxis.labels.dx = -20
            self.bar.categoryAxis.labels.boxAnchor = 'w'
            self.bar.categoryAxis.tickShift  = 1
            
            if bars_colors:
                for i in range(num_bars):
                    self.bar.bars[i].fillColor = colors.HexColor(bars_colors[i])
               

            self.bar.barLabels.nudge = 0
            self.bar.barLabelFormat = '%d'

            # self.bar.barLabels.dx = 0
            # self.bar.barLabels.dy = -5
            # self.bar.barLabels.boxAnchor = 'n'  # irrelevant (becomes 'c')
            self.bar.barLabels.textAnchor = 'middle'
            self.bar.barLabels.fontName = 'ArialB'
            self.bar.barLabels.fontSize = 10
            self.bar.barLabels.nudge = 5 

            self.bar.valueAxis.labels.fontSize  = 6  
            self.bar.strokeWidth                = 0.1  
            self.bar.bars.strokeWidth           = 0.5  
            # self.bar.categoryAxis.style='stacked'
            #add and set up legend  
            self._add(self,Legend(),name='legend',validate=None,desc=None)  
            self.legend.colorNamePairs  = [(colors.HexColor("#99FF66"), 'OK'), (colors.HexColor("#FF6666"), 'NOK'), (colors.HexColor("#C6DEF3"), 'SKIPPED')]
            self.legend.fontName        = 'ArialN'  
            self.legend.fontSize        = 7  
            self.legend.boxAnchor       = 'w'  
            self.legend.x               = 500  
            self.legend.y               = 150  
            self.legend.dx              = 8  
            self.legend.dy              = 8  
            self.legend.alignment       = 'right'  
            self.legend.yGap            = 0  
            self.legend.deltay          = 11  
            self.legend.dividerLines    = 1|2|4  
            self.legend.subCols.rpad    = 10  
            self.legend.dxTextSpace     = 5  
            self.legend.strokeWidth     = 1  
            self.legend.dividerOffsY    = 6  

            self._add(self,Label(),name='Title',validate=None,desc="The title at the top of the chart")
            self.Title.fontName = 'ArialB'
            self.Title.fontSize = 16
            self.Title.x = 270
            self.Title.y = 150
            self.Title._text = 'Test Results per Test Area'
            self.Title.maxWidth = 280
            self.Title.height = 20
            self.Title.textAnchor ='middle'

    
    drawing = FactSheetHoldingsVBar(data=[ok_per_testsuite, nok_per_testsuite, skipped_per_testsuite], num_bars=3, bars_colors=["#99FF66", "#FF6666","#C6DEF3"])  
    elements.append(drawing)

    elements.append(pdf.page_break())
    elements.append(pdf.b(txt="4. Incident Overview", fontSize=14))
    elements.append(pdf.br(width=16, height=16))
    elements.append(pdf.p(txt="In the following table, all incidents identified during the test execution are listed. Rows are colour coded and error types are abbrevated according to table in section \"Summary\". For each identified incident, an Jira ticket shall be produced and listed in the appropriate column.."))
    elements.append(pdf.br())
    elements.append(pdf.p_center(txt="Analysis Results"))
    elements.append(pdf.br())

    table_data = [
            [
                [pdf.p(txt="Executed Test Suites")],
                [pdf.p(txt=str(test_testsuites_sum))],
            ],
            [
                [pdf.p(txt="Executed Test Cases")],
                [pdf.p(txt=str(test_executed_sum))],
            ],
            [
                [pdf.p(txt="Failed Test Cases")],
                [pdf.p(txt=str(test_failure_sum))],
            ],
            [
                [pdf.p(txt="New Error (NE)")],
                [pdf.p(txt=str(test_new_sum))],
            ],
            [
                [pdf.p(txt="Known Error (KE)")],
                [pdf.p(txt=str(test_known_sum))],
            ],
			[
                [pdf.p(txt="Test Case Problem (TcP)")],
                [pdf.p(txt=str(test_testcaseproblem_sum))],
            ],
            [
                [pdf.p(txt="Unknown")],
                [pdf.p(txt=str(test_unknown_sum))],
            ],
			[
                [pdf.p(txt="Skipped / Not Testable")],
                [pdf.p(txt=str(test_skipped_sum))],
            ],
    ]

    cells_width = [180, 50]
    table = Table(table_data, cells_width,
        style=[('VALIGN',(0,0),(-1,-1), 'CENTER'),
            ('ALIGN',(0,0),(-1,-1), 'CENTER'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 3), (1, 3), colors.HexColor("#FF6666")),
            ('BACKGROUND', (0, 4), (1, 4), colors.HexColor("#FFC167")),
            ('BACKGROUND', (0, 5), (1, 5), colors.HexColor("#FFFF66")),
			('BACKGROUND', (0, 6), (1, 6), colors.HexColor("#F5F0EB")),
			('BACKGROUND', (0, 7), (1, 7), colors.HexColor("#C6DEF3")),
			

        ],hAlign='CENTER')
    elements.append(table)
    logging.error("HER!!")
    logging.error(new_errors_per_testsuite)
    logging.error(known_per_testsuite)
    logging.error(testcaseproblem_per_testsuite)
    logging.error(unknown_per_testsuite)
    logging.error(skipped_per_testsuite)
    data = []
    bars_colors=[]
    
    if not all(v is None for v in new_errors_per_testsuite):
        data.append(new_errors_per_testsuite)
        bars_colors.append("#FF6666")
    if not all(v is None for v in known_per_testsuite):
        data.append(known_per_testsuite)
        bars_colors.append("#FFC167")
    if not all(v is None for v in testcaseproblem_per_testsuite):
        data.append(testcaseproblem_per_testsuite)
        bars_colors.append("#FFFF66")
    if not all(v is None for v in unknown_per_testsuite):
        data.append(unknown_per_testsuite)
        bars_colors.append("#F5F0EB")
    if not all(v is None for v in skipped_per_testsuite):
        data.append(skipped_per_testsuite)
        bars_colors.append("#C6DEF3")
    drawing = FactSheetHoldingsVBar(data=data, x=10, y=-200, num_bars=5, bar_height=300, bars_colors=["#FF6666", "#FFC167", "#FFFF66","#F5F0EB", "#C6DEF3"])  
    elements.append(drawing)
    



    return pdf.save(elements)

def release_note_pdf(db, note_id):
    bold_style = 'Heading5'
    logo_pdf_path = os.path.join(MEDIA_ROOT, 'images', 'harman_logo.jpg')

    details_query = """
        SELECT * FROM release_note rn 
        JOIN database_info di ON di.note_id = rn.id
        JOIN nds_file_structure nfs ON nfs.note_id = rn.id
        JOIN known_issues ki ON ki.note_id = rn.id
        JOIN features_info fi ON fi.note_id = rn.id
        where rn.id = %s
        """
    
    details = release_note_db.executesql(details_query%note_id, as_dict = True)[0]

    pdf = PdfPlatypus()
    elements = []
    elements.append(pdf.br(width=28, height=1))
    elements.append(pdf.image(logo_pdf_path))
    elements.append(pdf.br(width=108, height=148))

    elements.append(pdf.title(txt="DB Production", fontSize=25))
    elements.append(pdf.br(width=28, height=28))
    elements.append(pdf.title(txt="Release Notes", fontSize=25))
    elements.append(pdf.br(width=28, height=28))
    elements.append(pdf.title(txt=details['release_note_name'], fontSize=20))
    
    table_data = [
            [
                [pdf.p(txt="Date:")],
                [pdf.p(txt=str(details['date']))],
            ],
            [
                [pdf.p(txt="Version:")],
                [pdf.p(txt=details['version'])],
            ],
            [
                [pdf.p(txt="Owner:")],
                [pdf.p(txt=details['owner'])],
            ],
            [
                [pdf.p(txt="Approved by:")],
                [pdf.p(txt=details['approved_by'])],
            ]
    ]
    cells_width = [80, 200]

    table = Table(table_data, cells_width, hAlign="LEFT")

    elements.append(pdf.br(width=100, height=300))
    elements.append(pdf.b(txt="CONFIDENTIAL", fontSize = 18))
    elements.append(pdf.br(width=100, height=15))
    elements.append(table)

    elements.append(pdf.page_break())
    elements.append(pdf.p_center(txt="OEM", fontSize = 20))

    db_type = details["db_type"]
    
    if db_type == "AMD":
        table_cells_width = [75, 200, 275]
    else:
        table_cells_width = [75, 75, 150, 250]

    table_style = [
        ('VALIGN',(0,0),(-1,-1), 'CENTER'),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black)
    ]

    table_data = []
    
    row = []
    if db_type == "AMD":
        row.append(pdf.p_center(txt="AMD"))
    else:
        row.append(pdf.p_center(txt="Full NDS"))
    table_data.append(row)

    if db_type == "AMD":
        table_style.append(('SPAN', (0, 0), (2, 0)))
    else:
        table_style.append(('SPAN', (0, 0), (3, 0)))

    row = []
    row.append(pdf.p_center(txt="General\nInformation"))
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="PON #"))
    row.append(pdf.p(txt=str(details['pon'])))
    table_data.append(row)

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="Customer"))
    row.append(pdf.p(txt=details['customer']))
    table_data.append(row)

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="Map Data Supplier"))
    row.append(pdf.p(txt=details['map_data_supplier']))
    table_data.append(row)

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="DB Release"))
    row.append(pdf.p(txt=details['db_release']))
    table_data.append(row)

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="Region"))
    row.append(pdf.p(txt=details['region']))
    table_data.append(row)

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="UpdateRegion/Country List"))
    row.append(pdf.p(txt=details['country_list']))
    table_data.append(row)

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="Compiler Release"))
    row.append(pdf.p(txt=details['compiler_release']))
    table_data.append(row)

    if db_type == "Full-NDS":
        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="Full NDS ROOT file"))
        row.append(pdf.p(txt=details['root_file']))
        table_data.append(row)

    row = []
    row.append([])
    if db_type == "AMD":
        row.append(pdf.p(txt="AMD NDS DB name"))
    else:
        row.append([])
        row.append(pdf.p(txt="Full NDS Product file"))
    row.append(pdf.p(txt=details['product_file']))
    table_data.append(row)

    if db_type == "Full-NDS":
        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="AMD"))
        row.append(pdf.p(txt=details['amd']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="OMB"))
        row.append(pdf.p(txt=details['omb']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="UR 01"))
        row.append(pdf.p(txt=details['ur_01']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="UR 02"))
        row.append(pdf.p(txt=details['ur_02']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="UR 03"))
        row.append(pdf.p(txt=details['ur_03']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="UR 04"))
        row.append(pdf.p(txt=details['ur_04']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="UR 05"))
        row.append(pdf.p(txt=details['ur_05']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="UR 06"))
        row.append(pdf.p(txt=details['ur_06']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="UR 07"))
        row.append(pdf.p(txt=details['ur_07']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="UR 08"))
        row.append(pdf.p(txt=details['ur_08']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="UR 09"))
        row.append(pdf.p(txt=details['ur_09']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="UR 10"))
        row.append(pdf.p(txt=details['ur_10']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="UR 11"))
        row.append(pdf.p(txt=details['ur_11']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="UR 12"))
        row.append(pdf.p(txt=details['ur_12']))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="DB size"))
        row.append(pdf.p(txt=details['db_size']))
        table_data.append(row)

    if db_type == "AMD":
        row = []
        row.append([])
        row.append(pdf.p(txt="AMD NDS DB files uncompressed"))
        row.append(pdf.p(txt=details['amd_db_files_uncompressed']))
        table_data.append(row)

        row = []
        row.append([])
        row.append(pdf.p(txt="AMD NDS DB files compressed"))
        row.append(pdf.p(txt=details['amd_db_files_compressed'], boolToStr="1"))
        table_data.append(row)

        row = []
        row.append([])
        row.append(pdf.p(txt="NDSC mode"))
        row.append(pdf.p(txt=details['nds_compression_mode']))
        table_data.append(row)

    if db_type == "AMD":
        table_style.append(('SPAN', (0, 1), (0, 11)))
    else:
        table_style.append(('SPAN', (0, 1), (1, 24)))

    row = []
    row.append(pdf.p(txt="Features"))
    if db_type == "Full-NDS":
        row.append(pdf.p(txt="AMD"))
    row.append(pdf.p(txt="“normal” DTM"))
    row.append(pdf.p(txt=details['amd_normal_dtm'], boolToStr="1"))
    table_data.append(row)    

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="“flat” DTM  (no elevation/depth levels)"))
    row.append(pdf.p(txt=details['amd_flat_dtm'], boolToStr="1"))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="SAT images"))
    row.append(pdf.p(txt=details['amd_sat_images'], boolToStr="1"))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="aerial photos"))
    row.append(pdf.p(txt=details['amd_aerial_photos'], boolToStr="1"))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="3D landmarks"))
    row.append(pdf.p(txt=details['amd_3d_landmarks'], boolToStr="1"))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="3D city models"))
    row.append(pdf.p(txt=details['amd_3d_city_models'], boolToStr="1"))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="enhanced 3D city models"))
    row.append(pdf.p(txt=details['amd_enhanced_3d_city_models'], boolToStr="1"))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="road furniture to enhanced 3D city model"))
    row.append(pdf.p(txt=details['amd_road_furniture'], boolToStr="1"))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="OEM specific enhancements for shoebox city models"))
    row.append(pdf.p(txt=details['amd_oem_specific_enhancements'], boolToStr="1"))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="shaded maps"))
    row.append(pdf.p(txt=details['amd_shaded_maps'], boolToStr="1"))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="3D bridges"))
    row.append(pdf.p(txt=details['amd_3d_bridges']))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="3D tunnels"))
    row.append(pdf.p(txt=details['amd_3d_tunnels'], boolToStr="1"))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="motorway junction objects (MoJO)"))
    row.append(pdf.p(txt=details['amd_motorway_junction_objects'], boolToStr="1"))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="superelevation"))
    row.append(pdf.p(txt=details['amd_superelevation'], boolToStr="1"))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="2D landmark icons"))
    row.append(pdf.p(txt=details['amd_2d_landmark_icons'], boolToStr="1"))
    table_data.append(row) 
    
    
    if db_type == "Full-NDS":
        row = []
        row.append([])
        row.append([pdf.p(txt="Basic-NDS")])
        row.append(pdf.p(txt="BMD"))
        row.append(pdf.p(txt=details['basic_nds_bmd'], boolToStr="1"))
        table_data.append(row) 

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="POI"))
        row.append(pdf.p(txt=details['basic_nds_poi'], boolToStr="1"))
        table_data.append(row) 

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="Routing"))
        row.append(pdf.p(txt=details['basic_nds_routing'], boolToStr="1"))
        table_data.append(row)

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="ADAS"))
        row.append(pdf.p(txt=details['basic_nds_adas'], boolToStr="1"))
        table_data.append(row) 

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="Phonemes"))
        row.append(pdf.p(txt=details['basic_nds_phonemes'], boolToStr="1"))
        table_data.append(row) 

        row = []
        row.append([])
        row.append([])
        row.append(pdf.p(txt="Traffic Information"))
        row.append(pdf.p(txt=details['basic_nds_traffic_information'], boolToStr="1"))
        table_data.append(row) 
    
    if db_type == "AMD":
        table_style.append(('SPAN', (0, 12), (0, 26)))
    else:
        table_style.append(('SPAN', (0, 25), (0, 45)))
        table_style.append(('SPAN', (1, 25), (1, 39)))
        table_style.append(('SPAN', (1, 40), (1, 45)))
    
    row = []
    row.append(pdf.p(txt="Advanced Information"))
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="DTM (base level, upper level)"))
    row.append(pdf.p(txt=details['advanced_dtm']))
    table_data.append(row)   
    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="Integrate features into DTM"))
    row.append(pdf.p(txt=details['advanced_integrate_features']))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="SAT (base level, upper level)"))
    row.append(pdf.p(txt=details['advanced_sat']))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="ShadedMap (base level, upper level)"))
    row.append(pdf.p(txt=details['advanced__shadedmap']))
    table_data.append(row) 

    row = []
    row.append([])
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="Images/Textures Format"))
    row.append(pdf.p(txt=details['advanced_textures_format']))
    table_data.append(row)

    if db_type == "AMD":
        table_style.append(('SPAN', (0, 27), (0, 31)))
    else:
        table_style.append(('SPAN', (0, 46), (1, 50)))

    row = []
    row.append(pdf.p(txt="ELVIS"))
    if db_type == "Full-NDS":
        row.append([])
    row.append(pdf.p(txt="Fixed tickets #"))
    row.append(pdf.p(txt=details['elvis_tickets']))
    table_data.append(row)

    if db_type == "Full-NDS":
        table_style.append(('SPAN', (0, 51), (1, 51)))

    row = []
    if db_type == "AMD":
        row.append(pdf.p_center(txt="AMD"))
        table_style.append(('SPAN', (0, 33), (2, 33)))
    else:
        row.append(pdf.p_center(txt="Full NDS"))
        table_style.append(('SPAN', (0, 52), (3, 52)))
    table_data.append(row)



    """
    row = []
    row.append(pdf.p(txt="Known Issues"))
    row.append(pdf.p(txt="3D city model"))
    row.append(pdf.p(txt=details['ki_amd_3d_city_model']))
    table_data.append(row)

    row = []
    row.append([])
    row.append(pdf.p(txt="3D Enhanced city model"))
    row.append(pdf.p(txt=details['ki_amd_3d_enhanced_city_model']))
    table_data.append(row)

    row = []
    row.append([])
    row.append(pdf.p(txt="3D landmark"))
    row.append(pdf.p(txt=details['ki_amd_3d_landmark']))
    table_data.append(row)

    row = []
    row.append([])
    row.append(pdf.p(txt="SAT"))
    row.append(pdf.p(txt=details['ki_amd_sat']))
    table_data.append(row)

    row = []
    row.append([])
    row.append(pdf.p(txt="DTM"))
    row.append(pdf.p(txt=details['ki_amd_dtm']))
    table_data.append(row)

    row = []
    row.append([])
    row.append(pdf.p(txt="ShadedMap"))
    row.append(pdf.p(txt=details['ki_amd_shaded_map']))
    table_data.append(row)

    #table_style.append(('SPAN', (0, 33), (0, 38)))
    
    row = []
    row.append(pdf.p_center(txt="AMD"))
    table_data.append(row)
    
    
    """

    table = Table(table_data, table_cells_width,
        style=table_style, hAlign='LEFT')

    elements.append(pdf.br(width=100, height=15))
    elements.append(table)

    # logging.error(dir(styles))
    # logging.error(styles.list())

    # return pdf.save(elements) 

    return pdf.save(elements) 
