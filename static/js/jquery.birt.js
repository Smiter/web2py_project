/*
* jquery.birt
*
* Contains utilities for birt application
*
*/
(function($){
    $.birt = {
           addTestRunToReportPreview: function (table){
            /*
            * add to report preview menu new item
            *
            */
                $('#addtolabel').live('click',function () {
                    $("#shortreportpreview .none").css('display','none')
                    var tempMap={}
                    var aTrs = table.oTable.fnGetNodes();
                    for ( var i=0 ; i<aTrs.length ; i++ )
                      {
                        if ( $(aTrs[i]).hasClass('datatablerowhighlight') )
                        {
                          var testsuiteId = table.oTable.fnGetData(aTrs[i]).testsuite.id
                          var testsuiteName = table.oTable.fnGetData(aTrs[i]).testsuite.testsuitename
                          tempMap[testsuiteId] = testsuiteName
                        }
                    }
                    $.ajax({
                      type: "POST",
                      url: "/" + appName + "/fact/saveLabelList",
                      data: "array="+JSON.stringify(tempMap)
                      }).done(function( msg ) {
                        var testsuites = JSON.parse(msg);
                        $.each(testsuites, function(val, text) {
                          $("#fact_runnings_preview_list").append('<li><i class="icon-remove"></i><i class="icon-pencil"></i><p value='+val+'>'+text+'</p></li>');
                        });
                      });

                });
           },

           iconRemoveFromReportPreview: function (){
            /*
            * Remove rows in show report preview menu after clicking on remove icon.
            * Also it removes test run from session
            *
            */
                $('#shortreportpreview .icon-remove').live('click',function () {
                    testsuiteid =  $(this).closest('li').children('p').attr('value')
                    $(this).closest('li').remove()
                      $.ajax({
                            type: "POST",
                            url: "/" + appName + "/fact/removeLabelFromSession",
                            data: "testsuiteid=" + testsuiteid
                            }).done(function( msg ) {
                            if (msg == 0){
                                $("#shortreportpreview .none").css('display','block')
                            }
                        });
                });
           },

           editTestSuiteFromReportPreview: function (){
            /*
            * Edit testsuite by clicking on edit icon in report preview menu
            *
            */
                $('#shortreportpreview .icon-pencil').live('click',function () {
                    testsuiteid =  $(this).closest('li').children('p').attr('value')
                    testsuitelist = []
                    testsuitelist.push(testsuiteid)
                    $('#tests_run_form').unbind('submit')
                    $("#tests_run_form").attr("action", "/" + appName + "/fact/analysis");
                    $('#tests_run_form').submit( function() {
                        $('<input />').attr('type', 'hidden')
                        .attr('name', "testsuitelist")
                        .attr('value',  JSON.stringify(testsuitelist) )
                        .appendTo('#tests_run_form');
                        return true;
                    } );
                    $("#tests_run_form").submit();
                });
           },
           addActionsForShortReportPreview: function (){
            /*
            * Deletes all rows in report preview menu and adds 'none' row after
            * new report is created.
            *
            * By clicking on save report button on report preview menu,
            * it checks whether to show form for creating new label or show warning 
            * that you should add some run to preview
            *
            */
                $('.modal-backdrop fade in').unbind('click');
                $('#savelabelbutton').live('click',function () {
                      $('#fact_runnings_preview_list li p').empty();
                      $("#shortreportpreview .none").css('display','block')
                });
                $('#shortreportpreview #savelabel').live('click',function () {
                  if ( $("#fact_runnings_preview_list li").length == 0) {
                     alert("Label list is empty. Add some labels.")
                  }
                  else{
                    $('#reportModalForm').modal('show')
                  }
                  
                });
           },

           analysisBackClickHandler: function (){
            /*
            * Click handler for go back from analysis page
            */
                $('#analysisback').live('click',function () {
                     history.back();
                })
           },

           ShowNOKTestsForAnalysisDatatablesByDefault: function (testsuiteArray_size){
            /*
            * When we go to analysis page, show by default NOK tests
            */
                for(var i=0;i<testsuiteArray_size;i++){
                  $('#collapseOne'+i+' #nok').click()
                }
           },

           addClickHandlerForCollapseTables: function (testsuiteArray_size){
            /*
            * Click handler for analysis page collapse images (tables)
            */
                  $('.collapse_button').find("img").click(function() {
                  }).toggle(function() { 
                      $(this).attr("src", "../static/images/close.png"); 
                      $($(this).parent().attr("href")).collapse('show')
                  }, function(){
                      $(this).attr("src", "../static/images/more.png");
                      $($(this).parent().attr("href")).collapse('hide')
                });
           },
   


    }
    $.fn.birt = function(method){
            // Method calling logic
            if ( $.birt[method] ) {
              return $.birt[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
            } else if ( typeof method === 'object' || ! method ) {
              return $.birt.init.apply( this, arguments );
            } else {
              $.error( 'Method ' +  method + ' does not exist on jQuery.birt' );
            }
    }
})(jQuery);