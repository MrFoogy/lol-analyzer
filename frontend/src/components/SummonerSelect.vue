<template>
  <div class="summonerSelect">
    <input ref="summonerNameInput" type="text" v-model="selectedSummonerName"> 
    <select ref="regionPick" v-model="selectedServer">
      <option v-for="server in servers" :value="server.routeName" :key="server.displayName"> {{ server.displayName }} </option>
    </select>
    <router-link :to="{name: 'summonerMain', params: {server: selectedServer, summonerName: selectedSummonerName}}">
      <button> 
        Go! 
      </button>
    </router-link>
  </div>
</template>

<script>

export default {
  name: 'summonerSelect',
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

<style scoped>
.summonerSelect {
  position: absolute;
  right: 0;
  top: 15px;
  display: flex;
  justify-content: flex-end;
  align-content: center;
}
.summonerSelect * {
  margin-left: 5px;
  margin-right: 5px;
  align-self: center;
}
</style>

