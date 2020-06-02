<template>
  <div class="menu-right">
    <el-button icon="el-icon-search" plain>搜索</el-button>
    <el-button icon="el-icon-plus" type="primary" plain @click="clickAdd">添加</el-button>
    <el-upload
      class="upload-demo"
      action="https://jsonplaceholder.typicode.com/posts/"
      :on-preview="handlePreview"
      :on-remove="handleRemove"
      :before-remove="beforeRemove"
      multiple
      :limit="3"
      :on-exceed="handleExceed">
      <el-button icon="el-icon-upload2" type="primary" plain>导入</el-button>
    </el-upload>
    <el-button icon="el-icon-delete" type="danger" plain @click="clickDelete">删除</el-button>

    <el-dropdown class="avatar-container">
      <div class="avatar-wrapper">
        <el-avatar icon="el-icon-user-solid" size="medium"></el-avatar>
        <i class="el-icon-caret-bottom"/>
      </div>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item>个人中心</el-dropdown-item>
        <el-dropdown-item>选项二</el-dropdown-item>
        <el-dropdown-item divided>退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>

    <!-- 点击“添加”弹出的表单 -->
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
  name: 'RightMenu',
  data: function () {
    return {
      form: {
        name: '',
        email: '',
        region: ''
      },
      formLabelWidth: '120px',
      dialogFormVisible: false,
      fileList: []
    }
  },
  methods: {
    clickAdd: function () {
      this.dialogFormVisible = true
    },
    clickDelete: function () {
      this.$eventHub.$emit('click-delete')
    },
    handleRemove: function (file, fileList) {
      console.log(file, fileList)
    },
    handlePreview: function (file) {
      console.log(file)
    },
    handleExceed: function (files, fileList) {
      this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
    },
    beforeRemove: function (file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`)
    }
  }
}
</script>

<style scoped>
.el-avatar {
  vertical-align: middle;
}

.menu-right {
  float: right;
  padding-right: 20px;
}

.avatar-container {
  padding-left: 15px;
}

.el-input {
  width: 300px;
}

.el-form {
  text-align: left;
}

.upload-demo {
  display: inline-block;
}

.el-upload-list {
  display: none;
}

.el-button {
  margin-left: 10px;
}
</style>
