(function( $ ){

	$('.posts').fisotope({
		    itemSelector : '.post',
	   	 	layoutMode : 'masonry',
	    	empty_selection_behaviour: "hide"
	    },
	    function ( $items ) {
	    	$.scrollTo($('header nav'), 1);
	    }
	);

  $('.post').removeClass('start-hidden')

})( jQuery );