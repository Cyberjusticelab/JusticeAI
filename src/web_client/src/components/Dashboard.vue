<style lang="scss" scoped>
@import "../theme/Dashboard"
</style>

<template>
    <transition name="fade">
        <div id="dashboard-component">
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
export default {
    components: {
        Chat, Sidebar
    }
}
</script>
