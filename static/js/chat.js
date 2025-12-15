$(document).ready(function () {
  function appendMessage(message, type) {
    let msgDiv = $('<div class="msg"></div>');
    let bubble = $('<div class="bubble"></div>').text(message);
    let avatar = $('<img class="avatar">');

    if (type === "user") {
      msgDiv.addClass("userMsg");
      avatar.attr("src", "/static/img/user.png");
      msgDiv.append(bubble).append(avatar);
    } else {
      msgDiv.addClass("aiMsg");
      avatar.attr("src", "/static/img/leona.png");
      msgDiv.append(avatar).append(bubble);
    }

    $("#chatBox").append(msgDiv);
    $("#chatBox").scrollTop($("#chatBox")[0].scrollHeight);
  }

  $("#sendBtn").click(function () {
    let userInput = $("#userInput").val().trim();
    if (userInput === "") return;
    appendMessage(userInput, "user");
    $("#userInput").val("");

    $.ajax({
      type: "POST",
      url: "/chat",
      contentType: "application/json",
      data: JSON.stringify({ message: userInput }),
      success: function (response) {
        appendMessage(response.reply, "ai");
      },
      error: function () {
        appendMessage("模型暫時無法回應", "ai");
      },
    });
  });

  $("#userInput").keypress(function (e) {
    if (e.which == 13) {
      $("#sendBtn").click();
    }
  });
});
