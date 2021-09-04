//与python通信
var socket;       
var ws = new WebSocket("ws://127.0.0.1:10086/right");
socket = ws;
ws.onopen = function() {
	console.log('连接成功right');
	socket.send("connection");
};

ws.onmessage = function(evt) {
	var received_msg = evt.data;
	var Head = received_msg.split("$")[0]
	var Content = received_msg.split("$")[1]
	// console.log("right:"+Content)
	//判断输出的Head类型是不是item_style，是的话reload()
	if (Head =="item_style") {
		location.reload();
	}
	//判断输出的Head类型是不是reset_css，是的话reload()
	if (Head =="reset_css") {
		location.reload();
	}
	//判断输出的Head类型是不是save，是的话在console页面显示"css保存成功"
	if (Head =="save") {
		console.log(Content);
		save_correct.innerText="success";
		setTimeout( function(){save_correct.innerText="";},500);
	}
	//判断输出的Head类型是不是changeBlindBox，是的话reload()
	if (Head =="changeBlindBox") {
		location.reload();
	}
};

ws.onclose = function() {
	s = 'right断开了连接，请重新启动'
	// alert(s);
	console.log(s)
};

var reset_item = document.getElementById("reset_item");
var copy_item = document.getElementById("copy_item");
var item_text = document.getElementById("item_text");
var copy_correct = document.getElementById("copy_correct");
var save_item = document.getElementById("save_item");

//复制功能
copy_item.onclick = function(){
	item_text.select();
	if (document.execCommand('copy')) {
			document.execCommand('copy');
			console.log('复制成功');
			copy_correct.innerText="success";
			setTimeout( function(){copy_correct.innerText="";},500);
		};
};
//重置功能(与python通信实现)
reset_item.onclick=function(){
	//获取url参数
	socket.send("reset_css");
};

//保存功能 (与python通信实现)
save_item.onclick = function(){
	var url = window.location.href;
	console.log("save$"+url)
	socket.send("save$"+url +"$"+item_text.value);
};

