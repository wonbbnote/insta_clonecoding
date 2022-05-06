function openActivity() {
    if ($("#activity").css("display") == "block") {
        $("#activity").hide();
    } else {
        $("#activity").show();
    }
}

//     $('#body').click(function (e) {
//     if(!$('#activity').has(e.target).length) $('#activity').hide();
// });

function openProfile() {
    if ($("#profile_and_logout").css("display") == "block") {
        $("#profile_and_logout").hide();
    } else {
        $("#profile_and_logout").show();
    }
}