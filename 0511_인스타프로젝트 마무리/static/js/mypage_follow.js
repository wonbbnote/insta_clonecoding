// 활동 시작 시 팔로우 수 업데이트?
$(document).ready(function () {
    let friend = $('#page_id').text();
    console.log('readystart');
    su(friend);
    su2(friend);
});

// 로그아웃
function logout() {
    console.log('로그아웃');
    $.removeCookie('mytoken');
    alert('로그아웃!')
    window.location.href = '/login'
}

// 팔로우+팔로우 취소
function loginOrnot() {
    let friend = $('#page_id').text();
    $('#su').empty();
    $.ajax({
        type: "GET",
        url: "/api/nick",
        data: {},
        success: function (response) {
            if (response['result'] == 'success') {
                console.log(response)
                const btn = document.getElementById('btn');
                if (btn.innerText == '팔로우') {
                    btn.innerText = '팔로잉';
                    follow(response['user_id']);
                    su(friend);
                    // window.location.reload() //새로고침

                } else {
                    btn.innerText = "팔로우";
                    unfollow(response['user_id']);
                    su(friend);
                }
            }
        }
    })
}

function modal_follow(){
    $.ajax({
        type: "GET",
        url: "/api/nick",
        data: {},
        success: function (response) {
            if (response['result'] == 'success') {
                let friend = $('#page_id').text();
                unfollow(response['user_id'])
                su(friend);
            }
        }
    })
}


// 팔로우 db 추가
function follow(user) {
    let friend = $('#page_id').text();
    $.ajax({
        type: "POST",
        url: "/api/follow",
        data: {'userid_give': user, 'followid_give': friend},
        success: function (response) {
            if (response['result'] == 'success') {
                alert(response['msg'])
            }
            else if (response['result'] == 'dup'){
                alert(response['msg'])
            }
            else if(response['result'] == 'myself'){
                alert(response['msg'])
            }
        }
    })
}

// 팔로우 db 삭제
function unfollow(nickname) {
    let friend = $('#page_id').text();
    $.ajax({
        type: "POST",
        url: "/api/unfollow",
        data: {'userid_give': nickname, 'unfollowid_give': friend},
        success: function (response) {
            if (response['result'] == 'success') {
                alert(response['msg'])
            }
        }
    })
}

// 팔로워 수 조회
function su(friend) {
    $('#su').empty();
    $.ajax({
        type: "GET",
        url: "/api/following?nickname_give=" + friend,
        data: {},
        success: function (response) {
            console.log(response['follower'])
            let su = response['follower']
            temp_html = `<b>${su}</b>`
            $('#su').append(temp_html)
        }
    })
}

// 팔로잉 수 조회
function su2(friend) {
    $('#su').empty();
    $.ajax({
        type: "GET",
        url: "/api/following2?nickname_give=" + friend,
        data: {},
        success: function (response) {
            console.log(response['follower'])
            let su2 = response['follower']
            temp_html = `<b>${su2}</b>`
            $('#su2').append(temp_html)
        }
    })
}
