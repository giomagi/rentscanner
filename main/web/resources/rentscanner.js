function removeProperty(propertykey) {
    actionOnProperty(propertykey, 'remove');
}

function saveProperty(propertykey) {
    actionOnProperty(propertykey, 'save');
}

function changeCursor(busy) {
    $('body').css('cursor', busy ? 'wait' : 'default');
    $('.clickable').css('cursor', busy ? 'wait' : 'pointer');
}

function actionOnProperty(propertyKey, action) {
    changeCursor(true);
    $.ajax({
        type : 'POST',
        url : '/rate/' + propertyKey + '/' + action,
        success : function (data) {
            $('#' + propertyKey).remove();
            changeCursor(false);
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
    changeCursor(true);
    $.ajax({
        type : 'GET',
        url : retrievalUrl,
        success : function (data) {
            $('#properties').replaceWith(data);
            changeCursor(false);
            $('.selected').removeClass('selected');
            $('#' + retrievalUrl.substring(1)).addClass('selected');
        }
    });
}

function setUser() {
    user = $('#username').val()
    $.cookie('user', user, {expires : 365});
    $('#user').replaceWith('<div id="user">Ciao ' + user + '</div>')
}