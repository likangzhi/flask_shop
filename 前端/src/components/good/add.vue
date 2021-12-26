<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品管理</el-breadcrumb-item>
      <el-breadcrumb-item>增加商品</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-alert
        title="增加商品信息"
        type="info"
        center
        show-icon
        style="margin-bottom: 10px"
      ></el-alert>
      <el-steps :active="active - 0" finish-status="success" align-center>
        <el-step title="基本信息"></el-step>
        <el-step title="商品静态参数"></el-step>
        <el-step title="商品动态参数"></el-step>
        <el-step title="添加图片"></el-step>
        <el-step title="添加内容"></el-step>
        <el-step title="完成"></el-step>
      </el-steps>
      <el-form :model="addForm" ref="addFormRef" :rules="addFormRules">
        <el-tabs
          v-model="active"
          :tab-position="'left'"
          :before-leave="beforeLeave"
        >
          <el-tab-pane label="基本信息" name="0">
            <el-form-item label="商品名称" label-width="80px" prop="name">
              <el-input v-model="addForm.name"></el-input>
            </el-form-item>
            <el-form-item label="商品价格" label-width="80px" prop="price">
              <el-input v-model="addForm.price"></el-input>
            </el-form-item>
            <el-form-item label="商品数量" label-width="80px" prop="number">
              <el-input v-model="addForm.number"></el-input>
            </el-form-item>
            <el-form-item label="商品权重" label-width="80px" prop="weight">
              <el-input v-model="addForm.weight"></el-input>
            </el-form-item>
            <el-form-item label="商品分类" prop="cid">
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
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="商品静态参数" name="1">
            <el-form-item
              :label="s.name"
              v-for="s in staticList"
              :key="s.id"
              label-width="150px"
              class="el-form-item__label"
            >
              <el-input v-model="s.val"></el-input>
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="商品动态参数" name="2">
            <el-form-item
              :label="d.name"
              v-for="d in dynamicList"
              :key="d.id"
              label-width="80px"
            >
              <el-checkbox-group v-model="d.val">
                <el-checkbox
                  :label="dv"
                  v-for="(dv, i) in d.val"
                  :key="i"
                  border
                ></el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="添加图片" name="3">
            <el-upload
              class="upload-demo"
              action="http://127.0.0.1:5000/upload_img"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :on-success="handleSuccess"
              list-type="picture"
            >
              <el-button size="small" type="primary">点击上传</el-button>
            </el-upload>
          </el-tab-pane>
          <el-tab-pane label="添加内容" name="4">
            <quill-editor v-model="addForm.introduce"></quill-editor>
            <el-button
              type="primary"
              @click="addGood"
              style="margin-top: 10px; margin-right: 5%; float: right"
              >完成</el-button
            >
          </el-tab-pane>
        </el-tabs>
      </el-form>
    </el-card>
    <el-dialog title="图片预览" :visible.sync="perViewVisible" width="40%">
      <img :src="perviewUrl" class="perImg" />
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      active: '0',
      addForm: {
        name: '',
        price: 0,
        number: 0,
        weight: 0,
        cid_one: 0,
        cid_two: 0,
        cid_three: 0,
        pics: [],
        introduce: '',
        attr_static: [],
        attr_dynamic: []
      },
      addFormRules: {
        name: [{ required: true, message: '请填写商品名称', tigger: 'blur' }],
        price: [{ required: true, message: '请填写商品价格', tigger: 'blur' }],
        number: [{ required: true, message: '请填写商品数量', tigger: 'blur' }],
        weight: [{ required: true, message: '请填写商品权重', tigger: 'blur' }]
      },
      selectkeys: [],
      cateIdList: [],
      staticList: [],
      dynamicList: [],
      perviewUrl: '',
      perViewVisible: false
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
      if (this.selectkeys.length < 3) return
      this.addForm.cid_one = this.selectkeys[0]
      this.addForm.cid_two = this.selectkeys[1]
      this.addForm.cid_three = this.selectkeys[2]
    },
    beforeLeave(activeName, oldActiveName) {
      if (this.selectkeys.length < 3) {
        this.$msg.error('请选择商品分类')
        return false
      }
      if (activeName === '1') this.getAttr('static')
      if (activeName === '2') this.getAttr('dynamic')
    },
    async getAttr(_type) {
      const { data: resp } = await this.$axios.get('category/attr_list', {
        params: { cid: this.selectkeys[2], _type: _type }
      })
      if (resp.status !== 200) return this.$msg.error(resp.msg)
      if (_type === 'static') {
        this.staticList = resp.data
      } else {
        resp.data.forEach((item) => {
          item.val = item.val ? item.val.split(',') : []
        })
        this.dynamicList = resp.data
      }
    },
    handleSuccess(resp) {
      this.addForm.pics.push(resp.data.path)
      this.$msg.success(resp.msg)
    },
    handleRemove(file) {
      const i = this.addForm.pics.findIndex(
        (x) => x === file.response.data.path
      )
      this.addForm.pics.splice(i, 1)
      this.$msg.success('删除图片成功')
    },
    handlePreview(file) {
      this.perViewVisible = true
      this.perviewUrl = file.response.data.url
    },
    addGood() {
      this.$refs.addFormRef.validate(async (valid) => {
        if (!valid) {
          this.$msg.error('请填写必要的参数！！')
        } else {
          const staticLict = []
          this.staticList.forEach((attr) => {
            staticLict.push({ id: attr.id, val: attr.val })
          })
          this.addForm.attr_static = JSON.stringify(staticLict)
          const dynamicLict = []
          this.dynamicList.forEach((attr) => {
            dynamicLict.push({ id: attr.id, val: attr.val.join(',') })
          })
          this.addForm.attr_dynamic = JSON.stringify(dynamicLict)
          this.addForm.pics = JSON.stringify(this.addForm.pics)
          this.saveGoods()
        }
      })
    },
    async saveGoods() {
      const { data: resp } = await this.$axios.post(
        '/goods',
        this.$qs.stringify(this.addForm)
      )
      if (resp.status !== 200) return this.$msg.error(resp.msg)
      this.$msg.success(resp.msg)
      this.$router.push('/goods_list')
    }
  }
}
</script>

<style>
.el-tabs {
  margin-top: 10px;
}
.el-checkbox {
  margin: 0 15px 0 0 !important;
}
.perImg {
  width: 100%;
}
</style>
