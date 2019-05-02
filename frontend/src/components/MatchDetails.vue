<template>
  <div id="container">
    <div v-if="matchData != []" class="matchDetails">
      <p> {{ formatDuration(matchData["duration"]) }} </p>
      <div id="teams">
        <div class="teamContent">
          <p> {{ matchData['teams']['red']['stats']['win'] }}
          <li
            is="MatchParticipant"
            v-for="player in matchData['teams']['red']['participants']"
            :key="player.id"
            :playerData="player"
          ></li>
        </div>
        <div class="teamContent">
          <p> {{ matchData['teams']['blue']['stats']['win'] }}
          <li
            is="MatchParticipant"
            v-for="player in matchData['teams']['blue']['participants']"
            :key="player.id"
            :playerData="player"
          ></li>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as dataFetch from '../assets/js/data_fetch.js';
import MatchParticipant from './MatchParticipant';

export default {
  name: 'matchDetails',
  props: {
    server: String,
  },
  components: {
    "MatchParticipant": MatchParticipant,
  },
  data: function() {
      return {
          matchData: []
      }
  },
  methods: {
    fetchMatchDetails(matchId) {
      axios.get(dataFetch.matchDetailsUrl(this.server, matchId)).then(response => {
        this.matchData = response.data
      });
    },
    formatDuration(duration) {
      var hrs = ~~(duration / 3600);
      var mins = ~~((duration % 3600) / 60);
      var secs = ~~duration % 60;

      var ret = "";
      if (hrs > 0) {
          ret += "" + hrs + ":" + (mins < 10 ? "0" : "");
      }
      ret += "" + mins + ":" + (secs < 10 ? "0" : "");
      ret += "" + secs;
      return ret;
    }
  }
}
</script>

<style scoped>
#container * {
  margin-top: 5px;
  margin-bottom: 0;
}
#teams {
    display: flex;
    flex-direction: row;
}
.teamContent {
  flex: 50%;
}
</style>

