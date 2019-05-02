<template>
  <div id="content">
    <img :src="'http://ddragon.leagueoflegends.com/cdn/9.8.1/img/champion/' + playerData['championName'] + '.png'" width="40" height="40">
    <p> {{ playerData["summonerName"] }} </p>
    <p> {{ kdaString }} </p>
  </div>
</template>

<script>

export default {
  name: 'home',
  props: ["playerData"],
  computed: {
    kdaString: function() {
      return this.playerData["kills"] + "/" + this.playerData["deaths"] + "/" + this.playerData["assists"];
    }
  }
}
</script>

<style scoped>
#content {
  margin: 3px;
  width: 100%;
  height: 40px;
  display: flex;
  flex-direction: row;
}
#content p {
  margin-left: 6px;
  font-size: small;
}
</style>

