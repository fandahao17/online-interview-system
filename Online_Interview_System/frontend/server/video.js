var express = require('express');
var app = express();
var http = require('http');
var fs = require('fs');
var IO = require('socket.io');
var { API_PORT } = require('../configure');


app.use(express.static('dist'));

var server = http.createServer(app).listen(API_PORT);
console.log('The HTTPS server is up and running');

var io = IO(server);
console.log('Socket Secure server is up and running.');

// All joined users
var allUsers = {};
// Room-users table
var allRooms = {};
// All joined sockets
var allSockets = {};

io.on('connect', function(socket) {
  var user = ''; // current joined user

  socket.on('message', function(data) {
    var data = JSON.parse(data);
    switch (data.event) {
      // When has new user join in
      case 'join':
        user = data.name;
        // Duplicated user name is not allowed
        if (allUsers[user]) {
          sendTo(socket, {
            event: 'join',
            message: '该用户名已存在, 请重新输入',
            success: false,
          });
        } else {
          console.log('User joined', data.name);
          // Save users info
          allUsers[user] = true; // 'true' means has not call, 'false' means calling
          if (!(data.roomid in allRooms)) {
            allRooms[data.roomid] = [];
          }
          allRooms[data.roomid].push(user);
          allSockets[user] = socket;
          socket.name = user;
          sendTo(socket, {
            event: 'join',
            allUsers: allRooms[data.roomid],
            success: true,
          });
          showUserInfo(data.roomid);
        }
        break;

      case 'offer':
        // i.e. UserA wants to call UserB
        console.log('Sending offer to: ', data.connectedUser);
        //if UserB exists then send him offer details
        var conn = allSockets[data.connectedUser];
        allUsers[user] = false;
        if (conn != null) {
          // Setting that UserA connected with UserB
          socket.otherName = data.connectedUser;
          sendTo(conn, {
            event: 'offer',
            offer: data.offer,
            name: socket.name,
          });
        } else {
          sendTo(socket, {
            event: 'msg',
            message: 'Not found this name',
          });
        }
        break;

      case 'answer':
        console.log('Sending answer to: ', data.connectedUser);
        // i.e. UserB answers UserA
        var conn = allSockets[data.connectedUser];
        allUsers[user] = false;
        if (conn != null) {
          sendTo(conn, {
            event: 'answer',
            answer: data.answer,
          });
        }
        break;

      case 'candidate':
        console.log('Sending candidate to:', data.connectedUser);
        var conn = allSockets[data.connectedUser];
        if (conn != null) {
          sendTo(conn, {
            event: 'candidate',
            candidate: data.candidate,
          });
        }
        break;

      case 'leave':
        console.log('Disconnecting from', data.connectedUser);
        allUsers[socket.name] = true;
        // Notify the other user so he can disconnect his peer connection
        broadcastRoom(data.roomid, {
          event: 'leave',
          fromUser: data.fromUser,
        });
        break;
    }
  });

  socket.on('disconnect', function() {
    if (socket.name) {
      delete allUsers[socket.name];
      delete allSockets[socket.name];
      // Trick to get roomid here
      roomid = socket.name.substr(0, 6);
      allRooms[roomid].splice(allRooms[roomid].indexOf(socket.name), 1);
      broadcastRoom(roomid, {
        event: 'leave',
        fromUser: socket.name,
      });
    }
  });
});

function showUserInfo(roomid) {
  broadcastRoom(roomid, {
    event: 'show',
    allUsers: allRooms[roomid],
  });
}

function broadcastRoom(roomid, msg) {
  allRooms[roomid].forEach(e => {
    sendTo(e, msg);
  });
}

function sendTo(connection, message) {
  connection.send(message);
}
