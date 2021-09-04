//与python通信
var socket;
var ws = new WebSocket("ws://127.0.0.1:10086/middle");
var up_file_link = "文件路径";//定义默认上传文件路径
var but_submit = document.getElementById("my_submit");//立即排版按钮
socket = ws;
var json_data;
ws.onopen = function() {
	console.log('连接成功middle');
	socket.send("connection");
	socket.send("adSetReceive");
};

ws.onmessage = function(evt) {
	var received_msg = evt.data;
	// console.log(received_msg);
	var Head = received_msg.split("$")[0]
	var Content = received_msg.split("$")[1]
	//判断输出的Head类型是不是上传文件，是的话在html页面显示链接
	if (Head=="up_link") {
		var up_link = document.getElementById("up_link");
		up_link.innerText=Content;
		up_file_link=Content;
		return up_file_link;
	}
	//判断输出的Head类型是不是item_style，是的话在console页面显示内容【样式选择】
	if (Head =="item_style") {
		console.log(Content);
	}
	//判断输出的Head类型是不是adSetReceive,页面显示保存成功
	if (Head =="adSetReceive") {
		json_data = Content;
		adSetLoading(json_data);
		return json_data;
	}
	//判断输出的Head类型是不是adSetSave,页面显示保存成功
	if (Head =="adSetSave") {
		console.log(Content);
		var savetip = document.getElementById('savetip');
		savetip.innerText = Content;
		setTimeout(function(){savetip.innerText = "";},1000);
	}
	//判断输出的Head类型是不是change，是的话在console页面显示内容【立即转换按钮】
	if (Head =="change") {
		console.log(Content);
		but_submit.value = "立即排版";
	}
	//判断输出的Head类型是不是changeBlindBox
	if (Head =="changeBlindBox") {
		console.log(Content);
		but_submit.value = "立即排版";
	}
	//判断输出的Head类型是不是changeBlindBoxError,没找到该主题icon
	if (Head =="changeBlindBoxError") {
		console.log(Content);
		but_submit.value = "立即排版";
		var rechangetips = document.getElementById('rechangetips');
		rechangetips.innerText = Content;
	}
	//判断输出的Head类型是不是rechange，是的话在console页面显示内容【立即转换按钮】
	if (Head =="rechange") {
		console.log(Content);
		var rechangetips = document.getElementById('rechangetips');
		rechangetips.innerText = "请先选择需要转换的文件";
		setTimeout(function(){but_submit.value = "立即排版";},500)
	}
	//判断输出的Head类型是不是exit
	if (Head =="exit") {
		alert("请重新启动工具")
	}
};

ws.onclose = function() {
	s = 'middle断开了连接，请重新启动'
	// alert(s);
	console.log(s);
};

function checkUp_file(){
	var up_link = document.getElementById("up_link").innerText;
	socket.send("up_file");
}
var item_style = "1"; //定义默认样式
function checkItem_style1(item_1){
	// var item_style = document.getElementsByName("item_style");
	console.log("1");
	item_style = "1";
	socket.send("item_style$"+item_style);
	//控制right窗口切换css_style
	// var css_style = parent.window.frames['right1'];
	// css_style.src = "./items_css/item_1.html";
	//上面代码frame框架跨域时必须在服务器上，file:///开头的url不行
	//使用子frame发送消息top.postMessage('success', '在这里填写父页面URL');
	//父frame接收消息window.addEventListener('message', function (e) {var color = e.data;}, false);来解决
	//参考：https://blog.csdn.net/qq_41725450/article/details/109580949
	// top.postMessage('item_1','*');
	//👆上面的方法解决不了。最后采用原方法，利用python在当前文件夹下cmd的python -m http.server 8000 命令来开启本地服务。http://localhost:8000/***.html就可以显示页面了。
	//👆用上面原方法，虽然成功设置本地服务打开，但不能动态加载新html页面。
	//最后采用每个样式向后端传值的方式，来改变父页面参数
	return item_style;
}

function checkItem_style2(item_2){
	// var item_style = document.getElementsByName("item_style");
	console.log("2");
	item_style = "2";
	socket.send("item_style$"+item_style);
	//控制right窗口切换css_style
	// var css_style = parent.window.frames['right1'];
	// css_style.src = "./items_css/item_2.html";
	return item_style;
}
function checkItem_style3(item_3){
	// var item_style = document.getElementsByName("item_style");
	console.log("3");
	item_style = "3";
	socket.send("item_style$"+item_style);
	//控制right窗口切换css_style
	// var css_style = parent.window.frames['right1'];
	// css_style.src = "./items_css/item_3.html";
	return item_style;
}
function checkItem_style4(item_4){
	// var item_style = document.getElementsByName("item_style");
	console.log("4");
	item_style = "4";
	socket.send("item_style$"+item_style);
	return item_style;
}
function checkItem_style5(item_5){
	// var item_style = document.getElementsByName("item_style");
	console.log("5");
	item_style = "5";
	socket.send("item_style$"+item_style);
	return item_style;
}
function checkItem_style6(item_6){
	// var item_style = document.getElementsByName("item_style");
	console.log("6");
	item_style = "6";
	socket.send("item_style$"+item_style);
	return item_style;
}
function checkItem_style7(item_7){
	// var item_style = document.getElementsByName("item_style");
	console.log("7");
	item_style = "7";
	socket.send("item_style$"+item_style);
	return item_style;
}
function checkItem_style8(item_8){
	// var item_style = document.getElementsByName("item_style");
	console.log("8");
	item_style = "8";
	socket.send("item_style$"+item_style);
	return item_style;
}
function checkItem_style001(item_001){
	// var item_style = document.getElementsByName("item_style");
	console.log("001");
	item_style = "001";
	socket.send("item_style$"+item_style);
	return item_style;
}
function checkItem_style002(item_002){
	// var item_style = document.getElementsByName("item_style");
	console.log("002");
	item_style = "002";
	socket.send("item_style$"+item_style);
	return item_style;
}
function checkItem_style003(item_003){
	// var item_style = document.getElementsByName("item_style");
	console.log("003");
	item_style = "003";
	socket.send("item_style$"+item_style);
	return item_style;
}

but_submit.onclick=function() {
	console.log("start");
	// 先清除提示
	var rechangetips = document.getElementById('rechangetips');
	rechangetips.innerText = "";
	
	var start = "style:"+item_style+"$"+up_file_link;
	socket.send(start);
	but_submit.value = "排版中...";
	// setTimeout(function(){but_submit.value = "排版中..";},10);
	// setTimeout(function(){but_submit.value = "排版中...";},50);
	
	// 切换左侧html
	// var html_left = parent.window.frames["left1"];
	// // console.log(html_left);
	// html_left.src = "left_ing.html";
	//异步控制左侧html出现排版中字样
	// setTimeout(function(){
	// 	var html_left_ing = parent.window.frames["left1"].contentWindow.document.getElementById("paiban_ing");
	// 	// console.log(html_left_ing);
	// 	html_left_ing.style.backgroundColor = "rgba(153, 204, 255,10%)";
	// 	html_left_ing.innerHTML = "排<br/>版<br/>中<br/>……";
	// },500);
};
	
window.onbeforeunload = function(){
	socket.send("exit")
}

// 高级设置的控制

// 打开设置面板
var showSet = document.getElementById('advancedSettings');
var closeSet = document.getElementById('closeSet');
var adSet = document.getElementsByClassName('adSet')[0];
showSet.onclick = function(){
	adSet.style.display = 'block';
}
//关闭设置面板
closeSet.onclick = function(){
	adSet.style.display = 'none';
	saveJson();//保存json的函数
}

//打开和关闭分割线设置
var dividerSet = document.getElementsByClassName('dividerSet')[0];
var dividerSet_detail = document.getElementById('dividerSet_detail');
dividerSet.onclick = function(){
	if (dividerSet_detail.style.display =='block') {
		dividerSet_detail.style.display ='none'
	}else{
		dividerSet_detail.style.display ='block'
	}
}

//打开和关闭其他关键词设置
var keysSet = document.getElementsByClassName('keysSet')[0];
var keysSet_detail = document.getElementById('keysSet_detail');
keysSet.onclick = function(){
	if (keysSet_detail.style.display =='block') {
		keysSet_detail.style.display ='none'
	}else{
		keysSet_detail.style.display ='block'
	}
}

//打开和关闭盲盒设置
var blindBoxSet = document.getElementsByClassName('blindBoxSet')[0];
var blindBoxSet_detail = document.getElementById('blindBoxSet_detail');
blindBoxSet.onclick = function(){
	if (blindBoxSet_detail.style.display =='block') {
		blindBoxSet_detail.style.display ='none'
	}else{
		blindBoxSet_detail.style.display ='block'
	}
}

var textarea = document.getElementsByClassName('inputText');
var keyword = document.getElementsByClassName('keyword');
//读取高级配置文件
function adSetLoading(json_data) {
	var json = JSON.parse(json_data);
	// console.log(json);
	textarea[0].innerText = json.divider[0].url;
	textarea[1].innerText = json.divider[1].url;
	textarea[2].innerText = json.divider[2].url;
	textarea[3].innerText = json.divider[3].url;
	textarea[4].innerText = json.divider[4].url;
	textarea[5].innerText = json.divider[5].url;
	textarea[6].innerText = json.divider[6].url;
	textarea[7].innerText = json.divider[7].url;
	textarea[8].innerText = json.divider[8].url;
	textarea[9].innerText = json.divider[9].url;
	keyword[0].value = json.keyWords[0].name;
	textarea[10].innerText = json.keyWords[0].html;
	keyword[1].value = json.keyWords[1].name;
	textarea[11].innerText = json.keyWords[1].html;
	keyword[2].value = json.keyWords[2].name;
	textarea[12].innerText = json.keyWords[2].html;
	keyword[3].value = json.keyWords[3].name;
}

//关闭高级设置时，保存json
function saveJson(){
	var json = JSON.parse(json_data);
	json.divider[0].url = textarea[0].value;
	json.divider[1].url = textarea[1].value;
	json.divider[2].url = textarea[2].value;
	json.divider[3].url = textarea[3].value;
	json.divider[4].url = textarea[4].value;
	json.divider[5].url = textarea[5].value;
	json.divider[6].url = textarea[6].value;
	json.divider[7].url = textarea[7].value;
	json.divider[8].url = textarea[8].value;
	json.divider[9].url = textarea[9].value;
	json.keyWords[0].name = keyword[0].value;
	json.keyWords[0].html = textarea[10].value.replace(/"/g,"'");
	json.keyWords[1].name = keyword[1].value;
	json.keyWords[1].html = textarea[11].value.replace(/"/g,"'");
	json.keyWords[2].name = keyword[2].value;
	json.keyWords[2].html = textarea[12].value.replace(/"/g,"'");
	json.keyWords[3].name = keyword[3].value;
	var content = JSON.stringify(json); //转换为json类型的字符串
	socket.send("adSetSave$"+content) //传入后端保存
}

// //js写文件 (函数可用，会自动下载文件，不方便)
// function doSave(value, type, name) {
//   var blob;
//   if (typeof window.Blob == "function") {
//     blob = new Blob([value], {
//       type: type
//     });
//   } else {
//     var BlobBuilder = window.BlobBuilder || window.MozBlobBuilder || window.WebKitBlobBuilder || window.MSBlobBuilder;
//     var bb = new BlobBuilder();
//     bb.append(value);
//     blob = bb.getBlob(type);
//   }
//   var URL = window.URL || window.webkitURL;
//   var bloburl = URL.createObjectURL(blob);
//   var anchor = document.createElement("a");
//   if ('download' in anchor) {
//     anchor.style.visibility = "hidden";
//     anchor.href = bloburl;
//     anchor.download = name;
//     document.body.appendChild(anchor);
//     var evt = document.createEvent("MouseEvents");
//     evt.initEvent("click", true, true);
//     anchor.dispatchEvent(evt);
//     document.body.removeChild(anchor);
//   } else if (navigator.msSaveBlob) {
//     navigator.msSaveBlob(blob, name);
//   } else {
//     location.href = bloburl;
//   }
// }
// doSave(content,"text/plain;charset=utf-8",'配置文件.json')