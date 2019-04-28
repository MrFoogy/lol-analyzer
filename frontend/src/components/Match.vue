<template>
  <div class="matchItem" @click="$emit('matchClick', $event, gameId)">
    <img :src="'http://ddragon.leagueoflegends.com/cdn/9.8.1/img/champion/' + championName + '.png'">
    <p> {{ timeText }} </p>
    <p id="queueText"> {{ queue }} </p>
  </div>
</template>

<script>
import { format, render, cancel, register } from 'timeago.js'

export default {
  name: 'championMastery',
  props: ["gameId", "championName", "role", "lane", "timestamp", "queue"],
  data: function() {
      return {
      }
  },
  computed: {
    timeText: function() {
        return format(this.timestamp);
    }
  },
}
</script>

<style scoped>
.matchItem {
  width: 100%;
  display: flex;
  flex-direction: row;
  margin: 3px;
  background-color: #f0f0f0;
}
.matchItem * {
  padding: 5px;
}
#queueText {
  right: 0;
  margin-left: auto;
}
img {
  width: 50px;
  height: 50px;
}
</style>

