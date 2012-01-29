function removeProperty(propertykey) {
    $.ajax({
        type:'POST',
        url:'/rate/' + propertykey + '/remove',
        success:handleSuccessFor(propertykey)
    });
}

function saveProperty(propertykey) {
    $.ajax({
        type:'POST',
        url:'/rate/' + propertykey + '/save',
        success:handleSuccessFor(propertykey)
    });
}

function handleSuccessFor(propertykey) {
    return function (data) {
        $('#' + propertykey).remove();
    }
}

function showNewProperties() {
    showProperties('/newProperties');
}

function showGioLikesProperties() {
    showProperties('/gioLikes');
}

function showSaraLikesProperties() {
    showProperties('/saraLikes');
}

function showBothLikeProperties() {
    showProperties('/bothLike');
}

function showDiscardedProperties() {
    showProperties('/discardedProperties');
}

function showProperties(retrievalUrl) {
    $.ajax({
        type:'GET',
        url:retrievalUrl,
        success:function (data) {
            $('#properties').replaceWith(data);
        }
    });
}

function setUser() {
    user = $('#username').val()
    $.cookie('user', user, {expires : 365});
    $('#user').replaceWith('Hi ' + user)
}