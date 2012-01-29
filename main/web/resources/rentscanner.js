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
    $.ajax({
        type:'GET',
        url:'/newProperties',
        success:function (data) {
            $('#properties').replaceWith(data);
        }
    });
}

function showSavedProperties() {
    $.ajax({
        type:'GET',
        url:'/savedProperties',
        success:function (data) {
            $('#properties').replaceWith(data);
        }
    });
}

function showDiscardedProperties() {
    $.ajax({
        type:'GET',
        url:'/discardedProperties',
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