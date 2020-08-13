var app = require('http').createServer()
var io = require('socket.io')(app)
var _ = require('underscore')
const { exec } = require("child_process")
var fs=require('fs');
var PORT = 8011
app.listen(PORT,'0.0.0.0')
//app.listen(PORT)
var group = new Array()
var grouplength = new Array()
var groupcode = new Array()
io.on('connection', function (socket) {
  socket.on('client_update', function (data) {
    console.log('someone change code')
    console.log(data)
    groupcode[data.id] = data.code
    var templength = 0
    while(templength != grouplength[data.id]) {
    	if (group[data.id][templength] == socket.id) {
    		templength++
    		continue
    	}
    	var toSocket = _.findWhere(io.sockets.sockets, {id: group[data.id][templength]})
        if (toSocket) {
    	   toSocket.emit('server_update', {code:data.code})
        }
    	templength++
    }
  })
  socket.on('client_enter', function (data) {
    console.log('一个用户建立了连接')
    console.log(data)
    if (group[data.id]) {
    	group[data.id][grouplength[data.id]] = socket.id
    	grouplength[data.id]++
    } else {
        exec(`mkdir -p server/roomfile/${data.id}`, (error, stdout, stderr) => {
            if (error) {
                console.log(`error: ${error.message}`);
            }
            if (stderr) {
                console.log(`stderr: ${stderr}`);
            }
            console.log(`stdout: ${stdout}`);
        });
    	group[data.id] = []
    	group[data.id][0] = socket.id
    	grouplength[data.id] = 1
    }
    if (groupcode[data.id]) {
    	socket.emit('server_update', {code: groupcode[data.id]})
    }
  })
  socket.on('code_run', function (data) {
    console.log('一个用户提交了代码')
    console.log(data)
    fs.writeFile(`./server/roomfile/${data.id}/codefile`,data.code, function(err) {
        if(err) {
            console.log(err)
        }
    })
    if (data.language === 'python') {
        exec(`python3 ./server/roomfile/${data.id}/codefile`, (error, stdout, stderr) => {
            if (error) {
                console.log(`error: ${error.message}`);
            }
            if (stderr) {
                console.log(`stderr: ${stderr}`);
            }
            console.log(`stdout: ${stdout}`);
        });
    }
  })
})
console.log('app listen at：' + PORT)
