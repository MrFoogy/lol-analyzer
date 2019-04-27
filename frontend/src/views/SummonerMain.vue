<template>
  <div>
    <SummonerLoad v-if="!this.$store.state.accountId" :server="server" :summonerName="summonerName"/>
    <div v-else>
      <SummonerNavigation/>
      <router-view/>
    </div>
  </div>
</template>

<script>
import SummonerNavigation from '../components/SummonerNavigation';
import SummonerLoad from '../components/SummonerLoad'
export default {
  name: 'summonerMain',
  components: {
    'SummonerNavigation': SummonerNavigation,
    'SummonerLoad': SummonerLoad,
  },
  props: {
    server: String,
    summonerName: String,
  },
}
</script>

<style>
</style>

