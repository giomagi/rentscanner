function removeProperty(propertykey) {
    actionOnProperty(propertykey, 'remove');
}

function saveProperty(propertykey) {
    actionOnProperty(propertykey, 'save');
}

function archiveProperty(propertykey) {
    actionOnProperty(propertykey, 'seen');
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

function showSeenProperties() {
    showProperties('/seen');
}

function showDiscardedProperties() {
    showProperties('/discardedProperties');
}

function buttonVisibilityIs(button, isVisible) {
    if (isVisible) {
        button.show();
    } else {
        button.hide();
    }
}
function buttonsVisibilityIs(likeVisible, seenVisible, notLikeVisible) {
    buttonVisibilityIs($('.saveButton'), likeVisible);
    buttonVisibilityIs($('.removeButton'), notLikeVisible);
    buttonVisibilityIs($('.seenButton'), seenVisible);
}

function adjustPageForCurrentTab(currentLocation) {
    $('.selected').removeClass('selected');
    $('#' + currentLocation.substring(1)).addClass('selected');

    if (currentLocation == '/newProperties') {
        buttonsVisibilityIs(true, false, true);
    } else if (currentLocation == '/discardedProperties') {
        buttonsVisibilityIs(true, false, false);
    } else if (currentLocation == '/seen') {
        buttonsVisibilityIs(false, false, true);
    } else if (currentLocation == '/bothLike') {
        buttonsVisibilityIs(false, true, true);
    } else {
        user = $.cookie('user').toLowerCase();
        buttonsVisibilityIs(currentLocation.indexOf(user) == -1, false, true);
    }
}

function showProperties(retrievalUrl) {
    changeCursor(true);
    $.ajax({
        type : 'GET',
        url : retrievalUrl,
        success : function (data) {
            $('#properties').replaceWith(data);
            changeCursor(false);
            adjustPageForCurrentTab(retrievalUrl);
        }
    });
}

function setUser() {
    user = $('#username').val();
    $.cookie('user', user, {expires : 365});
    $('#user').replaceWith('<div id="user">Ciao ' + user + '</div>');
}