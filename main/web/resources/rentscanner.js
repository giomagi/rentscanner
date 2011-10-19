function removeProperty(propertykey) {
    $.ajax({
      type: 'POST',
      url: '/rate/' + propertykey + '/remove',
      success: handleSuccessFor(propertykey)
    });
}

function handleSuccessFor(propertykey) {
    return function(data) {
        $('#' + propertykey).remove();
    }
}
