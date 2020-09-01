<template>
  <div class="video-window">
    <div class="button-area">
      <button class="btn-success btn" :disabled="!users[user_name]" @click="call" style="position: absolute;left:0px; top:0px">Call</button>
      <button class="btn-danger btn" :disabled="users[user_name]" @click="hangUp" style="position: absolute;left:50px; top:0px">Hang Up</button>
    </div>
    <div class="video-play">
      <video id="localVideo" autoplay style="position: absolute; left:0px; top:60px; width: 45%; height: 60%; object-fit: fill"></video>
      <video id="remoteVideo" :src="remote_video" autoplay style="position: absolute; left:150px; top:60px; width: 45%; height: 60%; object-fit: fill"></video>
    </div>
    <div class="preview" v-show="accept_video">
      <div class="preview-wrapper">
        <div class="preview-container">
          <div class="preview-body">
            <h4>您有视频邀请，是否接受?</h4>
            <button class="btn-success btn" style="width: 50%; height: 50%" @click="accept">接受</button>
            <button class="btn-danger btn" style="width: 10%; height: 50%" @click="reject">拒绝</button>
          </div>
          <div class="confirm" @click="closePreview">×</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as config from '../../configure'
/* eslint-disable */

navigator.getUserMedia = navigator.getUserMedia || navigator.mozGetUserMedia || navigator.webkitGetUserMedia
window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection
window.RTCIceCandidate = window.RTCIceCandidate || window.mozRTCIceCandidate || window.webkitRTCIceCandidate
window.RTCSessionDescription =
  window.RTCSessionDescription || window.mozRTCSessionDescription || window.webkitRTCSessionDescription

// const socket = io.connect('http://106.14.227.202:3000');
// var socket;

const configuration = {
  iceServers: [config.DEFAULT_ICE_SERVER],
};

let localStream, peerConn;
let connectedUser = null;

export default {
  name: 'VideoWindow',
  props: ['roomInfo'],
  data() {
    return {
      socket: '',
      user_name: '',
      show: true,
      users: '',
      call_username: '',
      remote_video: '',
      accept_video: false,
    };
  },
  created () {
    this.socket = io.connect('http://106.14.227.202:3000');
    // 36 挪到这里试试看
  },
  mounted() {
    var path = this.$route.path;
    var str_roomid = this.$route.params.roomid;
    var str_name = null;
    var str_name_other = null;
    if(path.indexOf("interviewee") != -1){
      str_name = "itve";
      str_name_other = "itvr";
    }
    else{
      str_name = "itvr";
      str_name_other = "itve";
    }
    this.user_name = str_roomid + str_name;
    this.call_username = str_roomid + str_name_other;
    this.send({
      event: 'join',
      name: this.user_name,
    });
    this.socket.on(
      'message',
      function(data) {
        console.log(data);
        switch (data.event) {
          case 'show':
            this.users = data.allUsers;
            break;
          case 'join':
            this.handleLogin(data);
            break;
          case 'call':
            this.handleCall(data);
            break;
          case 'accept':
            this.handleAccept(data);
            break;
          case 'offer':
            this.handleOffer(data);
            break;
          case 'candidate':
            this.handleCandidate(data);
            break;
          case 'msg':
            this.handleMsg(data);
            break;
          case 'answer':
            this.handleAnswer(data);
            break;
          case 'leave':
            this.handleLeave();
            break;
          default:
            break;
        }
      }.bind(this)
    );
  },
  methods: {
    send(message) {
      if (connectedUser !== null) {
        message.connectedUser = connectedUser;
      }
      this.socket.send(JSON.stringify(message));
    },
    handleLogin(data) {
      if (data.success === false) {
        alert('Ooops...please try a different username');
      } else {
        this.show = false;
        this.users = data.allUsers;
        this.initCreate();
      }
    },
    addVideoURL(elementId, stream) {
      var video = document.getElementById(elementId);
      // Older brower may have no srcObject
      if ('srcObject' in video) {
        video.srcObject = stream;
      } else {
        // 防止在新的浏览器里使用它，应为它已经不再支持了
        video.src = window.URL.createObjectURL(stream);
      }
    },
    initCreate() {
      const self = this;
      navigator.mediaDevices
        .getUserMedia({ audio: true, video: true })
        .then(function(stream) {
          var video = document.getElementById('localVideo');
          self.addVideoURL('localVideo', stream);
          video.muted = true;
          localStream = stream;
        })
        .catch(function(err) {
          console.log(err.name + ': ' + err.message);
        });
    },
    call() {
      if (this.call_username.length > 0) {
        if (this.users[this.call_username] === true) {
          connectedUser = this.call_username;
          this.createConnection();
          this.send({
            event: 'call',
          });
        } else {
          alert('The current user is calling, try another');
        }
      } else {
        alert('Ooops...this username cannot be empty, please try again');
      }
    },
    createConnection() {
      peerConn = new RTCPeerConnection(configuration);
      peerConn.addStream(localStream);
      peerConn.onaddstream = e => {
        this.addVideoURL('remoteVideo', e.stream);
      };
      peerConn.onicecandidate = event => {
        setTimeout(() => {
          if (event.candidate) {
            this.send({
              event: 'candidate',
              candidate: event.candidate,
            });
          }
        });
      };
    },
    handleCall(data) {
      this.accept_video = true;
      connectedUser = data.name;
    },
    reject() {
      this.send({
        event: 'accept',
        accept: false,
      });
      this.accept_video = false;
    },
    accept() {
      this.send({
        event: 'accept',
        accept: true,
      });
      this.accept_video = false;
    },
    handleAccept(data) {
      if (data.accept) {
        // Create an offer
        peerConn.createOffer(
          offer => {
            this.send({
              event: 'offer',
              offer: offer,
            });
            peerConn.setLocalDescription(offer);
          },
          error => {
            alert('Error when creating an offer');
          }
        );
      } else {
        alert('对方已拒绝');
      }
    },
    handleOffer(data) {
      connectedUser = data.name;
      this.createConnection();
      peerConn.setRemoteDescription(new RTCSessionDescription(data.offer));
      // Create an answer to an offer
      peerConn.createAnswer(
        answer => {
          peerConn.setLocalDescription(answer);
          this.send({
            event: 'answer',
            answer: answer,
          });
        },
        error => {
          alert('Error when creating an answer');
        }
      );
    },
    handleMsg(data) {
      console.log(data.message);
    },
    handleAnswer(data) {
      peerConn.setRemoteDescription(new RTCSessionDescription(data.answer));
    },
    handleCandidate(data) {
      // ClientB 通过 PeerConnection 的 AddIceCandidate 方法保存起来
      peerConn.addIceCandidate(new RTCIceCandidate(data.candidate));
    },
    hangUp() {
      this.send({
        event: 'leave',
      });
      this.handleLeave();
    },
    handleLeave() {
      alert('通话已结束');
      connectedUser = null;
      this.remote_video = '';
      peerConn.close();
      peerConn.onicecandidate = null;
      peerConn.onaddstream = null;
      if (peerConn.signalingState === 'closed') {
        this.initCreate();
      }
    },
    closePreview() {
      this.accept_video = false;
    },
  },
};
</script>

<style scoped>
.video-window {
  height: 200px;
  line-height: 200px;
}
.button-area {
  height: 10%;
}
.video-play {
  height: 100px;
  width: 100px;
}
.preview {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}
.preview-wrapper {
  display: table-cell;
  vertical-align: middle;
}
.preview-container {
  width: 600px;
  height: 300px;
  margin: 0px auto;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
  position: relative;
}
.confirm {
  position: absolute;
  right: 10px;
  top: 0px;
  font-size: 40px;
}
.confirm:hover {
  color: red;
  cursor: pointer;
}
.preview-body {
  position: absolute;
  width: 380px;
  height: 130px;
  margin: 10px 10px 10px 10px;
}
.preview-body > h4 {
  position: absolute;
  top: 25%;
  left: 20%;
}
.preview-body > button {
  position: absolute;
  right: 10px;
  bottom: 0px;
}
.green_color {
  color: green;
}
.red_color {
  color: red;
}
</style>
