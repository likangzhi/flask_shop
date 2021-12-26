<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品管理</el-breadcrumb-item>
      <el-breadcrumb-item>分类管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-alert
        title="注意: 只可以选择第三级的分类参数"
        type="warning"
        close-text="知道了"
        style="width: 40%"
      ></el-alert>
      <el-row>
        <el-col>
          <span>请选择商品分类: </span>
          <el-cascader
            v-model="selectkeys"
            :options="cateIdList"
            :props="{
              expandTrigger: 'hover',
              label: 'name',
              value: 'id'
            }"
            clearable
            separator=" > "
            @change="chanageSeletor"
          ></el-cascader>
        </el-col>
      </el-row>
      <el-row>
        <el-col>
          <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="静态参数" name="static">
              <el-button
                type="primary"
                size="mini"
                @click="addDialogVisible = true"
                :disabled="isBtnDisable"
                >增加参数</el-button
              >
              <el-table :data="staticAttr">
                <el-table-column type="expand">
                  <template slot-scope="scope">
                    <el-tag>{{ scope.row.val }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column type="index"></el-table-column>
                <el-table-column label="参数名称" prop="name"></el-table-column>
                <el-table-column label="操作">
                  <template>
                    <el-button type="success" size="mini">编辑</el-button>
                    <el-button type="danger" size="mini">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="动态参数" name="dynamic">
              <el-button
                type="primary"
                size="mini"
                @click="addDialogVisible = true"
                :disabled="isBtnDisable"
                >增加参数</el-button
              >
              <el-table :data="dynamicAttr">
                <el-table-column type="expand">
                  <template slot-scope="scope">
                    <el-tag
                      @click="removeTag(scope.row, i)"
                      closable
                      v-for="(v, i) in scope.row.val"
                      :key="i"
                      >{{ v }}</el-tag
                    >
                    <el-input
                      class="input-new-tag"
                      v-if="scope.row.inputVisible"
                      v-model="scope.row.inputValue"
                      ref="saveTagInput"
                      size="small"
                      @keyup.enter.native="handleInputConfirm(scope.row)"
                      @blur="handleInputConfirm(scope.row)"
                      style="width: 15%"
                    >
                    </el-input>
                    <el-button
                      v-else
                      size="small"
                      @click="showInput(scope.row)"
                      class="button-new-tag"
                      >+ New Tag</el-button
                    >
                  </template>
                </el-table-column>
                <el-table-column type="index"></el-table-column>
                <el-table-column label="参数名称" prop="name"></el-table-column>
                <el-table-column label="操作">
                  <template>
                    <el-button type="success" size="mini">编辑</el-button>
                    <el-button type="danger" size="mini">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
    </el-card>
    <el-dialog
      :title="'添加参数' + titleText"
      :visible.sync="addDialogVisible"
      width="30%"
      @close="addDialogClose"
    >
      <el-form
        :model="addForm"
        :rules="addFormRules"
        ref="addFormRef"
        label-width="80px"
      >
        <el-form-item :label="titleText" prop="name">
          <el-input v-model="addForm.name"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addAttr">确定</el-button>
          <el-button @click="addDialogVisible = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      cateIdList: [],
      selectkeys: [],
      activeName: 'static',
      dynamicAttr: [],
      staticAttr: [],
      staticFlag: false,
      dynamicFlag: false,
      addDialogVisible: false,
      addForm: {
        name: ''
      },
      addFormRules: {
        name: [{ required: true, message: '请填写参数', tigger: 'blur' }]
      },
      inputVisible: false,
      inputValue: ''
    }
  },
  computed: {
    titleText() {
      if (this.activeName === 'static') return '静态参数'
      else return '动态参数'
    },
    isBtnDisable() {
      if (this.selectkeys.length < 3) {
        return true
      } else {
        return false
      }
    }
  },
  created() {
    this.getCateIdList()
  },
  methods: {
    async getCateIdList() {
      const { data: resp } = await this.$axios.get('/category_list')
      this.cateIdList = resp.data.data
    },
    chanageSeletor() {
      //   console.log(this.selectkeys)
      this.staticFlag = true
      this.dynamicFlag = true
      if (this.selectkeys.length < 3) {
        this.staticAttr = []
        this.dynamicAttr = []
        return
      }
      this.getAttribute()
    },
    handleClick() {
      //   console.log(this.selectkeys[2])
      if (!this.staticFlag && this.activeName === 'static') return
      if (!this.dynamicFlag && this.activeName === 'dynamic') return
      //   console.log(this.activeName)
      if (this.selectkeys.length < 3) return
      this.getAttribute()
    },
    async getAttribute() {
      const { data: resp } = await this.$axios.get('category/attr_list', {
        params: { cid: this.selectkeys[2], _type: this.activeName }
      })
      if (resp.status !== 200) return this.$msg.error(resp.msg)
      if (this.activeName === 'static') {
        this.staticAttr = resp.data
        this.staticFlag = false
      } else {
        resp.data.forEach((item) => {
          item.val = item.val ? item.val.split(',') : []
          item.inputVisible = false
          item.inputValue = ''
        })
        this.dynamicAttr = resp.data
        this.dynamicFlag = false
      }
    },
    addDialogClose() {
      this.$refs.addFormRef.resetFields()
    },
    addAttr() {
      this.$refs.addFormRef.validate(async (valid) => {
        if (!valid) return
        const { data: resp } = await this.$axios.post(
          '/category/attribute',
          this.$qs.stringify({
            cid: this.selectkeys[2],
            _type: this.activeName,
            name: this.addForm.name
          })
        )
        if (resp.status !== 200) return this.$msg.error(resp.msg)
        this.getAttribute()
        this.addDialogVisible = false
        return this.$msg.success(resp.msg)
      })
    },
    showInput(row) {
      row.inputVisible = true
      this.$nextTick((_) => {
        this.$refs.saveTagInput.$refs.input.focus()
      })
    },
    handleInputConfirm(row) {
      if (row.inputValue.trim().length === 0) {
        row.inputVisible = false
        row.inputValue = ''
      } else {
        row.val.push(row.inputValue.trim())
        row.inputVisible = false
        row.inputValue = ''
        this.saveAttr(row)
      }
    },
    async saveAttr(row) {
      const { data: resp } = await this.$axios.put(
        '/category/attribute',
        this.$qs.stringify({
          cid: row.cid,
          id: row.id,
          name: row.name,
          val: row.val.join(',')
        })
      )
      if (resp.status !== 200) return this.$msg.error(resp.msg)
      return this.$msg.success(resp.msg)
    },
    removeTag(row, i) {
      row.val.splice(i, 1)
      this.saveAttr(row)
    }
  }
}
</script>

<style>
.el-tab-pane {
  color: slategray;
}
.el-tabs {
  margin-top: 5px;
}
.el-cascader {
  width: 300px;
  margin-top: 10px;
}
.el-tag {
  margin: 5px;
  font-size: 30px;
}
</style>
