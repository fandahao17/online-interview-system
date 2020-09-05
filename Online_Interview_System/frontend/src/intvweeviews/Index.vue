<template>
  <el-container>
    <el-header>
      Header
      <!-- <el-button type="primary" plain @click="clickButton">控制台输出房间信息</el-button> -->
    </el-header>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-row class="grid-content bg-purple">
            <video-window v-bind:room-info="roomInfo" :isHr="ture"></video-window>
          </el-row>
          <el-row class="text-window grid-content bg-purple">
            <text-window></text-window>
          </el-row>
        </el-col>
        <el-col :span="13" class="editor-and-board">
          <el-tabs type="border-card" class="card">
            <el-tab-pane label="editor" class="editor-window">
              <editor-window></editor-window>
            </el-tab-pane>
            <el-tab-pane label="white board" class="board-window">
              <board-window></board-window>
            </el-tab-pane>
          </el-tabs>
        </el-col>
        <el-col :span="5" class="question-window">
          <div class="grid-content bg-purple question-window">
            <h4 class="top-head">题目</h4>
            {{ queDetail['name'] }}<br/>
            <h4>描述</h4>
            {{ queDetail['desc'] }}<br/>
            <h4>输入描述</h4>
            {{ queDetail['input'] }}<br/>
            <h4>输出描述</h4>
            {{ queDetail['output'] }}<br/>
            <h4>样例输入</h4>
            {{ queDetail['input_sample'] }}<br/>
            <h4>样例输出</h4>
            {{ queDetail['output_sample'] }}<br/>
          </div>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import axios from 'axios'
import VideoWindow from './Video'
import TextWindow from './Text'
import EditorWindow from './Editor'
import BoardWindow from './Board'

export default {
  name: 'IntvweeHome',
  components: {
    VideoWindow,
    TextWindow,
    EditorWindow,
    BoardWindow
  },
  data () {
    return {
      roomInfo: [],
      testInfo: 'aaaaa',
      queDetail: {},
      messageList: []
    }
  },
  methods: {
    // 获取房间信息：房间号、面试者等等
    getRoomInfo: function (_this) {
      axios.get('http://106.14.227.202/api/room/info/' + this.$route.params.roomid + '/', {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        console.log('type:', typeof (response.data))
        _this.roomInfo = response.data
        if (_this.roomInfo['roomid'] === '') {
          _this.$message.error('This room id does not exist!')
        }
      }).catch(function (error) {
        console.log('get room info error:')
        console.log(error.response)
      })
    },
    clickButton: function () {
      console.log('roominfo:')
      console.log(this.roomInfo)
      console.log(this.roomInfo['roomid'])
    },
    conWebSocket: function () {
      let vm = this
      let _this = this
      if (window.WebSocket) {
        vm.socket = new WebSocket('ws://106.14.227.202:8088')
        let socket = vm.socket

        socket.onopen = function (e) {
          console.log('候选人连接题目服务器成功')
        }
        socket.onclose = function (e) {
          console.log('候选人发送题目服务器关闭')
        }
        socket.onerror = function () {
          console.log('候选人发送题目连接出错')
        }
        // 接收服务器的消息
        socket.onmessage = function (e) {
          console.log(vm.messageList)
          let message = JSON.parse(e.data)
          console.log('message = ', message)
          vm.messageList.push(message)
          // if(message.users) {
          //   vm.users = message.users;
          // }
          axios.get('http://106.14.227.202/api/problem/' + message['msg'] + '/', {
            headers: {
              'Content-Type': 'application/json'
            }
          }).then(function (response) {
            console.log(response.data)
            console.log('type:', typeof (response.data))
            _this.queDetail = response.data
            console.log(_this.queDetail)
          }).catch(function (error) {
            console.log('get problems detail error:')
            console.log(error.response)
          })
        }
      }
    },
    send: function (msg) {
      // if(!this.msg){
      //   return
      // }
      this.sendMessage(this.msg)
    },
    sendMessage: function (msg) {
      this.socket.send(JSON.stringify({
        roomid: this.roomid,
        // uid: this.uid,
        // type: type,
        // nickname: this.nickname,
        msg: msg,
        bridge: this.bridge
      }))
      // this.msg = ''
    }
  },
  mounted: function () {
    this.getRoomInfo(this)
    let vm = this
    vm.conWebSocket()
  }
}
</script>

<style scoped>
.text-window {
  height: 400px;
  line-height: 400px;
  margin-top: 10px;
}

.question-window {
  height: 600px;
}

.card {
  height: 600px;
}

.el-header {
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  height: 650px;
}

body > .el-container {
  margin-bottom: 40px;
}

.el-col {
  border-radius: 4px;
}

.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.bg-purple-dark {
  background: #99a9bf;
}
.grid-content {
  border-radius: 5px;
  min-height: 36px;
}

h4 {
  margin-bottom: 10px
}

.top-head {
  margin-top: 0;
}
</style>
