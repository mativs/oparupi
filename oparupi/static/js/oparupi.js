(function( $ ){
	var total = $('.post').length

	$('.posts').fisotope({
		    itemSelector : '.post',
	   	 	layoutMode : 'masonry',
	    	empty_selection_behaviour: "hide"
	    },
	    function ( $items ) {
	    	// if ( $items.length == total) {
	    	//  	$('.posts').hide();
	    	// } else {
	    	//  	$('.posts').show();
	    	// }
	    	// $.scrollTo($('#nav'), 1);
	    }
	);

  $('.post').removeClass('start-hidden')

})( jQuery );