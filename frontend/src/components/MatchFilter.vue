<template>
  <div class="matchFilter">
    <div id="queueSelect" >
      <div id="mapSelect">
        <div>
          <input type="radio" id="sr" value="SR" v-model="selectedMap">
          <label for="sr">Summoner's Rift</label>
        </div>
        <div>
          <input type="radio" id="tt" value="TT" v-model="selectedMap"> 
          <label for="sr">Twisted Treeline</label>
        </div>
        <div>
          <input type="radio" id="ha" value="HA" v-model="selectedMap"> 
          <label for="sr">Howling Abyss</label>
        </div>
      </div>
      <div class="queueList" v-if="selectedMap == 'SR'">
        <li v-for="queue in queues.SR" :key="queue.id">
          <input type="checkbox" :value="queue.id" :id="queue.id" v-model="selectedQueues.SR"> {{queue.name}}
        </li>
      </div>
      <div class="queueList" v-if="selectedMap == 'HA'">
        <li v-for="queue in queues.HA" :key="queue.id">
          <input type="checkbox" :value="queue.id" :id="queue.id" v-model="selectedQueues.HA"> {{queue.name}}
        </li>
      </div>
      <div class="queueList" v-if="selectedMap == 'TT'">
        <li v-for="queue in queues.TT" :key="queue.id">
          <input type="checkbox" :value="queue.id" :id="queue.id" v-model="selectedQueues.TT"> {{queue.name}}
        </li>
      </div>
    </div>
    <input type="radio" id="allchamps" value="false" v-model="useChampFilter">
    <label for="sr">Any Champion</label>
    <input type="radio" id="filterchamps" value="true" v-model="useChampFilter"> 
    <label for="sr">Specific Champions</label>
    <div id="champSelect">
      <Select2Multiple v-if="useChampFilter == 'true'" :options="allChampions" v-model="selectedChampions">
        <option disabled value="0">Select champions</option>
      </Select2Multiple>
    </div>
    <!--
    <select class="champSelect" name="states[]" multiple="multiple">
      <option value="AL">Alabama</option>
      <option value="WY">Wyoming</option>
    </select>
    -->
  </div>
</template>

<script>
import axios from 'axios';
import Select2Multiple from './Select2Multiple'

export default {
  name: 'matchFilter',
  components: {
    "Select2Multiple": Select2Multiple,
  }, 
  data: function() {
    return {
      selectedMap: 'SR',
      useChampFilter: "false",
      allChampions: [
      ],
      selectedChampions: [],
      selectedQueues: {
        'SR': [],
        'HA': [],
        'TT': [],
      },
      queues: {
        TT: [
          {id: 460, name: "Normal 3v3"},
          {id: 470, name: "Ranked 3v3"},
        ],
        SR: [
          {id: 430, name: "Normal Blind"},
          {id: 400, name: "Normal Draft"},
          {id: 420, name: "Ranked Solo/Duo"},
          {id: 440, name: "Ranked Flex"},
          {id: 900, name: "ARURF"},
          {id: 1020, name: "One for All"},
        ],
        HA: [
          {id: 450, name: "ARAM"},
        ]
      }
    }
  },
  computed: {
    fullFilter: function() {
      return {
        queues: this.selectedQueues[this.selectedMap],
        champions: this.selectedChampions,
        useChampFilter: this.useChampFilter,
      }
    }
  },
  methods: {
  },
  mounted() {
      axios.get("http://ddragon.leagueoflegends.com/cdn/9.8.1/data/en_US/champion.json").then(response => {
        this.allChampions = [];
        var champsJson = response.data["data"];
        for (var prop in champsJson) {
          if (champsJson.hasOwnProperty(prop)) {
            this.allChampions.push({id: parseInt(champsJson[prop].key), text: champsJson[prop].name});
          }
        }
      });
  }, watch: {
    selectedMap: function(val) {
      this.$emit('setMap', val);
    },
    fullFilter: function(val) {
      this.$emit('filterChange', val);
    }
  }
}
</script>

<style scoped>
#mapSelect {
  height: 70px;
}
#queueSelect {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 140px;
}
#champSelect {
  margin-top: 10px;
}
.queueList {
  width: 80%;
  columns: 2;
  text-align: left;
  -webkit-columns: 2;
  -moz-columns: 2;
  list-style-type: none
}
select {
  width: 300px;
}
</style>

