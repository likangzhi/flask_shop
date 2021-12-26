import Vue from 'vue'
import {
  Button,
  Form,
  FormItem,
  Input,
  Message,
  Alert,
  Tabs,
  TabPane,
  Option,
  Cascader,
  Tree,
  Select,
  Dialog,
  Tag,
  Pagination,
  Table,
  TableColumn,
  Col,
  Row,
  Card,
  Container,
  Aside,
  Main,
  Header,
  Submenu,
  MenuItem,
  MenuItemGroup,
  Menu,
  Breadcrumb,
  BreadcrumbItem,
  MessageBox,
  Step,
  Steps,
  CheckboxGroup,
  Checkbox,
  Upload,
  Timeline,
  TimelineItem
} from 'element-ui'
import TreeTable from 'vue-table-with-tree-grid'
import VueQuillEditor from 'vue-quill-editor'

import 'quill/dist/quill.core.css' // import styles
import 'quill/dist/quill.snow.css' // for snow theme
import 'quill/dist/quill.bubble.css' // for bubble theme
Vue.use(Button)
Vue.use(Form)
Vue.use(Alert)
Vue.use(FormItem)
Vue.use(TabPane)
Vue.use(Input)
Vue.use(Tabs)
Vue.use(Container)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Header)
Vue.use(Submenu)
Vue.use(MenuItem)
Vue.use(MenuItemGroup)
Vue.use(Menu)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Card)
Vue.use(Row)
Vue.use(Col)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Pagination)
Vue.use(Dialog)
Vue.use(Tag)
Vue.use(Select)
Vue.use(Option)
Vue.use(Tree)
Vue.use(Cascader)
Vue.use(Step)
Vue.use(Steps)
Vue.use(Checkbox)
Vue.use(CheckboxGroup)
Vue.use(Upload)
Vue.use(Timeline)
Vue.use(TimelineItem)
Vue.component('tree-table', TreeTable)
Vue.prototype.$msg = Message
Vue.prototype.$confirm = MessageBox.confirm
Vue.use(VueQuillEditor /* { default global options } */)
