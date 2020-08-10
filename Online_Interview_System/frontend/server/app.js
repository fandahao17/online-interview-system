var app = require('http').createServer()
var io = require('socket.io')(app)
var PORT = 8002
app.listen(PORT)
io.on('connection', function (socket) {
  socket.on('client_update', function (data) {
    console.log('some one change code')
    io.emit('server_update', data)
  })
  socket.on('client_enter', function (data) {
    console.log('一个用户建立了连接')
  })
})
console.log('app listen at：' + PORT)
