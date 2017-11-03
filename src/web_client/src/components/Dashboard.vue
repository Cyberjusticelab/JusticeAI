<style lang="scss" scoped>
@import "../theme/Dashboard"
</style>

<template>
    <div id="dashboard-component">
        <el-container>
            <el-row>
                <el-col :sm="5" >
                    <sidebar></sidebar>
                </el-col>
                <el-col :sm="19">
                    <chat></chat>
                </el-col>
            </el-row>
        </el-container>
    </div>
</template>

<script>
import Chat from './Chat'
import Sidebar from './Sidebar'
export default {
    components: {
        Chat, Sidebar
    },
    created () {
        this.$localStorage.set('username', 'Bruce Lee')
    }
}
</script>
