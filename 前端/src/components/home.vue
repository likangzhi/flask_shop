<template>
  <el-container class="home-container">
    <el-header>
      <div>
        <img src="../assets/logo.png" />
        <span>电子后台管理系统</span>
      </div>
      <el-button type="primary" plain @click="loginout">退出</el-button>
    </el-header>
    <el-container>
      <el-aside width="200px">
        <el-menu
          :default-active="actionPath"
          class="el-menu-vertical-demo"
          unique-opened
          router
          @open="handleOpen"
          @close="handleClose"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#409EFF"
        >
          <el-submenu
            :index="item.id + ''"
            v-for="item in menuList"
            :key="item.id"
          >
            <template slot="title">
              <i :class="iconObj[item.id + ' ']"></i>
              <span>{{ item.name }}</span>
            </template>
            <el-menu-item
              :index="subItem.path"
              v-for="subItem in item.children"
              :key="subItem.id"
              @click="saveActionPath"
            >
              <i :class="iconObj[subItem.id + ' ']"></i>
              <span>{{ subItem.name }}</span>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      menuList: [],
      iconObj: {
        '2 ': 'el-icon-user',
        '3 ': 'el-icon-s-tools',
        '4 ': 'el-icon-shopping-cart-full',
        '5 ': 'el-icon-ice-cream-square',
        '6 ': 'el-icon-box',
        '21 ': 'el-icon-user',
        '31 ': 'el-icon-s-tools',
        '32 ': 'el-icon-s-tools',
        '41 ': 'el-icon-shopping-cart-full',
        '42 ': 'el-icon-shopping-cart-full',
        '43 ': 'el-icon-shopping-cart-full',
        '51 ': 'el-icon-ice-cream-square'
      },
      actionPath: ''
    }
  },
  created() {
    this.getMenuList()
    this.actionPath = window.sessionStorage.getItem('actionPath')
  },
  methods: {
    loginout() {
      window.sessionStorage.clear()
      this.$router.push('/login')
    },
    handleOpen(key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath)
    },
    async getMenuList() {
      const { data: res } = await this.$axios.get('/menu')
      // console.log(res)
      this.menuList = res.data
    },
    saveActionPath(ap) {
      // console.log(ap.index)
      window.sessionStorage.setItem('actionPath', ap.index)
      this.actionPath = ap.index
    }
  }
}
</script>

<style lang='less' scoped>
.home-container {
  height: 100%;
}
.el-header {
  display: flex;
  background-color: rgb(169, 160, 247);
  align-items: center;
  justify-content: space-between;
  font-size: 20px;
  color: cornsilk;
  img {
    height: 50px;
    width: 250px;
  }
  div {
    display: flex;
    align-items: center;
  }
}
.el-aside {
  background-color: #545c64;
}
.el-main {
  background-color: rgb(248, 246, 241);
}
</style>
