import Vue from 'vue'
import Chat from '@/components/Chat'

describe('Chat.vue', () => {

    it('tests something', () => {
        const Ctor = Vue.extend(Chat)
        const vm = new Ctor().$mount()
    })

})
