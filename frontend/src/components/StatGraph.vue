<template>
  <div id="container">
    <canvas id="chart" width="350" height="350"> </canvas>
  </div>
</template>

<script>
import Chart from 'chart.js'

export default {
  name: 'statGraph',
  props: ["statType"],
  data: function() {
    return {
      fullStats: null,
      chart: null,
      lineColors: {
        gold: 'rgba(255, 200, 0, 1)',
        cs: 'rgba(200, 0, 100, 1)', 
        kill: 'rgba(255, 0, 0, 1)',
        death: 'rgba(20, 20, 20, 1)',
        assist: 'rgba(0, 0, 255, 1)',
        wardplace: 'rgba(180, 255, 50, 1)',
        wardkill: 'rgba(255, 180, 50, 1)',
      }
    }
  },
  mounted() {
    this.chart = new Chart('chart', {
      type: 'line',
      data: {
        datasets: []
      },
      options: {
        scales: {
          xAxes: [{
            type: 'time',
            position: 'bottom',
          }]
        }
      }
    })
  },
  methods: {
    updateChartScale(lastTimeStepMillis) {
      var hours = lastTimeStepMillis / 3600000; 
      var stepSize = Math.ceil(hours * 60 / 10);
      var timeFormat = hours > 1 ? 'H:mm:ss' : 'mm:ss';
      this.chart.options.scales.xAxes[0].time = {
        stepSize: stepSize,
        unit: 'minute',
        displayFormats: {
          minute: timeFormat
        },
        tooltipFormat: timeFormat,
        }
    },
    setTimelineData(jsonData) {
      this.fullStats = jsonData;
      this.updateChart();
    },
    updateChart() {
      var chartData = {datasets: [{label: this.statType.displayName, data: [], fill: false, 
        borderColor: this.lineColors[this.statType.paramName],
        pointBorderColor: this.lineColors[this.statType.paramName],
        pointBackgroundColor: 'rgba(255, 255, 255, 1)',
        }]};
      for (var i = 0; i < this.fullStats.length; i++) {
        var millis = this.fullStats[i]["timestamp"]
        // This is due to my time zone?
        var xval = millis - 3600000;
        var yval = this.fullStats[i][this.statType.paramName];
        chartData["datasets"][0]["data"].push({x: xval, y: yval});
        if (i == this.fullStats.length - 1) {
          this.updateChartScale(millis);
        }
      }
      this.chart.data = chartData;
      this.chart.update();
    },
  }, watch: {
    statType: function(val) {
      this.updateChart();
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
canvas {
  display: inline;
  position: absolute;
  top: 0;
  left: 0;
}
</style>

