import Vue from 'vue'
import Chat from '@/components/Chat'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import VueLocalStorage from 'vue-localstorage'
Vue.use(ElementUI)
Vue.use(VueLocalStorage)
Vue.use(VueResource)

describe('Chat.vue', () => {

    it('tests something', () => {
        const Ctor = Vue.extend(Chat)
        const vm = new Ctor().$mount()
    })

})
