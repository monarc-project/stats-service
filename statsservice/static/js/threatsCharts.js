function drawThreatsChart() {
  let allThreats = [];
  let ctx = document.getElementById("threats-chart").getContext('2d');
  let topThreatsInput = document.getElementById("topThreats")
  let displayThreatsBy = document.getElementById("displayThreatsBy")
  let orderThreatsBy = document.getElementById("orderThreatsBy")
  let sortParams = {
    valueTop: topThreatsInput.value,
    valueDisplay : displayThreatsBy.value,
    valueOrder: orderThreatsBy.value,
  }

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
      updateChart(allThreats, sortParams, 'threats', ctx, config);

  }).catch((error) => {
      console.error('Error:', error);
  });

  topThreatsInput.onchange = function() {
      sortParams.valueTop = topThreatsInput.value;
      updateChart(allThreats, sortParams, 'threats', ctx, config);
  }

  displayThreatsBy.onchange = function() {
      sortParams.valueDisplay = displayThreatsBy.value;
      updateChart(allThreats, sortParams, 'threats', ctx, config);
  }

  orderThreatsBy.onchange = function() {
      sortParams.valueOrder = orderThreatsBy.value;
      updateChart(allThreats, sortParams, 'threats', ctx, config);
  }
}
