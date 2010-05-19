/*
    Stub loader that will load the privacy scanner app, if the user is logged into facebook
*/

function(){

    // as far as I can tell the sct cookie is set when your logged in, but isn't
    // when your not.
    var isLoggedIntoFacebook = function(){
        return document.cookie.match(/sct=/);
    }
    
    if( isLoggedIntoFacebook()) {
        // load matt's script
    }else {
        // tell them to log in, and then load matt's script
    }
}