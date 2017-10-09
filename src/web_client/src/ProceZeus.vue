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
  background: #516395;
  background: -webkit-linear-gradient(to top, #614385, #516395);
  background: linear-gradient(to top, #614385, #516395);
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #efefef;
}
</style>
