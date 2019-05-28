<template>
  <div id="container">
    <template v-if="matchData" class="matchDetails">
      <p> Game time: {{ formatDuration(matchData["duration"]) }} </p>
      <div id="teams">
        <div class="teamContent">
          <p> {{ matchData['teams']['red']['stats']['win'] }}
          <li
            is="MatchParticipant"
            v-for="player in matchData['teams']['red']['participants']"
            @playerClick="playerClicked"
            :key="player.participantId"
            :isSelected="player.summonerName == selectedSummoner"
            :playerData="player"
          ></li>
        </div>
        <div class="teamContent">
          <p> {{ matchData['teams']['blue']['stats']['win'] }}
          <li
            is="MatchParticipant"
            v-for="player in matchData['teams']['blue']['participants']"
            @playerClick="playerClicked"
            :key="player.participantId"
            :isSelected="player.summonerName == selectedSummoner"
            :playerData="player"
          ></li>
        </div>
      </div>
    </template>
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
    summonerName: String,
  },
  components: {
    "MatchParticipant": MatchParticipant,
  },
  data: function() {
      return {
          matchData: null,
          selectedSummoner: null,
      }
  },
  methods: {
    fetchMatchDetails(matchId) {
      this.selectedSummoner = this.summonerName;
      axios.get(dataFetch.matchDetailsUrl(this.server, matchId)).then(response => {
        this.matchData = response.data
        this.tryPassSelectedSummoner(this.summonerName);
      });
    },
    getParticipantId(summonerName) {
      if (this.matchData != []) {
        var blue = this.matchData.teams.blue.participants;
        var red = this.matchData.teams.red.participants;
        for (var i = 0; i < blue.length; i++) {
          if (blue[i].summonerName == summonerName) {
            return blue[i].participantId;
          }
        }
        for (var i = 0; i < red.length; i++) {
          if (red[i].summonerName == summonerName) {
            return red[i].participantId;
          }
        }
      }
      return -1;
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
    },
    playerClicked(event, playerData) {
      this.selectedSummoner = playerData.summonerName;
    },
    tryPassSelectedSummoner(summonerName) {
      if (summonerName == null || this.matchData == null) return;
      var participantId = this.getParticipantId(summonerName);
      if (participantId != -1) {
        this.$emit('participantSelected', participantId);
      }
    }
  },
  watch: {
    selectedSummoner: function(val) {
      this.tryPassSelectedSummoner(val);
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
    flex-direction: column;
}
.teamContent {
  flex: 50%;
}
</style>