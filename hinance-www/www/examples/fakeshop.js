$(function(){

// http://stackoverflow.com/a/901144
function param(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(
                                     results[1].replace(/\+/g, " "));
}

["label", "price", "cur"].forEach(function(x){
  $("#" + x).text(param(x));});

$("#shop").text({
  awesome: "Awesome Stuff",
  itchyback: "Itchy Back",
  viogor: "Violently Gorgeous",
  megarags: "Mega Rags"
}[param("shopname")]);

})
