<template>
  <div>
    <el-row v-for="rn in rowNum" v-bind:key="rn">
      <el-col :span="8" v-for="i in 3" v-bind:key="i">
        <el-card class="box-card" shadow="hover" @click.native="clickCard">
          <div slot="header" class="clearfix">
            <span> 候选人{{ (((rn-1) * 3) + i) }}</span>
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </div>

          <el-col :span="18">
            <div v-for="n in 3" :key="n" class="text item">
              {{'列表内容 ' + n }}
            </div>
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
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>候选人{{ intvweeNum - lastRow + i }}</span>
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </div>
          <el-col :span="18">
            <div v-for="n in 3" :key="n" class="text item">
              {{'列表内容 ' + n }}
            </div>
          </el-col>
          <el-col :span="6">
            <el-checkbox v-model="checked" v-if="isDeleting"></el-checkbox>
          </el-col>
        </el-card>
      </el-col>
    </el-row>

    <!-- 点击 delete 后出现的确认取消按钮 -->
    <el-button icon="el-icon-search" plain class="cancel-delete" v-if="isDeleting" @click="clickCancelDelete">取消</el-button>
    <el-button icon="el-icon-delete" type="danger" plain class="confirm-delete" v-if="isDeleting" @click="clickConfirmDelete">删除</el-button>

    <!-- 点击卡片弹出的表单 -->
    <el-dialog title="候选人信息" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="姓名" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="email" :label-width="formLabelWidth">
          <el-input v-model="form.email" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="活动区域" :label-width="formLabelWidth">
          <el-select v-model="form.region" placeholder="请选择活动区域">
            <el-option label="区域一" value="shanghai"></el-option>
            <el-option label="区域二" value="beijing"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'AppMain',
  data: function () {
    return {
      test: 0,
      intvweeNum: 11, // 从 API 请求到的 interviewee 的数量
      dialogFormVisible: false, // 是否显示弹出表单
      form: { // 弹出表单的内容
        name: '',
        email: '',
        region: ''
      },
      formLabelWidth: '120px', // 弹出表单的宽度
      checked: false, // 复选框是否选中
      isDeleting: false // 现在是否在删除过程中
    }
  },
  computed: {
    rowNum: function () { // 除最后一行外有多少行
      return Math.floor(this.intvweeNum / 3)
    },
    lastRow: function () { // 最后一行有多少个元素
      return this.intvweeNum - 3 * this.rowNum
    }
  },
  methods: {
    clickCard: function () {
      this.dialogFormVisible = true
    },
    handleDelete: function () {
      // 处理 RightMenu 中“删除”按钮被点击的事件
      // note: 点击 delete 后这个函数会被触发两次
      this.test = this.test + 1
      console.log(this.test)
      alert('delete button was clicked' + this.test)
      this.isDeleting = true
    },
    clickCancelDelete: function () {
      this.isDeleting = false
    },
    clickConfirmDelete: function () {
      this.isDeleting = false
    }
  },
  created: function () {
    this.$eventHub.$on('click-delete', this.handleDelete)
  },
  beforeDestory: function () {
    this.$eventHub.$off('click-delete')
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
  width: 300px;
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
</style>
