<template>
  <div id="proceZeus">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'proceZeus'
}
</script>

<style>
html, body {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
}

#proceZeus {
  position: relative;
  min-width: 100%;
  min-height: 100%;
  text-align: center;
}
</style>
