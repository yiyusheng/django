function prefixUrl(){
    var loca = window.location;
    if (loca.search.length == 0) {
        return (window.location.href + "?");
    } else {
        var query = loca.search.substr(1);
        if (query.indexOf("page") == -1) {
            return (window.location.href + "&");
        } else {
            var obj = {}
            var arr = query.split("&");
            for (var i = 0; i < arr.length; i++) {
                arr[i] = arr[i].split("=");
                obj[arr[i][0]] = arr[i][1];
            };
            delete obj["page"];
            var url = window.location.origin + window.location.pathname + "?" + JSON.stringify(obj).replace(/[\"\{\}]/g,"").replace(/\:/g,"=").replace(/\,/g,"&") + "&";
            return url;
        }
    }
}
