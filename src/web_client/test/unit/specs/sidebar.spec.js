/*
import dependencies
*/

import Vue from 'vue'
import Sidebar from '@/components/Sidebar'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import VueLocalStorage from 'vue-localstorage'
import VueRouter from 'vue-router'
import { EventBus } from '@/components/EventBus.js'

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
        EventBus.$emit('hideSidebar', {
            progress: 50
        })
        expect(vm.progress).to.equal(50)
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
                    curves: [],
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
                    curves: [{
                        name: {}
                    }],
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

})
