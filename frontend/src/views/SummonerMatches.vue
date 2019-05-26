<template>
  <div>
    <!-- Rounded switch -->
    <!--
    <label class="switch">
      <input type="checkbox" v-model="combine">
      <span class="slider round"></span>
    </label>
    -->
    <div id="mainContainer">
      <div id="querySelect">
        <div id="matchSelect">
          <MatchFilter/>
          <div id="details" v-show="selectedMatchIds.length == 1">
            <MatchDetails 
              ref="matchDetails" 
              :server="server" 
              :summonerName="summonerName"
              @participantSelected="participantSelected"/>
          </div>
          <div id="matchList">
            <li
              is="Match"
              v-for="match in matches"
              @matchClick="matchClicked"
              :key="match.championId"
              :id="match.gameId"
              :gameId="match.gameId"
              :championName="match.championName"
              :lane="match.lane"
              :role="match.role"
              :timestamp="match.timestamp"
              :queue="match.queue"
              :isSelected="selectedMatchIds.includes(match.gameId)"
            ></li>
          </div>
        </div>
      </div>
      <div id="dataDisplayContainer">
        <div id="dataDisplay">
          <select ref="statPick" v-model="selectedStatType">
            <option v-for="statType in statTypes" :value="statType" :key="statType.displayName"> {{ statType.displayName }} </option>
          </select>
          <StatGraph ref="statGraph" :statType="selectedStatType"/>
          <select ref="eventPick" v-model="selectedEventType">
            <option v-for="eventType in eventTypes" :value="eventType.paramName" :key="eventType.displayName"> {{ eventType.displayName }} </option>
          </select>
          <Heatmap ref="heatmap" :eventType="selectedEventType"/>
          <!--
          <button @click="refreshHeatmap"> Update </button>
          -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Match from '../components/Match';
import StatGraph from '../components/StatGraph';
import Heatmap from '../components/Heatmap';
import MatchFilter from '../components/MatchFilter'
import MatchDetails from '../components/MatchDetails';
import MatchCombiner from '../components/MatchCombiner';
import axios from 'axios';
import * as dataFetch from '../assets/js/data_fetch.js';

export default {
  name: 'summonerMatches',
  props: ["server", "summonerName"],
  data: function() {
    return {
      combine: false,
      matches: [],
      matchKills: [],
      selectedMatchIds: [],
      selectedParticipant: null,
      selectedEventType: "kill",
      selectedStatType: {"displayName": "Gold Earned", "paramName": "gold"},
      statTypes: [
        {"displayName": "Gold Earned", "paramName": "gold"},
        {"displayName": "Minions Killed", "paramName": "cs"},
        {"displayName": "Kills", "paramName": "kill"},
        {"displayName": "Deaths", "paramName": "death"},
        {"displayName": "Assists", "paramName": "assist"},
        {"displayName": "Wards Placed", "paramName": "wardplace"},
        {"displayName": "Wards Killed", "paramName": "wardkill"},
      ],
      eventTypes: [
        {
          "displayName": "Kills",
          "paramName": "kill",
        },
        {
          "displayName": "Deaths",
          "paramName": "death",
        },
        {
          "displayName": "Assists",
          "paramName": "assist",
        },
        /*
        {
          "displayName": "Wards Placed",
          "paramName": "wardplace",
        },
        {
          "displayName": "Wards Killed",
          "paramName": "wardkill",
        },
        */
      ],
    }
  },
  components: {
    'Match': Match,
    'Heatmap': Heatmap,
    'StatGraph': StatGraph,
    'MatchDetails': MatchDetails,
    'MatchCombiner': MatchCombiner,
    'MatchFilter': MatchFilter,
  },
  methods: {
    matchClicked: function(event, matchId) {
      this.selectedParticipant = null;
      if (this.selectedMatchIds.includes(matchId)) {
        this.selectedMatchIds.splice(this.selectedMatchIds.indexOf(matchId), 1);
      } else {
        this.selectedMatchIds.push(matchId);
      }
      if (this.selectedMatchIds.length == 1) {
        this.$refs.matchDetails.fetchMatchDetails(this.selectedMatchIds[0]);
      } else if (this.selectedMatchIds.length > 0) {
        this.refreshHeatmap();
      }
    },
    onTimelineQuery() {
      this.fetchFullTimeline();
    },
    fetchData() {
      axios.get(dataFetch.matchListUrl(this.server, this.$store.state.accountId)).then(response => {
        this.matches = response.data;
      });
    },
    fetchTimeline() {
      if (this.selectedMatchIds.length == 1) {
        this.fetchMatchTimeline();
      } else if (this.selectedMatchIds.length > 0) {
        this.fetchSelectedMatchesTimeline();
      } 
    },
    fetchMatchTimeline() {
      axios.get(dataFetch.matchTimelineUrl(this.server, this.selectedMatchIds[0]), 
          { 
            params: {
              pID: this.selectedParticipant,
              event: this.selectedEventType,
              matchIDs: this.selectedMatchIds,
            }
          }).then(response => {
        this.$refs.heatmap.setTimelineData(response.data["events"]);
        this.$refs.statGraph.setTimelineData(response.data["stats"]);
      });
    },
    fetchSelectedMatchesTimeline() {
      axios.get(dataFetch.combinedTimelineUrl(this.server, this.$store.state.accountId), 
          { 
            params: {
              event: this.selectedEventType,
              matchIDs: "[" + this.selectedMatchIds.toString() + "]",
            }
          }).then(response => {
        console.log(response.data);
        this.$refs.heatmap.setTimelineData(response.data["timeline"]["events"]);
        this.$refs.statGraph.setTimelineData(response.data["timeline"]["stats"]);
      });
    },
    fetchFullTimeline() {
      axios.get(dataFetch.fullTimelineUrl(this.server, this.$store.state.accountId), 
          { 
            params: {
              event: this.selectedEventType
            }
          }).then(response => {
        console.log(response.data);
        this.$refs.heatmap.setTimelineData(response.data["timeline"]["events"]);
        this.$refs.statGraph.setTimelineData(response.data["timeline"]["stats"]);
      });
    },
    participantSelected: function(participantId) {
      this.selectedParticipant = participantId;
      this.refreshHeatmap();
    },
    refreshHeatmap() {
      this.$refs.heatmap.clear();
      this.fetchTimeline();
    }
  },
  mounted() {
    this.fetchData();
  }
}
</script>

<style>
#mainContainer {
  display: flex;
  flex-direction: row;
  justify-content: center;
}
#matchSelect {
  display: flex;
  flex-direction: row;
  justify-content: center;
}
#querySelect {
  width: 60%;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
}
#dataDisplayContainer {
  width: 40%;
  margin-left: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
#dataDisplay {
  display: flex;
  flex-direction: column;
  align-items: center;
}
#dataDisplay * {
  margin-bottom: 10px;
}
#matchList {
  display: flex;
  flex-direction: column;
  width: 400px;
  margin-left: 20px;
}
#details {
  width: 400px;
  display: flex;
  flex-direction: column;
}

/* The switch - the box around the slider */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>

