function drawThreatsChart() {
  let ctx = document.getElementById("threats-chart").getContext('2d');
  let topThreatsInput = document.getElementById("topThreats")
  let valueTop = topThreatsInput.value;
  let config = {
      data: {},
      type: 'bar',
      options: {
        indexAxis: 'y',
        plugins : {
          legend: {
            display: false,
          }
        },
        onClick: function(evt) {
          let activePoints = charts.threats.getElementsAtEventForMode(evt, 'point', charts.threats.options);
          let firstPoint = activePoints[0];
          let object_label = charts.threats.data.labels[firstPoint.index];
          mosp_lookup_by_label(object_label)
          .then(function(result_mosp) {
            let_pie_charts_modals(result_mosp);
          })
        }
      },
  };

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
          return b.averages.averageRate - a.averages.averageRate;
      });

      updateChart(allThreats, valueTop, 'threats', ctx, config);

  }).catch((error) => {
      console.error('Error:', error);
  });

  topThreatsInput.onchange = function() {
      valueTop = topThreatsInput.value;
      updateChart(allThreats, valueTop, 'threats', ctx, config);
  }
}
