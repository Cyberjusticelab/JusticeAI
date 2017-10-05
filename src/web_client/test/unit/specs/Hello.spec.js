import Vue from 'vue'
import Hello from '@/components/Hello'

describe('Hello.vue', () => {
  it('should render the landing page title', () => {
    const Constructor = Vue.extend(Hello)
    const vm = new Constructor().$mount()
    expect(vm.$el.querySelector('.landing h1').textContent)
      .to.equal('Hi! I\'m ProceZeus.')
  })

  it('should have default component data', () => {
    const Constructor = Vue.extend(Hello)
    const vm = new Constructor()

    expect(vm.landingPageTitle).to.be.a('string')
    expect(vm.landingPageMessage).to.be.a('string')
    expect(vm.landingPagePrompt).to.be.a('string')
    expect(vm.botName).to.be.a('string')
    expect(vm.startChat).to.equal(false)
    expect(vm.botMessageLog).to.be.a('array')
    expect(vm.userMessageLog).to.be.a('array')
  })

  it('openChatBot should push a default message into the bot message queue', () => {
    const Constructor = Vue.extend(Hello)
    const vm = new Constructor().$mount()

    vm.username = 'Bob'
    expect(vm.startChat).to.equal(false)
    expect(vm.botMessageLog.length).to.equal(0)

    vm.openChatBot()

    expect(vm.startChat).to.equal(true)
    expect(vm.botMessageLog.length).to.equal(1)
  })

  it('openChatBot should push a default message into the bot message queue', () => {
    const Constructor = Vue.extend(Hello)
    const vm = new Constructor().$mount()

    vm.username = 'Bob'
    expect(vm.startChat).to.equal(false)
    expect(vm.botMessageLog.length).to.equal(0)

    vm.openChatBot()

    expect(vm.startChat).to.equal(true)
    expect(vm.botMessageLog.length).to.equal(1)
  })

  it('openChatBot should not push a default message into the bot message queue if the provided username is empty', () => {
    const Constructor = Vue.extend(Hello)
    const vm = new Constructor().$mount()

    vm.username = '   '
    expect(vm.startChat).to.equal(false)
    expect(vm.botMessageLog.length).to.equal(0)

    vm.openChatBot()

    expect(vm.startChat).to.equal(false)
    expect(vm.botMessageLog.length).to.equal(0)
  })

  it('submitUserText should add a message to the user and bot message queues and clear the text area', () => {
    const Constructor = Vue.extend(Hello)
    const vm = new Constructor().$mount()

    vm.userTextInput = 'hotdogs'
    expect(vm.userTextInput).to.equal('hotdogs')
    expect(vm.botMessageLog.length).to.equal(0)
    expect(vm.userMessageLog.length).to.equal(0)

    vm.submitUserText()

    expect(vm.userTextInput).to.equal('')
    expect(vm.botMessageLog.length).to.equal(1)
    expect(vm.userMessageLog.length).to.equal(1)
  })

  it('submitUserText should not add a message to the user or bot message queues and not clear the text area', () => {
    const Constructor = Vue.extend(Hello)
    const vm = new Constructor().$mount()

    vm.userTextInput = '   '
    expect(vm.userTextInput).to.equal('   ')
    expect(vm.botMessageLog.length).to.equal(0)
    expect(vm.userMessageLog.length).to.equal(0)

    vm.submitUserText()

    expect(vm.userTextInput).to.equal('   ')
    expect(vm.botMessageLog.length).to.equal(0)
    expect(vm.userMessageLog.length).to.equal(0)
  })
})
