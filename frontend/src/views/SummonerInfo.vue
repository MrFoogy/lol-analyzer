<template>
  <div id="container">
    <div class="shadowBox">
      <h1> {{ summonerName }} </h1>
      <div v-if="profileIconId != -1" id="summonerInfo">
        <img :src="'http://ddragon.leagueoflegends.com/cdn/9.8.1/img/profileicon/' + profileIconId + '.png'">
        <h2> Level {{ summonerLevel }} </h2>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as dataFetch from '../assets/js/data_fetch.js';

export default {
  name: 'summonerInfo',
  props: {
    server: String,
    summonerName: String,
  },
  data: function() {
    return {
      profileIconId: -1,
    }
  },
  methods: {
    fetchBaseInfo() {
      axios.get(dataFetch.summonerInfoUrl(this.server, this.summonerName)).then(response => {
        this.profileIconId = response.data["profileIconId"];
        this.summonerLevel = response.data["summonerLevel"]
      });
    }
  },
  /*
  watch: {
    summonerName: function() {
      this.fetchBaseInfo();
    },
    server: function() {
      this.fetchBaseInfo();
    }
  },
  */
  mounted() {
    this.fetchBaseInfo();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
img {
  border-radius: 8px;
}
#container {
  display:flex;
  flex-direction: column;
  align-items: center;
}
.shadowBox {
  display: flex;
  flex-direction: column;
  padding: 16px;
  width: 500px;
}
</style>
