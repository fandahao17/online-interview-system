<template>
  <el-container>
    <el-header>Header</el-header>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-row class="grid-content bg-purple">
            <video-window></video-window>
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
</template>

<script>
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
</style>
