
$(document).ready(function(){
	$("a,input:checkbox,input:radio,button,input:button").on('focus',function(){$(this).blur();});
});


function hideElement(currentElement, targetElement) {
	if (!$.isArray(targetElement)) {
		targetElement = [ targetElement ];
	}
	$(document).on("click.hideElement", function(e) {
		var len = 0, $target = $(e.target);
		for (var i = 0, length = targetElement.length; i < length; i++) {
			$.each(targetElement[i], function(j, n) {
				if ($target.is($(n)) || $.contains($(n)[0], $target[0])) {
					len++;
				}
			});
		}
		if ($.contains(currentElement[0], $target[0])) {
			len = 1;
		}
		if (len == 0) {
			currentElement.hide();
		}
	});
};

function add_search(){
	var val = $(".searchInput").val();
	window.location.href="/search/?q="+val+"&s_type="+$(".searchItem.current").attr('data-type');
}