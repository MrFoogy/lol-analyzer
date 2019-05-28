<template>
  <div id="app">
    <div id="topBar"/>
    <div id="mainView">
      <h1 id="appTitle"> LoL Analyzer </h1>
      <SummonerSelect> </SummonerSelect>
      <router-view id="routerView"/>
    </div>
  </div>
</template>

<script>
import SummonerSelect from '@/components/SummonerSelect'
export default {
  name: 'App',
  components: {
    'SummonerSelect': SummonerSelect,
  },
}
</script>

<style>
#appTitle {
  position: absolute;
  left: 5px;
  top: 10px;
  margin-block-end: 0px;
  margin-block-start: 0px;
  display: flex;
  align-content: center;
}
.shadowBox {
  box-shadow: 3px 4px 3px -1px rgba(0,0,0,.2);
  background-color: #e8e8e8;
  border-radius: 5px;
}
#topBar {
  position: absolute;
  top: 0;
  left: 0;
  display: block;
  width: 100%;
  height: 80px;
  background-color: #f0f0f0;
  z-index: -1;
  box-shadow: 0 6px 4px -4px rgba(0,0,0,.2);
}
#routerView {
  display: flex;
  flex-direction: column;
  flex: 1 1 auto;
  width: 100%;
}
#routerView > div {
  display: flex;
  flex-direction: column;
  flex: 1 1 auto;
  width: 100%;
}
body,html{
  height: 100%;
  background-color: #83ADA3;
  z-index: -1;
}
body, #app {
  display: block;
  position:absolute;
  height:auto;
  bottom:0;
  top:0;
  left:0;
  right:0;
  margin: 0px;
  align-items: center;
  flex-direction: column;
}
#mainView {
  position: absolute;
  top: 16px;
  right: 16px;
  bottom: 16px;
  left: 16px;
  display: flex;
  flex-direction: column;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
}
#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
