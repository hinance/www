$(function(){

// http://stackoverflow.com/a/901144
function param(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(
                                     results[1].replace(/\+/g, " "));
}

["shopname", "label", "price", "cur"].forEach(function(x){
  $("#" + x).text(param(x));});

})
