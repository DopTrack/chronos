$(document).ready(function() {
	$( ".frame1 .faldon .texto .textoFrame2").hide();
	$( ".frame1 .faldon .texto .textoFrame2Linea2").hide();
	$( ".frame1 .faldon .texto .textoFrame1").hide();
	$( "#background").hide();
	$( "#background2").hide();
	$( "#background3").hide();
});
var loop = 0;
var stop = 0;
var time;
var frame = 1;

function changeBackground()
{
	switch(frame){
  	case 1:
  		name = "#background3";
  		nameIn = "#background"
  		//frame = 1;
  		break;
  	case 2:
  		name = "#background";
  		nameIn = "#background2"
  		//frame = 2;
  		break;
  	case 3:
  		name = "#background2";
  		nameIn = "#background3";
  		//frame = 0;
  		break;
  }
  $( name ).fadeOut(1000);
  $( nameIn ).fadeIn(1000);
}

function ini(){
	$("#background" ).delay(400).fadeIn( "slow");
	/*
	var frame = 0;
	var name = "";
	var nameIn = "";
	time = setInterval(function() {
	  switch(frame){
	  	case 0:
	  		name = "#background";
	  		nameIn = "#background2"
	  		frame = 1;
	  		break;
	  	case 1:
	  		name = "#background2";
	  		nameIn = "#background3"
	  		frame = 2;
	  		break;
	  	case 2:
	  		name = "#background3";
	  		nameIn = "#background";
	  		frame = 0;
	  		break;
	  }
      $( name ).fadeOut(1000);
	  $( nameIn ).fadeIn(1000);
	}, 4000);
*/
	$(".logo").animate({
		marginLeft:'0px',
     },350,'easeInExpo',function(){
     });
	$(".texto").delay(100).animate({
		width: '254px',
	},350,'easeInExpo',function(){
		
		var posY = ($( ".frame1 .faldon .texto" ).height() - $( ".frame1 .faldon .texto .textoFrame1" ).height())/2;
		$( ".frame1 .faldon .texto .textoFrame1").css('margin-top',posY+'px');

		$( ".frame1 .faldon .texto .textoFrame1" ).fadeIn( "fast");
		$(".texto").css("float","right");
	});
	$(".frame1 .botonSuperior").delay(100).animate({
		marginRight: '5px',
	},350,'easeInExpo',function(){
		frame2();
	});
}
function frame2(){
		frame = 1;
		$( ".frame1 .faldon .texto .textoFrame1" ).delay(4000).fadeOut( "slow", function(){
			frame = 2;
			changeBackground();
			var posY = ($( ".frame1 .faldon .texto" ).height() - $( ".frame1 .faldon .texto .textoFrame2" ).height())/2;
			$( ".frame1 .faldon .texto .textoFrame2").css('margin-top',posY+'px');
		});
		$( ".frame1 .faldon .texto .textoFrame2" ).delay(4500).fadeIn( "slow", function(){

		});
		if(descuento == 0 ){
			$( ".frame1 .faldon .texto .textoFrame2").css("width","250px");
			$( ".frame1 .faldon .texto .textoFrame2").css("font-size","14px");
			$( ".frame1 .faldon .texto .textoFrame2").css("line-height","16px");
			$( ".frame1 .faldon .texto .textoFrame2").css("font-family", "gotham-medium");
			$( ".frame1 .faldon .texto .textoFrame2").css("-webkit-font-smoothing", "antialiased");
			$( ".frame1 .faldon .texto .textoFrame2").css("text-align","center");
			$( ".frame1 .faldon .texto .textoFrame2").css("padding","0");

		}else{

			$( ".frame1 .faldon .texto .textoFrame2Linea2" ).delay(4500).fadeIn( "slow");
		}
		$(".frame1 .botonSuperior #btnText").delay(4500).animate({
			marginTop:'-20px',
	    },350,'easeInBack',function(){
	    	frame = 2;
	    	$(".frame1 .botonSuperior #btnText").css("margin-top","23px");
	    	$(".frame1 .botonSuperior #btnText").delay(50).animate({
				marginTop:'0px',
		    },350,'easeOutBack',function(){

		    });
	    });
		$(".frame1 .botonSuperior").delay(8500).animate({
			marginRight: '-115px',
		},350,'easeInExpo',function(){

		});

		$(".texto").delay(8500).animate({
			width: '0px',
		},500,'easeInExpo',function(){
			$( ".frame1 .faldon .texto .textoFrame2" ).hide();
			$( ".frame1 .faldon .texto .textoFrame2Linea2" ).hide();
		});
		$(".frame1 .faldon .logo").delay(8500).animate({
			width: '343px',
			float: "left",
		},500,'easeInExpo',function(){
			frame = 3;
			changeBackground();
			$(".frame1 .faldon .boton").animate({
				marginTop: '25px',
			},500,'easeOutExpo',function(){
				$(".frame1 .faldon .boton").delay(3600).animate({
					marginTop: '103px',
				},500,'easeInExpo',function(){
					$(".frame1 .faldon .logo").animate({
						width: '89px',
					},350,'easeInExpo',function(){
						frame=1;
						changeBackground();
					});
					$(".texto").animate({
						width: '254px',
					},350,'easeInExpo',function(){
						$( ".frame1 .faldon .texto .textoFrame1" ).fadeIn( "slow");
						$(".frame1 .botonSuperior").delay(130).animate({
							marginRight: '5px',
						},350,'easeInExpo',function(){
							$(".frame1 .faldon .boton").css('marginTop', '-50px');
							loop +=1;
							if(stop == 0){
								if(loop <= (loopTotal-1) || loopTotal == 0){
									frame2();
								}else{
									clearInterval(time);
								}
							}
						});
					});
				});
			});
		});
	}
