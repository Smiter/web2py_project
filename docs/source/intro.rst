Install BIRT Guide
****************************************

BIRT - web application written using web2py python framework and eclipse birt java application for generation pdf.

Installing web2py framework
======================================

* Install python 2.7
* Download web2py python web framework: http://www.web2py.com/examples/default/download
* Read instructions on the link above how to run it.
* Download last sources from PERFORCE: ``//CoC_Navigation/DigitalMap/Nds/Anaconda/Tools/BIRT/BIRT_SRC/``
* Put all code into your folder inside ``web2py/application`` directory like this:

::

   d:\Pyprojects\web2py\applications\birt\your_source

* Run web2py framework from command line:

::

    >>> cd $HOME_WEB2PY_DIRECTORY
    >>> python web2py

* Go to the browser and enter http://127.0.0.1:8000/birt/

local settings configuration
============================

To get the web2py application work you need local_settings.py file for development and production configs.

* First, you need to create ``local_settings.py`` in ``web2py/application/birt/modules/`` file where all user settings will be stored.
* Create a variable ``my_db_name`` to establish mysql connection
* Create a variable ``tomcat_web_server_birt_url`` for report generation via eclipse birt

::
    
    #local_settings.py
    #production db configuration:
    my_db_name = "mysql://nds:test@oekalxap68/ndsreport"
    tomcat_web_server_birt_url = 'http://172.30.136.225:8080/birt/frameset?__report=BirtReports/Designs/AnacondaTest/%s.rptdesign&Release Candidate=%s&__format=pdf'


.. note::
    
    It is strictly forbidden to use production database for development.


Installing eclipse birt
======================================

* Install Eclipse IDE for Java and Report Developers: http://www.eclipse.org/downloads/packages/eclipse-ide-java-and-report-developers/junosr2
* Download last sources of report design from ``//CoC_Navigation/DigitalMap/Nds/Anaconda/Tools/BIRT/BIRT_TEMPLATES/``
* Start eclipse. Go to ``File->Project->New project->Business Intelligence and Reporting Tools->Report Project``
* Copy ``BirtReports`` folder from sources to the root of the new created project in Eclipse 
* Use ``Report Design`` eclipse perspective to edit report design

Installing Apache Tomcat web server
======================================

* Install last Tomcat server: http://tomcat.apache.org/download-60.cgi
* Copy ``BirtReports`` folder to ``$HOME_TOMCAT/webapps/birt/``
* Run Tomcat using ``$HOME_TOMCAT/bin/startup.bat`` or stop using ``$HOME_TOMCAT/bin/shutdown.bat``