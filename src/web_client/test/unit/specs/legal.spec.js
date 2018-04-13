/*
import dependencies
*/

import Vue from 'vue'
import Legal from '@/components/Legal'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'

/*
inject dependencies
*/

Vue.use(ElementUI)
Vue.use(VueResource)

/*
test
*/

describe('Legal.vue', () => {

  it('should get EULA text', () => {
    const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    promiseCall.resolves({
      body: [
        {
          abbreviation: 'EULA',
          html: {
            mock: 'mock'
          }
        }
      ]
    })
    const vm = new Vue(Legal).$mount()
    expect(vm.eula.mock).to.be.equal('mock')
    Vue.http.get.restore()
  })

  it('should get PP text', () => {
    const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    promiseCall.resolves({
      body: [
        {
          abbreviation: 'PP',
          html: {
            mock: 'mock'
          }
        }
      ]
    })
    const vm = new Vue(Legal).$mount()
    expect(vm.pp.mock).to.be.equal('mock')
    Vue.http.get.restore()
  })

  it('should fail to get legal text', () => {
    const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    promiseCall.rejects()
    const vm = new Vue(Legal).$mount()
    expect(vm.connectionError).to.be.true
    Vue.http.get.restore()
  })

})
