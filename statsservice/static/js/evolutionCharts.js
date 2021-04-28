function drawEvolutionChart() {
  let allThreats = [];
  let config_threats = cloneDeep(config_base_evolution_chart);
  let ctx_threats = document.getElementById("canvas-threatsEvolution").getContext("2d");
  let displayThreatsEvolutionBy = document.getElementById("displayThreatsEvolutionBy")
  let orderThreatsEvolutionBy = document.getElementById("orderThreatsEvolutionBy")
  let sortParams_threats = {
    valueDisplay : displayThreatsEvolutionBy.value,
    valueOrder_threats : orderThreatsEvolutionBy.value,
  }

  let allVulnerabilities = [];
  let config_vulnerabilities = cloneDeep(config_base_evolution_chart);
  let ctx_vulnerabilities = document.getElementById("canvas-vulnerabilitiesEvolution").getContext("2d");
  let displayVulnerabilitiesEvolutionBy = document.getElementById("displayVulnerabilitiesEvolutionBy")
  let orderVulnerabilitiesEvolutionBy = document.getElementById("orderVulnerabilitiesEvolutionBy")
  let sortParams_vulnerabilities = {
    valueDisplay : displayVulnerabilitiesEvolutionBy.value,
    valueOrder : orderVulnerabilitiesEvolutionBy.value,
  }

  // fetch stats for threats (averages per threats per date)  and display the chart
  fetch("/stats/threats.json?processor=threat_average_on_date&days=180", {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then((resp) => resp.json())
  .then(function(resp_json) {
    allThreats = resp_json;
    updateEvolutionCharts(allThreats,sortParams_threats,'threatsEvolution',ctx_threats,config_threats);
  }).catch((error) => {
    console.error('Error:', error);
  });

  displayThreatsEvolutionBy.onchange = function() {
      sortParams_threats.valueDisplay = displayThreatsEvolutionBy.value;
      updateEvolutionCharts(allThreats,sortParams_threats,'threatsEvolution',ctx_threats,config_threats);
  }
  orderThreatsEvolutionBy.onchange = function() {
      sortParams_threats.valueOrder = orderThreatsEvolutionBy.value;
      updateEvolutionCharts(allThreats,sortParams_threats,'threatsEvolution',ctx_threats,config_threats);
  }

  // fetch stats for vulnerabilities (averages per vulnerabilities per date)  and display the chart
  fetch("/stats/vulnerabilities.json?processor=vulnerability_average_on_date&days=180", {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then((resp) => resp.json())
  .then(function(resp_json) {
    allVulnerabilities = resp_json;
    updateEvolutionCharts(allVulnerabilities,sortParams_vulnerabilities,'vulnerabilitiesEvolution',ctx_vulnerabilities,config_vulnerabilities);
  }).catch((error) => {
    console.error('Error:', error);
  });

  displayVulnerabilitiesEvolutionBy.onchange = function() {
      sortParams_vulnerabilities.valueDisplay = displayVulnerabilitiesEvolutionBy.value;
      updateEvolutionCharts(allVulnerabilities,sortParams_vulnerabilities,'vulnerabilitiesEvolution',ctx_vulnerabilities,config_vulnerabilities);
  }

  orderVulnerabilitiesEvolutionBy.onchange = function() {
      sortParams_vulnerabilities.valueOrder = orderVulnerabilitiesEvolutionBy.value;
      updateEvolutionCharts(allVulnerabilities,sortParams_vulnerabilities,'vulnerabilitiesEvolution',ctx_vulnerabilities,config_vulnerabilities);
  }
}
