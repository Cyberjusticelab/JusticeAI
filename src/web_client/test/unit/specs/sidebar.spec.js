/*
import dependencies
*/

import Vue from 'vue'
import Sidebar from '@/components/Sidebar'
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

describe('Sidebar.vue', () => {

    it('should successfully submit feedback', () => {
        const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
        promiseCall.resolves()
        const vm = new Vue(Sidebar).$mount()
        vm.openFeedbackModal = true
        vm.feedback = 'Hello'
        vm.submitFeedback()
        expect(vm.connectionError).to.be.false
        expect(vm.openFileList).to.be.false
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
        expect(vm.openFileList).to.be.false
        Vue.http.post.restore()
    })

    it('should validate empty feedback', () => {
        const vm = new Vue(Sidebar).$mount()
        vm.openFeedbackModal = true
        vm.feedback = ''
        vm.submitFeedback()
        expect(vm.connectionError).to.be.false
        expect(vm.openFileList).to.be.false
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
    })

})
