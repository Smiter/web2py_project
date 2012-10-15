var MyApp = {

    addDataTable: function(tableid,tableColumns,sorting, handler,buttons){
        var self = this;
            $(function(){
                 self.oTable = $('#' + tableid).dataTable( {

                 "fnDrawCallback": function(){
                    for (var i in buttons){
                        $('#' + buttons[i]).attr('disabled',true);  
                    }

                    $('#' + tableid +' td').bind('mouseenter', function () { 
                        $(this).parent().children().each(function(){
                            $(this).addClass('datatablerowhighlight');
                        });
                    });

                    $('#' + tableid +' td').bind('mouseleave', function () { 
                        $(this).parent().children().each(function(){
                            $(this).removeClass('datatablerowhighlight');
                        });
                    });

                    },
                 "aoColumns": tableColumns,
                 "aaSorting": sorting,
                 "bJQueryUI": true,
                 "bServerSide" : true,
                 "bProcessing" : true,
                 "bFilter" : true,
                 "sPaginationType": "full_numbers",
                 "sAjaxSource" : handler,
                 "fnServerParams": function ( aoData ) {
                    aoData.push( { "name": "testsuiteid", "value": self.testsuiteid } );
                }
                            } );   

            });
    },

    addFiltering: function(){
        var self = this;
        var asInitVals = new Array();
            $(function(){
                  $("tfoot input").keyup( function () {
                        /* Filter on the column (the index) of this element */
                        self.oTable.fnFilter( this.value, $("tfoot input").index(this) );
                    } );

                    $("tfoot input").each( function (i) {
                        asInitVals[i] = this.value;
                    } );
                     
                    $("tfoot input").focus( function () {
                        if ( this.className == "search_init_focus_of" )
                        {
                            this.className = "search_init_focus_on";
                            this.value = "";
                        }
                    } );
                     
                    $("tfoot input").blur( function (i) {
                        if ( this.value == "" )
                        {
                            this.className = "search_init_focus_of";
                            this.value = asInitVals[$("tfoot input").index(this)];
                        }
                    } );    
           });
    },

    addButton: function(buttonid,tableid,style,type){
        var self = this;
            $(function(){
                $('<button class="'+style+'" type="'+type+'"  id='+buttonid + 
                 ' disabled>'+ buttonid +'</button>').insertAfter('#' + tableid);
            });
    },

    addSingleClickRawHandler: function(buttons,tableid){
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
    },

    addMultiClickRawHandler: function(buttons,tableid){
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
    },

    addAnalyzeButtonHandler: function(){
        var self = this;
        $(function(){
            $('#form').submit( function() {
                $('<input />').attr('type', 'hidden')
                .attr('name', "testsuiteId")
                .attr('value',  self.rawData.testsuite.id)
                .appendTo('#form');
                return true;
            } );
        });
    },

    addSaveButtonHandler: function(){
        var self = this;

        $(function(){
            $('#form').submit( function() {
                    var analysisMap = new Array();
                    var aTrs = self.oTable.fnGetNodes();

                    for ( var i=0 ; i<aTrs.length ; i++ )
                    {
                        if ( $(aTrs[i]).hasClass('datatablerowhighlight') )
                        {
                            var tempmap = {}
                            tempmap['errortype'] = $('#errortype',aTrs[i]).find('option:selected').text();
                            tempmap['jira_id'] = $('#jira_id',aTrs[i]).val();
                            tempmap['comment'] = $('#comment_id',aTrs[i]).val();
                            tempmap['testresult_id'] = self.oTable.fnGetData(aTrs[i]).testresult.id;
                            analysisMap.push( tempmap );
                        }
                    }

                $('<input />').attr('type', 'hidden')
                .attr('name', "analysisMap")
                .attr('value',  JSON.stringify(analysisMap))
                .appendTo('#form');
                $('<input />').attr('type', 'hidden')
                .attr('name', "testsuiteid")
                .attr('value',  self.testsuiteid)
                .appendTo('#form');
                return true;
            } );
        });
    }
    
};
