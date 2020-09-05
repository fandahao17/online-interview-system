<template>
  <div class="menu-right">
    <el-button icon="el-icon-search" plain @click="isSearching = true" v-if="isSearching === false">搜索</el-button>
    <el-input
      v-else
      v-model="searchInfo"
      @change="searchChange"
      placeholder="输入关键字搜索"/>
    <el-button icon="el-icon-plus" type="primary" plain @click="clickAdd">添加</el-button>
    <!-- <el-upload
      class="upload-demo"
      action="https://jsonplaceholder.typicode.com/posts/"
      :on-preview="handlePreview"
      :on-remove="handleRemove"
      :before-remove="beforeRemove"
      multiple
      :limit="3"
      :on-exceed="handleExceed">
      <el-button icon="el-icon-upload2" type="primary" plain>导入</el-button>
    </el-upload> -->
    <el-button icon="el-icon-delete" type="danger" plain @click="clickDelete">删除</el-button>

    <el-dropdown class="avatar-container">
      <div class="avatar-wrapper">
        <el-avatar icon="el-icon-user-solid" size="medium"></el-avatar>
        <i class="el-icon-caret-bottom"/>
      </div>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item>个人中心</el-dropdown-item>
        <el-dropdown-item>选项二</el-dropdown-item>
        <el-dropdown-item divided @click.native="logout">退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
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
      fileList: [],
      searchInfo: '',
      isSearching: false
    }
  },
  methods: {
    clickAdd: function () {
      this.$eventHub.$emit('admin-add')
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
    },
    searchChange: function () {
      console.log('info = ')
      console.log(this.searchInfo)
      this.$eventHub.$emit('search-info', this.searchInfo)
    },
    logout: function () {
      console.log('logout')
      localStorage.clear()
      this.$router.push('/')
    }
  },
  created: function () {
    let _this = this
    if (localStorage.getItem('email') === null) {
      alert('need to login')
      _this.$router.push('/login/')
    } else if (localStorage.getItem('identity').toString() !== '2') {
      alert('permission denied: not a admin')
      if (localStorage.getItem('identity').toString() === '3') {
        _this.$router.push('/hr')
      } else if (localStorage.getItem('identity').toString() === '1') {
        _this.$router.push('/interviewer')
      } else {
        alert('can\'t identify ')
        _this.$router.push('/')
      }
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
