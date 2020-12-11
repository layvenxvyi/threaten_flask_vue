<style scoped>
    @import '../assets/styles/common.css';
</style>
<template>
<div class="layout-wrapper">
    <div class="layout-side" :class="{'layout-side-extend': !isCollapse}" style="color:rgb(191,203,217);background-color:rgb(48,65,86);">
        <div class="layout-logo" v-if="!isCollapse" style="color: #fff;font-size: 20px;">威胁情报</div>
        <div class="layout-logo" v-else>...</div>
        <el-menu :collapse="isCollapse" :default-active="current_index" @select="handleSelect" unique-opened router>
            <template v-for="item in menus">
                <el-submenu v-if="item.subs" :index="item.key">
                    <template slot="title">
                        <i :class="item.icon"></i>
                        <span slot="title">{{ item.desc }}</span>
                    </template>
                    <el-menu-item :index="sub.key" v-for="sub in item.subs" key="sub.key">{{ sub.desc }}</el-menu-item>
                </el-submenu>
                <el-menu-item v-else :index="item.key">
                    <i :class="item.icon"></i>
                    <span slot="title">{{ item.desc }}</span>
                </el-menu-item>
            </template>
        </el-menu>
    </div>
    <div class="layout-main">
        <div class="layout-header">
            <div class="i-button">
                <i class="fa fa-sign-out" ></i>
            </div>
            <div class="i-button">
                <span class="el-dropdown-link "><i class="fa fa-user"></i> 无需登录</span>    
            </div>
            <div style="flex-grow: 1"></div>
            <div class="i-button">
                <i class="fa fa-bars" @click="isCollapse = !isCollapse"></i>
            </div>
        </div>
        <div class="layout-body">
            <!-- 条件查询 -->
            <div class="app-container" style="margin-bottom: 20px;">
            <div class="filter-container">
              <el-select v-model="select_origin" placeholder="来源选择" clearable style="width: 200px" class="filter-item" @change="handleFilter">
                <el-option v-for="(value,key) in orgin_Options" :key="key" :label="value" :value="key" />
              </el-select>
              <el-select v-model="select_type" placeholder="类型选择" clearable style="width: 200px" class="filter-item" @change="handleFilter">
                <el-option v-for="(value,key) in type_Options" :key="key" :label="value" :value="key" />
              </el-select>
              <el-select  v-model="select_shotkey" multiple placeholder="关键字多选" clearable style="width: 240px" class="filter-item" @change="handleFilter">
                <el-option-group v-for="(value,key) in shotkey_Options" :key="key" :label="key" :value="key" >
                <el-option v-for="item in value" :key="item" :label="item" :value="item" />
                </el-option-group>
              </el-select>
              <!-- <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
                Search
              </el-button> -->
              <el-button type="primary" icon="el-icon-search" @click="refresh()">重置</el-button>
              <el-button  :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">导出
              </el-button>
            </div>
            </div>
            <!-- 条件查询 -->

        <!-- 表格主体内容 -->
        <el-table :data="tableData.data" stripe border v-loading="listLoading" style="width: 100%" @row-click="dealmodal"
                  :default-sort="{prop: 'time', order: 'descending'}">
            <el-table-column type="index" width="60"></el-table-column>
            <el-table-column label="标题" width="640" >
                <template scope="scope">
                    <el-icon name="name"></el-icon>
                    <span style="text-decoration:underline;cursor:pointer;" >{{ scope.row.name }}</span>
                </template>

            </el-table-column>
            <el-table-column prop="time" label="通告时间" sortable width="170"></el-table-column>
            <el-table-column prop="origin" label="来源" sortable width="100"></el-table-column>
            <el-table-column prop="shottype" label="分类" width="100"></el-table-column>
            <el-table-column label="命中关键字" width="150">
                <template slot-scope="scope">
                    <el-tag  prop="shotkey" v-if="scope.row.shotkey"> {{ scope.row.shotkey }}</el-tag>
                </template>
            </el-table-column>
            
        </el-table>
        <!-- 表格主体内容 -->

        <!--详情模态框内容-->
            <el-dialog :visible.sync="dialogVisible" :title="name" @dragDialog="handleDrag" width="70%">
                <a :href="urlhref" target="_blank">点击阅读原文</a>
                <p>{{time}}</p>
                <p>{{urldetail}}</p>
            </el-dialog>
        <!--详情内容-->

        <!--分页-->
        <div class="pagination-bar" v-if="tableData.total > 20">
            <el-pagination
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"  layout="total, prev, pager, next"
                    :total="tableData.total"
                    :page-size="20">
            </el-pagination>
        </div>
        <!--分页-->
        
            <router-view @routerChange="routerChange"></router-view>
        </div>
    </div>
</div>
</template>
<script>
import menu from '../../config/menu'
import {getDetailInfo} from '../api/auth'
export default {
    // name: 'HelloWorld',
    data() {
        return{
            dialogVisible: false,
            tableData: {},
            listLoading: false,
            currentPage: 1,
            menus: menu.menus,
            isCollapse: false,
            current_index: undefined,
            name:'',
            urlhref:'',
            urldetail:'',
            time:'',
            downloadLoading: false,
            select_origin: '',
            select_type: '',
            select_shotkey: [],
            orgin_Options: [],
            type_Options:[],
            shotkey_Options:[],
            shotkey:'',
        }
    },
    methods: {
        handleCurrentChange(val) {
            this.currentPage = val;
            this.getDatas(this.currentPage,this.select_origin,this.select_origin);
        },

        //modal查看详情
        dealmodal(row){
            this.dialogVisible=true,
            this.name=row.name,
            this.urlhref=row.urlhref,
            this.urldetail=row.urldetail,
            this.time=row.time
        },

        handleFilter() {
            //为了把shotkey写在一个参数里
            let s = [];
            for(var i = 0; i < this.select_shotkey.length; i++) {
                s.push(this.select_shotkey[i])
            };
            this.shotkey = s.join();
          this.getDatas(this.currentPage,this.select_origin,this.select_type)
        },
        //重置操作
        refresh(){
            this.getDatas(1);
            this.select_origin='',
            this.select_type='',
            this.select_shotkey=[]
        },

        //获取用户列表
        getDatas(page,select_origin,select_type) {
            // debugger
            if (!page) page = 1;
            this.listLoading = true;
            if (!select_origin) select_origin = 0;
            if (!select_type) select_type = 0;
            getDetailInfo(page,select_origin,select_type,this.shotkey).then((res) => {
                console.log(res);
                console.log(this.shotkey);
              this.tableData = res.data;
              this.listLoading = false;
              this.orgin_Options=res.data.orgin_Options;
              this.type_Options=res.data.type_Options;
              this.shotkey_Options=res.data.shotkey_Options;
              this.select_val=res.data.select_val;
            })
        },
        // 导出
        handleDownload() {
          this.downloadLoading = true
          import('../vendor/Export2Excel').then(excel => {
            const tHeader = ['标题', '通告时间', '来源', '分类', '命中关键字','原始链接','通告内容']
            const filterVal = ['name', 'time', 'origin', 'shottype', 'shotkey','urlhref','urldetail']
            const data = this.formatJson(filterVal)
            excel.export_json_to_excel({
              header: tHeader,
              data,
              filename: '威胁情报'
            })
            this.downloadLoading = false
          })
        },

        formatJson(filterVal) {
          return this.tableData.data.map(v => filterVal.map(j => {
            return v[j]
            }))
        },

        routerChange() {
            this.current_index = this.$route.path;
        },

        handleSelect(path) {
            this.current_index = path
        },

        handleDrag() {
            this.$refs.select.blur()
        },
        // this.$router.push('/threaten_query');
    },
    mounted() {
        this.getDatas(1);
    }
}
</script>