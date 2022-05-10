function login() {
    let data = {
        id : $("#id").val(),
        pw : $("#pw").val()
    };

    $.ajax({
        type: 'POST',
        url: '/login',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        success: function (response) {
            if (response["result"] == "success") {                
                $.cookie('token', response['token']);
                alert('로그인 성공');
                window.location.href = '/';
                // window.location.replace('/index')
            } else {
                alert(response['msg']);
            }                    
        }
    })
}