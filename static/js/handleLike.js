// Function to retrieve the value of a cookie by name
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

$(document).ready(function () {
  $(".like").each(function () {
    $(this).click(function () {
      var csrftoken = getCookie("csrftoken");
      var postId = $(this).attr("data-post-id");
      var profileId = $(this).attr("data-liked-by");
      console.log(postId, profileId);
      // Make an AJAX request to create the "like" object
      $.ajax({
        url: "/like/",
        type: "POST",
        data: {
          post_id: postId,
          profile_id: profileId,
        },
        headers: {
          "X-CSRFToken": csrftoken,
        },
        success: function (response) {
          // Like object created successfully
          console.log(response)
          console.log("Like created!");
        },
        error: function (xhr, status, error) {
          // Error handling
          console.error("Error creating like:", error);
        },
      });
    });
  });
});
