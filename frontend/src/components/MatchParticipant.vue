<template>
  <div id="content" :class="styleClass" @click="$emit('playerClick', $event, playerData)">
    <img :src="'http://ddragon.leagueoflegends.com/cdn/9.8.1/img/champion/' + playerData['championName'] + '.png'" width="32" height="32">
    <p> {{ playerData["summonerName"] }} </p>
    <p> {{ kdaString }} </p>
  </div>
</template>

<script>

export default {
  name: 'home',
  props: ["playerData", "isSelected"],
  computed: {
    kdaString: function() {
      return this.playerData["kills"] + "/" + this.playerData["deaths"] + "/" + this.playerData["assists"];
    },
    styleClass: function() {
      if (this.isSelected) {
        return "selected";
      } else {
        return "normal"
      }
    }
  },
  methods: {
    selectElement() {
      this.isSelected = true;
    },
    deselectElement() {
      this.isSelected = false;
    }
  },
}
</script>

<style scoped>
#content {
  margin: 3px;
  width: 100%;
  height: 40px;
  display: flex;
  flex-direction: row;
  align-items: center;
  box-shadow: 1px 3px 3px -2px rgba(0,0,0,.2);
}
img {
  margin-left: 5px;
}
#content * {
  pointer-events: none;
}
.normal {
  background-color: #C9D6CC;
  border-radius: 3px;
}
.selected {
  background-color: #E0CE98;
  border-radius: 3px;
}
#content p {
  margin-left: 6px;
  font-size: small;
}
</style>

