<template>
  <div>
    <div>
      <li
        is="ChampionMastery"
        v-for="champion in champions"
        :key="champion.championId"
        :id="champion.championId"
        :points="champion.championPoints"
        :level="champion.championLevel"
        :name="champion.championName"
      ></li>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as dataFetch from '../assets/js/data_fetch.js';
import ChampionMastery from '../components/ChampionMastery'

export default {
  name: 'summonerChampions',
  props: {
    server: String,
    summonerName: String,
  },
  components: {
    'ChampionMastery': ChampionMastery,
  },
  data: function() {
    return {
      champions: []
    }
  },
  methods: {
    fetchData() {
      axios.get(dataFetch.championMasteryUrl(this.server, this.$store.state.summonerId)).then(response => {
        this.champions = response.data
      });
    }
  },
  mounted() {
    this.fetchData();
  }
}
</script>

<style scoped>
</style>

