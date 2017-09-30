import Vue from 'vue'
import Hello from '@/components/Hello'

describe('Hello.vue', () => {
  it('should render the landing page title', () => {
    const Constructor = Vue.extend(Hello)
    const vm = new Constructor().$mount()
    expect(vm.$el.querySelector('.landing h1').textContent)
      .to.equal('Hi! I\'m ProceZeus.')
  })
})
