/*
    Stub loader that will load the privacy scanner app, if the user is logged into facebook
*/

(function(){
    // as far as I can tell the sct cookie is set when your logged in, but isn't
    // when your not.
    var isLoggedIntoFacebook = function(){
        return document.cookie.match(/sct=/);
    }
    
    if( isLoggedIntoFacebook()) {
        // load matt's script
        var script=document.createElement('script');
        script.src='http://www.reclaimprivacy.org/javascripts/privacyscanner.js';       
        document.getElementsByTagName('head')[0].appendChild(script);
    }else {
        // tell them to log in
        var body = document.getElementsByTagName('body')[0];
        var div=document.createElement('div');
        div.style= "position: absolute; top:0px;left:0px; width:100%;height:20px";
        div.innerHTML = "<h2>ReclaimPrivacy:</h2><p>Log into Facebook so we can run the scanner</p>";
        body.insertBefore(div, body.firstChild);
    }
})();