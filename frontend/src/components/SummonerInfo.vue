<template>
  <div>
    <h1> {{ summonerName }} </h1>
    <h2> {{ server }} </h2>
    <h2> {{ info }} </h2>
    <div id="nav">
      <!--
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
      -->
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SummonerInfo',
  props: {
    server: String,
    summonerName: String,
  },
  data: function() {
    return {
      info: null,
      regionEndPoints: {
        "br": "br1.api.riotgames.com",
        "eune": "eun1.api.riotgames.com",
        "euw": "euw1.api.riotgames.com",
        "jp": "jp1.api.riotgames.com",
        "kr": "kr.api.riotgames.com",
        "lan": "la1.api.riotgames.com",
        "las": "la2.api.riotgames.com",
        "na": "na1.api.riotgames.com",
        "oce": "oc1.api.riotgames.com",
        "tr": "tr1.api.riotgames.com",
        "ru": "ru.api.riotgames.com",
      },
    }
  },
  methods: {
    composeUrl(url) {
      return "https://" + this.regionEndPoints[this.server] + url + "?api_key=" + require("../assets/apikey.json");
    },
    baseInfoUrl() {
      return this.composeUrl("/lol/summoner/v4/summoners/by-name/" + this.summonerName);
    }
  },
  mounted() {
    axios.get(this.baseInfoUrl()).then(response => (this.info = response));
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
