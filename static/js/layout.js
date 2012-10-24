
$(function(){

	//show label preview menu at start
	$(this).find('#label_dropdown_menu').fadeToggle(0);

	//show hide label preview menu by clicking on button
	$('#dropdownbutton').live('click',function () {
	   	$(this).find('#label_dropdown_menu').fadeToggle("fast");
	});

	//stop hiding menu after clicking on label preview menu. (tested on firefox)
	$('#label_dropdown_menu').live('click',function () {
	    event.stopPropagation();
	});

	//removing rows in show label preview menu after clicking on remove icon. Also it removes from session
	$('.icon-remove').live('click',function () {
	    testsuiteid =  $(this).closest('a').attr('value')
	  	$(this).closest('li').remove()
	    	$.ajax({
		      	type: "POST",
		      	url: "/web2py_birt/fact/removeLabelFromSession",
		      	data: "testsuiteid=" + testsuiteid
		      	}).done(function( msg ) {
		         	if (msg == 0){
		            	$('#vsrunningsdivider').before($('<li id="nonefactrunnings" class="none"><h8>none</h8></li>'))
		        	}
	    		});
	});

	//edit testsuite by ckicking on edit icon in label preview menu
	$('.icon-pencil').live('click',function () {
	    testsuiteid =  $(this).closest('a').attr('value')
	    $('#form').unbind('submit')
	  	            $('#form').submit( function() {
	  	                $('<input />').attr('type', 'hidden')
	  	                .attr('name', "testsuiteId")
	  	                .attr('value',  testsuiteid)
	  	                .appendTo('#form');
	  	                return true;
	  	            } );
	  	$("#form").submit();
	});

	//deletes all rows in label preview menu and adds 'none' row after new label is created
    $('#savelabelbutton').live('click',function () {
      $('#label_dropdown_menu li a').empty();
      $('#vsrunningsdivider').before($('<li id="nonefactrunnings" class="none"><h8>none</h8></li>'))
    });

    //by clicking on save label button on label preview menu,
    //it checks whether to show form for creating new label or show warning 
    //that you should add some run to preview
    $('#savelabel').live('click',function () {
        console.log($("#nonefactrunnings").length)
      if ( $("#nonefactrunnings").length == 0) {
        $('#myModal').modal('show')
      }
      else
      {
        alert("Label list is empty. Add some labels.")
      }
      
    });

	  // $('#test2').live('click',function () {
	  //   $('#nonevsrunnings').remove()
	  //   var myOptions = {
	  //       val2 : '<a value="10" href="#"><i class="icon-remove"></i>Vs gagaga</a>'
	  //   };
	  //   $.each(myOptions, function(val, text) {
	  //     $('#vsrunnings').after($('<li></li>').val(val).html(text));
	  //   });
	  // });
	
	// make all buttons bootstrap buttons
	$('button, form input[type="submit"], form input[type="button"]').addClass('btn').css({'margin-right':'2px','margin-bottom':'2px'});

});
