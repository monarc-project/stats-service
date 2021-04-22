function drawThreatsChart() {
  let allThreats = [];
  let ctx = document.getElementById("threats-chart").getContext('2d');
  let topThreatsInput = document.getElementById("topThreats")
  let valueTop = topThreatsInput.value;
  let displayThreatsBy = document.getElementById("displayThreatsBy")
  let valueDisplay = displayThreatsBy.value;
  let specificOptions = {
      onClick: function(evt) {
        let activePoints = charts.threats.canvas.getElementsAtEventForMode(evt, 'point', charts.threats.canvas.options);
        let firstPoint = activePoints[0];
        let object_label = charts.threats.canvas.data.labels[firstPoint.index];
        mosp_lookup_by_label(object_label)
        .then(function(result_mosp) {
          let_pie_charts_modals(result_mosp);
        })
      }
  };

  let config = cloneDeep(config_base_bar_chart);
  config.options.onClick = specificOptions.onClick;

  fetch("stats/threats.json?processor=threat_average_on_date&last_stats=1", {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
      },
  })
  .then((resp) => resp.json())
  .then(function(resp_json) {
      allThreats = resp_json;
      allThreats.sort(function(a, b) {
          return b.averages[valueDisplay] - a.averages[valueDisplay];
      });

      updateChart(allThreats, valueTop, valueDisplay, 'threats', ctx, config);

  }).catch((error) => {
      console.error('Error:', error);
  });

  topThreatsInput.onchange = function() {
      valueTop = topThreatsInput.value;
      updateChart(allThreats, valueTop, valueDisplay, 'threats', ctx, config);
  }

  displayThreatsBy.onchange = function() {
      valueDisplay = displayThreatsBy.value;
      allThreats.sort(function(a, b) {
          return b.averages[valueDisplay] - a.averages[valueDisplay];
      });
      updateChart(allThreats, valueTop, valueDisplay, 'threats', ctx, config);
  }
}
