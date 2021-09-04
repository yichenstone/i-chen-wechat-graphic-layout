//与python通信
var socket;       
var ws = new WebSocket("ws://127.0.0.1:10086/left");
socket = ws;
ws.onopen = function() {
	console.log('连接成功left');
	socket.send("connection");
};

ws.onmessage = function(evt) {
	var received_msg = evt.data;
	var Head = received_msg.split("$")[0]
	var Content = received_msg.split("$")[1]
	// console.log("left:"+Content)
	//判断输出的Head类型是不是item_style，是的话reload()
	if (Head =="item_style") {
		location.reload();
	}
	//判断输出的Head类型是不是change，是的话reload()
	if (Head =="change") {
		location.reload();
	}
	//判断输出的Head类型是不是changeBlindBox，是的话reload()
	if (Head =="changeBlindBox") {
		location.reload();
	}
	//判断输出的Head类型是不是reset_css，是的话reload()
	if (Head =="reset_css") {
		location.reload();
	}
	//判断输出的Head类型是不是save，是的话reload()
	if (Head =="save") {
		location.reload();
	}
};

ws.onclose = function() {
	s = 'left断开了连接，请重新启动'
	// alert(s);
	console.log(s);
};
