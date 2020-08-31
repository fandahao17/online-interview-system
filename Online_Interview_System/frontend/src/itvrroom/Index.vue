<template>
  <div>
    <el-container>
      <el-header>
        Header 这是面试官的房间
        <el-button type="primary" :disabled="isStart" @click="onStartBtn">开始录制</el-button>
        <el-button type="primary" :disabled="!isStart" @click="onEndBtn">结束录制</el-button>
        <el-button type="primary" :disabled="!isFinish" @click="onDownloadBtn">下载</el-button>
        <el-button type="primary" :disabled="!isFinish||isUpload" @click="onUploadBtn">上传</el-button>
        <el-button type="primary" plain @click="clickButton">控制台输出房间信息</el-button>
        <el-button type="primary" plain @click="endInterview">结束面试</el-button>
      </el-header>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="6">
            <el-row class="grid-content bg-purple">
              <video-window v-bind:room-info="roomInfo"></video-window>
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
          <el-col :span="5" class="question-window"><div class="grid-content bg-purple question-window">这里是展示问题的窗口</div></el-col>
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
      textsList: ['D', 'C', 'B', 'A', 'S']
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
    }
  },
  mounted: function () {
    this.getRoomInfo(this)
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
  line-height: 600px;
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

.el-textarea {
  width: 95%
}

.el-rate {
  line-height: 2.6;
}
</style>
