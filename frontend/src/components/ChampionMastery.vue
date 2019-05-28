<template>
  <div id="content">
    <img :src="'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/' + name + '_0.jpg'">
    <div id="infoBox">
      <div id="bg"/>
      <p> {{ points }}p </p>
      <p> Level {{ level }} </p>
    </div>
  </div>
</template>

<script>

export default {
  name: 'championMastery',
  props: ["id", "name", "points", "level"]
}
</script>

<style scoped>
#content {
  width: 154px;
  height: 280px;
  position: relative;
  display: inline-block;
  margin: 5px 5px 5px 5px;
  box-shadow: 3px 4px 3px -1px rgba(0,0,0,.2);
  border-radius: 5px;
}
#infoBox {
  width: 100%;
  height: 22%;
  position: absolute;
  bottom: 0;
  display: flex;
  flex-direction: column;
}
#bg {
  width: 100%;
  height: 100%;
  background-color: black;
  position: absolute;
  border-radius: 5px;
  opacity: 0.4;
  z-index: -5;
}
p {
  margin: 5px;
  color: white;
  opacity: 1;
}
img {
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: black;
  position: absolute;
  object-fit: cover;
  border-radius: 5px;
  z-index: -10;
}
</style>

