(function( $ ){
	$('.posts').fisotope({
	    itemSelector : '.post',
	    layoutMode : 'masonry',
      default_facet_operator: {
        sections:'or'
      }
	});
})( jQuery );