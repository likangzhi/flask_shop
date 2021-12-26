<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <div>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input placeholder="请输入用户名" v-model="queryInfo.name">
              <el-button
                slot="append"
                icon="el-icon-search"
                @click="searchUser"
              ></el-button>
            </el-input>
          </el-col>
          <el-col :span="2">
            <el-button
              icon="el-icon-zoom-in"
              type="primary"
              @click="addDialogVisible = true"
              >新增用户</el-button
            >
          </el-col>
        </el-row>
        <el-row>
          <el-col>
            <el-table :data="userList" border style="width: 100%">
              <el-table-column type="index"></el-table-column>
              <el-table-column prop="id" label="ID"></el-table-column>
              <el-table-column prop="name" label="用户名"></el-table-column>
              <el-table-column prop="nick_name" label="昵称"></el-table-column>
              <el-table-column prop="email" label="邮箱"></el-table-column>
              <el-table-column prop="phone" label="电话"></el-table-column>
              <el-table-column
                prop="role_name"
                label="角色名称"
              ></el-table-column>
              <el-table-column label="操作" width="200px">
                <template slot-scope="scope">
                  <el-button
                    icon="el-icon-edit"
                    circle
                    type="primary"
                    @click="save_edit(scope.row)"
                  ></el-button>
                  <el-button
                    icon="el-icon-refresh"
                    circle
                    type="info"
                    @click="show_reset(scope.row)"
                  ></el-button>
                  <el-button
                    icon="el-icon-delete"
                    circle
                    type="danger"
                    @click="show_del(scope.row)"
                  ></el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="queryInfo.pnum"
          :page-sizes="[1, 2, 5, 10]"
          :page-size="queryInfo.psize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        >
        </el-pagination>
      </div>
    </el-card>
    <!-- <el-button type="text" @click="addDialogVisible = true">点击打开 Dialog</el-button> -->
    <el-dialog
      title="新增用户"
      :visible.sync="addDialogVisible"
      width="30%"
      :before-close="addFormClose"
    >
      <el-form :model="addForm" ref="addRormRef" :rules="addFormRules">
        <el-form-item label="用户名" prop="name">
          <el-input v-model="addForm.name"></el-input>
        </el-form-item>
        <el-form-item label="昵称" prop="nick_name">
          <el-input v-model="addForm.nick_name"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="pwd">
          <el-input v-model="addForm.pwd"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="real_pwd">
          <el-input v-model="addForm.real_pwd"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="addForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="addForm.email"></el-input>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="addForm.role_name" placeholder="请选择角色">
            <el-option
              :label="r.name"
              :value="r.id"
              v-for="r in Roles"
              :key="r.id"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addFormClose">取 消</el-button>
        <el-button type="primary" @click="addUser">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="编辑用户"
      :visible.sync="editDialogVisible"
      width="30%"
      :before-close="editFormClose"
    >
      <el-form :model="editForm" ref="editRormRef" :rules="editFormRules">
        <el-form-item label="用户名" prop="name">
          <el-input v-model="editForm.name" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="昵称" prop="nick_name">
          <el-input v-model="editForm.nick_name" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="editForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editForm.email"></el-input>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="editForm.role_name" placeholder="请选择角色">
            <el-option
              :label="r.name"
              :value="r.id"
              v-for="r in Roles"
              :key="r.id"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editFormClose">取 消</el-button>
        <el-button type="primary" @click="editUser">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="删除用户" :visible.sync="DelDialogVisible" width="30%">
      <span
        ><h3>
          确认删除用户名为{{ DelName }}昵称为{{ DelNickName }}的用户嘛
        </h3></span
      >
      <span slot="footer" class="dialog-footer">
        <el-button @click="DelDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="DelUser">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="重置密码" :visible.sync="ReDialogVisible" width="30%">
      <span
        ><h3>
          确认重置用户名为{{ ReName }}昵称为{{ ReNickName }}的密码嘛
        </h3></span
      >
      <span slot="footer" class="dialog-footer">
        <el-button @click="ReDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="ReUser">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
export default {
  data() {
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.addForm.real_pwd) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    const validatePhone = (rule, value, callback) => {
      const phoneReg = /^1[0-9]{10}$/
      if (phoneReg.test(value)) {
        return callback()
      }
      return callback(new Error('请输入有效手机号码!'))
    }
    const validateEmail = (rule, value, callback) => {
      const phoneEmail =
        /^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$/
      if (phoneEmail.test(value)) {
        return callback()
      }
      return callback(new Error('请输入有效邮箱!'))
    }
    return {
      userList: [],
      queryInfo: {
        name: '',
        pnum: 1,
        psize: 2
      },
      total: 0,
      addDialogVisible: false,
      editDialogVisible: false,
      DelDialogVisible: false,
      ReDialogVisible: false,
      addForm: {},
      editForm: {},
      DelName: {},
      DelNickName: {},
      DelId: 0,
      ReId: 0,
      Roles: [],
      ReName: {},
      ReNickName: {},
      addFormRules: {
        name: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 2, max: 6, message: '长度在 2 到 6 个字符', trigger: 'blur' }
        ],
        nick_name: [
          { required: true, message: '请输入昵称', trigger: 'blur' },
          { min: 2, max: 6, message: '长度在 2 到 6 个字符', trigger: 'blur' }
        ],
        pwd: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 2, max: 6, message: '长度在 2 到 6 个字符', trigger: 'blur' }
        ],
        real_pwd: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { validator: validatePass2, trigger: 'blur' }
        ],
        phone: [{ validator: validatePhone, trigger: 'blur' }],
        email: [{ validator: validateEmail, trigger: 'blur' }]
      },
      editFormRules: {
        phone: [{ validator: validatePhone, trigger: 'blur' }],
        email: [{ validator: validateEmail, trigger: 'blur' }]
      }
    }
  },
  created() {
    this.getUserList()
    this.getRole()
  },
  methods: {
    async getUserList() {
      const { data: res } = await this.$axios.get('/user/user_list', {
        params: this.queryInfo
      })
      if (res.status !== 200) return this.$msg.error(res.msg)
      this.total = res.data.totalPage
      this.userList = res.data.users
    },
    handleSizeChange(val) {
      this.queryInfo.psize = val
      this.getUserList()
    },
    handleCurrentChange(val) {
      this.queryInfo.pnum = val
      this.getUserList()
    },
    searchUser() {
      this.queryInfo.pnum = 1
      this.getUserList()
    },
    addFormClose() {
      this.$refs.addRormRef.resetFields()
      this.addDialogVisible = false
    },
    editFormClose() {
      this.$refs.editRormRef.resetFields()
      this.editDialogVisible = false
    },
    addUser() {
      this.$refs.addRormRef.validate(async (valid) => {
        if (!valid) return
        const { data: res } = await this.$axios.post(
          '/user/user',
          this.$qs.stringify(this.addForm)
        )
        if (res.status !== 200) return this.$msg.error(res.msg)
        this.$msg.success(res.msg)
        this.$refs.addRormRef.resetFields()
        this.addDialogVisible = false
        this.getUserList()
      })
    },
    async save_edit(row) {
      const { data: res } = await this.$axios.get('user/user', {
        params: { id: row.id }
      })
      // console.log(row.id)
      if (res.status !== 200) return this.$msg.error(res.msg)
      this.editForm = res.data
      this.editDialogVisible = true
    },
    editUser() {
      this.$refs.editRormRef.validate(async (valid) => {
        if (!valid) return
        const { data: res } = await this.$axios.put(
          '/user/user',
          this.$qs.stringify(this.editForm)
        )
        // console.log(res)
        if (res.status !== 200) return this.$msg.error(res.msg)
        this.$msg.success(res.msg)
        this.editDialogVisible = false
        this.getUserList()
      })
    },
    show_del(row) {
      this.DelId = row.id
      this.DelName = row.name
      this.DelNickName = row.nick_name
      this.DelDialogVisible = true
    },
    async DelUser() {
      const { data: res } = await this.$axios.delete('/user/user', {
        data: { id: this.DelId }
      })
      if (res.status !== 200) return this.$msg.error(res.msg)
      this.$msg.success(res.msg)
      this.DelDialogVisible = false
      this.getUserList()
    },
    show_reset(row) {
      this.ReId = row.id
      this.ReName = row.name
      this.ReNickName = row.nick_name
      this.ReDialogVisible = true
    },
    async ReUser() {
      const { data: res } = await this.$axios.get('/user/reset', {
        params: { id: this.ReId }
      })
      if (res.status !== 200) return this.$msg.error(res.msg)
      this.$msg.success(res.msg)
      this.ReDialogVisible = false
    },
    async getRole() {
      const { data: res } = await this.$axios.get('/role')
      if (res.status !== 200) return this.$msg.error(res.msg)
      this.Roles = res.data
      // console.log(res.data)
    }
  }
}
</script>
<style scoped lang='less'>
.el-table {
  margin-top: 10px;
}
</style>
