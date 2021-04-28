function drawEvolutionChart() {
  var limitDatasets = 15; // we limit the datasets to 15

  // fetch stats for threats (averages per threats per date)  and display the chart
  fetch("/stats/threats.json?processor=threat_average_on_date&days=180", {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then((resp) => resp.json())
  .then(function(resp_json) {
    let config = cloneDeep(config_base_evolution_chart);
    let ctx_threats = document.getElementById("canvas-threats").getContext("2d");
    ctx_threats.canvas.height = config.height;

    resp_json.map(threat =>
      threat.rate = threat.values
        .map(value => value.averageRate)
        .reduce((a, b) => a + b) / threat.values.length
    );

    let threats = resp_json
      .sort(function(a, b) {
        return b.rate - a.rate;
      })
      .slice(0, limitDatasets);

    updateEvolutionCharts(threats,limitDatasets,'threats',ctx_threats,config);
  }).catch((error) => {
    console.error('Error:', error);
  });

  // fetch stats for vulnerabilities (averages per vulnerabilities per date)  and display the chart
  fetch("/stats/vulnerabilities.json?processor=vulnerability_average_on_date&days=180", {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then((resp) => resp.json())
  .then(function(resp_json) {
    let config = cloneDeep(config_base_evolution_chart);
    let ctx_vulnerabilities = document.getElementById("canvas-vulnerabilities").getContext("2d");
    ctx_vulnerabilities.canvas.height = config.height;

    resp_json.map(vulnerability =>
      vulnerability.rate = vulnerability.values
        .map(value => value.averageRate)
        .reduce((a, b) => a + b) / vulnerability.values.length
    );

    let vulnerabilities = resp_json
      .sort(function(a, b) {
        return b.rate - a.rate;
      })
      .slice(0, limitDatasets);

    updateEvolutionCharts(vulnerabilities,limitDatasets,'vulnerabilities',ctx_vulnerabilities,config);

  }).catch((error) => {
    console.error('Error:', error);
  });
}
