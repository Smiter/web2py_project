
function fnFormatDetails (innerhtml,value)
{
    var sOut = innerhtml+value+'</textarea>'
    return sOut;
}

function addFiltering(that){
  var self = that;
      $(function(){
            $(".display tfoot input").keyup( function () {
                  /* Filter on the column (the index) of this element */
                  self.oTable.fnFilter( this.value, $(".display tfoot input").index(this) );
              } );

              $(".display tfoot input").each( function (i) {
                  if(self.asInitVals[i] != null){
                      self.asInitVals[i] = this.value;
                  }
              } );
               
              $(".display tfoot input").focus( function () {
                  if ( this.className == "search_init_focus_of" )
                  {
                      $(this).css('color',"black")
                      this.className = "search_init_focus_on";
                      this.value = "";
                  }
              } );
               
              $(".display tfoot input").blur( function (i) {
                  if ( this.value == "" )
                  {
                      $(this).css('color',"#999")
                      this.className = "search_init_focus_of";
                      this.value = "Search"
                  }
              } );    
     });
}

function TestRunsDataTable(){
        var tableColumns = [
          { "sTitle": "", "bSortable": false ,"sWidth": "2%","mData" : null,
            "sDefaultContent": '<input type = "checkbox">'},
          { "sTitle": "Id","sWidth": "5%", "mData": "testsuite.id" },
          { "sTitle": "Name", "bSortable": false ,"sWidth": "26%", "mData": "testsuite.testsuitename" },
          { "sTitle": "Start date" ,"sWidth": "8%", "mData": "testsuite.starttime" },
          { "sTitle": "Finish date" ,"sWidth": "8%", "mData": "testsuite.endtime" },
          { "sTitle": "Branch" , "bSortable": false,"sWidth": "8%", "mData": "anaconda.name" },
          { "sTitle": "CL" , "bSortable": false,"sWidth": "8%", "mData": "anaconda.changelist" },
          { "sTitle": "Analyzed","sWidth": "7%", "mData": "testsuite.analyzed",
                      "mRender": function ( data, type, full ) {
                        if (data == 0){
                          return '<img style="width:22px; height:22px"  src="../static/images/no1.jpg">'
                        }
                        else{
                          return '<img style="width:22px; height:22px"  src="../static/images/yes2.jpg">'
                        }sScrollY
                      }
          }
          ]
        var sorting = [[ 1, "desc" ]]
        var tableid = "testsuitetable"
        var handler = "/" + appName + "/fact/runsHandler"
        var buttons = ['analyzebutton', 'addtolabel']
        var self = this;
        var asInitVals = new Array()
        self.app_name = '{{=request.application}}'
        self.asInitVals = asInitVals
        self.testresult = 'NOK'

            $(function(){
                 self.oTable = $('#' + tableid).dataTable( {

                 "fnDrawCallback": function(){

                    if (tableid == "testsuitetable"){

                        $('td:eq(2)', self.oTable.fnGetNodes()).editable( '/'+ appName +'/fact/edit_testsuitename', {
                                        "callback": function( sValue, y ) {
                                            var aPos = self.oTable.fnGetPosition( this );
                                            self.oTable.fnUpdate( sValue, aPos[0], aPos[1], false );
                                        },
                                        "submitdata": function ( value, settings ) {
                                            var aPos = self.oTable.fnGetPosition( this );
                                            testsuite_id = self.oTable.fnGetData(aPos[0]).testsuite.id
                                            return { "testsuite_id": testsuite_id };
                                        },
                                        "height": "30px",
                                        tooltip: 'Click to Edit',
                                        cancel: 'Cancel',
                                        submit: 'Save',
                        } );
                    }

                    $("#"+tableid+" tfoot input").each( function (i) {
                        if(this.value == ""){
                            self.asInitVals[i] = "Search"
                            $(this).blur(); 
                            $(this).css('color',"#999")
                        }
                    } );

                    },
                 "aoColumns": tableColumns,
                 "aaSorting": sorting,
                 "bAutoWidth": false,
                 // "bJQueryUI": true,
                 "bServerSide" : true,
                 "bProcessing" : true,
                 "bFilter" : true,
                 "sAjaxSource" : handler,
                 "sPaginationType": "full_numbers",
                 "bLengthChange": true,
                 "bPaginate" : true,
                 "bStateSave": true,
                 "iDisplayLength ":25,
                   "sScrollY": "300px",
                    "bScrollCollapse": true,
                 "sDom": '<"top"li>rt<"bottom"p>',

                         "fnStateSave": function (oSettings, oData) {
                             localStorage.setItem( 'DataTables_'+window.location.pathname, JSON.stringify(oData) );
                         },
                         "fnStateLoad": function (oSettings) {
                             return JSON.parse( localStorage.getItem('DataTables_'+window.location.pathname) );
                         },

                 "fnStateLoadParams": function (oSettings, oData) {
                    var searchVals = oData.aoSearchCols
                    $(".display tfoot input").each( function (i) {
                        if(searchVals[i] != null){
                        if (searchVals[i].sSearch != "" ){
                            this.value = searchVals[i].sSearch
                            self.asInitVals[i] = this.value;
                            this.className = "search_init_focus_on";
                            $(this).css('color',"black")
                            $(this).focus()
                        }
                    }
                    })
                    self.asInitVals = asInitVals
                 },

                 "fnServerParams": function ( aoData ) {
                    aoData.push( { "name": "testsuiteid", "value": -1 } , {"name" : "testresult","value": self.testresult} );
                }
                            } );   

            });
      
      this.addFiltering = function(){
          addFiltering(this)
      }

      this.addAnalyzeButtonHandler = function(){
        var self = this;
        var test_from = '#tests_run_form'
        $(function(){
            $(test_from).submit( function() {
                var aTrs = self.oTable.fnGetNodes();
                var testsuiteList = new Array()
                for ( var i=0 ; i<aTrs.length ; i++ )
                {
                    if ( $(aTrs[i]).hasClass('datatablerowhighlight') )
                    {
                        testsuiteList.push(self.oTable.fnGetData(aTrs[i]).testsuite.id)
                    }
                }
                $('<input />').attr('type', 'hidden')
                .attr('name', "testsuiteId")
                .attr('value',  self.rawData.testsuite.id)
                .appendTo(test_from);
                 $('<input />').attr('type', 'hidden')
                .attr('name', "testsuitelist")
                .attr('value',  JSON.stringify(testsuiteList))
                .appendTo(test_from);
                return true;
            } );
        });
    };

        this.addMultiClickRawHandler = function(){
            var self = this;
            $(function(){

                $('#' + tableid+' tbody tr').filter(':has(:checkbox:checked)').end().live('click',function(event) {
                    self.rawData = self.oTable.fnGetData(this);
                  
                    if($(':checkbox', this).is(':checked') == false) {
                        var allUnchecked = true
                        $(this).removeClass('datatablerowhighlight');
                        $('#' + tableid+' tbody tr').parent().children().each(function(){
                            if($(':checkbox', this).is(':checked') == true) {
                                allUnchecked = false
                            }
                        });
                        if (allUnchecked){
                            for (var i in buttons){
                                $('#' + buttons[i]).attr('disabled',true)
                        }
                        }
                    }
                    else
                    {
                        
                        for (var i in buttons){
                            $('#' + buttons[i]).attr('disabled',false)
                        }
                        $(':checkbox', this).attr('checked',true)
                        $(this).addClass('datatablerowhighlight');
                        self.row = this
                    }
                    
                });        
            });
        };
         
    };











    function ReportListDataTable(){
            var self = this;
            var tableid = "reporttableid"
            var handler = "/" + appName + "/labels/labelHandler"
            var asInitVals = new Array()
            self.asInitVals = asInitVals
            var buttons = ['analyzeReportButton', 'generateReport', 'generateNewReport']
            var tableColumns = [
              { "sTitle": "Select", "bSortable": false ,"sWidth": "6%","mData" : null,
                "sDefaultContent": '<input type = "checkbox">'},
              { "sTitle": "Id",   "sWidth": "10%", "mData": "id" },
              { "sTitle": "Name", "sWidth": "45%", "mData": "releasecandidatename" },
              { "sTitle": "Date", "sWidth": "20%", "mData": "date" },
              { "sTitle": "User", "sWidth": "30%","mData": "user" }]

            var sorting = [[ 1, "desc" ]]

                $(function(){
                     self.oTable = $('#' + tableid).dataTable( {

                     "fnDrawCallback": function(){
                        $("#"+tableid+" tfoot input").each( function (i) {
                            if(this.value == ""){
                                self.asInitVals[i] = "Search"
                                $(this).blur(); 
                                $(this).css('color',"#999")
                            }
                        } );

                        },
                     "aoColumns": tableColumns,
                     "aaSorting": sorting,
                     "bAutoWidth": false,
                     "bServerSide" : true,
                     "bProcessing" : true,
                     "bFilter" : true,
                     "sAjaxSource" : handler,
                     "sPaginationType": "full_numbers",
                     "bLengthChange": true,
                     "bPaginate" : true,
                     "bStateSave": true,
                     "iDisplayLength ":25,
                       "sScrollY": "300px",
                        "bScrollCollapse": true,
                     "sDom": '<"top"li>rt<"bottom"p>',

                     "fnStateSave": function (oSettings, oData) {
                         localStorage.setItem( 'DataTables_'+window.location.pathname, JSON.stringify(oData) );
                     },
                     "fnStateLoad": function (oSettings) {
                         return JSON.parse( localStorage.getItem('DataTables_'+window.location.pathname) );
                     },

                     "fnStateLoadParams": function (oSettings, oData) {
                        var searchVals = oData.aoSearchCols
                        $(".display tfoot input").each( function (i) {
                            if(searchVals[i] != null){
                            if (searchVals[i].sSearch != "" ){
                                this.value = searchVals[i].sSearch
                                self.asInitVals[i] = this.value;
                                this.className = "search_init_focus_on";
                                $(this).css('color',"black")
                                $(this).focus()
                            }
                        }
                        })
                        self.asInitVals = asInitVals
                     },
                  } );   

                });
          
          this.addFiltering = function(){
              addFiltering(this)
          };

          this.addSingleClickRawHandler = function(){
              var self = this;
              $(function(){

                  $('#' + tableid+' tbody tr').filter(':has(:checkbox:checked)').end().live('click',function(event) {
                      
                      if($(':checkbox', this).is(':checked') == false) {
                            for (var i in buttons){
                                $('#' + buttons[i]).attr('disabled',true);  
                            }
                          $(this).removeClass('datatablerowhighlight');
                      }
                      else
                      {
                          $('#' + tableid+' tbody tr').parent().children().each(function(){
                              $(this).removeClass('datatablerowhighlight');
                              $(':checkbox', this).attr('checked',false)
                          });
                          for (var i in buttons){
                              $('#' + buttons[i]).attr('disabled',false)
                          }
                          $(':checkbox', this).attr('checked',true)
                          $(this).addClass('datatablerowhighlight');
                      }
                      self.rawData = self.oTable.fnGetData(this);
                  });        
              });
          };

          this.addShowReportButtonHandler = function(){
              var self = this;
              var reportlist_form = '#report_list_form'
              $(function(){
                  $(reportlist_form).submit( function() {
                      $('<input />').attr('type', 'hidden')
                      .attr('name', "labelid")
                      .attr('value',  self.rawData.id)
                      .appendTo(reportlist_form);
                      return true;
                  } );
              });
          };



        this.addGenerateReportButtonAjaxHandler = function(buttonid, report_design_name){
            var self = this;
            $(function(){

                $('#'+buttonid).live('click',function () {
                     $.ajax({
                     type: "POST",
                     url: '/'+appName+'/fact/checkifanalyzed',
                     data: "labelid="+self.rawData.id
                     }).done(function( isAnalyzed ) {
                      if (isAnalyzed == "True"){
                            $('#waitingModal').modal({
                              backdrop: 'static',
                              keyboard: false
                            })

                            $.ajax({
                            type: "POST",
                            url:'/'+appName+'/labels/generateReport',
                            data: {"labelid": self.rawData.id, "report_design_name": report_design_name}
                            }).done(function( url ) {
                              $('#waitingModal').modal('hide')
                              window.location.href = url
                            })
                      }
                      else{
                        alert("You should analyzed testsuites from label before generating report")
                      }
                    
                     });
                });
            });
        };
             
        };






    function AnalysisDataTable(i, testsuiteid){
        var self = this;
        var asInitVals = new Array()
        self.asInitVals = asInitVals
        var tableid = "analysistable"+i
        var collapseid = "collapseOne"+i
        var analyzeButtonid = "Save"+i
        var analyzedCheckboxid = "analyzedcheckbox"+i
        var handler = "/" + appName + "/fact/analyzeHandler"
        var testsuiteid = testsuiteid
        var tableColumns = [
          { "sTitle": "Testcase name","sWidth": "20%","mData" : "testdescription.name"},
          // { "sTitle": "Testcase description","bSortable": false,"sWidth": "20%", "mData": "testdescription.testdescription" },
          { "sTitle": "Status","sWidth": "6%", "mData": "testresult.testresult" },
          { "sTitle": "Error description", "bSortable": false, "sWidth": "6%", "mData": null,
            "mRender": function ( data, type, full ) {
                return '<img id="error_img" style="width:22px; height:22px"  src="../static/images/details_open.png">'
            }
          },
          { "sTitle": "Error description","bVisible" : false, "bSortable": false, "mData": "testresult.failuredescription" },
          { "sTitle": "Bug type","sWidth": "10%","bSortable": false, "mData": "analysis.errortype" },
          { "sTitle": "Jira Id (number only)","sWidth": "7%", "bSortable": false,"mData": "analysis.jira_id" },
          { "sTitle": "Comment", "bVisible" : false, "bSortable": false, "mData": "analysis.comment" },
          { "sTitle": "Testresult id", "bVisible" : false, "mData" : "testresult.id"},
          { "sTitle": "Analysis id", "bVisible" : false, "mData" : "analysis.id"},
          { "sTitle": "Comment", "sWidth": "6%", "bSortable": false,"mData": null,
            "mRender": function ( data, type, full ) {
                return '<img id="comment_img" style="width:22px; height:22px"  src="../static/images/details_open.png">'
            }
          },
          { "sTitle": "On/Off","sWidth": "3%","bSortable": false, "mData": "test.include_test" },


          ]

        var sorting = [[ 2,"desc" ]]

            $(function(){
                 self.oTable = $('#' + tableid).dataTable( {

                 "fnDrawCallback": function(){

                    $("#"+tableid+" tbody input").keyup(function() {
                       $('#'+collapseid+' .warningAnalysis').css('display','block')
                    }); 

                    $("#"+tableid+" tbody select").live("change", function()   
                    {   
                        $('#'+collapseid+' .warningAnalysis').css('display','block')
                    }); 


                    $("#"+tableid+" tfoot input").each( function (i) {
                        if(this.value == ""){
                            self.asInitVals[i] = "Search"
                            $(this).blur(); 
                            $(this).css('color',"#999")
                        }
                    } );

                    },
                 "aoColumns": tableColumns,
                 "aaSorting": sorting,
                 "bAutoWidth": false,
                 "bServerSide" : true,
                 "bProcessing" : true,
                 "bFilter" : true,
                 "sAjaxSource" : handler,
                 "bPaginate" : false,
                 "iDisplayLength ":25,
                    "bScrollCollapse": true,
                 "sDom": '<"top"li>rt<"bottom"p>',

                 "fnServerParams": function ( aoData ) {
                    aoData.push( { "name": "testsuiteid", "value": testsuiteid } , {"name" : "testresult","value": self.testresult} );
                  }

              } );   

            });
      
      this.addFiltering = function(){
          addFiltering(this)
      };


      this.addSaveButtonAjaxHandler = function(){
          var self = this;
          $(function(){

              $('#'+analyzeButtonid).live('click',function () {
                  var analysisMap = new Array();
                  var aTrs = self.oTable.fnGetNodes();               
                  for ( var i=0 ; i<aTrs.length ; i++ )
                  {
                          var tempmap = {}
                          tempmap['errortype'] = $('#errortype',aTrs[i]).find('option:selected').text();
                          tempmap['jira_id'] = $('#jira_id',aTrs[i]).val();

                          if( $("#comment_id",$(aTrs[i]).next()).val() )
                          {
                              tempmap['comment'] = $("#comment_id",$(aTrs[i]).next()).val()
                          }
                          else
                          {
                              tempmap['comment'] = self.oTable.fnGetData(aTrs[i]).analysis.comment;
                          }
                          tempmap['testresult_id'] = self.oTable.fnGetData(aTrs[i]).testresult.id;
                          tempmap['analysis_id'] = self.oTable.fnGetData(aTrs[i]).analysis.id;
                          tempmap['include_test'] = $('#include_test',aTrs[i]).prop('checked');
                          tempmap['testresult'] = self.oTable.fnGetData(aTrs[i]).testresult.testresult;

                          analysisMap.push( tempmap );
                  }
                  testsuite_id = -1
                  if($('#'+analyzedCheckboxid).is(':checked')== true){
                          testsuite_id = testsuiteid
                  }

                  $('#waitingModal').modal({
                    backdrop: 'static',
                    keyboard: false
                  })
                  $.ajax({
                    type: "POST",
                    cache: false,
                    url: '/'+ appName +'/fact/saveAnalyze',
                    data: {"analysisMap":JSON.stringify(analysisMap),"testsuiteid":testsuite_id},
                    success: function(data, status, xml){
                      // do something is successful
                      $('#'+collapseid+' .warningAnalysis').css('display','none')
                      if (testsuiteid!=-1){
                          $("#img"+testsuiteid).attr("src", "../static/images/yes2.jpg");
                      }
                     },
                     error: function(xml, status, error){
                      // do something if there was an error
                          window.alert('Something has gone wrong. Please try to click Save button again')
                     },
                     complete: function(xml, status){
                      $('#waitingModal').modal('hide')
                      // do something after success or error no matter what
                     }
                    })               
              });
          });
      };

      this.addSwitchDataHandler = function(){
          var self = this;
          $('#' + collapseid +' #nok').live('click',function () {
              self.testresult = 'NOK'
              self.oTable.fnDraw(false);
          })

          $('#' + collapseid +' #ok').live('click',function () {
              self.testresult = 'OK'
              self.oTable.fnDraw(false);
          })

          $('#' + collapseid +' #ok_and_nok').live('click',function () {
              self.testresult = 'ALL'
              self.oTable.fnDraw(false);
          })
      };


      this.addCommentColumnHandler = function(imgid , textareaid, innerhtml, tablename, columnname ){
          var self = this;
          $('#'+tableid+ ' tbody td #'+imgid).live('click', function () {
                  var nTr = $(this).parents('tr')[0];
                  console
                  if ( self.oTable.fnIsOpen(nTr) )
                  {
                      if($(this).attr('id') == $(self.img_id).attr('id') ){
                          self.oTable.fnGetData(nTr)[tablename][columnname] = $('#'+self.textareaid,$(nTr).next()).val()
                          this.src = "../static/images/details_open.png";
                          self.oTable.fnClose( nTr );
                      }else{
                          $(self.img_id).attr('src', "../static/images/details_open.png")
                          $(this).attr('src', "../static/images/details_close.png")
                          self.oTable.fnOpen( nTr, fnFormatDetails(innerhtml, self.oTable.fnGetData( nTr )[tablename][columnname]), 'details' );
                          self.textareaid = textareaid
                          self.img_id = $(this)
                      }
                  }
                  else
                  {
                      /* Open this row */
                      this.src = "../static/images/details_close.png";
                      self.oTable.fnOpen( nTr, fnFormatDetails(innerhtml, self.oTable.fnGetData( nTr )[tablename][columnname]), 'details' );
                      self.textareaid = textareaid
                      self.img_id = $(this)
                       $("#"+tableid+" tbody #comment_id").keyup(function() {
                          $('#'+collapseid+' .warningAnalysis').css('display','block')
                      }); 
                  }
              } );
      };

             
    };



