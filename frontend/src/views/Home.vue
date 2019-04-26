<template>
  <div class="home">
    <h1> Home Page </h1>
    <p> Summoner Name: </p>
    <input ref="summonerNameInput" type="text" v-model="selectedSummonerName"> 
    <select ref="regionPick" v-model="selectedServer">
      <option v-for="server in servers" :value="server.routeName" :key="server.displayName"> {{ server.displayName }} </option>
    </select>
    <router-link :to="{name: 'summonerInfo', params: {server: selectedServer, summonerName: selectedSummonerName}}">
      <button> 
        Go! 
      </button>
    </router-link>
  </div>
</template>

<script>
/*
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
*/

export default {
  name: 'home',
  data: function() {
    return {
      selectedServer: "br",
      selectedSummonerName: "",
      servers: [
        {
          "displayName": "BR",
          "routeName": "br",
        },
        {
          "displayName": "EUW",
          "routeName": "euw",
        },
        {
          "displayName": "EUNE",
          "routeName": "eune",
        },
        {
          "displayName": "LAN",
          "routeName": "lan",
        },
        {
          "displayName": "LAS",
          "routeName": "las",
        },
        {
          "displayName": "NA",
          "routeName": "na",
        },
        {
          "displayName": "OCE",
          "routeName": "oce",
        },
        {
          "displayName": "RU",
          "routeName": "ru",
        },
        {
          "displayName": "TR",
          "routeName": "tr",
        },
        {
          "displayName": "JP",
          "routeName": "jp",
        },
      ]
    }
  },
}
</script>

<style>
select {
  margin-top: 10px;
}
</style>

