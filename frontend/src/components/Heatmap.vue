<template>
  <div id="container">
    <img v-if="mapId != 0" :src="minimapImgUrl"/>
    <!-- Height and Width set here determine reference for data points! -->
    <canvas id="canvas" width="350" height="350"> </canvas>
  </div>
</template>

<script>
import * as simpleheat from 'simpleheat';

export default {
  name: 'heatmap',
  props: ["eventType", "mapId"],
  data: function() {
    return {
      fullTimeline: null,
      positions: [],
      heat: null,
      miny: {
        11: -120,
        10: 0,
        12: -19,
      },
      minx: {
        11: -120,
        10: 0,
        12: -28,
      },
      maxy: {
        11: 14980,
        10: 15398,
        12: 12858,
      },
      maxx: {
        11: 14870,
        10: 15398,
        12: 12849,
      },
    }
  }, computed: {
    minimapImgUrl: function() {
      return "http://ddragon.leagueoflegends.com/cdn/9.8.1/img/map/map" + this.mapId.toString() + ".png"
    },
  },
  mounted() {
    this.heat = simpleheat('canvas');
    this.redraw();
  },
  methods: {
    setTimelineData(jsonData) {
      this.fullTimeline = jsonData;
      this.updateHeatmap();
    },
    updateHeatmap() {
      this.positions = [];
      for (var i = 0; i < this.fullTimeline[this.eventType].length; i++) {
        var rawPos = this.fullTimeline[this.eventType][i]["position"];
        this.positions.push(this.getHeatmapPoint(rawPos));
      }
      this.redraw();
    },
    clear() {
      this.positions = [];
      this.redraw();
    },
    redraw() {
      this.heat.radius(15, 10);
      this.heat.data(this.positions).draw();
    },
    getHeatmapPoint(rawPos) {
      var width = 350;
      var height = 350;
      // TODO: y-axis is reversed???
      var transX = this.map_range(rawPos["x"], this.minx[this.mapId], this.maxx[this.mapId], 0, width);
      var transY = this.map_range(rawPos["y"], this.miny[this.mapId], this.maxy[this.mapId], height, 0);
      return [transX, transY, 0.5]
    },
    map_range(value, low1, high1, low2, high2) {
      return low2 + (high2 - low2) * (value - low1) / (high1 - low1);
    }
  }, watch: {
    eventType: function(val) {
      this.updateHeatmap();
    }
  }
}
</script>

<style scoped>
#container {
  width: 350px;
  height: 350px;
  position: relative;
}
img {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: -10;
  top: 0;
  left: 0;
  border-radius: 5px;
}
canvas {
  display: inline;
  position: absolute;
  top: 0;
  left: 0;
}
</style>

