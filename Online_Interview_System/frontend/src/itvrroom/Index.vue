<template>
  <div>
    <el-container>
      <el-header>
        <img src="../assets/logo3.png" width="120px" height="60px" class="top-img">
        在线面试（房间号：{{ $route.params.roomid }}）
        <el-button type="primary" size="medium" :disabled="isStart" @click="onStartBtn" class="head-button">开始录制</el-button>
        <el-button type="primary" size="medium" :disabled="!isStart" @click="onEndBtn" class="head-button">结束录制</el-button>
        <el-button type="primary" size="medium" :disabled="!isFinish" @click="onDownloadBtn" class="head-button">下载</el-button>
        <el-button type="primary" size="medium" :disabled="!isFinish||isUpload" @click="onUploadBtn" class="head-button">上传</el-button>
        <!-- <el-button type="primary" plain @click="clickButton">控制台输出房间信息</el-button> -->
      </el-header>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="6">
            <el-row class="grid-content video-row">
              <video-window v-bind:room-info="roomInfo" :isHr="false"></video-window>
            </el-row>
            <el-row class="text-window grid-content text-row">
              <text-window :isHr="false"></text-window>
            </el-row>
          </el-col>
          <el-col :span="13" class="editor-and-board">
            <el-tabs type="border-card" class="card">
              <el-tab-pane label="editor" class="editor-window">
                <editor-window :isHr="false" :isItvr="true"></editor-window>
              </el-tab-pane>
              <el-tab-pane label="white board" class="board-window">
                <board-window :isHr="false"></board-window>
              </el-tab-pane>
            </el-tabs>
          </el-col>
          <el-col :span="5" class="question-window">
            <el-scrollbar>
              <div class="grid-content question-window">
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
            </el-scrollbar>
            <div class="bottom-toolbar">
              <el-button type="primary" @click="addQuestion" class="end-button">添加题目</el-button>
              <el-button type="primary" @click="endInterview" class="end-button">结束面试</el-button>
            </div>
          </el-col>
        </el-row>
      </el-main>
    </el-container>

    <el-dialog title="提交评价" :visible.sync="judgeDialogFormVisible">
      <el-form :model="judgeForm">
        <el-form-item label="评级" :label-width="judgeFormLabelWidth">
          <el-rate v-model="judgeForm.score" show-text :texts=textsList></el-rate>
        </el-form-item>
        <el-form-item label="评价" :label-width="judgeFormLabelWidth">
          <el-input type="textarea" v-model="judgeForm.remark"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="commitJudge">提 交</el-button>
      </div>
    </el-dialog>

    <el-dialog title="选择题目" :visible.sync="chooseQueDialogFormVisible">
      <el-table
        :data="queTableData"
        style="width: 90%">
        <el-table-column
          prop="id"
          label="编号"
          width="180">
        </el-table-column>
        <el-table-column
          prop="name"
          label="题目"
          width="230">
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              @click="handleChooseQue(scope.$index, scope.row)">选择</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" size="medium" @click="chooseQueDialogFormVisible = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import VideoWindow from '@/intvweeviews/Video'
import TextWindow from '@/intvweeviews/Text'
import EditorWindow from '@/intvweeviews/Editor'
import BoardWindow from '@/intvweeviews/Board'

export default {
  name: 'ItvrRoom',
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
      isStart: false,
      isFinish: false,
      isUpload: false,
      data: [],
      mediaRecorder: null,
      stream: null,
      uploadResult: '',
      judgeDialogFormVisible: false,
      judgeFormLabelWidth: '100px',
      judgeForm: {
        score: 1,
        remark: ''
      },
      textsList: ['D', 'C', 'B', 'A', 'S'],
      chooseQueDialogFormVisible: false,
      chooseQueFormLabelWidth: '120px',
      queForm: {},
      queTableData: [],
      queDetail: {},
      messageList: '',
      bridge: []
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
          this.$message.error('This room id does not exist!')
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
    async onStartBtn () {
      this.isStart = true
      this.isFinish = false
      this.data = []
      this.stream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
        audio: false
      })
      this.mediaRecorder = new MediaRecorder(this.stream, {
        mimeType: 'video/webm'
      })
      this.mediaRecorder.ondataavailable = e => {
        this.data.push(e.data)
      }
      this.mediaRecorder.start()
    },
    onEndBtn () {
      this.isStart = false
      this.isFinish = true
      this.mediaRecorder.pause()
      this.mediaRecorder.stop()
      this.stream.getTracks().forEach(track => {
        track.stop()
      })
    },
    onDownloadBtn () {
      let res = new Blob(this.data, { type: 'video/webm' })
      let url = URL.createObjectURL(res)
      let a = document.createElement('a')
      a.href = url
      a.download = `${new Date().getTime()}.webm`
      a.click()
      a.remove()
    },
    onUploadBtn () {
      let res = new Blob(this.data, { type: 'video/webm' })
      var file = new File([res], 'msr-' + (new Date()).toISOString().replace(/:|\./g, '-') + '.webm', {
        type: 'video/webm'
      })
      var data = new FormData()
      data.append('userfile', file)
      console.log(data)
      axios.post('http://106.14.227.202/api/room/video/' + this.$route.params.roomid + '/', data)
        .then(response => {
          this.uploadResult = response.data
          alert(this.uploadResult.result)
        })
    },
    endInterview: function () {
      this.judgeDialogFormVisible = true
    },
    commitJudge: function () {
      let _this = this
      this.judgeDialogFormVisible = false
      console.log(this.judgeRate)
      this.judgeForm['roomid'] = this.$route.params.roomid
      this.judgeForm['score'] = this.judgeForm['score'] / 5 * 100
      axios.post('http://106.14.227.202/api/room/rate/', this.judgeForm, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        if (response.data['success'] === true) {
          console.log('add remark info successfully:')
          _this.$message('添加面试评价信息成功')
        } else {
          console.log('add remark info error:')
          _this.$alert('添加面试评价信息出错')
        }
      }).catch(function (error) {
        console.log('remark interview error:')
        console.log(error.response)
        _this.$alert(error.response.data.errmsg, '评价面试出错')
      })
    },
    addQuestion: function () {
      let _this = this
      axios.get('http://106.14.227.202/api/problem/getall/', {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        console.log('type:', typeof (response.data))
        _this.queTableData = response.data
      }).catch(function (error) {
        console.log('get problems info error:')
        console.log(error.response)
      })
      this.chooseQueDialogFormVisible = true
    },
    handleChooseQue: function (index, row) {
      console.log(index, row)
      console.log(this.queTableData[index] === row) // true
      let _this = this
      axios.get('http://106.14.227.202/api/problem/' + row['id'] + '/', {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        console.log('type:', typeof (response.data))
        _this.queDetail = response.data
      }).catch(function (error) {
        console.log('get problems detail error:')
        console.log(error.response)
      })
      this.chooseQueDialogFormVisible = false
      // 发送给候选人
      console.log('send que id')
      this.send(row['id'])
    },
    conWebSocket: function () {
      let vm = this
      if (window.WebSocket) {
        vm.socket = new WebSocket('ws://106.14.227.202:8088')
        let socket = vm.socket

        socket.onopen = function (e) {
          console.log('连接发送题目服务器成功')
        }
        socket.onclose = function (e) {
          console.log('发送题目服务器关闭')
        }
        socket.onerror = function () {
          console.log('发送题目连接出错')
        }
        // 接收服务器的消息
        socket.onmessage = function (e) {
          console.log(vm.messageList)
          let message = JSON.parse(e.data)
          vm.messageList.push(message)
        }
      }
    },
    send: function (msg) {
      // if(!this.msg){
      //   return
      // }
      this.sendMessage(msg)
    },
    sendMessage: function (queId) {
      this.socket.send(JSON.stringify({
        roomid: this.$route.params.roomid,
        msg: queId,
        bridge: this.bridge
      }))
      console.log('msg = ', queId)
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
.head-line {
  color: #BCC4C8;
}

.top-img {
  float: left;
}

.end-button,
.end-button:focus,
.end-button:hover,
.head-button:focus,
.head-button:hover {
  background-color: #25BB9B;
  border-color: #25BB9B;
}

.head-button {
  background-color: #25BB9B;
  border-color: #25BB9B;
  float: right;
  margin-top: 10px;
  margin-left: 10px;
}

.question-window {
  height: 540px;
  /* line-height: 500px; */
  background-color: #F5F5F5;
  border-width: 1px;
  border-color: #000;
}

.card {
  height: 600px;
}

.el-header {
  background-color: #3D444C;
  color: #FFF;
  text-align: left;
  line-height: 60px;
}

.el-main {
  background-color: #EDEDED;
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

.el-textarea {
  width: 95%
}

.el-rate {
  line-height: 2.6;
}

.bottom-toolbar {
  text-align: center;
  padding-top: 15px;
}

h4 {
  margin-bottom: 10px
}

.top-head {
  margin-top: 0;
}

.video-row {
  background-color: #3D444D;
}

.text-window {
  height: 400px;
  line-height: 400px;
  margin-top: 10px;
  background-color: #3D444D;
}

.el-tabs {
  background-color: #F5F5F5;
}

.el-tabs--border-card>.el-tabs__header {
  background-color: #F5F5F5;
}
</style>
