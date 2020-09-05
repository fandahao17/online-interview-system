<template>
  <div class="video-window">
    <div v-if="isHr" class="button-area">
      <el-button type="primary" @click="startAudio()">观看视频</el-button>
    </div>
    <div v-if="!isHr" class="button-area">
      <el-button type="primary" @click="call()">加入视频</el-button>
    </div>
    <div class="video-play">
      <video id="local-video" autoplay ></video>
      <video id="remote-video" autoplay ></video>
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
      OFF: 0,
      WAITING: 1,
      ON: 2,
      state: 0,
      connections: [],
    };
  },
  created () {
    this.socket = io.connect('http://106.14.227.202:3000');
    // 36 挪到这里试试看
  },
  computed: {
    str_name() {
      if (this.isHr) {
        return 'hr';
      }
      else if(this.$route.path.indexOf("interviewee") != -1){
        return "itve";
      }
      else{
        return "itvr";
      }
    },
    str_roomid() {
      return this.$route.params.roomid;
    }
  },
  mounted() {

    this.user_name = this.str_roomid + this.str_name;
    console.log('Video: Running');
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
            this.handleLeave(data);
            break;
          default:
            break;
        }
      }.bind(this)
    );
  },
  methods: {
    startAudio() {
      let silence = () => {
        let ctx = new AudioContext(), oscillator = ctx.createOscillator();
        let dst = oscillator.connect(ctx.createMediaStreamDestination());
        oscillator.start();
        return Object.assign(dst.stream.getAudioTracks()[0], {enabled: false});
      }

      let black = ({width = 640, height = 480} = {}) => {
        let canvas = Object.assign(document.createElement("canvas"), {width, height});
        canvas.getContext('2d').fillRect(0, 0, width, height);
        let stream = canvas.captureStream();
        return Object.assign(stream.getVideoTracks()[0], {enabled: false});
      }

      this.blackSilence = (...args) => new MediaStream([black(...args), silence()]);

      this.call();
    },
    send(message, toUser=null) {
      if (toUser != null) {
        message.connectedUser = toUser;
      }
      message.fromUser = this.user_name;
      message.roomid = this.str_roomid;
      this.socket.send(JSON.stringify(message));
    },
    handleLogin(data) {
      if (data.success === false) {
        alert('该用户已经登陆过，请退出！');
      } else {
        this.users = data.allUsers;
        if (!this.isHr) {
          this.initCreate();
        }
      }
    },
    addVideoURL(elementId, stream) {
      var video = document.getElementById(elementId);
      // Older brower may have no srcObject
      // if ('srcObject' in video) {
      //   video.srcObject = stream;
      // } else {
      //   // 防止在新的浏览器里使用它，应为它已经不再支持了
      //   video.src = window.URL.createObjectURL(stream);
      // }
      try {
        video.srcObject = event.stream;
      } catch(error) {
        video.src = URL.createObjectURL(event.stream);
      };
      video.play();
    },
    initCreate() {
      const self = this;
      this.state = this.WAITING;
      navigator.mediaDevices
        .getUserMedia({ audio: true, video: true })
        .then(stream => {
          this.addVideoURL('local-video', stream);
          this.state = this.OFF;
          localStream = stream;
          // this.call();
        })
        .catch(err => {
          alert('打开本地视频失败！');
          console.log(err.name + ': ' + err.message);
        });
    },
    call() {
      this.state = this.ON;
      this.users.forEach(e => {
        if (e == this.user_name) return;

        this.connections[e] = new RTCPeerConnection(configuration);

        // Add local stream & Wait for remote stream
        if (!this.isHr) {
          this.connections[e].addStream(localStream);
        } else {
          this.connections[e].addStream(this.blackSilence());
        }

        this.connections[e].onaddstream = s => {
          console.log('Got stream from: ', e);
          if (e.indexOf('hr') == -1) {
            console.log('Not HR, show video');
            // Ignore stream from HR
            if (this.isHr && e.indexOf('itvr') != -1) {
              // On HR page, treat interviewer stream as local stream
              console.log('Put video on local-video');
              this.addVideoURL('local-video', s.stream);
            } else {
              // Otherwise, put it on 'remote-video'
              console.log('Put video on remote-video');
              this.addVideoURL('remote-video', s.stream);
            }
          }
        };

        // Gather ICE candidates
        this.connections[e].onicecandidate = event => {
          setTimeout(() => {
            if (event.candidate) {
              this.send({
                event: 'candidate',
                candidate: event.candidate,
              }, e);
            }
          });
        };
        
        // Create offer
        this.connections[e].createOffer(
          offer => {
            this.connections[e].setLocalDescription(offer);
            this.send({
              event: 'offer',
              offer: offer,
            }, e);
          },
          error => {
            alert('通话失败（Error when creating an offer）');
          }
        );
      });
    },
    handleOffer(data) {
      console.log('Get offer from: ', data.fromUser, ' to ', this.user_name);
      if (data.fromUser == this.user_name) return;

      var from = data.fromUser;
      this.connections[from] = new RTCPeerConnection(configuration);

      // Let HR send a dummy stream
      if (!this.isHr) {
        this.connections[from].addStream(localStream);
      } else {
        this.connections[from].addStream(this.blackSilence());
      }

      this.connections[from].onaddstream = s => {
        console.log('Got stream from: ', from);
        if (from.indexOf('hr') == -1) {
          console.log('Not HR, show video');
          // Ignore stream from HR
          if (this.isHr && from.indexOf('itvr') != -1) {
            // On HR page, treat interviewer stream as local stream
            console.log('Put video on local-video');
            this.addVideoURL('local-video', s.stream);
          } else {
            console.log('Put video on remote-video');
            this.addVideoURL('remote-video', s.stream);
          }
        }
      };

      this.connections[from].setRemoteDescription(new RTCSessionDescription(data.offer));
      // Create an answer to an offer
      this.connections[from].createAnswer(
        answer => {
          this.connections[from].setLocalDescription(answer);
          this.send({
            event: 'answer',
            answer: answer,
          }, from);
        },
        error => {
          alert('通话失败（Error when creating an answer）');
        }
      );
      this.state = this.ON;
    },
    handleMsg(data) {
      console.log(data.message);
    },
    handleAnswer(data) {
      if (data.fromUser == this.user_name) return;

      this.connections[data.fromUser].setRemoteDescription(new RTCSessionDescription(data.answer));
    },
    handleCandidate(data) {
      if (data.fromUser == this.user_name) return;

      // ClientB 通过 PeerConnection 的 AddIceCandidate 方法保存起来
      this.connections[data.fromUser].addIceCandidate(new RTCIceCandidate(data.candidate));
    },
    hangUp() {
      this.send({
        event: 'leave',
      });
      this.connections.forEach(e => {
        e.close();
        e.onicecandidate = null;
        e.onaddstream = null;
      });
      this.connections = [];
      this.addVideoURL('remote-video', null);
      this.state = this.OFF;
    },
    handleLeave(data) {
      if (data.fromUser == this.user_name) return;

      console.log('User left: ', data.fromUser);

      if (data.fromUser.indexOf('hr') == -1) {
        // Ignore HR leave
        if (!this.isHr) {
          this.addVideoURL('remote-video', null);
        } else if (data.fromUser.indexOf('itve') != -1) {
          // Interviewee left on HR page
          this.addVideoURL('remote-video', null);
        } else {
          // Interviewer left on HR page
          this.addVideoURL('local-video', null);
        }
      }
      delete this.connections[data.fromUser];
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
  height: 80%;
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
