<template>
  <div id="container">
    <img v-show="canLoad" @click="$emit('click')" id="loadButton" src="../assets/refresh_white_96x96.png"/>
    <img v-show="loading" id="loading" src="../assets/Reload-1s-200px.svg"/>
  </div>
</template>

<script>
export default {
  name: 'loadButton',
  props: ["loading", "canLoad"],
  methods: {
  },
}
</script>

<style scoped>
div {
  width: 50px;
  height: 50px;
}
#loadButton {
  position: absolute;
  width: 50px;
  height: 50px;
  transform: scale(1);
  transition: 0.1s ease;
  cursor: pointer;
}
#loadButton path {
  fill: #FF0016;
}
#loadButton:hover {
  transform:scale(1.1);
}
#loading {
  position: absolute;
  width: 50px;
  height: 50px;
}
</style>
