// 웹 페이지 시작 시 보여주는 화면
$(document).ready(function () {
    Ativity_list();
    Feed_list();
});

// 활동 버튼을 누르면 실행되는 함수
function openActivity() {
    if ($("#activity").css("display") == "block") {
        $("#activity").hide();
    } else {
        $("#activity").show();
        $("#profile_and_logout").hide();
    }
}

// 프로필 버튼을 누르면 실행되는 함수
function openProfile() {
    if ($("#profile_and_logout").css("display") == "block") {
        $("#profile_and_logout").hide();
    } else {
        $("#profile_and_logout").show();
        $("#activity").hide();
    }
}

// 상대방이 나에게 댓글, 팔로우, 좋아요를 하면 활동 박스에 표시 GET
function Ativity_list() {
    $.ajax({
        type: "GET",
        url: "/api/activity",
        data: {},
        success: function (response) {
            if (response["result"] == "success") {
                let comments = response['comments'];
                let follower = response['follower'];
                let likes = response['likes'];
                // console.log(comments, follower, likes);
                for (let i = 0; i < comments.length; i++) {
                    let user_id = comments[i]['user_id'];
                    let comment_id = comments[i]['comment_id'];
                    // 해당 a 부분에 로그인 시 사용된 user_id값으로 바꿔줄 것
                    if (user_id == "a") {
                        let comment_add_html = `<p>${comment_id}님이 회원님의 게시물에 댓글을 남겼습니다.</p>`
                        $('#activity-box').append(comment_add_html)
                    }
                }
                for (let i = 0; i < follower.length; i++) {
                    let user_id = follower[i]['user_id'];
                    let follow_id = follower[i]['follow_id'];
                    // 해당 a 부분에 로그인 시 사용된 user_id값으로 바꿔줄 것
                    if (user_id == "a") {
                        let follow_add_html = `<p>${follow_id}님이 회원님과 팔로우를 했습니다.</p>`
                        $('#activity-box').append(follow_add_html)
                    }
                }
                for (let i = 0; i < likes.length; i++) {
                    let user_id = likes[i]['user_id'];
                    let like_id = likes[i]['like_id'];
                    // 해당 a 부분에 로그인 시 사용된 user_id값으로 바꿔줄 것
                    if (user_id == "a") {
                        let like_add_html = `<p>${like_id}님이 회원님의 게시물에 좋아요를 남겼습니다.</p>`
                        $('#activity-box').append(like_add_html)
                    }
                }
            }
        }
    })
}

// 게시물 작성 시 마이페이지 하단에 Feed 목록을 img 형태로 불러옴 GET
// 미완
function Feed_list() {
    $.ajax({
        type: "GET",
        url: "/api/feeds",
        data: {},
        success: function (response) {
            if (response["result"] == "success") {
                let posts = response['posts'];
                let cnt = 0;
                let i_idv = "feed-box";
                let f_idv = "";
                for (let i = 0; i < posts.length; i++) {
                    let img = posts[i]['img']
                    let user_id = posts[i]['user_id']

                    if (i % 3 == 0) {
                        f_idv = i_idv + cnt;
                        let feeds_add_html = `<div class="picture_boxes" id=${f_idv}></div>`
                        $('#feeds-box').append(feeds_add_html)
                        cnt+=1;
                    }

                    // 해당 a 부분에 로그인 시 사용된 user_id값으로 바꿔줄 것
                    if (user_id == 'a') {
                        let feed_add_html2 = `<div class="picture_box">
                                                <img src=${img} alt="">
                                            </div>`
                        $('#'+f_idv).append(feed_add_html2)
                    }
                }
            }
        }
    })
}