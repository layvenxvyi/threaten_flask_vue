import Vue from 'vue'
import Router from 'vue-router'
import main from '../components/main'
import query_threaten from '../components/query_threaten'
import hello from '../components/hello'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'main',
      component: main
    },
    {
    path: '/query_threaten',
    name: 'query_threaten',
    component: query_threaten,
    children:[
      {
     path:'/hello',
     name:'hello',
     component:hello
    }
      ]
    }
  ]
})

