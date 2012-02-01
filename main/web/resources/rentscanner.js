function removeProperty(propertykey) {
    actionOnProperty(propertykey, 'remove');
}

function saveProperty(propertykey) {
    actionOnProperty(propertykey, 'save');
}

function actionOnProperty(propertyKey, action) {
    $('body').css('cursor', 'wait');
    $.ajax({
        type : 'POST',
        url : '/rate/' + propertykey + '/' + action,
        success : function (data) {
            $('#' + propertykey).remove();
            $('body').css('cursor', 'default');
        }
    });
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
    $('body').css('cursor', 'wait');
    $('.selected').removeClass('selected');
    $.ajax({
        type : 'GET',
        url : retrievalUrl,
        success : function (data) {
            $('#properties').replaceWith(data);
            $('body').css('cursor', 'default');
            $('#' + retrievalUrl.substring(1)).addClass('selected');
        }
    });
}

function setUser() {
    user = $('#username').val()
    $.cookie('user', user, {expires : 365});
    $('#user').replaceWith('<div id="user">Ciao ' + user + '</div>')
}