$('body').prepend('<div id="noconflictowner">' +
		'<div id="noconflictlink">Poop poop poop yay!</div >' +
		'<div id="noconflictbox">Poop poop poop yay!</div >' +
		'</div>');
$('#noconflictlink').hide();
$('#noconflictbox').hide();
var asd = 5;

function positionTooltip(event){
	var tPosX = event.pageX;
	var tPosY = event.pageY;
	console.log("print to", tPosX, tPosY);
	//$('#noconflictbox').css({'position': 'absolute', 'top': tPosY, 'left': tPosX});
};

var searchUrl = 'https://localhost:5123/api?query=' + window.location.href;
req = new XMLHttpRequest();
req.open('GET', searchUrl);
req.onload = function() {
  alert( req.response );
	console.log("res loaded doing the thing");
	$('#noconflictlink').show();
	$('#noconflictbox').html(req.response);

	$('#noconflictlink').mouseenter( function( event ) {
		console.log("click detected");
		console.log("Showed the thing");
		$('#noconflictbox').show();
		positionTooltip(event);
	});
	$('#noconflictowner').mouseleave( function( event ) {
		$('#noconflictbox').hide(200);
	});
}
req.send()
