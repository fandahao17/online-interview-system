<template>
  <div>
    <el-row>
      <el-col :span="8">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>候选人</span>
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </div>
          <div v-for="n in 3" :key="n" class="text item">
            {{'列表内容 ' + n }}
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>候选人</span>
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </div>
          <div v-for="n in 3" :key="n" class="text item">
            {{'列表内容 ' + n }}
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>候选人</span>
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </div>
          <div v-for="n in 3" :key="n" class="text item">
            {{'列表内容 ' + n }}
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="8">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>候选人</span>
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </div>
          <div v-for="n in 3" :key="n" class="text item">
            {{'列表内容 ' + n }}
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>候选人</span>
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </div>
          <div v-for="n in 3" :key="n" class="text item">
            {{'列表内容 ' + n }}
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>候选人</span>
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </div>
          <div v-for="n in 3" :key="n" class="text item">
            {{'列表内容 ' + n }}
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="8">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>候选人</span>
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </div>
          <div v-for="n in 3" :key="n" class="text item">
            {{'列表内容 ' + n }}
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>候选人</span>
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </div>
          <div v-for="n in 3" :key="n" class="text item">
            {{'列表内容 ' + n }}
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>候选人</span>
            <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
          </div>
          <div v-for="n in 3" :key="n" class="text item">
            {{'列表内容 ' + n }}
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'AppMain'
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
</style>
