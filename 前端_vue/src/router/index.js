import Vue from 'vue'
import Router from 'vue-router'
import main from '../components/main'
import query_threaten from '../components/query_threaten'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'main',
      component: main
      // children:[
    //   {
    // 	path:'/threaten_query',
    // 	// name:'threaten_query',
    // 	component:threaten_query
    // }
      // ]
    },
    {
    path: '/query_threaten',
    name: 'query_threaten',
    component: query_threaten
    }
  ]
})

