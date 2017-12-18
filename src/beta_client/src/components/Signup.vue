<template>
  <el-col :span="16" :offset="4"><Chat></Chat></el-col>
</template>

<script>
import Chat from '@/components/Chat'
export default {
  components: {
    Chat
  },
  name: 'Signup'
}
</script>