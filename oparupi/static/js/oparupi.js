(function( $ ){
	$('.posts').fisotope({
	    itemSelector : '.post',
	    layoutMode : 'fitRows',
	    getSortData : {
	        title : function ( $elem ) {
	          return $elem.find('h4').text();
	        }
	    }
	});
})( jQuery );