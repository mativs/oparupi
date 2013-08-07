(function( $ ){
	$('.posts').fisotope({
	    itemSelector : '.post',
	    layoutMode : 'masonry',
	    getSortData : {
	        title : function ( $elem ) {
	          return $elem.find('h4').text();
	        }
	    }
	});
})( jQuery );