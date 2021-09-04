//与python通信
var socket;       
var ws = new WebSocket("ws://127.0.0.1:10086/top");
socket = ws;
ws.onopen = function() {
	console.log('连接成功top');
	socket.send("connection");
	socket.send("hello");
};

ws.onmessage = function(evt) {
	var received_msg = evt.data;
	var Head = received_msg.split("$")[0]
	var Content = received_msg.split("$")[1]
	// console.log("top:"+Content)
	//判断输出的Head类型是不是registered(注册成功)，是的话reload()
	if (Head =="registered") {
		var svip = document.getElementsByClassName('svip')[0];
		svip.innerHTML = "一陈认证的专属<font>SVIP</font>";
		svip.style.backgroundColor ="#FFA500";
		var tip = document.getElementsByClassName('tip')[0];
		tip.innerHTML = "🤗🤗🤗感谢关注一陈！"
		var register_text = document.getElementsByClassName('register_text')[0];
		register_text.style.display = "none";
	}
	//判断输出的Head类型是不是registerError(注册码错误)
	if (Head =="registerError") {
		var register = document.getElementById('register');
		register.value = ""
		register.placeholder = "注册码错误"
	}
	//判断输出的Head类型是不是noRegister(未注册)
	if (Head =="noRegister") {
		console.log("top:"+Content)
	}
};

ws.onclose = function() {
	s = 'top断开了连接，请重新启动'
	// alert(s);
	console.log(s);
};

var upload = document.getElementById('upload');
var register = document.getElementById('register');
upload.onclick = function(){
	socket.send('register$'+register.value)
}
