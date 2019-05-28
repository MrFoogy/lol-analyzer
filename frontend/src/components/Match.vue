<template>
  <div id="matchItem" :class="[styleClass, 'matchItem']" @click="$emit('matchClick', $event, gameId)">
    <img :src="'http://ddragon.leagueoflegends.com/cdn/9.8.1/img/champion/' + championName + '.png'">
    <p> {{ timeText }} </p>
    <p id="queueText"> {{ queue }} </p>
  </div>
</template>

<script>
import { format, render, cancel, register } from 'timeago.js'

export default {
  name: 'match',
  props: ["isSelected", "gameId", "championName", "role", "lane", "timestamp", "queue"],
  data: function() {
      return {
      }
  },
  computed: {
    timeText: function() {
        return format(this.timestamp);
    },
    styleClass: function() {
      if (this.isSelected) {
        return "selected";
      } else {
        return "normal"
      }
    }
  },
}
</script>

<style scoped>
.matchItem {
  width: 376px;
  display: flex;
  flex-direction: row;
  margin: 3px;
  background-color: #f0f0f0;
  box-shadow: 1px 3px 3px -2px rgba(0,0,0,.2);
}
.matchItem * {
  padding: 5px;
  margin-top: auto;
  margin-bottom: auto;
}
#queueText {
  margin-right: 8px;
  margin-left: auto;
}
img {
  width: 40px;
  height: 40px;
}
.normal {
  background-color: #C9D6CC;
  border-radius: 3px;
}
.selected {
  background-color: #E0CE98;
  border-radius: 3px;
}
</style>

