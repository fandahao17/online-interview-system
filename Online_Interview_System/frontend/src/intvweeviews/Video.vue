<template>
  <div class="video-window">
    <div class="button-area">
      <el-button type="primary" :disabled="(state != OFF) || isHr" @click="call" >加入视频</el-button>
      <el-button type="danger" :disabled="(state != ON) || isHr" @click="hangUp" >退出视频</el-button>
    </div>
    <div class="video-play">
      <video id="localVideo" :src="local_video" autoplay ></video>
      <video id="remoteVideo" :src="remote_video" autoplay ></video>
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

const configuration = {
  iceServers: [config.DEFAULT_ICE_SERVER],
};

let localStream, peerConn;

export default {
  name: 'VideoWindow',
  props: ['roomInfo', 'isHr'],
  data() {
    return {
      socket: '',
      user_name: '',
      users: [],
      call_username: '',
      local_video: '',
      remote_video: '',
      OFF: 0,
      WAITING: 1,
      ON: 2,
      state: 0,
      connections = [],
    };
  },
  created () {
    this.socket = io.connect('http://106.14.227.202:3000');
    // 36 挪到这里试试看
  },
  computed: {
    str_name() {
      if (isHr) {
        return 'hr';
      }
      else if(path.indexOf("interviewee") != -1){
        return "itve";
      }
      else{
        return "itvr";
      }
    }
  },
  mounted() {
    var path = this.$route.path;
    var str_roomid = this.$route.params.roomid;
    this.user_name = str_roomid + this.str_name;
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
    send(message, toUser=null) {
      if (toUser != null) {
        message.toUser = toUser;
      }
      this.socket.send(JSON.stringify(message));
    },
    handleLogin(data) {
      if (data.success === false) {
        alert('重复登录！');
      } else {
        this.users = data.allUsers;
        this.createConnection();
      }
    },
    initCreate() {
      const self = this;
      navigator.mediaDevices
        .getUserMedia({ audio: true, video: true })
        .then(function(stream) {
          this.local_video = stream;
          video.muted = true;
          localStream = stream;
        })
        .catch(function(err) {
          alert!('打开本地视频失败！');
          console.log(err.name + ': ' + err.message);
        });
    },
    call() {
      this.state = this.WAITING;
      initCreate();
      this.connections.forEach((_, conn) => {
        conn.addStream(localStream);
      });
    },
    createConnection() {
      this.users.forEach(e => {
        this.connections[e] = new RTCPeerConnection(configuration);
        this.connections[e].onaddstream = s => {
          if (isHr && e.indexOf('itve') != -1) {
            local_video = s;
          } else {
            remote_video = s;
          }
        };
        this.connections[e].onicecandidate = event => {
          setTimeout(() => {
            if (event.candidate) {
              this.send({
                event: 'candidate',
                candidate: event.candidate,
              });
            }
          });
        };
        
      });
    },
    handleAccept(data) {
      if (data.accept) {
        // Create an offer
        peerConn.createOffer(
          offer => {
            peerConn.setLocalDescription(offer);
            this.send({
              event: 'offer',
              offer: offer,
            });
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
      this.remote_video = '';
      peerConn.close();
      peerConn.onicecandidate = null;
      peerConn.onaddstream = null;
      if (peerConn.signalingState === 'closed') {
        this.initCreate();
      }
    },
  },
};
</script>

<style scoped>
.video-window {
  height: 200px;
}
.button-area {
  height: 25%;
  text-align: center;
}
.video-play {
  height: 75%;
  text-align: center;
}
video {
  width: 40%;
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
