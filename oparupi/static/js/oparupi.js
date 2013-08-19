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

  $('.last-post').cycle({
		fx: 'fade',
		delay:  -4000,
		timeout: 10000,
		speed: 500
	});

})( jQuery );