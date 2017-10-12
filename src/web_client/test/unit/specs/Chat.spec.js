import Vue from 'vue'
import Chat from '@/components/Chat'

describe('Chat.vue', () => {

  it('should render the landing page title', () => {
    const Constructor = Vue.extend(Chat)
    const vm = new Constructor().$mount()
    expect(vm.$el.querySelector('.landing h1').textContent)
      .to.equal('Hi! I\'m ProceZeus.')
  })


})
