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
	    	$.scrollTo($('#nav'));
	    }
	);

  	$('.post').removeClass('start-hidden')

})( jQuery );