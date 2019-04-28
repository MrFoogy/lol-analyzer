<template>
  <div id="container">
    <img src="http://ddragon.leagueoflegends.com/cdn/6.8.1/img/map/map11.png"/>
    <!-- Height and Width set here determine reference for data points! -->
    <canvas id="canvas" width="400" height="400"> </canvas>
  </div>
</template>

<script>
import * as simpleheat from 'simpleheat';

export default {
  name: 'heatmap',
  data: function() {
    return {
      positions: [],
      heat: null,
    }
  },
  mounted() {
    this.heat = simpleheat('canvas');
    this.redraw();
  },
  methods: {
    displayKills(jsonData) {
      this.positions = [];
      for (var i = 0; i < jsonData.length; i++) {
        var rawPos = jsonData[i]["position"];
        this.positions.push(this.getHeatmapPoint(rawPos));
      }
      this.redraw();
    },
    redraw() {
      this.heat.radius(15, 10);
      this.heat.data(this.positions).draw();
    },
    getHeatmapPoint(rawPos) {
      var minx = -120;
      var miny = -120;
      var maxx = 14870;
      var maxy = 14980;
      var width = 400;
      var height = 400;
      // TODO: y-axis is reversed???
      var transX = this.map_range(rawPos["x"], minx, maxx, 0, width);
      var transY = this.map_range(rawPos["y"], miny, maxy, height, 0);
      return [transX, transY, 0.5]
    },
    map_range(value, low1, high1, low2, high2) {
      return low2 + (high2 - low2) * (value - low1) / (high1 - low1);
    }
  }
}
</script>

<style scoped>
#container {
  width: 400px;
  height: 400px;
  position: relative;
}
img {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: -10;
  top: 0;
  left: 0;
}
canvas {
  display: inline;
  position: absolute;
  top: 0;
  left: 0;
}
</style>

