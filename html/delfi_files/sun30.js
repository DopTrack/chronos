function getDayNightOverlay(satmap)
{
	var cnt = 0;
	var dayNightArray = new Array();
	var lngStart = satmap.getBounds().getSouthWest().lng();
	var latStart = satmap.getBounds().getSouthWest().lat();
	var latEnd = latStart;
	var lngEnd = satmap.getBounds().getNorthEast().lng();
	var j = jd();
	for (var i=lngStart; i<=lngEnd; i++) 
	{
		var dt = new Date();
		var LT = dt.getUTCHours() + dt.getUTCMinutes()/60;
		// var tau = 15*(LT-12); INCORRECT!

		DY = dayofyear(dt);
		g = (360/365.25)*(DY + LT/24);
		TC = 0.004297+0.107029*Math.cos(g*Math.PI/180)-1.837877*Math.sin(g*Math.PI/180)-0.837378*Math.cos(2*g*Math.PI/180)-2.340475*Math.sin(2*g*Math.PI/180);
		SHA = (LT-12)*15 + TC;

		var dec = sunDecRA(1,j);
		var K = Math.PI/180.0;
		var longitude=i+SHA;
		var tanLat = - Math.cos(longitude*K)/Math.tan(dec*K);						
		var arctanLat = Math.atan(tanLat)/K;
		dayNightArray[cnt]=new google.maps.LatLng(arctanLat,i);
		cnt++;
	}

	dayNightArray[0]=new google.maps.LatLng(latStart,lngStart);
	dayNightArray[dayNightArray.length-1]=new google.maps.LatLng(latEnd,lngEnd);
	var dayNightOverlay = new google.maps.Polygon(dayNightArray, "#7171FF", 1, 0.5,"#7171FF",0.5);
	//var polylineEncoder = new PolylineEncoder();
	//var dumbArray = new Array();
	//dumbArray[0] = dayNightArray;
  	//var dayNightOverlay = polylineEncoder.dpEncodeToGPolygon(dumbArray, "#7171FF", 1, 0.5,"#7171FF",0.5); 
	return dayNightOverlay;
}

function getSunOverlay()
{

	var j = jd();
	var dec = sunDecRA(1,j);
	var dt = new Date();
	var LT = dt.getUTCHours() + dt.getUTCMinutes()/60;
//	var tau = 15*(LT-12); INCORRECT!

	DY = dayofyear(dt);
	g = (360/365.25)*(DY + LT/24);
	TC = 0.004297+0.107029*Math.cos(g*Math.PI/180)-1.837877*Math.sin(g*Math.PI/180)-0.837378*Math.cos(2*g*Math.PI/180)-2.340475*Math.sin(2*g*Math.PI/180);
	SHA = (LT-12)*15 + TC;

    var icon =  new google.maps.MarkerImage();
    icon.url = "http://www.n2yo.com/img/sun.gif";
    icon.size = new google.maps.Size(16.0, 16.0);
	icon.anchor = new google.maps.Point(3.0, 3.0);
	var pos = new google.maps.LatLng(dec,-SHA)
	var sunMarker = new google.maps.Marker({position:pos,icon:icon});
	return sunMarker;
}
function jd() {
	var dt = new Date();
    MM=dt.getUTCMonth() + 1;
    DD=dt.getUTCDate();
    YY=dt.getUTCFullYear();
    HR=dt.getUTCHours();
    MN= dt.getUTCMinutes();
    //SC=0;
	SC = dt.getUTCSeconds();
    with (Math) {  
      HR = HR + (MN / 60) + (SC/3600);
      GGG = 1;
      if (YY <= 1585) GGG = 0;
      JD = -1 * floor(7 * (floor((MM + 9) / 12) + YY) / 4);
      S = 1;
      if ((MM - 9)<0) S=-1;
      A = abs(MM - 9);
      J1 = floor(YY + S * floor(A / 7));
      J1 = -1 * floor((floor(J1 / 100) + 1) * 3 / 4);
      JD = JD + floor(275 * MM / 9) + DD + (GGG * J1);
      JD = JD + 1721027 + 2 * GGG + 367 * YY - 0.5;
      JD = JD + (HR / 24);
    }
    return JD;
}
function sunDecRA (what, jd) {
		var PI2 = 2.0*Math.PI;
		var cos_eps = 0.917482;
		var sin_eps = 0.397778;				
		var M, DL, L, SL, X, Y, Z, R;
		var T, dec, ra;		
		T = (jd - 2451545.0) / 36525.0;	// number of Julian centuries since Jan 1, 2000, 0 GMT								
		M = PI2*frac(0.993133 + 99.997361*T);
		DL = 6893.0*Math.sin(M) + 72.0*Math.sin(2.0*M);
		L = PI2*frac(0.7859453 + M/PI2 + (6191.2*T+DL)/1296000);
		SL = Math.sin(L);
		X = Math.cos(L);
		Y = cos_eps*SL;
		Z = sin_eps*SL;
		R = Math.sqrt(1.0-Z*Z);
		dec = (360.0/PI2)*Math.atan(Z/R);
		ra = (48.0/PI2)*Math.atan(Y/(X+R));
		if (ra<0) ra = ra + 24.0;
		if (what==1) return dec; else return ra;			
}
function frac(X) {
 X = X - Math.floor(X);
 if (X<0) X = X + 1.0;
 return X;		
}

function dayofyear(d) {   // d is a Date object
var yn = d.getFullYear();
var mn = d.getMonth();
var dn = d.getDate();
var d1 = new Date(yn,0,1,12,0,0); // noon on Jan. 1
var d2 = new Date(yn,mn,dn,12,0,0); // noon on input date
var ddiff = Math.round((d2-d1)/864e5);
return ddiff+1; }
