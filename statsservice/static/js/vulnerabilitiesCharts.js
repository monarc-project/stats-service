function drawVulnerabilitiesChart() {
  let allVulnerabilities = [];
  let ctx = document.getElementById("vulnerabilities-chart").getContext('2d');
  let topVulnerabilitiesInput = document.getElementById("topVulnerabilities")
  let valueTop = topVulnerabilitiesInput.value;
  let displayVulnerabilitiesBy = document.getElementById("displayVulnerabilitiesBy")
  let valueDisplay = displayVulnerabilitiesBy.value;
  let specificOptions = {
      onClick: function(evt) {
        let activePoints = charts.vulnerabilities.canvas.getElementsAtEventForMode(evt, 'point', charts.vulnerabilities.canvas.options);
        let firstPoint = activePoints[0];
        let object_label = charts.vulnerabilities.canvas.data.labels[firstPoint.index];
        mosp_lookup_by_label(object_label)
        .then(function(result_mosp) {
          let_pie_charts_modals(result_mosp);
        })
      }
  };

  config_base_bar_chart.options.onClick = specificOptions.onClick;

  let config = Object.assign({},config_base_bar_chart)

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
        return b.averages[valueDisplay] - a.averages[valueDisplay];
      });

      updateChart(allVulnerabilities, valueTop, valueDisplay, 'vulnerabilities', ctx, config);

  }).catch((error) => {
      console.error('Error:', error);
  });

  topVulnerabilitiesInput.onchange = function() {
      valueTop = topVulnerabilitiesInput.value;
      updateChart(allVulnerabilities, valueTop, valueDisplay, 'vulnerabilities', ctx, config);
  }

  displayVulnerabilitiesBy.onchange = function() {
      valueDisplay = displayVulnerabilitiesBy.value;
      allVulnerabilities.sort(function(a, b) {
        return b.averages[valueDisplay] - a.averages[valueDisplay];
      });
      updateChart(allVulnerabilities, valueTop, valueDisplay, 'vulnerabilities', ctx, config);
  }
}
