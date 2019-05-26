<template>
  <div >
    <div id="queueSelect" >
      <ul>
        <li v-for="queue in queues" :key="queue.id">
          <input type="checkbox" :value="queue.id" :id="queue.id" v-model="selectedQueues"> {{queue.name}}
        </li>
      </ul>
    </div>
    <p> {{selectedQueues}} </p>
  </div>
</template>

<script>

export default {
  name: 'matchFilter',
  data: function() {
    return {
      selectedQueues: [],
      queues: [
        {id: 400, name: "Normal (Draft Pick)"},
        {id: 420, name: "Ranked Solo/Duo"},
        {id: 430, name: "Normal (Blind Pick)"},
        {id: 440, name: "Ranked Flex"},
        {id: 450, name: "ARAM"},
        {id: 460, name: "Twisted Treeline (Normal)"},
        {id: 470, name: "Twisted Treeline (Ranked)"},
        {id: 900, name: "ARURF"},
        {id: 1020, name: "One for All"},
        {id: 1200, name: "Nexus Blitz"},
      ]
    }
  },
  props: {
  },
  methods: {
  },
  mounted() {
  }
}
</script>

<style scoped>
ul {
  list-style-type: none
}
</style>

