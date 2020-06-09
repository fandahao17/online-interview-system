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
        <el-card class="box-card" shadow="hover" @click.native="clickCard">
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
    <el-button icon="el-icon-close" plain class="cancel-delete" v-if="isDeleting" @click="clickCancelDelete">取消</el-button>
    <el-button icon="el-icon-delete" type="danger" plain class="confirm-delete" v-if="isDeleting" @click="clickConfirmDelete">删除</el-button>

    <!-- 点击候选人、面试官卡片弹出的表单 -->
    <el-dialog title="候选人信息" :visible.sync="intvwDialogFormVisible">
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
        <el-button @click="intvwDialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="intvwDialogFormVisible = false">确定</el-button>
      </div>
    </el-dialog>

    <!-- 点击 HR 卡片弹出的表单 -->
    <el-dialog width=85% :visible.sync="hrDialogFormVisible">
      <el-row :gutter="20">
        <el-col :span="7">
          <h3>HR 信息</h3>
          <el-form :model="form">
            <el-form-item label="姓名" :label-width="hrFormLabelWidth">
              <span v-if="editHrInfo === false" > {{ form.name }} </span>
              <el-input v-else v-model="form.name" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="email" :label-width="hrFormLabelWidth">
              <span v-if="editHrInfo === false" > {{ form.email }} </span>
              <el-input v-else v-model="form.email" autocomplete="off"></el-input>
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
export default {
  name: 'AppMain',
  data: function () {
    return {
      editHrInfo: false,
      addIntvweeDialogFormVisible: false,
      addIntvwerDialogFormVisible: false,
      intvweeNum: 11, // 从 API 请求到的 interviewee 的数量
      intvwDialogFormVisible: false, // 是否显示弹出表单
      hrDialogFormVisible: true, // 是否显示弹出表单
      form: { // 弹出表单的内容
        name: 'default',
        email: 'default@default.com',
        region: 'default'
      },
      formLabelWidth: '120px', // 弹出表单的宽度
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
      }]
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
      this.intvwDialogFormVisible = true
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
