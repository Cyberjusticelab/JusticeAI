<style lang="scss" scoped>
@import "../theme/Dashboard"
</style>

<template>
    <transition name="fade">
        <div id="dashboard-component" v-loading="initLoading" element-loading-text="Let's Talk!" element-loading-spinner="el-icon-loading" fullscreen="true">
            <el-container>
                <sidebar></sidebar>
                <chat></chat>
            </el-container>
        </div>
    </transition>
</template>

<script>
import Chat from './Chat'
import Sidebar from './Sidebar'
import { EventBus } from './EventBus.js'
export default {
    components: {
        Chat, Sidebar
    },
    data () {
        return {
            initLoading: true
        }
    },
    created () {
        EventBus.$on('initLoading', (isLoading) => {
            this.initLoading = isLoading
        })
    }
}
</script>
