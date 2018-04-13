import Vue from 'vue'
import Router from 'vue-router'
import Beta from '@/components/Beta'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Beta',
      component: Beta,
      props(route) {
        return {
          langQuery: route.query.lang
        }
      }
    }
  ]
})
