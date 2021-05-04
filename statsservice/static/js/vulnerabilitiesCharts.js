function drawVulnerabilitiesChart() {
  let allVulnerabilities = [];
  let ctx = document.getElementById("vulnerabilities-chart").getContext('2d');
  let topVulnerabilitiesInput = document.getElementById("topVulnerabilities");
  let displayVulnerabilitiesBy = document.getElementById("displayVulnerabilitiesBy");
  let orderVulnerabilitiesBy = document.getElementById("orderVulnerabilitiesBy");
  let exportVulnerabilitiesPNG = document.getElementById("exportVulnerabilitiesPNG");
  let exportVulnerabilitiesCSV = document.getElementById("exportVulnerabilitiesCSV");

  let sortParams = {
    valueTop: topVulnerabilitiesInput.value,
    valueDisplay : displayVulnerabilitiesBy.value,
    valueOrder: orderVulnerabilitiesBy.value,
  }

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

  let config = cloneDeep(config_base_bar_chart);
  config.options.onClick = specificOptions.onClick;

  fetch("stats/vulnerabilities.json?processor=vulnerability_average_on_date&last_stats=1", {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
      },
  })
  .then((resp) => resp.json())
  .then(function(resp_json) {
      allVulnerabilities = resp_json;
      updateChart(allVulnerabilities, sortParams, 'vulnerabilities', ctx, config);

  }).catch((error) => {
      console.error('Error:', error);
  });

  topVulnerabilitiesInput.onchange = function() {
      sortParams.valueTop = topVulnerabilitiesInput.value;
      updateChart(allVulnerabilities, sortParams, 'vulnerabilities', ctx, config);
  }

  displayVulnerabilitiesBy.onchange = function() {
      sortParams.valueDisplay = displayVulnerabilitiesBy.value;
      updateChart(allVulnerabilities, sortParams, 'vulnerabilities', ctx, config);
  }
  orderVulnerabilitiesBy.onchange = function() {
      sortParams.valueOrder = orderVulnerabilitiesBy.value;
      updateChart(allVulnerabilities, sortParams, 'vulnerabilities', ctx, config);
  }
  exportVulnerabilitiesPNG.onclick = function() {
    let filename = `Top${topVulnerabilitiesInput.value}Vulnerabilities_${displayVulnerabilitiesBy.value}.png`;
    exportPNG('vulnerabilities',filename)
  }
  exportVulnerabilitiesCSV.onclick = function() {
    let filename = 'AllVulnerabilities.csv';
    let jsonFormatted = allVulnerabilities.map(vulnerability =>{
      let row = {
        vulnerability: getLabel(vulnerability.labels),
        qualification: vulnerability.averages.averageRate.toString().replace(/\./g, ','),
        ocurrence: vulnerability.averages.count.toString().replace(/\./g, ','),
        ['Max. associated risk level']: vulnerability.averages.maxRisk.toString().replace(/\./g, ','),
      }
      return row;
    });
    exportCSV(jsonFormatted,filename)
  }
}
