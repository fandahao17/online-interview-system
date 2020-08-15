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
    if (data.language === 'python') {
        fs.writeFile(`./server/roomfile/${data.id}/codefile`,data.code, function(err) {
            if(err) {
                console.log(err)
            }
        })
        exec(`python3 ./server/roomfile/${data.id}/codefile`, (error, stdout, stderr) => {
            if (error) {
                console.log(`error: ${error.message}`);
                socket.emit('server_result', {msg: error.message});
                return
            }
            if (stderr) {
                console.log(`stderr: ${stderr}`);
                socket.emit('server_result', {msg: stderr});
                return
            }
            console.log(`stdout: ${stdout}`);
            socket.emit('server_result', {msg: stdout});
        });
    } else if (data.language === 'c') {
        fs.writeFile(`./server/roomfile/${data.id}/codefile.c`,data.code, function(err) {
            if(err) {
                console.log(err)
            }
        })
        exec(`gcc ./server/roomfile/${data.id}/codefile.c -o ./server/roomfile/${data.id}/a.out`, (error, stdout, stderr) => {
            if (error) {
                console.log(`error: ${error.message}`);
                socket.emit('server_result', {msg: error.message});
                return
            }
            if (stderr) {
                console.log(`stderr: ${stderr}`);
                socket.emit('server_result', {msg: stderr});
                return
            }
            console.log(`stdout: ${stdout}`);
        });
        exec(`././server/roomfile/${data.id}/a.out`, (error, stdout, stderr) => {
            if (error) {
                console.log(`error: ${error.message}`);
                socket.emit('server_result', {msg: error.message});
                return
                }
            if (stderr) {
                console.log(`stderr: ${stderr}`);
                socket.emit('server_result', {msg: stderr});
                return
            }
            console.log(`stdout: ${stdout}`);
            socket.emit('server_result', {msg: stdout});
        });
    } else if (data.language === 'cplus') {
        fs.writeFile(`./server/roomfile/${data.id}/codefile.cpp`,data.code, function(err) {
            if(err) {
                console.log(err)
            }
        })
        exec(`g++ ./server/roomfile/${data.id}/codefile.cpp -o ./server/roomfile/${data.id}/a.out`, (error, stdout, stderr) => {
            if (error) {
                console.log(`error: ${error.message}`);
                socket.emit('server_result', {msg: error.message});
                return
            }
            if (stderr) {
                console.log(`stderr: ${stderr}`);
                socket.emit('server_result', {msg: stderr});
                return
            }
            console.log(`stdout: ${stdout}`);
        });
        exec(`./server/roomfile/${data.id}/a.out`, (error, stdout, stderr) => {
            if (error) {
                console.log(`error: ${error.message}`);
                socket.emit('server_result', {msg: error.message});
                return
                }
            if (stderr) {
                console.log(`stderr: ${stderr}`);
                socket.emit('server_result', {msg: stderr});
                return
            }
            console.log(`stdout: ${stdout}`);
            socket.emit('server_result', {msg: stdout});
        });
    }
  })
})
console.log('app listen at：' + PORT)
