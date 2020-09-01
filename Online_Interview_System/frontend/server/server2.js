var ws = require("nodejs-websocket");
var moment = require('moment');

console.log("开始建立连接...")

let users = [];
let conns = {};

function boardcast(obj) {
  if(obj.bridge && obj.bridge.length){
    obj.bridge.forEach(item=>{
      conns[item].sendText(JSON.stringify(obj));
    })
    return;
  }
  server.connections.forEach((conn, index) => {
      conn.sendText(JSON.stringify(obj));
  })
}

var server = ws.createServer(function(conn){
  conn.on("text", function (obj) {
    obj = JSON.parse(obj);
    //console.log(obj.roomid);
    conns[''+obj.uid+''] = conn;
    boardcast({
      msg: obj.msg,
      roomid: obj.roomid,
      bridge: obj.bridge
    });
  })
  conn.on("close", function (code, reason) {
    console.log("关闭连接")
  });
  conn.on("error", function (code, reason) {
    console.log("异常关闭")
  });
}).listen(8088,'0.0.0.0')
console.log("WebSocket建立完毕")
