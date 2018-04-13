/*
import dependencies
*/

import Vue from 'vue'
import Chat from '@/components/Chat'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import VueLocalStorage from 'vue-localstorage'
import VueRouter from 'vue-router'

/*
inject dependencies
*/

Vue.use(ElementUI)
Vue.use(VueLocalStorage)
Vue.use(VueResource)
Vue.use(VueRouter)

/*
test
*/

describe('Chat.vue', () => {

  it('should resume chat session if conversation id exists', () => {
    Vue.localStorage.set('zeusId', 1)
    const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    promiseCall.resolves({
      body: {
        messages: [
          {
            text: 'some|where|over|the|rainbow'
          }
        ],
        fact_entities: ['mock_fact1'],
        name: 'Bruce'
      }
    })
    const spy = sinon.spy(Chat.methods, 'configChat')
    const vm = new Vue(Chat).$mount()
    expect(spy.called).to.be.true
    Chat.methods.configChat.restore()
    Vue.localStorage.remove('zeusId')
    Vue.http.get.restore()
  })

  it('should fail to resume chat session', () => {
    Vue.localStorage.set('zeusId', 1)
    const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    promiseCall.rejects()
    const spy = sinon.spy(Chat.methods, 'configChat')
    const vm = new Vue(Chat).$mount()
    expect(spy.called).to.be.false
    Chat.methods.configChat.restore()
    Vue.localStorage.remove('zeusId')
    Vue.http.get.restore()
  })

  it('should init new chat session if conversation id doesn\'t exist', () => {
    const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    promiseCall.resolves({
      body: {
        conversation_id: 1
      }
    })
    const spy = sinon.spy(Chat.methods, 'sendUserMessage')
    const vm = new Vue(Chat).$mount()
    expect(Vue.localStorage.get('zeusId')).to.be.equal('1')
    expect(spy.called).to.be.true
    Chat.methods.sendUserMessage.restore()
    Vue.http.post.restore()
    Vue.localStorage.remove('zeusId')
  })

  it('should fail to init new session', () => {
    const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    promiseCall.rejects()
    const spy = sinon.spy(Chat.methods, 'sendUserMessage')
    const vm = new Vue(Chat).$mount()
    expect(spy.called).to.be.false
    expect(vm.connectionError).to.be.true
    Chat.methods.sendUserMessage.restore()
    Vue.http.post.restore()
    Vue.localStorage.remove('zeusId')
  })

  it('should successfully retrive chat history and config chat', () => {
    Vue.localStorage.set('zeusId', 1)
    const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    promiseCall.resolves({
      body: {
        messages: [
          {
            text: 'some|where|over|the|rainbow'
          }
        ],
        fact_entities: ['mock_fact1'],
        name: 'Bruce'
      }
    })
    const clock = sinon.useFakeTimers()
    const spy = sinon.spy(Chat.methods, 'configChat')
    const vm = new Vue(Chat).$mount()
    clock.tick(1500)
    expect(spy.called).to.be.true
    expect(vm.zeus.input).to.equal('rainbow')
    Chat.methods.configChat.restore()
    Vue.http.get.restore()
    Vue.localStorage.remove('zeusId')
    clock.restore()
  })

  it('should successfully send message and config chat', () => {
    const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    promiseCall.resolves({
      body: {
        message: 'mock',
        enforce_possible_answer: true
      }
    })
    const clock = sinon.useFakeTimers()
    const spy = sinon.spy(Chat.methods, 'configChat')
    const vm = new Vue(Chat).$mount()
    vm.user.input = 'mock'
    vm.zeus.input = 'mock'
    vm.sendUserMessage()
    clock.tick(1500)
    expect(spy.called).to.be.true
    Chat.methods.configChat.restore()
    Vue.http.post.restore()
    clock.restore()
  })

  it('should successfully send message and config chat', () => {
    const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    promiseCall.resolves({
      body: {
        message: 'mock|split',
        enforce_possible_answer: true,
        possible_answers: '["yes"]'
      }
    })
    const clock = sinon.useFakeTimers()
    const spy = sinon.spy(Chat.methods, 'configChat')
    const vm = new Vue(Chat).$mount()
    vm.user.input = 'mock'
    vm.zeus.input = 'mock'
    vm.sendUserMessage()
    clock.tick(1500)
    expect(spy.called).to.be.true
    Chat.methods.configChat.restore()
    Vue.http.post.restore()
    clock.restore()
  })

  it('should successfully send message and config chat', () => {
    const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    promiseCall.resolves({
      body: {
        message: 'mock|split',
        enforce_possible_answer: true,
        possible_answers: 'null'
      }
    })
    const clock = sinon.useFakeTimers()
    const spy = sinon.spy(Chat.methods, 'configChat')
    const vm = new Vue(Chat).$mount()
    vm.user.input = 'mock'
    vm.zeus.input = 'mock'
    vm.sendUserMessage()
    clock.tick(1500)
    expect(spy.called).to.be.true
    Chat.methods.configChat.restore()
    Vue.http.post.restore()
    clock.restore()
  })

  it('should successfully send user feedback', () => {
    const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    promiseCall.resolves({})
    const vm = new Vue(Chat).$mount()
    vm.sendFeedback(true)
    expect(vm.promptFeedback).to.be.false
    Vue.http.post.restore()
  })

  it('should handle the failure of sending user feedback ', () => {
    const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    const vm = new Vue(Chat).$mount()
    vm.sendFeedback()
    promiseCall.rejects()
    expect(vm.connectionError).to.be.true
    Vue.http.post.restore()
  })

  it('should successfully remove resolved fact', () => {
    const promiseCall = sinon.stub(Vue.http, 'delete').returnsPromise()
    promiseCall.resolves({})
    const vm = new Vue(Chat).$mount()
    vm.removeFact(1)
    expect(vm.connectionError).to.be.false
    Vue.http.delete.restore()
  })

  it('should fail to remove resolved fact', () => {
    const promiseCall = sinon.stub(Vue.http, 'delete').returnsPromise()
    promiseCall.rejects({})
    const vm = new Vue(Chat).$mount()
    vm.removeFact(1)
    expect(vm.connectionError).to.be.true
    Vue.http.delete.restore()
  })

  it('should successfully get resolved fact', () => {
    Vue.localStorage.set('zeusId', 1)
    const promiseDeleteCall = sinon.stub(Vue.http, 'delete').returnsPromise()
    const promiseGetCall = sinon.stub(Vue.http, 'get').returnsPromise()
    promiseDeleteCall.resolves({})
    promiseGetCall.resolves({})
    const vm = new Vue(Chat).$mount()
    vm.removeFact(1)
    Vue.http.delete.restore()
    Vue.http.get.restore()
    Vue.localStorage.remove('zeusId')
  })

  it('should successfully update sidebar', () => {
    const vm = new Vue(Chat).$mount()
    vm.updateSidebarEvent(100)
    expect(Vue.localStorage.get('progress')).to.equal('100') //localstorage convert everything to string
    Vue.localStorage.remove('progress')
  })

})
