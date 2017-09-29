import Vue from 'vue'
import Hello from '@/components/Hello'

describe('Hello.vue', () => {
  it('should render correct contents', () => {
    const Constructor = Vue.extend(Hello)
    const vm = new Constructor().$mount()
    expect(vm.$el.querySelector('.welcome h1').textContent)
      .to.equal('Welcome to JusticeAI! To get started, please tell us what you’d like to do.')
  })
})
