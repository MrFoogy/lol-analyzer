<template>
  <header>
    <nav>
      <router-link class="navitem" :to="{name: 'summonerOverview'}"> 
        <p> Overview </p>
        <div class="underline"/>
      </router-link>
      <router-link class="navitem" :to="{name: 'summonerChampions'}"> 
        <p> Champions </p>
        <div class="underline"/>
      </router-link>
      <router-link class="navitem" :to="{name: 'summonerMatches'}"> 
        <p> Matches </p>
        <div class="underline"/>
      </router-link>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'SummonerNavigation',
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style >
header {
  top: 0;
  left: 0;
  right: 0;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: row;
  /* Magic calculation that compensates for scrollbar width */
  padding-left: calc(20px + 100vw - 100%);
  padding-right:20px;
  padding-bottom: 32px;
}
p {
  margin-block-start: 5px;
  margin-block-end: 5px;
}
header * {
  display: inline;
  text-decoration: none;
  color: black;
}
header nav {
  display: flex;
  flex-direction: row;
  margin: 20px;
}
.underline {
  height: 5px;
  width: 80px;
  background-color: #d0d0d070;
  border-radius: 2px;
  transform: scale(1.0, 1.0);
  transition: 0.15s ease;
}
header .navitem {
  width: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin:20px;
  font-size: larger;
}
header .navitem:hover:not(.router-link-exact-active) .underline {
  background-color: #d0d0d0d0;
  transform: scale(1.15, 1.0);
}
nav .router-link-exact-active {
  font-weight: bold;
}
nav .router-link-exact-active .underline {
  background-color: #5DFDCB;
  transform: scale(1.4, 1.2);
}
</style>
