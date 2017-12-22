/*
import dependencies
*/

import Vue from 'vue'
import Sidebar from '@/components/Sidebar'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import VueLocalStorage from 'vue-localstorage'

/*
inject dependencies
*/

Vue.use(ElementUI)
Vue.use(VueLocalStorage)
Vue.use(VueResource)

/*
test
*/

describe('Sidebar.vue', () => {

    it('should successfully get file list', () => {
        Vue.localStorage.set('zeusId', 1)
        Vue.localStorage.set('username', 'Bruce Wayne')
    	const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    	promiseCall.resolves({
    		body: {
    			files: [1, 2, 3]
    		}
    	})
    	const vm = new Vue(Sidebar).$mount()
        vm.openFileList = false
    	vm.getFileList()
        expect(vm.uploadedFileList.length).to.be.equal(3)
        expect(vm.openFileList).to.be.true
        expect(vm.openReportList).to.be.false
        Vue.http.get.restore()
        Vue.localStorage.remove('zeusId')
    })

    it('should successfully get empty file list', () => {
        Vue.localStorage.set('zeusId', 1)
        Vue.localStorage.set('username', 'Bruce Wayne')
        const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
        promiseCall.resolves({
            body: {
                files: []
            }
        })
        const vm = new Vue(Sidebar).$mount()
        vm.openFileList = false
        vm.getFileList()
        expect(vm.uploadedFileList.length).to.be.equal(0)
        expect(vm.openFileList).to.be.false
        Vue.http.get.restore()
        Vue.localStorage.remove('zeusId')
    })

    it('should fail to get file list', () => {
        Vue.localStorage.set('zeusId', 1)
        Vue.localStorage.set('username', 'Bruce Wayne')
        const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
        promiseCall.rejects()
        const vm = new Vue(Sidebar).$mount()
        vm.openFileList = false
        vm.getFileList()
        expect(vm.connectionError).to.be.true
        Vue.http.get.restore()
        Vue.localStorage.remove('zeusId')
    })

    it('should fail to get file list', () => {
        Vue.localStorage.set('username', 'Bruce Wayne')
        const vm = new Vue(Sidebar).$mount()
        vm.openFileList = true
        vm.getFileList()
        expect(vm.openFileList).to.be.false
    })

    it('successfully submit feedback', () => {
        const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
        promiseCall.resolves({
            body: {
                success: true
            }
        })
        const vm = new Vue(Sidebar).$mount()
        vm.openFeedbackModal = true
        vm.feedback = 'Hello'
        vm.submitFeedback()
        expect(vm.connectionError).to.be.false
        expect(vm.openFileList).to.be.false
    })
    it('fail to submit feedback', () => {
        const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
        promiseCall.rejects()
        const vm = new Vue(Sidebar).$mount()
        vm.openFeedbackModal = true
        vm.feedback = 'Hello'
        vm.submitFeedback()
        expect(vm.connectionError).to.be.true
        expect(vm.openFileList).to.be.false
    })
    it('fail to do anything', () => {
        const vm = new Vue(Sidebar).$mount()
        vm.openFeedbackModal = true
        vm.feedback = ''
        vm.submitFeedback()
        expect(vm.connectionError).to.be.false
        expect(vm.openFileList).to.be.false
    })
})
