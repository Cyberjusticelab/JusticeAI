<style lang="scss" scoped>
@import "../theme/Dashboard"
</style>

<template>
    <div id="dashboard-component">
        <b-container fluid>
            <b-row>
                <b-col md="3">
                    <sidebar></sidebar>
                </b-col>
                <b-col md="9">
                    <chat></chat>
                </b-col>
            </b-row>
        </b-container>
    </div>
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
