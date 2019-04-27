<template>
  <header>
    <nav>
      <router-link class="navitem" :to="{name: 'summonerOverview'}"> Overview </router-link>
      <router-link class="navitem" :to="{name: 'summonerChampions'}"> Champions </router-link>
      <router-link class="navitem" :to="{name: 'summonerMatches'}"> Matches </router-link>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'SummonerNavigation',
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
header {
  background: white;
  top: 0;
  left: 0;
  right: 0;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  /* Magic calculation that compensates for scrollbar width */
  padding-left: calc(20px + 100vw - 100%);
  padding-right:20px;
}
header * {
  display: inline;
  text-decoration: none;
  color: black;
}
header nav {
  margin: 20px;
}
header .navitem {
  margin:20px;
  font-size: larger;
}
nav .router-link-exact-active {
  font-weight: bold;
}
</style>
