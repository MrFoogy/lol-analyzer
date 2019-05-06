<template>
  <div id="mainContainer">
    <div id="matchList">
      <li
        is="Match"
        v-for="match in matches"
        @matchClick="matchClicked"
        :key="match.championId"
        :id="match.gameId"
        :gameId="match.gameId"
        :championName="match.championName"
        :lane="match.lane"
        :role="match.role"
        :timestamp="match.timestamp"
        :queue="match.queue"
      ></li>
    </div>
    <div id="details">
      <select ref="eventPick" v-model="selectedEventType">
        <option v-for="eventType in eventTypes" :value="eventType.paramName" :key="eventType.displayName"> {{ eventType.displayName }} </option>
      </select>
      <Heatmap ref="heatmap"/>
      <MatchDetails 
        ref="matchDetails" 
        :server="server" 
        :summonerName="summonerName"
        @participantSelected="participantSelected"/>
    </div>
  </div>
</template>

<script>
import Match from '../components/Match';
import Heatmap from '../components/Heatmap';
import MatchDetails from '../components/MatchDetails';
import axios from 'axios';
import * as dataFetch from '../assets/js/data_fetch.js';

export default {
  name: 'summonerMatches',
  props: ["server", "summonerName"],
  data: function() {
    return {
      matches: [],
      matchKills: [],
      currentMatchId: null,
      selectedParticipant: null,
      selectedEventType: "kill",
      eventTypes: [
        {
          "displayName": "Kills",
          "paramName": "kill",
        },
        {
          "displayName": "Deaths",
          "paramName": "death",
        },
        {
          "displayName": "Assists",
          "paramName": "assist",
        },
        {
          "displayName": "Wards Placed",
          "paramName": "wardplace",
        },
        {
          "displayName": "Wards Killed",
          "paramName": "wardkill",
        },
      ],
    }
  },
  components: {
    'Match': Match,
    'Heatmap': Heatmap,
    'MatchDetails': MatchDetails,
  },
  methods: {
    matchClicked: function(event, matchId) {
      this.selectedParticipant = null;
      this.$refs.matchDetails.fetchMatchDetails(matchId);
      this.currentMatchId = matchId;
    },
    fetchData() {
      axios.get(dataFetch.matchListUrl(this.server, this.$store.state.accountId)).then(response => {
        this.matches = response.data;
      });
    },
    fetchTimelineData() {
      axios.get(dataFetch.matchKillsUrl(this.server, this.currentMatchId), 
          { 
            params: {
              pID: this.selectedParticipant,
              event: this.selectedEventType
            }
          }).then(response => {
        this.$refs.heatmap.displayKills(response.data);
      });
    },
    participantSelected: function(participantId) {
      this.selectedParticipant = participantId;
      this.fetchTimelineData();
    }
  },
  watch: {
    selectedEventType: function(val) {
      if (this.selectedParticipant != null) {
        this.fetchTimelineData();
      }
    }
  },
  mounted() {
    this.fetchData();
  }
}
</script>

<style>
#mainContainer {
  display: flex;
  flex-direction: row;
  justify-content: center;
}
#matchList {
  display: flex;
  flex-direction: column;
  width: 400px;
  margin-right: 20px;
}
#details {
  display: flex;
  flex-direction: column;
}
</style>

