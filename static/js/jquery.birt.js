/*
* jquery.birt
*
* Contains utilities for birt application
*
*/
(function($){
    $.birt = {
           addEditable: function(table, cell_index, column_name){
             $('td:eq(' + cell_index + ')', table.fnGetNodes()).editable( '/'+ appName +'/fact/edit_cell_value', {
                  "callback": function( sValue, y ) {
                      var aPos = table.fnGetPosition( this );
                      table.fnUpdate( sValue, aPos[0], aPos[1], false );
                  },
                  "submitdata": function ( value, settings ) {
                      var aPos = table.fnGetPosition( this );
                      testsuite_id = table.fnGetData(aPos[0]).testsuite.id
                      return { "testsuite_id": testsuite_id, "column_name": column_name };
                  },
                  "height": "30px",
                  tooltip: 'Click to Edit',
                  cancel: 'Cancel',
                  submit: 'Save',
             });
         }
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