function go_profile(id) {
    if (id) {
        window.location.href = `/profile?id=${id}`
        return
    }
    window.location.href = `/profile`
}

function go_posting() {
    window.location.href = `/post/create`
}

<!--모달창 -->
window.onload = function () {
    function onClick() {
        document.querySelector('.modal_part').style.display = 'block';
        document.querySelector('.black_bg').style.display = 'block';
        $('body').css("overflow", "hidden");
        // $("#bg").scrollTop;
    }

    function offClick() {
        document.querySelector('.modal_part').style.display = 'none';
        document.querySelector('.black_bg').style.display = 'none';
        $('body').css("overflow", "scroll");
    }

    document.getElementById('modal_btn').addEventListener('click', onClick);


    document.querySelector('.modal_close').addEventListener('click', offClick);
    document.querySelector('.modal_close2').addEventListener('click', offClick);
};

<!--게시물 글 접고 펴기-->
$(document).ready(function () {

    $('.pic_desc').each(function () {
        var content = $(this).children('.desc');
        var content_txt = content.text();
        var content_txt_short = content_txt.substring(0, 60) + "...";
        var btn_more = $('<a href="javascript:void(0)" class="more" style="float:right; color: grey;">더보기</a>');


        $(this).append(btn_more);

        if (content_txt.length >= 100) {
            content.html(content_txt_short)

        } else {
            btn_more.hide()
        }

        btn_more.click(toggle_content);

        function toggle_content() {
            if ($(this).hasClass('short')) {
                // 접기 상태
                $(this).html('더보기');
                content.html(content_txt_short)
                $(this).removeClass('short');
            } else {
                // 더보기 상태
                $(this).html('접기');
                content.html(content_txt);
                $(this).addClass('short');

            }
        }
    });
});

// 좋아요
function like() {
    document.getElementById("like").src = "static/image/heart2.png";
}


$(document).ready(function () {
    show_post();
});

function show_post() {
    $('#container').empty()       // .append(temp_httml)//
    $.ajax({
        type: "GET",
        url: "/post/get",
        data: {},
        success: function (response) {
            let rows = response['posts']
            for (let i = 0; i < rows.length; i++) {
                let content = rows[i]['content']
                let user = rows[i]['user']
                let file = rows[i]['file']
                let create_time = rows[i]['create_time']
                let profile_img = rows[i]['profile_img']


                let tmep_html = `
                    <div id="container" style="background-color: white; border-radius: 10px;">
                        <!--        {% for post in posts %}  {# 포스트 디비에서 데이터를 불러와서 for문을 통해 하나 씩 보여준다.#}-->
                        <div class="post-wrapper">
                            <div class="post-header" class="border-bottom pb-2" style="align-items: center; display: flex;">
                                <div class="left-wrapper" onclick="go_profile('{{ post.user.id }}')">
                                    <img class="profile_img id_pic" src="static/image/profile.png">
                                    <p class='id_info' style="margin-left: 2%; margin-top: 2%; font-size: 20px"><b>${user}</b></p>
                                    </div>
                                <div class="right-wrapper">
                                    <button class="fa-solid fa-ellipsis dot btn-open-popup" id="modal_btn"
                                            style="margin: 20px 10px auto auto; background-color:transparent;"></button>
                                </div>
                            </div>

                            <div class="post-body">
                                <div class="post-img pictures">
                                    <img style="height: 100%; width: 100%;" src="static/${file}">
                                </div>
                                <div class="post-icons-wrapper">
                                    <div class="left-wrapper">
                                        <button class="bt" id="like" onclick="like()"><i style="margin-left: 2%;"
                                                              class="far fa-heart post-icon fa-2x"></i></button>
                                        <button class="bt"><i style="margin-left: 2%"
                                                              class="far fa-comment post-icon-2 fa-2x"></i></button>
                                        <button class="bt"><i style="margin-left: 2%"
                                                              class="far fa-paper-plane post-icon-3 fa-2x"></i></button>
                                        <div class="right-iwrapper index">
                                            <button class="bt"><i class="far fa-star fa-2x"></i></button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="post-footer">
                                <div class="post-like-wrapper">

                                    <!--                        <img src="data:image.png;base64, {{ return_profile_img(post.user._id) }}">-->
                                    <!--                        <img class="profile_img" src = "static/${profile_img}">-->
                                   
                                </div>
                                <div class="post-content-wrapper">
                                    <p class="post-author" style="margin-left: 10px;"><strong>${user}</strong> ${content} </p>
                                </div>
                                <p style="font-size: 12px; color: gray; margin-left: 10px;" class="post-time">
                                    ${create_time}
                                </p>
                                 <section class="section" style="height: 30px; padding-top: 0px; margin-bottom: 3%; padding-left: 2%;">
            <article class="media" style="padding-top: 10px">
                <div class="media-content" style="bottom: 1px">
                    <div class="field">
                        <p class="control">
                            <input id="input-post" class="input is-rounded" placeholder="댓글 달기,,?"
                                   onclick='$("#modal-post").addClass("is-active")'></p>
                    </div>
                </div>
            </article>
            <div class="modal" style="width: 100%;" id="modal-post">
<!--                <div class="modal-background" onclick='$("#modal-post").removeClass("is-active")'></div>-->
                <div class="modal-background" onclick="modal_show()"></div>                
<!--                <div id="disqus_thread"></div>-->
                <div class="modal-content" style="width: 60%; height: 700px" id="container-2">
                    <div class="comment-box" id="container-1" style="margin-right: 5%; min-height: 530px">       
<!--                        <li class="comments" style="margin-left: 2%"><p><b>${user}:</b> 으흐루꾸꾸루으흐루꾸꾸루으흐 </p></li>                                                                                                                            -->
                    </div>
                    <div class="box">
                        <article class="media">
                            <div class="media-content">
                                <div class="field" >
                                    <p class="control" style="height: 200px;">
                                        <textarea id="comment" class="textarea" placeholder="댓글 달기,,?"></textarea>
                                    </p>
                                </div>
                            </div>
                            <div class="rptl">
                                <button onclick="save_comment()" type="button" class=qjxms>보내기</button>                               
                            </div>
                        </article>
                    </div>
                </div>
                <button class="modal-close is-large" aria-label="close"
                        onclick="modal_show()"></button>                
<!--                <button class="modal-close is-large" aria-label="close"-->
<!--                        onclick='$("#modal-post").removeClass("is-active")'></button>-->
            </div>
        </section>
                                
                                
                                
<!--                                <div class="container my-3">-->
<!--                                    <h5 class="border-bottom pb-2"></h5>-->
<!--                                    <form action="comment/create" method="POST">-->
<!--                                        <div class="form-group" style="display:flex; justify-content: center; text-align: center;">-->
<!--                                            <label for="content"></label>-->
<!--                                            <img class="smile" style="margin-right: 10px;" src="https://cdn-icons-png.flaticon.com/512/35/35777.png" alt="My Image">-->
<!--                                            <input class="form-control cmt-box" name="content" id="content" rows="1" style="border:none;"> -->
<!--                                            <input type="hidden" name='post_id' value="{{ post._id }}">-->
<!--                                                &lt;!&ndash;                            {# 해당하는 포스트의 아이디를 받아오기 위해 인풋값을 히든으로 처리함 by 금성 that's good idea...#}&ndash;&gt;-->
<!--                                                <button type="submit" class="btn btn-primary com-btn" style="background-color: transparent; color: blue; border:none;"-->
<!--                                                        onclick="save_comment()">게시-->
<!--                                                </button>-->
<!--                                            &lt;!&ndash;                            {# 버튼의 속성값은 button, submit, reset이 있는데 submit은 Form 데이터를 서버로 전송 버튼의 디폴트 값이다. 추가적인 설명으로 타입 버튼은 자바스크 살행 목적으로 단순한 버튼을 의미하기에 설정시 꼭 타입 버튼을 작성해야함#}&ndash;&gt;-->
<!--                                        </div>-->
<!--                                    </form>-->
<!--                                </div>-->
                            
                            </div>
                            <!--        {% endfor %}-->
                        </div>`

                $('#container').append(tmep_html)
            }
        }
    });
}

// 이름과 칭찬에 들어간 데이터를 생성(POST)
function save_comment() {               // onclick="save_comment()"
    let comment = $('#comment').val()    // <<<< div id
    $.ajax({
        type: "POST",
        url: "/comment/create",
        data: {'comment': comment},
        success: function (response) {
            alert(response["msg"])
            window.location.reload()
        }
    });
}

function modal_show(){
    $("#modal-post").removeClass("is-active");
    comment_get()
}


$(document).ready(function () {
    comment_get();
});

function comment_get() {
    console.log("comment_get start");
    $('#container-1').empty()       // .append(temp_httml)//
    $.ajax({
        type: "GET",
        url: "/comment/get",
        data: {},
        success: function (response) {
            let rows = response['comments']
            for (let i = 0; i < rows.length; i++) {
                let comment = rows[i]['comment']
                let num = rows[i]['num']
                // let done = rows[i]['done']

                let atmep_html = `<li class="comments" style="margin-left: 2%"><p><b>${num}:</b> ${comment}</p></li>`

                $('#container-1').append(atmep_html)
            }
        }
    });
}


























