function getRequest(url, onSuccess, onError, reqData = {}) {
    $.ajax({
        url: url,
        data: reqData,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            onSuccess(data);
        },
        error: function (errorInfo, _textStatus, _errorThrown) {
            onError(errorInfo);
        }
    });
}