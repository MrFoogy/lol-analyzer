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
    <Heatmap ref="heatmap"/>
  </div>
</template>

<script>
import Match from '../components/Match';
import Heatmap from '../components/Heatmap';
import axios from 'axios';
import * as dataFetch from '../assets/js/data_fetch.js';

export default {
  name: 'summonerMatches',
  props: ["server", "summonerName"],
  data: function() {
    return {
      matches: [],
      matchKills: [],
    }
  },
  components: {
    'Match': Match,
    'Heatmap': Heatmap,
  },
  methods: {
    matchClicked: function(event, matchId) {
      this.fetchMatchKills(matchId);
    },
    fetchData() {
      axios.get(dataFetch.matchListUrl(this.server, this.$store.state.accountId)).then(response => {
        this.matches = response.data;
      });
    },
    fetchMatchKills(matchId) {
      axios.get(dataFetch.matchKillsUrl(this.server, matchId)).then(response => {
        this.$refs.heatmap.displayKills(response.data);
      });
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
</style>

