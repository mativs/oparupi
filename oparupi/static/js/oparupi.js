(function( $ ){
	$('.posts').fisotope({
		    itemSelector : '.post',
	   	 	filter: '.itecito-1',
	   	 	layoutMode : 'masonry',
	    	default_facet_operator: {
	    		sections:'or'
	    	},
	    	empty_selection_behaviour: "hide"
	    },
	    function ( $items ) {
	    	if ( $items.length == 0) {
	    		$('#pre-header').slideDown(400);
	    	} else {
	    		$('#pre-header').slideUp(1000);
	    	}
	    	// $.scrollTo($('#nav'), 1);
	    }
	);

	$('.fiso-toggle-category').click(function() {
		
	})
  	
  $('.post').removeClass('start-hidden')

})( jQuery );