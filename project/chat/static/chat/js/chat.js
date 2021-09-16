var set_interval_stop = new Map();
var chat_socket = new WebSocket(
    "ws://"
    + window.location.host
    + '/chat/'
    + nickname
    + '/' );
var time_socket = new WebSocket(
    "ws://"
    + window.location.host
    + '/time/');



function not_have_connect(status){
    //Есть соединение
    if(status){
        document.getElementById("have_connect").style.display="block";
        document.getElementById("no_connect").style.display="none";
    }else{
        document.getElementById("have_connect").style.display="none";
        document.getElementById("no_connect").style.display="block";
        document.getElementById("header_time").innerHTML="Соединение не установлено ожидайте!";

    }
}

chat_socket.onopen = function(e) {
    not_have_connect(true);
    web_socket_functions();
}
time_socket.onopen = function (e) {
    get_time();
    set_interval_stop.set("time", setInterval(get_time,20*1000));
}
function try_connect(){
    function check_connect() {
        if (chat_socket.readyState == 1 && time_socket.readyState == 1)
            return true;
        return false;
        alert("status connect chat_socket "+ chat_socket.readyState);
    }

    if (check_connect()){
        not_have_connect(true);
        web_socket_functions();
        get_time();
        set_interval_stop.set("time", setInterval(get_time,20*1000));
        chat_socket.onclose = function(e){
            onclose_connect()
        }
    }else {
        chat_socket = new WebSocket(
            "ws://"
            + window.location.host
            + '/chat/'
            + nickname
            + '/');
        time_socket = new WebSocket(
            "ws://"
            + window.location.host
            + '/time/');
        setTimeout(try_connect, 3*1000)
    }
}

chat_socket.onclose = function(e){
    onclose_connect()
}
function onclose_connect(){
    clearInterval(set_interval_stop.get("time"));
    chat_socket.close();
    time_socket.close();
    not_have_connect(false);
    setTimeout(try_connect, 3*1000)
}



function web_socket_functions() {
    time_socket.onmessage = function (e) {
        const data = JSON.parse(e.data)
        document.getElementById("header_time").innerHTML = data['date_time']['day_of_week']
            +', '
            +data['date_time']['time'];
    }
    chat_socket.onmessage = function (e) {
        // возврощает 1 если сообщене от него
        let chek_here_or_my_message = function (message_nickname) {
            if (message_nickname == nickname)
                return true
            return false
        }

        function add_my_message(chat_HTML, data) {
            document.getElementById("have_connect").innerHTML = chat_HTML
                + "<div class =\"my_message\">"
                + "<div class=\"text\">"
                + data.message['message']
                + "</div>"
                + "<p class=\"date_time\">"
                + data.message.date_time['date'] + "в" + data.message.date_time['time'] + "<br>"
                + "</p>"
                + "</div>"
        }

        function add_another_message(chat_HTML, data) {
            function get_logo(nickname) {
                let nickname_split = nickname.split('');
                return nickname_split[0]
            }

            document.getElementById("have_connect").innerHTML = chat_HTML
                + "<div class =\"hee_message\">"
                + "<div class=\"text\">"
                + data.message['message']
                + "</div>"
                + "<div class=\"logo\">"
                + get_logo(data.message['nickname'])
                + "</div>"
                + "<p class=\"date_time\">"
                + data.message.date_time['date'] + " в " + data.message.date_time['time'] + "<br>"
                + "username:" + data.message['nickname']
                + "</p>"
                + "</div>"
        }

        const data = JSON.parse(e.data)
        chat_HTML = document.getElementById("chat").innerHTML;
        if (chek_here_or_my_message(data.message['nickname'])) {
            add_my_message(chat_HTML, data)
        } else {
            add_another_message(chat_HTML, data)
        }
        scroll_chat()
        get_time()

    }

}
not_have_connect(false);

// прочие функции
function get_time(){
    time_socket.send("None");
}

function scroll_chat(){
     var chat_elem = document.getElementById('chat');
     chat_elem.scrollTop = chat_elem.scrollHeight;
}

function send_message(){
    let message = document.getElementById("send_message_in_input").value;
    if (message.replace( /\s/g, "").length == 0)
        return
    chat_socket.send(JSON.stringify({
        'nickname':nickname,
        'message':message
    }))
    document.getElementById("send_message_in_input").value = "";
}

function onload_function(){
    scroll_chat();
    add_enter_button_listening();

    function add_enter_button_listening() {
        document.getElementById("send_message_in_input").addEventListener("keyup", function (event) {
            if (event.keyCode === 13) {
                document.getElementById("send_message_button").click();
            }
        });
    }
}