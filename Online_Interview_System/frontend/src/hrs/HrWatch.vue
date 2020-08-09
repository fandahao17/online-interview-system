<template>
  <div>
    <el-container>
      <el-header><head-menu></head-menu></el-header>
      <el-main>
        <el-row v-for="rn in rowNum" v-bind:key="rn">
          <el-col :span="8" v-for="i in 3" v-bind:key="i">
            <el-card class="box-card" shadow="hover" @click.native="clickCard">
              <div slot="header" class="clearfix">
                <span>面试{{ (((rn-1) * 3) + i) }}</span>
                <el-button style="float: right; padding: 3px 0" type="text">进入房间</el-button>
              </div>
              <div v-for="n in 3" :key="n" class="text item">
                {{'列表内容 ' + n }}
              </div>
            </el-card>
          </el-col>
        </el-row>
        <!-- 最后一行 -->
        <el-row v-if="lastRow > 0">
          <el-col :span="8" v-for="i in lastRow" v-bind:key="i">
            <el-card class="box-card" shadow="hover" @click.native="clickCard">
              <div slot="header" class="clearfix">
                <span>面试{{ intvwNum - lastRow + i }}</span>
                <el-button style="float: right; padding: 3px 0" type="text">进入房间</el-button>
              </div>
              <div v-for="n in 3" :key="n" class="text item">
                {{'列表内容 ' + n }}
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
// note!
// 列表内容应该换成 面试官、面试者、面试时间范围
import HeadMenu from '@/hrs/HeadMenu'

export default {
  name: 'HrWatch',
  components: {
    HeadMenu
  },
  data: function () {
    return {
      intvwNum: 11 // 从 API 请求到的 interview 的数量
    }
  },
  computed: {
    rowNum: function () { // 除最后一行外有多少行
      return Math.floor(this.intvwNum / 3)
    },
    lastRow: function () { // 最后一行有多少个元素
      return this.intvwNum - 3 * this.rowNum
    }
  },
  methods: {
    clickCard: function () {
      // click card
      console.log('enter the interview room')
    }
  }
}
</script>

<style scoped>
  .el-header {
    background-color: #DCDFE6;
    text-align: center;
    line-height: 55px;
  }

  .el-main {
    color: #333;
  }

  body > .el-container {
    margin-bottom: 40px;
  }

  .box-card {
    width: 400px;
    height: 200px;
    margin-left: 40px;
    border-radius: 20px;
    border-width: 2px;
  }

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

  .el-row {
    margin-bottom: 20px;
  }

  .el-col {
    border-radius: 4px;
    height: 100%;
  }
</style>
