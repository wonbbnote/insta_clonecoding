function go_profile(id) {
    if(id){
        window.location.href = `/profile?id=${id}`
        return
    }
    window.location.href = `/profile`
}

function go_posting() {
    window.location.href = `/post/create`
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
    <div id="container">
<!--        {% for post in posts %}  {# 포스트 디비에서 데이터를 불러와서 for문을 통해 하나 씩 보여준다.#}-->
            <div class="post-wrapper">
            
                <div class="post-header">
                    <div class="left-wrapper" onclick="go_profile('{{ post.user.id }}')">
                        <img class="profile_img" src="static/${profile_img}">
                        <p style="margin-left: 2%; font-size: 25px"><b>${user}</b> </p>                     
                        <div class="right-wrapper">
                            <img src="/static/img/more@3x.png">
                        </div>                          
                    </div>
                  
                </div>
                
                <div class="post-body">
                    <div class="post-img">                        
                        <img style="height: 100%; width: 100%;" src="static/${file}">                        
                    </div>
                    <div class="post-icons-wrapper">
                        <div class="left-wrapper">
                            <i style="margin-left: 2%" class="far fa-heart post-icon fa-2x"></i>
                            <i style="margin-left: 2%" class="far fa-comment post-icon-2 fa-2x"></i>
                            <i  style="margin-left: 2%"class="far fa-paper-plane post-icon-3 fa-2x"></i>
                            <div class="right-iwrapper">
                                <i class="far fa-star fa-2x"></i>
                            </div>
                        </div>
                    </div>                    
                </div>
                
                <div class="post-footer">
                    <div class="post-like-wrapper">

<!--                        <img src="data:image.png;base64, {{ return_profile_img(post.user._id) }}">-->
<!--                        <img class="profile_img" src = "static/${profile_img}">-->
                        <p><strong>${ user }</strong>님 <strong>외 {{ post.like }}명</strong>이 좋아합니다</p>
                    </div>
                    <div class="post-content-wrapper">
                        <p class="post-author"><strong>${ user }</strong> ${content} </p>                        
                    </div>
                        <p style="font-size: 12px; color: gray" class="post-time"> 
                        ${ create_time }
                        </p>
                </div>
<!--                {#if문을 통해 post안에 댓글이 있으면 아래 댓글 박스를 보여준다. 아래의 post는 for문을 통해 받아온 post data#}-->
<!--                {% if post.comments %}-->
<!--                    {% for comment in post.comments %}  &lt;!&ndash; 받아온 comment는 어레이 형식으로  FOR 문을 통해 데이터를 출력  &ndash;&gt;-->
                        <div class="comment-wrapper">
                            <div class="comment-show-box">
                                <span style="white-space: pre-line; color:cornflowerblue;">{{ comment.user }}</span>
                                <span>
                                            {{ comment.content }}, <strong>{{ comment.create_time }}</strong>
                                        </span>
<!--                                {% if user['id'] == comment['user'] %}   &lt;!&ndash; 삭제 버튼 이미지는 if문을 통해 유저의 아이디와 댓글의 아이디가 일치하면 보여주게 작성 &ndash;&gt;-->
<!--                                    {% set comment_id = comment['comment_id']  %}-->
<!--                                    {% set post_id = post['_id']  %}-->
                                     <input class="x-btn" onclick="del_comment('{{ comment['comment_id'] }}','{{ post['_id'] }}')"
                                           type="button" value="X">
<!--                                {% endif %}-->
                            </div>
                        </div>
<!--                    {% endfor %}-->
<!--                {% endif %}-->


                <div class="container my-3">
                    <h5 class="border-bottom pb-2">댓글</h5>
                    <form action="comment/create" method="POST">
                        <div class="form-group">
                            <label for="content"></label>
                            <textarea class="form-control cmt-box" name="content" id="content" rows="3"></textarea>
                            <input type="hidden" name='post_id' value="{{ post._id }}">
<!--                            {# 해당하는 포스트의 아이디를 받아오기 위해 인풋값을 히든으로 처리함 by 금성 that's good idea...#}-->
                            <button type="submit" class="btn btn-primary com-btn" onclick="save_comment"()>저장하기</button>
<!--                            {# 버튼의 속성값은 button, submit, reset이 있는데 submit은 Form 데이터를 서버로 전송 버튼의 디폴트 값이다. 추가적인 설명으로 타입 버튼은 자바스크 살행 목적으로 단순한 버튼을 의미하기에 설정시 꼭 타입 버튼을 작성해야함#}-->
                        </div>
                    </form>
                </div>
            </div>
<!--        {% endfor %}-->
    </div>
`
                $('#container').append(tmep_html)
            }
        }
    });
}

// // 이름과 칭찬에 들어간 데이터를 생성(POST)
// function save_comment () {
//     let comment = $('#comment').val()
//     $.ajax({
//         type: "POST",
//         url: "/comment/create",
//         data: {'comment_give': comment},
//         success: function (response) {
//             alert(response["msg"])
//             window.location.reload()
//         }
//     });
// }



























