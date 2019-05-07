
<template>
  <div id="container">
      <button @click="triggerTimelineFetch"> Trigger fetch </button>
  </div>
</template>

<script>
import axios from 'axios';
import * as dataFetch from '../assets/js/data_fetch.js';

export default {
  name: 'matchCombiner',
  props: {
    server: String,
    summonerName: String,
  },
  data: function() {
      return {
      }
  },
  methods: {
      triggerTimelineFetch() {
          this.$emit("onTimelineQuery")
      }
  },
  watch: {
      /*
    selectedSummoner: function(val) {
      this.tryPassSelectedSummoner(val);
    }
    */
  }
}
</script>

<style scoped>
</style>
