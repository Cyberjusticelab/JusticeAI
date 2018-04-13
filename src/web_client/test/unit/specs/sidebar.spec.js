/*
import dependencies
*/

import Vue from 'vue'
import Sidebar from '@/components/Sidebar'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import VueLocalStorage from 'vue-localstorage'
import VueRouter from 'vue-router'
import {EventBus} from '@/components/EventBus.js'

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

describe('Sidebar.vue', () => {

  it('should successfully listen to event', () => {
    const vm = new Vue(Sidebar).$mount()
    Vue.localStorage.set('progress', 66)
    EventBus.$emit('updateSidebar')
    expect(vm.progress).to.equal(66)
    Vue.localStorage.remove('progress')
  })

  it('should successfully listen to event', () => {
    const spy = sinon.spy(Sidebar.methods, 'view')
    const vm = new Vue(Sidebar).$mount()
    Vue.localStorage.set('progress', 100)
    EventBus.$emit('updateSidebar')
    expect(vm.progress).to.equal(100)
    expect(spy.called).to.be.true
    Vue.localStorage.remove('progress')
    Sidebar.methods.view.restore()
  })

  it('should successfully get report', () => {
    Vue.localStorage.set('zeusId', 1)
    const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    promiseCall.resolves({
      body: {
        report: {
          accuracy: '0',
          similar_case: '5',
          similar_precedents: [
            {
              precedent: 'AZ-1',
              outcomes: {
                o1: true
              },
              facts: {
                f1: true
              }
            }
          ],
          curves: {
            additional_indemnity_money: {
              mean: 1477.7728467101024,
              outcome_value: 600,
              std: 1927.8147997893939,
              variance: 3716469.9022870203
            }
          },
          data_set: '1000',
          outcomes: {
            o1: true
          }

        }
      }
    })
    const spy = sinon.spy(Sidebar.methods, 'createPrecedentTable')
    const vm = new Vue(Sidebar).$mount()
    vm.view()
    expect(spy.called).to.be.true
    Sidebar.methods.createPrecedentTable.restore()
    Vue.localStorage.remove('zeusId')
    Vue.http.get.restore()
  })

  it('should successfully get report without regressor', () => {
    Vue.localStorage.set('zeusId', 1)
    const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    promiseCall.resolves({
      body: {
        report: {
          accuracy: '0',
          similar_case: '5',
          similar_precedents: [
            {
              precedent: 'AZ-1',
              outcomes: {
                o1: true
              },
              facts: {
                f1: true
              }
            }
          ],
          curves: {},
          data_set: '1000',
          outcomes: {
            o1: true
          }

        }
      }
    })
    const spy = sinon.spy(Sidebar.methods, 'createBellCurves')
    const vm = new Vue(Sidebar).$mount()
    vm.view()
    expect(spy.called).to.be.false
    expect(vm.hasGraph).to.be.false
    Sidebar.methods.createBellCurves.restore()
    Vue.localStorage.remove('zeusId')
    Vue.http.get.restore()
  })

  it('should successfully get report', () => {
    Vue.localStorage.set('zeusId', 1)
    const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    promiseCall.resolves({
      body: {
        report: {
          accuracy: '0',
          similar_case: '5',
          similar_precedents: [
            {
              precedent: 'AZ-1',
              outcomes: {
                o1: true
              },
              facts: {
                f1: true
              }
            }
          ],
          curves: {
            additional_indemnity_money: {
              mean: 1477.7728467101024,
              outcome_value: 600,
              std: 1927.8147997893939,
              variance: 3716469.9022870203
            }
          },
          data_set: '1000',
          outcomes: {
            o1: true
          }
        }
      }
    })
    const spy = sinon.spy(Sidebar.methods, 'createPrecedentTable')
    const vm = new Vue(Sidebar).$mount()
    vm.view()
    expect(spy.called).to.be.true
    Sidebar.methods.createPrecedentTable.restore()
    Vue.localStorage.remove('zeusId')
    Vue.http.get.restore()
  })

  it('should successfully create precedent table', () => {
    Vue.localStorage.set('zeusId', 1)
    const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    promiseCall.resolves({
      body: {
        report: {
          accuracy: '0',
          similar_case: '5',
          similar_precedents: [
            {
              precedent: 'AZ-1',
              outcomes: {
                o1: true
              },
              facts: {
                f1: true
              }
            }
          ],
          curves: {
            additional_indemnity_money: {
              mean: 1477.7728467101024,
              outcome_value: 600,
              std: 1927.8147997893939,
              variance: 3716469.9022870203
            }
          },
          data_set: '1000',
          outcomes: {
            o1: true
          }
        },
        fact_entities: [
          {
            fact: {
              name: 'f1'
            },
            value: true
          }
        ]
      }
    })
    const vm = new Vue(Sidebar).$mount()
    vm.createPrecedentTable()
    expect(vm.connectionError).to.be.false
    Vue.localStorage.remove('zeusId')
    Vue.http.get.restore()
  })

  it('should fail to create precedent table', () => {
    Vue.localStorage.set('zeusId', 1)
    const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    promiseCall.rejects()
    const vm = new Vue(Sidebar).$mount()
    vm.createPrecedentTable()
    expect(vm.connectionError).to.be.true
    Vue.localStorage.remove('zeusId')
    Vue.http.get.restore()
  })

  it('should fail to get report', () => {
    Vue.localStorage.set('zeusId', 1)
    const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    promiseCall.rejects()
    const spy = sinon.spy(Sidebar.methods, 'createPrecedentTable')
    const vm = new Vue(Sidebar).$mount()
    vm.view()
    expect(spy.called).to.be.false
    Sidebar.methods.createPrecedentTable.restore()
    Vue.localStorage.remove('zeusId')
    Vue.http.get.restore()
  })

  it('should successfully submit feedback', () => {
    const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    promiseCall.resolves()
    const vm = new Vue(Sidebar).$mount()
    vm.openFeedbackModal = true
    vm.feedback = 'Hello'
    vm.submitFeedback()
    expect(vm.connectionError).to.be.false
    Vue.http.post.restore()
  })

  it('should fail to submit feedback', () => {
    const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    promiseCall.rejects()
    const vm = new Vue(Sidebar).$mount()
    vm.openFeedbackModal = true
    vm.feedback = 'Hello'
    vm.submitFeedback()
    expect(vm.connectionError).to.be.true
    Vue.http.post.restore()
  })

  it('should validate empty feedback', () => {
    const vm = new Vue(Sidebar).$mount()
    vm.openFeedbackModal = true
    vm.feedback = ''
    vm.submitFeedback()
    expect(vm.connectionError).to.be.false
  })

  it('should reset chat', () => {
    const Component = Vue.extend(Sidebar)
    const vm = new Component({
      router: new VueRouter({
        routes: [
          {
            path: '/'
          }
        ]
      })
    }).$mount()
    Vue.localStorage.set('zeusId', 1)
    Vue.localStorage.set('username', 'Bruce Wayne')
    Vue.localStorage.set('usertype', 'tenant')
    vm.resetChat()
    expect(Vue.localStorage.get('zeusId')).to.be.equal(null)
    expect(Vue.localStorage.get('username')).to.be.equal(null)
    expect(Vue.localStorage.get('usertype')).to.be.equal(null)
    Vue.localStorage.remove('zeusId')
    Vue.localStorage.remove('username')
    Vue.localStorage.remove('usertype')
  })

  it('should generate data corresponding to a vertical line', () => {
    const vm = new Vue(Sidebar).$mount()
    let data = vm._generateBellCurveVerticalData(0)
    expect(data.length == 2).to.be.true
    expect(data[0]).to.be.an('object').that.is.not.empty
    expect(data[0]).to.have.own.property('q')
    expect(data[0]).to.have.own.property('p')
    expect(data[0].p).to.equal(0)
    expect(data[1].p).to.equal(1)
  })

  it('should generate data corresponding to a normal distribution with mean and standard deviation', () => {
    const vm = new Vue(Sidebar).$mount()
    let data = vm._generateBellCurveData(0, 1)
    expect(data.length > 500).to.be.true // Expect reasonable sample size
    expect(data[0]).to.be.an('object').that.is.not.empty
    expect(data[0]).to.have.own.property('q')
    expect(data[0]).to.have.own.property('p')
    expect(data[0].p <= data[1].p).to.be.true
    expect(data[0].q <= data[1].q).to.be.true
  })
})
