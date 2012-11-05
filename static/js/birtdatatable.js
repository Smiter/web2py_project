function DataTable(){
    this.addDataTable = function(tableid,tableColumns,sorting,handler,buttons,testsuiteid,blenchChange,bPaginate){
        var self = this;
        var asInitVals = new Array()
        self.asInitVals = asInitVals
            $(function(){
                 self.oTable = $('#' + tableid).dataTable( {

                 "fnDrawCallback": function(){
                    for (var i in buttons){
                        $('#' + buttons[i]).attr('disabled',true);  
                    }

                    $("#"+tableid+" tfoot input").each( function (i) {
                        if(this.value == ""){
                            self.asInitVals[i] = "Search"
                            $(this).blur(); 
                        }
                    } );

                    },
                 "aoColumns": tableColumns,
                 "aaSorting": sorting,
                 "bJQueryUI": true,
                 "bServerSide" : true,
                 "bProcessing" : true,
                 "bFilter" : true,
                 "sAjaxSource" : handler,
                 "sPaginationType": "full_numbers",
                 "bLengthChange": blenchChange,
                 "bPaginate" : bPaginate,
                 "bStateSave": true,
                 "fnStateLoadParams": function (oSettings, oData) {
                    var searchVals = oData.aoSearchCols
                    $("#"+tableid+" tfoot input").each( function (i) {
                        if (searchVals[i].sSearch != "" ){
                            this.value = searchVals[i].sSearch
                            self.asInitVals[i] = this.value;
                            this.className = "search_init_focus_on";
                        }
                    })
                    self.asInitVals = asInitVals
                 },

                 "fnServerParams": function ( aoData ) {
                    aoData.push( { "name": "testsuiteid", "value": testsuiteid } );
                }
                            } );   

            });
    };

    this.addFiltering = function(tableid){
        var self = this;
        // var asInitVals = self.asInitVals
            $(function(){
                  $("#"+tableid+" tfoot input").keyup( function () {
                        /* Filter on the column (the index) of this element */
                        self.oTable.fnFilter( this.value, $("#"+tableid+" tfoot input").index(this) );
                    } );

                    $("#"+tableid+" tfoot input").each( function (i) {
                        if(self.asInitVals[i] != null){
                            self.asInitVals[i] = this.value;
                        }
                    } );
                     
                    $("#"+tableid+" tfoot input").focus( function () {
                        if ( this.className == "search_init_focus_of" )
                        {
                            this.className = "search_init_focus_on";
                            this.value = "";
                        }
                    } );
                     
                    $("#"+tableid+" tfoot input").blur( function (i) {
                        if ( this.value == "" )
                        {
                            this.className = "search_init_focus_of";
                            this.value = "Search"
                        }
                    } );    
           });
    };

    this.addButton = function(buttonid,tableid,style,type,buttonname){
        var self = this;
            $(function(){
                $('<button class="'+style+'" type="'+type+'"  id='+buttonid  
                 +'>'+ buttonname +'</button>').insertAfter('#' + tableid);
            });
    };

    

    this.addSingleClickRawHandler = function(buttons,tableid){
        var self = this;
        $(function(){

            $('#' + tableid+' tbody tr').filter(':has(:checkbox:checked)').end().live('click',function(event) {
                
                if (event.target.type !== 'checkbox') {
                    $(':checkbox', this).attr('checked', function() {
                        return !this.checked;
                    });
                }
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

    this.addMultiClickRawHandler = function(buttons,tableid){
        var self = this;
        var clickOnCombo = false
        $(function(){

            $('#' + tableid+' tbody tr').filter(':has(:checkbox:checked)').end().live('click',function(event) {
                self.rawData = self.oTable.fnGetData(this);
                $('#errortype',this).live('click',function(event) {
                         clickOnCombo = true
                });

                if (event.target.type !== 'checkbox') {
                    
                    $(':checkbox', this).attr('checked', function() {
                        if(this.checked == true && (clickOnCombo == true || event.target.type == 'text' || event.target.type == 'textarea' || event.target.type == 'select-one'))
                        {
                            clickOnCombo=false
                            return;
                        }
                        return !this.checked;
                    });
                }
                if($(':checkbox', this).is(':checked') == false) {
                    var allUnchecked = true
                    $(this).removeClass('datatablerowhighlight');
                    clickOnCombo = false
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

    this.addAnalyzeButtonHandler = function(){
        var self = this;
        $(function(){
            $('#form').submit( function() {
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
                .appendTo('#form');
                 $('<input />').attr('type', 'hidden')
                .attr('name', "testsuitelist")
                .attr('value',  JSON.stringify(testsuiteList))
                .appendTo('#form');
                return true;
            } );
        });
    };

    this.addSaveButtonHandler = function(){
        var self = this;

        $(function(){
            $('#form').submit( function() {
                    var analysisMap = new Array();
                    var aTrs = self.oTable.fnGetNodes();

                    for ( var i=0 ; i<aTrs.length ; i++ )
                    {
                        // if ( $(aTrs[i]).hasClass('datatablerowhighlight') )
                        // {

                            var tempmap = {}
                            tempmap['errortype'] = $('#errortype',aTrs[i]).find('option:selected').text();
                            tempmap['jira_id'] = $('#jira_id',aTrs[i]).val();
                            tempmap['comment'] = $('#comment_id',aTrs[i]).val();
                            tempmap['testresult_id'] = self.oTable.fnGetData(aTrs[i]).testresult.id;

                            analysisMap.push( tempmap );
                            
                        // }
                    }

                // console.log(analysisMap)
                if(analysisMap.length){
                    testsuiteid = -1
                    if($("#analyzedcheckbox").is(':checked') == true){
                        testsuiteid = self.testsuiteid
                    }
                    $('<input />').attr('type', 'hidden')
                    .attr('name', "analysisMap")
                    .attr('value',  JSON.stringify(analysisMap))
                    .appendTo('#form');
                    $('<input />').attr('type', 'hidden')
                    .attr('name', "testsuiteid")
                    .attr('value',  testsuiteid)
                    .appendTo('#form');
                }
                // self.oTable.fnDraw(false); 
                return true;
            } );
        });
    };

    this.addSaveButtonAjaxHandler = function(buttonid){
        var self = this;

        $(function(){

            $('#'+buttonid).live('click',function () {
                var analysisMap = new Array();
                var aTrs = self.oTable.fnGetNodes();               
                for ( var i=0 ; i<aTrs.length ; i++ )
                {
                    // if ( $(aTrs[i]).hasClass('datatablerowhighlight') )
                    // {
                        var tempmap = {}
                        tempmap['errortype'] = $('#errortype',aTrs[i]).find('option:selected').text();
                        tempmap['jira_id'] = $('#jira_id',aTrs[i]).val();
                        tempmap['comment'] = $('#comment_id',aTrs[i]).val();
                        tempmap['testresult_id'] = self.oTable.fnGetData(aTrs[i]).testresult.id;
                        tempmap['analysis_id'] = self.oTable.fnGetData(aTrs[i]).analysis.id;
                        analysisMap.push( tempmap );
                        
                    // }
                }
                testsuiteid = -1
                if($('#'+buttonid).parent().find('input:checkbox:first').is(':checked')== true){
                        testsuiteid = self.testsuiteid
                }

                $('#waitingModal').modal({
                  backdrop: 'static',
                  keyboard: false
                })

                $.ajax({
                  type: "POST",
                  cache: false,
                  url: "/web2py_birt/fact/saveAnalyze",
                  data: {"analysisMap":JSON.stringify(analysisMap),"testsuiteid":testsuiteid}
                  }).done(function( msg ) {
                    $('#waitingModal').modal('hide')

                    if (testsuiteid!=-1){
                        $("#img"+testsuiteid).attr("src", "../static/images/yes2.jpg");
                    }
                    // self.oTable.fnDraw(false); 
                    self.oTable.fnReloadAjax()
                  })
            });
        });
    };


    this.addGenerateReportButtonAjaxHandler = function(buttonid){
        var self = this;

        $(function(){

            $('#'+buttonid).live('click',function () {
                console.log(self.rawData.id)
                 $.ajax({
                 type: "POST",
                 url: "/web2py_birt/fact/checkifanalyzed",
                 data: "labelid="+self.rawData.id
                 }).done(function( isAnalyzed ) {
                    console.log(isAnalyzed)
                  if (isAnalyzed == "True"){
                        $.ajax({
                        type: "POST",
                        url: "/web2py_birt/labels/generateReport",
                        data: "labelid="+self.rawData.id
                        }).done(function( url ) {
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


    this.addShowLabelButtonHandler = function(){
        var self = this;
        $(function(){
            $('#form').submit( function() {
                $('<input />').attr('type', 'hidden')
                .attr('name', "labelid")
                .attr('value',  self.rawData.id)
                .appendTo('#form');
                return true;
            } );
        });
    };
}