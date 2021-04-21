function drawVulnerabilitiesChart() {
  let ctx = document.getElementById("vulnerabilities-chart").getContext('2d');
  let topVulnerabilitiesInput = document.getElementById("topVulnerabilities")
  let allVulnerabilities = [];
  let valueTop = topVulnerabilitiesInput.value;
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
          let activePoints = charts.vulnerabilities.canvas.getElementsAtEventForMode(evt, 'point', charts.vulnerabilities.canvas.options);
          let firstPoint = activePoints[0];
          let object_label = charts.vulnerabilities.canvas.data.labels[firstPoint.index];
          mosp_lookup_by_label(object_label)
          .then(function(result_mosp) {
            let_pie_charts_modals(result_mosp);
          })
        }
      },
  };

  fetch("stats/vulnerabilities.json?processor=vulnerability_average_on_date&last_stats=1", {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
      },
  })
  .then((resp) => resp.json())
  .then(function(resp_json) {
      allVulnerabilities = resp_json;
      allVulnerabilities.sort(function(a, b) {
        return b.averages.averageRate - a.averages.averageRate;
      })

      updateChart(allVulnerabilities, valueTop, 'vulnerabilities', ctx, config);

  }).catch((error) => {
      console.error('Error:', error);
  });

  topVulnerabilitiesInput.onchange = function() {
      valueTop = topVulnerabilitiesInput.value;
      updateChart(allVulnerabilities, valueTop, 'vulnerabilities', ctx, config);
  }
}
