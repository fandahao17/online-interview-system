<template>
  <div>
    <el-container>
      <el-header><head-menu></head-menu></el-header>
      <el-main>
        <div>
          <el-button type="primary" plain size="medium" @click="clickHire">录用</el-button>
          <el-button type="primary" plain size="medium" @click="clickReject">拒绝</el-button>
          <el-button type="primary" plain size="medium" @click="clickNextRound">下一轮</el-button>
        </div>
        <el-table
          :data="intvTableData"
          style="width: 100%"
          @selection-change="handleSelectionChange">
          <el-table-column
            type="selection"
            width="55">
          </el-table-column>
          <el-table-column
            prop="itvwee"
            label="候选人"
            width="180">
          </el-table-column>
          <el-table-column
            prop="itvwer"
            label="面试官"
            width="180">
          </el-table-column>
          <el-table-column
            prop="grade"
            label="评级"
            width="180">
          </el-table-column>
          <el-table-column
            prop="start"
            label="开始时间"
            width="180">
          </el-table-column>
          <el-table-column
            prop="end"
            label="结束时间"
            width="180">
          </el-table-column>
          <el-table-column
            prop="status"
            label="状态">
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import HeadMenu from '@/hrs/HeadMenu'

export default {
  name: 'HrRecall',
  components: {
    HeadMenu
  },
  data: function () {
    return {
      intvTableData: [{
        itvwee: '曹宇昂',
        itvwer: '张俊霞',
        grade: 'A',
        start: '2016-05-02 14:01:22',
        end: '2016-05-02 15:01:22',
        status: '未分配'
      }, {
        itvwee: '樊金昊',
        itvwer: '包信和',
        grade: 'A',
        start: '2016-05-02 14:01:22',
        end: '2016-05-02 15:01:22',
        status: '未分配'
      }, {
        itvwee: '刘硕',
        itvwer: '潘建伟',
        grade: 'A',
        start: '2016-05-02 14:01:22',
        end: '2016-05-02 15:01:22',
        status: '未分配'
      }],
      multipleSelection: []
    }
  },
  methods: {
    handleSelectionChange: function (val) {
      this.multipleSelection = val
      console.log('multipleSelection = ', this.multipleSelection)
    },
    clickHire: function () {
      console.log('clickHire')
    },
    clickReject: function () {
      console.log('clickReject')
    },
    clickNextRound: function () {
      console.log('clickNextRound')
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
</style>
