import Vue from 'vue'
import Router from 'vue-router'
import Signup from '@/components/Signup'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Signup',
            component: Signup
        }
    ]
})
