<template>
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
        <MatchFilter class="matchFilter shadowBox" @filterChange="onMatchFilterChange" @setMap="onSelectMap"/>
        <div class="shadowBox" id="matchListFrame">
          <div class="dataOutdatedBlock" v-show="isMatchListOutdated">
            <LoadButton ref="timelineLoad" :loading="isLoadingMatches" :canLoad="canFetchMatches" @click="fetchMatches"/>
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
      <div class="shadowBox" id="selectedMatchView">
        <div id="details" v-show="selectedMatchIds.length == 1">
          <MatchDetails 
            ref="matchDetails" 
            :server="server" 
            :summonerName="summonerName"
            @participantSelected="participantSelected"/>
        </div>
        <div class="noSelectedMatchText" v-show="selectedMatchIds.length > 1">
          <h3> Combining matches </h3>
        </div>
        <div class="noSelectedMatchText" v-show="selectedMatchIds.length == 0">
          <h3> No matches selected </h3>
        </div>
      </div>
    </div>
    <div id="dataDisplayFrame">
      <div class="dataOutdatedBlock" v-show="isDataViewOutdated">
        <LoadButton ref="timelineLoad" :loading="isLoadingTimeline" :canLoad="canFetchTimeline" @click="fetchTimelineData"/>
      </div>
      <div id="dataDisplayContainer">
        <div class="dataDisplay shadowBox">
          <h2> Match Stats </h2>
          <select ref="statPick" v-model="selectedStatType">
            <option v-for="statType in statTypes" :value="statType" :key="statType.displayName"> {{ statType.displayName }} </option>
          </select>
          <StatGraph ref="statGraph" :statType="selectedStatType"/>
        </div>
        <div class="dataDisplay shadowBox">
          <h2> Match Events </h2>
          <select ref="eventPick" v-model="selectedEventType">
            <option v-for="eventType in eventTypes" :value="eventType.paramName" :key="eventType.displayName"> {{ eventType.displayName }} </option>
          </select>
          <Heatmap ref="heatmap" :eventType="selectedEventType" :mapId="selectedMapId"/>
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
import LoadButton from '../components/LoadButton';
import axios from 'axios';
import * as dataFetch from '../assets/js/data_fetch.js';
import jQuery from 'jquery';
var _ = require("underscore");

export default {
  name: 'summonerMatches',
  props: ["server", "summonerName"],
  data: function() {
    return {
      matchFilter: null,
      lastUsedFilter: null,
      combine: false,
      matches: [],
      matchKills: [],
      selectedMatchIds: [],
      lastUsedMatchIds: [],
      selectedMap: 'SR',
      selectedParticipant: null,
      lastUsedParticipant: null,
      isLoadingTimeline: false,
      isLoadingMatches: false,
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
        {"displayName": "Kills", "paramName": "kill"},
        {"displayName": "Deaths", "paramName": "death"},
        {"displayName": "Assists", "paramName": "assist"},
      ],
    }
  }, computed: {
    selectedMapId: function() {
      if (this.selectedMap == 'TT') {
        return 10;
      } 
      if (this.selectedMap == 'SR') {
        return 11;
      } 
      if (this.selectedMap == 'HA') {
        return 12;
      } 
      return 0;
    },
    isMatchListOutdated: function() {
      return this.isLoadingMatches || this.lastUsedFilter == null || !_.isEqual(this.lastUsedFilter, this.matchFilter);
    },
    isDataViewOutdated: function() {
      return this.isLoadingTimeline || this.selectedMatchIds.length == 0 || !_.isEqual(this.selectedMatchIds, this.lastUsedMatchIds) || (this.lastUsedMatchIds.length == 1 && !_.isEqual(this.selectedParticipant, this.lastUsedParticipant));
    },
    canFetchTimeline: function() {
      return this.selectedMatchIds.length > 0 && !this.isLoadingTimeline;
    },
    canFetchMatches: function() {
      return this.matchFilter != null && !this.isLoadingMatches;
    }
  },
  components: {
    'Match': Match,
    'Heatmap': Heatmap,
    'StatGraph': StatGraph,
    'MatchDetails': MatchDetails,
    'MatchCombiner': MatchCombiner,
    'MatchFilter': MatchFilter,
    'LoadButton': LoadButton,
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
      } 
      console.log(this.selectedMatchIds);
      console.log(this.lastUsedMatchIds);
      console.log( !_.isEqual(this.selectedMatchIds, this.lastUsedMatchIds))
    },
    onSelectMap(mapName) {
      this.selectedMap = mapName;
    },
    onMatchFilterChange(matchFilter) {
      this.matchFilter = matchFilter;
    },
    onTimelineQuery() {
      this.fetchFullTimeline();
    },
    fetchMatches() {
      // Deep copy
      this.lastUsedFilter = jQuery.extend(true, {}, this.matchFilter);
      this.selectedMatchIds = []
      this.isLoadingMatches = true;
      axios.get(dataFetch.matchListUrl(this.server, this.$store.state.accountId), {
        params: {
          queues: "[" + this.matchFilter.queues.toString() + "]",
          champions: this.matchFilter.useChampFilter == "true" ? "[" + this.matchFilter.champions.toString() + "]" : "[]",
        }
      }).then(response => {
        this.matches = response.data;
        this.isLoadingMatches = false;
      }).catch((error) => {
        this.isLoadingMatches = false;
      });
    },
    fetchTimeline() {
      // Clone
      this.lastUsedMatchIds = [...this.selectedMatchIds];
      this.lastUsedParticipant = this.selectedParticipant;
      if (this.selectedMatchIds.length == 1) {
        this.isLoadingTimeline = true;
        this.fetchMatchTimeline();
      } else if (this.selectedMatchIds.length > 0) {
        this.isLoadingTimeline = true;
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
        this.isLoadingTimeline = false;
      }).catch((error) => {
        this.isLoadingTimeline = false;
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
        this.isLoadingTimeline = false;
      }).catch((error) => {
        this.isLoadingTimeline = false;
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
    },
    fetchTimelineData() {
      this.$refs.heatmap.clear();
      this.fetchTimeline();
    }
  }
}
</script>

<style>
#mainContainer {
  display: flex;
  flex-direction: row;
  height: 100%;
}
#matchSelect {
  display: flex;
  flex-direction: column;
  justify-self: start;
  align-items: center;
  height: 100%;
}
#querySelect {
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  flex: 0 0 0;
}
.matchFilter {
  width: 400px;
  height: 220px;
  padding-top:10px;
  padding-bottom:10px;
  border-radius: 5px;
}
.dataOutdatedBlock {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}
#matchList {
  flex: 1 1 0px;
  padding: 8px 16px 8px 8px;
}
.dataOutdatedBlock {
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
  background-color: #83ADA3d0;
}
#dataDisplayFrame {
  margin-left: 20px;
  position: relative;
  flex: 1 1 0;
}
#dataDisplayContainer {
  flex: 1 1 0px;
  display: flex;
  flex-direction: row;
  height: 100%;
  justify-content: space-around;
  align-items: center;
}
.dataDisplay {
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 1;
  margin-left: 4px;
  margin-right: 4px;
  padding: 8px 18px 8px 18px;
  border-radius: 5px;
}
.dataDisplay * {
  margin-bottom: 10px;
}
#matchListFrame {
  margin-top:10px;
  width: 400px;
  flex: 1 1 0px;
  position: relative;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
}
#matchList {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
}
.noSelectedMatchText {
  padding-left: 8px;
}
#selectedMatchView {
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-radius: 5px;
  margin-left: 10px;
  width: 250px;
  padding: 16px 16px 16px 8px;
}
#details {
  width: 100%;
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

