<template>
  <div>
    <el-row>
      <el-col :span="12" class="left-top">
        <el-row>
          <div class="title">候选人</div>
        </el-row>
        <el-row :gutter="100" class="blank-row">
          <!-- <el-col :span="12">
            <el-checkbox v-model="leftChecked1">已安排</el-checkbox>
          </el-col>
          <el-col :span="12">
            <el-checkbox v-model="leftChecked2">未安排</el-checkbox>
          </el-col> -->
        </el-row>

        <el-row v-for="num in itveNum" v-bind:key="num">
          <el-card class="box-card" shadow="hover">
            <el-col :span="22">
              <div class="icon"><el-avatar :size="50" :src="circleUrl"></el-avatar></div>
              <div class="item">Name: {{ leftCardData[num-1]['name'] }}</div>
              <div class="item">Email: {{ leftCardData[num-1]['email'] }}</div>
            </el-col>
            <el-col :span="2">
              <el-radio v-model="itveChoosed" :label="num" v-if="isDistributing">{{''}}</el-radio>
            </el-col>
          </el-card>
        </el-row>
      </el-col>

      <!-- <div class="vertical-bar"></div> -->

      <el-col :span="12" class="right-top">
        <el-row>
          <el-col :span="20" :offset="3">
            <div class="title">面试官</div>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="5" :offset="5">
            <el-checkbox v-model="rightChecked1">有空闲时间</el-checkbox>
          </el-col>
          <el-col :span="5" :offset="5">
            <el-checkbox v-model="rightChecked2">无空闲时间</el-checkbox>
          </el-col>
        </el-row>
        <el-row v-for="num in itvrNum" v-bind:key="num">
          <el-card class="box-card" shadow="hover" @click.native="clickItvr(num)"
            v-if="(rightChecked1 === false && rightChecked2 === false) || (rightChecked1 === true && rightChecked2 === true) || (rightChecked1 === true && rightChecked2 === false && rightCardData[num-1]['busyall'] === false) || (rightChecked1 === false && rightChecked2 === true && rightCardData[num-1]['busyall'] === true)">
            <el-col :span="22">
              <div class="icon"><el-avatar :size="50" :src="circleUrl"></el-avatar></div>
              <div class="item">Name: {{ rightCardData[num-1]['name'] }}</div>
              <div class="item">Email: {{ rightCardData[num-1]['email'] }}</div>
            </el-col>
            <el-col :span="2">
              <el-radio v-model="itvrChoosed" :label="num" v-if="isDistributing">{{''}}</el-radio>
            </el-col>
          </el-card>
        </el-row>
      </el-col>
    </el-row>

    <!-- 点击 delete 后出现的确认取消按钮 -->
    <el-button icon="el-icon-user" type="primary" plain class="confirm-dist" v-if="!isDistributing" @click="startDist">分配面试</el-button>
    <el-button icon="el-icon-close" plain class="cancel-dist" v-if="isDistributing" @click="clickCancelDist">取消</el-button>
    <el-button icon="el-icon-check" type="primary" plain class="confirm-dist" v-if="isDistributing" @click="clickConfirmDist">分配</el-button>

    <el-dialog title="分配面试" :visible.sync="distDialogFormVisible" class="dist-dialog" :before-close="clickCancelDist">
      <el-row>
        <el-col :span="12">
          <h3>候选人</h3>
          <el-form :model="itveForm">
            <el-form-item label="姓名" :label-width="distFormLabelWidth">
              <span>{{ itveForm.name }}</span>
            </el-form-item>
            <el-form-item label="Email" :label-width="distFormLabelWidth">
              <span>{{ itveForm.email }}</span>
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :span="12">
          <h3>面试官</h3>
          <el-form :model="itvrForm">
            <el-form-item label="姓名" :label-width="distFormLabelWidth">
              <span>{{ itvrForm.name }}</span>
            </el-form-item>
            <el-form-item label="Email" :label-width="distFormLabelWidth">
              <span>{{ itvrForm.email }}</span>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
      <el-row>
        <h3>选择面试时间</h3>
        <el-radio-group v-model="itvrTimeRadio">
          <el-radio :label="0" :disabled="!itvrForm.free1">上午</el-radio>
          <el-radio :label="1" :disabled="!itvrForm.free2">下午</el-radio>
          <el-radio :label="2" :disabled="!itvrForm.free3">晚上</el-radio>
        </el-radio-group>
      </el-row>
      <div slot="footer" class="dialog-footer">
        <el-button @click="clickCancelDist">取 消</el-button>
        <el-button type="primary" @click="commitDistItve">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="面试官信息" :visible.sync="itvrDialogFormVisible" class="dist-dialog" width="60%" :before-close="clickCancelItvr">
      <el-row>
        <h3>面试官</h3>
        <el-form :model="itvrFormInItvrDia">
          <el-form-item label="姓名" :label-width="itvrFormLabelWidth">
            <span>{{ itvrFormInItvrDia.name }}</span>
          </el-form-item>
          <el-form-item label="Email" :label-width="itvrFormLabelWidth">
            <span>{{ itvrFormInItvrDia.email }}</span>
          </el-form-item>
        </el-form>
      </el-row>
      <el-row>
        <h3>时间段</h3>
        <el-slider
          class="time-slider"
          v-model="timeRange"
          range
          show-stops
          :max="2"
          :marks="timeMarks">
        </el-slider>
      </el-row>
      <el-row>
        <h3>已安排面试</h3>
        <span v-if="itvrItveNum === 0">该面试官未安排面试</span>
        <el-col :span="8" v-for="i in itvrItveNum" v-bind:key="i">
          <el-popover
            v-if="itvrItveCardData[i-1]['time'] >= timeRange[0] && itvrItveCardData[i-1]['time'] <= timeRange[1]"
            placement="top-start"
            width="300px"
            trigger="hover"
            class="room-popover">
            <!-- 这是 popover 中的内容 -->
            <el-form :model="itvrItveCardData[i-1]">
              <el-form-item label="房间号" :label-width="formLabelWidth">
                <span>{{ itvrItveCardData[i-1]['roomid'] }}</span>
              </el-form-item>
              <el-form-item label="面试时间" :label-width="formLabelWidth">
                <span>{{ itvrItveCardData[i-1]['time_str'] }}</span>
              </el-form-item>
              <el-form-item label="候选人" :label-width="formLabelWidth">
                <span>{{ itvrItveCardData[i-1]['interviewee__name'] }}</span>
              </el-form-item>
              <el-form-item label="电话" :label-width="formLabelWidth">
                <span>{{ itvrItveCardData[i-1]['interviewee__mobile'] }}</span>
              </el-form-item>
              <el-form-item label="邮箱" :label-width="formLabelWidth">
                <span>{{ itvrItveCardData[i-1]['interviewee__email'] }}</span>
              </el-form-item>
            </el-form>
            <div style="text-align: right; margin: 0">
              <el-button type="danger" plain size="mini" @click="deleteRoom(i)">删除</el-button>
            </div>
            <!-- 在该元素上触发 popover -->
            <el-card class="itve-card" shadow="hover" slot="reference">
              <el-col :span="24">
                <div class="text item">
                  <span>候选人: </span>
                  {{ itvrItveCardData[i-1]['interviewee__name'] }}
                </div>
                <div class="text item">
                  <span>电话: </span>
                  {{ itvrItveCardData[i-1]['interviewee__mobile'] }}
                </div>
                <div class="text item">
                  <span>邮箱: </span>
                  {{ itvrItveCardData[i-1]['interviewee__email'] }}
                </div>
              </el-col>
            </el-card>
          </el-popover>
        </el-col>
      </el-row>
      <div slot="footer" class="dialog-footer">
        <el-button @click="clickCancelItvr">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import draggable from 'vuedraggable'

export default {
  name: 'HrDistribute',
  components: {
    draggable
  },
  data: function () {
    return {
      circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      leftChecked1: false,
      leftChecked2: false,
      rightChecked1: false,
      rightChecked2: false,
      leftCardData: [{}],
      rightCardData: [{}],
      itveChoosed: '',
      itvrChoosed: '',
      isDistributing: false,
      distDialogFormVisible: false,
      distFormLabelWidth: '80px',
      itveForm: {},
      itvrForm: {},
      itvrTimeRadio: '',
      itvrDialogFormVisible: false,
      itvrFormLabelWidth: '120px',
      itvrFormInItvrDia: {},
      timeRange: [0, 2],
      timeMarks: {
        0: '上午',
        1: '下午',
        2: {
          style: {
            width: '28px'
          },
          label: '晚上'
        }
      },
      checked: false,
      itvrItveCardData: [{}],
      formLabelWidth: '80px',
      detailItvrNumNow: ''
    }
  },
  computed: {
    itveNum: function () {
      return this.leftCardData.length
    },
    itvrNum: function () {
      return this.rightCardData.length
    },
    itvrItveNum: function () {
      return this.itvrItveCardData.length
    }
  },
  mounted: function () {
    this.getItveInfo(this)
    this.getItvrInfo(this)
  },
  methods: {
    getItveInfo: function (_this) {
      axios.get('http://106.14.227.202/api/itve/getall/', { // 106.14.227.202/api
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        console.log('type:', typeof (response.data))
        _this.leftCardData = response.data
        // _this.checked = Array(_this.leftCardData.length).fill(false)
      }).catch(function (error) {
        console.log('get itve info error:')
        console.log(error.response)
      })
    },
    getItvrInfo: function (_this) {
      axios.get('http://106.14.227.202/api/itvr/getall/', {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        console.log('type:', typeof (response.data))
        _this.rightCardData = response.data
        for (let i = 0; i < _this.rightCardData.length; i++) {
          if (_this.rightCardData[i]['free1'] === false && _this.rightCardData[i]['free2'] === false && _this.rightCardData[i]['free3'] === false) {
            _this.rightCardData[i]['busyall'] = true
          } else {
            _this.rightCardData[i]['busyall'] = false
          }
        }
      }).catch(function (error) {
        console.log('get itvr info error:')
        console.log(error.response)
      })
    },
    startDist: function () {
      this.isDistributing = true
    },
    clickConfirmDist: function () {
      console.log('itveChoosed = ', this.itveChoosed)
      console.log('itveChoosed !== 空串', this.itveChoosed !== '')
      if (this.itveChoosed === '' || this.itvrChoosed === '') {
        this.$alert('请选择要分配的候选人与面试官', '分配面试出错')
      } else {
        this.isDistributing = false
        this.distDialogFormVisible = true
        this.itveForm = this.leftCardData[this.itveChoosed - 1]
        this.itvrForm = this.rightCardData[this.itvrChoosed - 1]
        // this.itvrForm.email = this.rightCardData[this.itvrChoosed - 1]['email']
      }
    },
    clickCancelDist: function () {
      this.itveChoosed = ''
      this.itvrChoosed = ''
      this.isDistributing = false
      this.distDialogFormVisible = false
      this.itvrTimeRadio = ''
    },
    commitDistItve: function () {
      let _this = this
      this.distDialogFormVisible = false
      let roomForm = {
        itve: this.leftCardData[this.itveChoosed - 1]['email'],
        itvr: this.rightCardData[this.itvrChoosed - 1]['email'],
        time: this.itvrTimeRadio
      }
      let itveNum = this.itveChoosed
      let itvrNum = this.itvrChoosed
      console.log('roomForm = ', roomForm)
      axios.post('http://106.14.227.202/api/room/add/', roomForm, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        // if (response.data)
        console.log('response.data')
        console.log(response.data)
        _this.$message('将候选人 ' + _this.leftCardData[itveNum - 1]['name'] + ' 分配给面试官 ' + _this.rightCardData[itvrNum - 1]['name'])
      }).catch(function (error) {
        console.log('add new interview error:')
        console.log(error.response)
        // _this.$alert(error.response.data.errmsg, '添加新面试出错')
        _this.$message('将候选人 ' + _this.leftCardData[itveNum - 1]['name'] + ' 分配给面试官 ' + _this.rightCardData[itvrNum - 1]['name'])
      })
      this.itveChoosed = ''
      this.itvrChoosed = ''
      this.itvrTimeRadio = ''
      this.getItvrInfo(this)
    },
    clickItvr: function (num) {
      if (this.isDistributing === false) {
        let _this = this
        this.itvrFormInItvrDia = this.rightCardData[num - 1]
        this.itvrDialogFormVisible = true
        this.detailItvrNumNow = num
        axios.get('http://106.14.227.202/api/itvr/getitves/' + this.rightCardData[num - 1]['email'] + '/', {
          headers: {
            'Content-Type': 'application/json'
          }
        }).then(function (response) {
          console.log('response.data = ')
          console.log(response.data)
          _this.itvrItveCardData = response.data
          for (let i = 0; i < _this.itvrItveCardData.length; i++) {
            if (_this.itvrItveCardData[i]['time'] === 0) {
              _this.itvrItveCardData[i]['time_str'] = '上午'
            } else if (_this.itvrItveCardData[i]['time'] === 1) {
              _this.itvrItveCardData[i]['time_str'] = '下午'
            } else {
              _this.itvrItveCardData[i]['time_str'] = '晚上'
            }
          }
        }).catch(function (error) {
          console.log('request itvr info error:')
          console.log(error.response)
          _this.$alert(error.response.data.errmsg, '请求面试信息出错')
        })
      }
    },
    clickCancelItvr: function () {
      this.itvrDialogFormVisible = false
      this.timeRange = [0, 2]
    },
    deleteRoom: function (i) {
      let _this = this
      console.log('delete room: ')
      console.log(this.itvrItveCardData[i - 1])
      axios.delete('http://106.14.227.202/api/room/delete/', {
        headers: {
          'Content-Type': 'application/json'
        },
        data: {roomid: this.itvrItveCardData[i - 1]['roomid']}
      }).then(function (response) {
        console.log('received info for delete user method: ', response)
        if (response.data.success === true) {
          _this.$message('删除面试成功')
        } else {
          _this.$message.error('删除面试失败')
        }
        _this.clickItvr(_this.detailItvrNumNow)
      }).catch(function (error) {
        console.log('delete ', _this.currentMenu, ' error: ' + error)
        _this.$alert('删除面试出错', '删除出错')
      })
      this.getItvrInfo(this)
    }
  }
}
</script>

<style scoped>
.vertical-bar {
  width: 5px;
  height: 700px;
  background: lightgray;
  display: inline-block;
  margin-top: 15px;
  vertical-align: top;
  margin-left: 310px;
}

.left-top {
  text-align: center;
  float: left;
}

.el-row {
  margin-bottom: 25px;
}

.el-col {
  border-radius: 4px;
}

.icon {
  float: left;
}

.but {
  padding-top: 0;
}

.item {
  margin-bottom: 13px;
}

.title {
  margin-top: 15px;
  margin-right: 5px;
  font-size: 30px;
  line-height: 50px;
  text-align: center;
}

.box-card {
  font-size: 16px;
  width: 400px;
  height: 100px;
  border-radius: 20px;
  border-width: 2px;
  margin: auto;
}

.grid-content {
  border-radius: 4px;
  min-height: 26px;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}

.cancel-dist {
  position: fixed;
  right: 150px;
  bottom: 25px;
}

.confirm-dist {
  position: fixed;
  right: 40px;
  bottom: 25px;
}

.dist-dialog {
  text-align: left;
}

.el-radio-group {
  margin-left: 50px;
}

.time-slider {
  width: 60%;
  margin: auto;
}

.el-slider-mark {
  width: 28px;
}

.itve-card {
  width: 90%;
  height: auto;
  margin: auto;
  /* margin-left: 40px; */
  border-radius: 20px;
  border-width: 2px;
}

.room-popover {
  width: 300px;
}

.blank-row {
  height: 19.2px;
}
</style>
