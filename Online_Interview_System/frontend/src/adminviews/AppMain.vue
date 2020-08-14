<template>
  <div>
    <el-row v-for="rn in rowNum" v-bind:key="rn">
      <el-col :span="8" v-for="i in 3" v-bind:key="i">
        <el-card class="box-card" shadow="hover" @click.native="clickCard(((rn-1) * 3) + i - 1)">
          <div slot="header" class="clearfix">
            <span> {{ cardDataAll[(((rn-1) * 3) + i - 1)]['name'] }} </span>
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </div>
          <el-col :span="18">
            <div class="text item">
              <span>mobile: </span>
              {{ cardDataAll[(((rn-1) * 3) + i - 1)]['mobile'] }}
            </div>
            <div class="text item">
              <span>email: </span>
              {{ cardDataAll[(((rn-1) * 3) + i - 1)]['email'] }}
            </div>
            <!-- <div class="text item"  v-if="currentMenu !== 'itve'">
              <span>password: </span>
              {{ cardDataAll[(((rn-1) * 3) + i - 1)]['password'] }}
            </div> -->
          </el-col>
          <el-col :span="6">
            <el-checkbox v-model="checked" v-if="isDeleting"></el-checkbox>
          </el-col>
        </el-card>
      </el-col>
    </el-row>
    <!-- 最后一行 -->
    <el-row v-if="lastRow > 0">
      <el-col :span="8" v-for="i in lastRow" v-bind:key="i">
        <el-card class="box-card" shadow="hover" @click.native="clickCard(peopleNum - lastRow + i - 1)">
          <div slot="header" class="clearfix">
            <span>{{ cardDataAll[peopleNum - lastRow + i - 1]['name'] }}</span>
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </div>
          <el-col :span="18">
            <div class="text item">
              <span>mobile: </span>
              {{ cardDataAll[peopleNum - lastRow + i - 1]['mobile'] }}
            </div>
            <div class="text item">
              <span>email: </span>
              {{ cardDataAll[peopleNum - lastRow + i - 1]['email'] }}
            </div>
            <!-- <div class="text item"  v-if="currentMenu !== 'itve'">
              <span>password: </span>
              {{ cardDataAll[peopleNum - lastRow + i - 1]['password'] }}
            </div> -->
          </el-col>
          <el-col :span="6">
            <el-checkbox v-model="checked" v-if="isDeleting"></el-checkbox>
          </el-col>
        </el-card>
      </el-col>
    </el-row>

    <!-- 点击 delete 后出现的确认取消按钮 -->
    <el-button icon="el-icon-close" plain class="cancel-delete" v-if="isDeleting" @click="clickCancelDelete">取消</el-button>
    <el-button icon="el-icon-delete" type="danger" plain class="confirm-delete" v-if="isDeleting" @click="clickConfirmDelete">删除</el-button>

    <!-- 点击候选人、面试官卡片弹出的表单 -->
    <el-dialog title="候选人信息" :visible.sync="userDialogFormVisible">
      <el-form :model="userForm">
        <el-form-item label="姓名" :label-width="formLabelWidth">
          <el-input v-model="userForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="mobile" :label-width="formLabelWidth">
          <el-input v-model="userForm.mobile" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="email" :label-width="formLabelWidth">
          <el-input v-model="userForm.email" autocomplete="off"></el-input>
        </el-form-item>
        <!-- <el-form-item label="password" :label-width="formLabelWidth" v-if="currentMenu !== 'itve'">
          <el-input v-model="userForm.password" autocomplete="off"></el-input>
        </el-form-item> -->
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="closeUserDialog">取消</el-button>
        <el-button type="primary" @click="commitUserDialog">确定</el-button>
      </div>
    </el-dialog>

    <!-- 点击 HR 卡片弹出的表单 -->
    <el-dialog width=85% :visible.sync="hrDialogFormVisible">
      <el-row :gutter="20">
        <el-col :span="7">
          <h3>HR 信息</h3>
          <el-form :model="hrForm">
            <el-form-item label="姓名" :label-width="hrFormLabelWidth">
              <span v-if="editHrInfo === false" > {{ hrForm.name }} </span>
              <el-input v-else v-model="hrForm.name" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="email" :label-width="hrFormLabelWidth">
              <span v-if="editHrInfo === false" > {{ hrForm.email }} </span>
              <el-input v-else v-model="hrForm.email" autocomplete="off"></el-input>
            </el-form-item>
          </el-form>
          <div class="hrinfo-footer">
            <el-button size="medium" type="primary" plain v-if="editHrInfo === false" @click="editHrInfo = true">编 辑</el-button>
            <el-button size="medium" v-if="editHrInfo" @click="editHrInfo = false">取 消</el-button>
            <el-button size="medium" type="primary" plain v-if="editHrInfo" @click="editHrInfo = false">确 定</el-button>
          </div>
        </el-col>
        <el-col :span="1">
          <el-divider direction="vertical"></el-divider>
        </el-col>
        <el-col :span="8">
          <h3>分配给该 HR 的候选人</h3>
          <el-table
            ref="multipleTable"
            :data="intvweeTableData"
            style="width: 100%"
            max-height="340">
            <el-table-column type="expand">
              <template slot-scope="props">
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item label="姓名">
                    <span>{{ props.row.name }}</span>
                  </el-form-item>
                  <el-form-item label="候选人 ID">
                    <span>{{ props.row.id }}</span>
                  </el-form-item>
                  <el-form-item label="email">
                    <span>{{ props.row.email }}</span>
                  </el-form-item>
                  <el-form-item label="商品分类">
                    <span>{{ props.row.category }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column
              label="姓名"
              prop="name"
              show-overflow-tooltip>
            </el-table-column>
            <el-table-column
              label="email"
              prop="email">
            </el-table-column>
            <el-table-column
              type="selection"
              width="55">
            </el-table-column>
          </el-table>
          <div class="hr-intvwee-footer">
            <el-button size="medium" type="danger" plain @click="hrDialogFormVisible = true">删 除</el-button>
            <el-button size="medium" type="primary" plain @click="addIntvweeDialogFormVisible = true">添 加</el-button>
          </div>
        </el-col>
        <el-col :span="1">
          <el-divider direction="vertical"></el-divider>
        </el-col>
        <el-col :span="7">
          <h3>分配给该 HR 的面试官</h3>
          <el-table
            ref="multipleTable"
            :data="intvwerTableData"
            style="width: 100%"
            max-height="340">
            <el-table-column type="expand">
              <template slot-scope="props">
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item label="姓名">
                    <span>{{ props.row.name }}</span>
                  </el-form-item>
                  <el-form-item label="面试官 ID">
                    <span>{{ props.row.id }}</span>
                  </el-form-item>
                  <el-form-item label="email">
                    <span>{{ props.row.email }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column
              label="姓名"
              prop="name"
              show-overflow-tooltip>
            </el-table-column>
            <el-table-column
              label="email"
              prop="email"
              show-overflow-tooltip>
            </el-table-column>
            <el-table-column
              type="selection"
              width="55">
            </el-table-column>
          </el-table>
          <div class="hr-intvwer-footer">
            <el-button size="medium" type="danger" plain @click="hrDialogFormVisible = true">删 除</el-button>
            <el-button size="medium" type="primary" plain @click="addIntvwerDialogFormVisible = true">添 加</el-button>
          </div>
        </el-col>
      </el-row>
    </el-dialog>

    <!-- 在 HR 弹窗中点击添加候选人弹出的表单 -->
    <el-dialog title="候选人列表" :visible.sync="addIntvweeDialogFormVisible">
      <el-table
        ref="multipleTable"
        :data="intvweeTableData"
        style="width: 100%"
        max-height="350">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="姓名">
                <span>{{ props.row.name }}</span>
              </el-form-item>
              <el-form-item label="候选人 ID">
                <span>{{ props.row.id }}</span>
              </el-form-item>
              <el-form-item label="email">
                <span>{{ props.row.email }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
          label="姓名"
          prop="name"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          label="email"
          prop="email">
        </el-table-column>
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addIntvweeDialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="addIntvweeDialogFormVisible = false">确定</el-button>
      </div>
    </el-dialog>

    <!-- 在 HR 弹窗中点击添加面试官弹出的表单 -->
    <el-dialog title="面试官列表" :visible.sync="addIntvwerDialogFormVisible">
      <el-table
        ref="multipleTable"
        :data="intvwerTableData"
        style="width: 100%"
        max-height="350">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="姓名">
                <span>{{ props.row.name }}</span>
              </el-form-item>
              <el-form-item label="面试官 ID">
                <span>{{ props.row.id }}</span>
              </el-form-item>
              <el-form-item label="email">
                <span>{{ props.row.email }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
          label="姓名"
          prop="name"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          label="email"
          prop="email">
        </el-table-column>
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addIntvwerDialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="addIntvwerDialogFormVisible = false">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AppMain',
  data: function () {
    return {
      currentMenu: '', // 记录当前处于哪一个 menu
      editHrInfo: false,
      addIntvweeDialogFormVisible: false,
      addIntvwerDialogFormVisible: false,
      // peopleNum: 11, // 从 API 请求到的 interviewee 的数量
      userDialogFormVisible: false, // 是否显示弹出表单
      userForm: {},
      formLabelWidth: '120px', // 弹出表单的宽度
      hrDialogFormVisible: false, // 是否显示弹出表单
      hrForm: {},
      hrFormLabelWidth: '70px', // 弹出表单的宽度
      checked: false, // 复选框是否选中
      isDeleting: false, // 现在是否在删除过程中
      intvweeTableData: [{
        id: '1',
        name: '候选人1',
        email: 'aaa@gmail.com',
        category: '江浙小吃、小吃零食'
      }, {
        id: '2',
        name: '候选人2',
        email: 'bbb@gmail.com',
        category: '江浙小吃、小吃零食'
      }, {
        id: '3',
        name: '候选人3',
        email: 'ccc@gmail.com',
        category: '江浙小吃、小吃零食'
      }, {
        id: '4',
        name: '候选人4',
        email: 'ddd@gmail.com',
        category: '江浙小吃、小吃零食'
      }],
      intvwerTableData: [{
        id: '1',
        name: '面试官1',
        email: 'aaa@gmail.com',
        category: '江浙小吃、小吃零食'
      }, {
        id: '2',
        name: '面试官2',
        email: 'bbb@gmail.com',
        category: '江浙小吃、小吃零食'
      }],
      cardDataAll: [{}]
    }
  },
  computed: {
    peopleNum: function () {
      return this.cardDataAll.length
    },
    rowNum: function () { // 除最后一行外有多少行
      return Math.floor(this.peopleNum / 3)
    },
    lastRow: function () { // 最后一行有多少个元素
      return this.peopleNum - 3 * this.rowNum
    }
  },
  methods: {
    getItveInfo: function (_this) {
      axios.get('http://106.14.227.202/api/itve/getall/', {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        console.log('type:', typeof (response.data))
        _this.cardDataAll = response.data
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
        _this.cardDataAll = response.data
      }).catch(function (error) {
        console.log('get itvr info error:')
        console.log(error.response)
      })
    },
    getHrInfo: function (_this) {
      axios.get('http://106.14.227.202/api/hr/getall/', {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        console.log('type:', typeof (response.data))
        _this.cardDataAll = response.data
      }).catch(function (error) {
        console.log('get hr info error:')
        console.log(error.response)
      })
    },
    clickCard: function (index) {
      if (this.currentMenu === 'hr') {
        this.hrDialogFormVisible = true
        // this.hrForm = this.cardDataAll[index]
        this.hrForm = Object.assign({}, this.cardDataAll[index]) // 复制
      } else {
        this.userDialogFormVisible = true
        // this.userForm = this.cardDataAll[index]
        this.userForm = Object.assign({}, this.cardDataAll[index]) // 复制
      }
    },
    handleDelete: function () {
      // 处理 RightMenu 中“删除”按钮被点击的事件
      // note: 点击 delete 后这个函数会被触发两次
      this.isDeleting = true
    },
    clickCancelDelete: function () {
      this.isDeleting = false
    },
    clickConfirmDelete: function () {
      this.isDeleting = false
    },
    handleMenuChange: function (key) {
      console.log('catch menu change to ', key)
      this.currentMenu = key
      if (key === 'itve') {
        this.getItveInfo(this)
      } else if (key === 'itvr') {
        this.getItvrInfo(this)
      } else if (key === 'hr') {
        this.getHrInfo(this)
      } else {
        console.log('[error] unknown user type')
      }
    },
    closeUserDialog: function () {
      this.userDialogFormVisible = false
    },
    commitUserDialog: function () {
      let _this = this
      axios.post('http://106.14.227.202/api/' + this.currentMenu + '/', this.userForm, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log('edit ' + this.currentMenu + ' info successfully:')
        console.log(response.data)
        _this.$message('编辑 ' + this.currentMenu + ' 成功')
        if (_this.currentMenu === 'itve') {
          _this.getItveInfo(_this)
        } else {
          _this.getItvrInfo(_this)
        }
      }).catch(function (error) {
        console.log('edit ' + this.currentMenu + ' info error:')
        console.log(error.response)
        _this.$alert(error.response.data.errmsg, '编辑 ' + this.currentMenu + ' 出错')
      })
      this.userDialogFormVisible = false
      if (this.currentMenu === 'itve') {
        this.getItveInfo(this)
      } else if (this.currentMenu === 'itvr') {
        this.getItvrInfo(this)
      }
    },
    closeHrDialog: function () {
      this.hrDialogFormVisible = false
      this.getHrInfo(this)
    }
  },
  created: function () {
    this.$eventHub.$on('click-delete', this.handleDelete)
    this.$eventHub.$on('menu-change', this.handleMenuChange)
  },
  beforeDestory: function () {
    this.$eventHub.$off('click-delete')
    this.$eventHub.$off('menu-change')
  },
  mounted: function () {
    this.getItveInfo(this)
    this.currentMenu = 'itve'
  }
}
</script>

<style scoped>
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both
}

.box-card {
  width: 400px;
  height: 200px;
  margin-left: 40px;
  border-radius: 20px;
  border-width: 2px;
}

.el-row {
  margin-bottom: 20px;
}
.el-col {
  border-radius: 4px;
  height: 100%;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}

.el-input {
  width: 90%;
}

.el-form {
  text-align: left;
}

.el-checkbox {
  float: right;
}

.cancel-delete {
  position: fixed;
  right: 150px;
  bottom: 25px;
}

.confirm-delete {
  position: fixed;
  right: 40px;
  bottom: 25px;
}

.hrinfo-footer,
.hr-intvwee-footer,
.hr-intvwer-footer {
  float: right;
  padding-top: 20px;
}
</style>
