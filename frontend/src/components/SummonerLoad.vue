<template>
  <div id="summonerLoad">
    <h2> Loading summoner {{ summonerName }} ...</h2>
  </div>
</template>

<script>
import axios from 'axios';
import * as dataFetch from '../assets/js/data_fetch.js';

export default {
  name: 'summonerLoad',
  props: {
    server: String,
    summonerName: String,
  },
  methods: {
    fetchAccountId() {
      axios.get(dataFetch.accountIdUrl(this.server, this.summonerName)).then(response => {
        this.$store.commit("setAccountId", response.data["accountId"]);
        this.$store.commit("setSummonerId", response.data["id"]);
      });
    }
  },
  mounted() {
    this.fetchAccountId();
  }
}
</script>

<style scoped>
h2 {
  margin-block-start: 12px;
}
</style>

