function drawEvolutionChart() {
  let allThreats = [];
  let config_threats = cloneDeep(config_base_evolution_chart);
  let ctx_threats = document.getElementById("canvas-threatsEvolution").getContext("2d");
  let displayThreatsEvolutionBy = document.getElementById("displayThreatsEvolutionBy")
  let orderThreatsEvolutionBy = document.getElementById("orderThreatsEvolutionBy")
  let inverseThreatsSelection = document.getElementById("inversethreatsEvolutionSelection");
  let exportThreatsEvolutionPNG = document.getElementById('exportThreatsEvolutionPNG');
  let exportThreatsEvolutionCSV = document.getElementById('exportThreatsEvolutionCSV');
  let sortParams_threats = {
    valueDisplay : displayThreatsEvolutionBy.value,
    valueOrder_threats : orderThreatsEvolutionBy.value,
  }

  let allVulnerabilities = [];
  let config_vulnerabilities = cloneDeep(config_base_evolution_chart);
  let ctx_vulnerabilities = document.getElementById("canvas-vulnerabilitiesEvolution").getContext("2d");
  let displayVulnerabilitiesEvolutionBy = document.getElementById("displayVulnerabilitiesEvolutionBy")
  let orderVulnerabilitiesEvolutionBy = document.getElementById("orderVulnerabilitiesEvolutionBy")
  let inverseVulnerabilitiesSelection = document.getElementById("inversevulnerabilitiesEvolutionSelection");
  let exportVulnerabilitiesEvolutionPNG = document.getElementById('exportVulnerabilitiesEvolutionPNG');
  let exportVulnerabilitiesEvolutionCSV = document.getElementById('exportVulnerabilitiesEvolutionCSV');
  let sortParams_vulnerabilities = {
    valueDisplay : displayVulnerabilitiesEvolutionBy.value,
    valueOrder : orderVulnerabilitiesEvolutionBy.value,
  }

  // fetch stats for threats (averages per threats per date)  and display the chart
  fetch(SITE_ROOT + "/stats/threats.json?processor=threat_average_on_date&days=180", {
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
  exportThreatsEvolutionPNG.onclick = function() {
    let filename = `EvolutionThreats_${displayThreatsEvolutionBy.value}.png`;
    exportPNG('threatsEvolution',filename)
  }
  exportThreatsEvolutionCSV.onclick = function() {
    let filename = `EvolutionThreats_${displayThreatsEvolutionBy.value}.csv`;
    let dates = [...new Set(allThreats.flatMap(threat => threat.values.map(value => value.date)))];
    let jsonFormatted = allThreats.map(threat =>{
      let row = {
        threat: getLabel(threat.labels),
      }
      dates.forEach(date =>{
        row[date] = '';
        threat.values.forEach(data => {
             if (data.date === date) {
               row[date] = data[displayThreatsEvolutionBy.value].toString().replace(/\./g, ',');
             }
        });
      });
      return row;
    });
    exportCSV(jsonFormatted,filename)
  }
  inverseThreatsSelection.onclick = function() {
      charts['threatsEvolution'].canvas.data.datasets.forEach(function(dataset,index) {
        let meta = charts['threatsEvolution'].canvas.getDatasetMeta(index);
        meta.hidden = !meta.hidden || null;
      });
      charts['threatsEvolution'].canvas.update();
  };

  // fetch stats for vulnerabilities (averages per vulnerabilities per date)  and display the chart
  fetch(SITE_ROOT + "/stats/vulnerabilities.json?processor=vulnerability_average_on_date&days=180", {
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
  exportVulnerabilitiesEvolutionPNG.onclick = function() {
    let filename = `EvolutionVulnerabilities_${displayVulnerabilitiesEvolutionBy.value}.png`;
    exportPNG('threatsEvolution',filename)
  }
  exportVulnerabilitiesEvolutionCSV.onclick = function() {
    let filename = `EvolutionVulnerabilities_${displayVulnerabilitiesEvolutionBy.value}.csv`;
    let dates = [...new Set(allVulnerabilities.flatMap(vulnerability => vulnerability.values.map(value => value.date)))];
    let jsonFormatted = allVulnerabilities.map(vulnerability =>{
      let row = {
        vulnerability: getLabel(vulnerability.labels),
      }
      dates.forEach(date =>{
        row[date] = '';
        vulnerability.values.forEach(data => {
             if (data.date === date) {
               row[date] = data[displayVulnerabilitiesEvolutionBy.value].toString().replace(/\./g, ',');
             }
        });
      });
      return row;
    });
    exportCSV(jsonFormatted,filename)
  }
  inverseVulnerabilitiesSelection.onclick = function() {
      charts['vulnerabilitiesEvolution'].canvas.data.datasets.forEach(function(dataset,index) {
        let meta = charts['vulnerabilitiesEvolution'].canvas.getDatasetMeta(index);
        meta.hidden = !meta.hidden || null;
      });
      charts['vulnerabilitiesEvolution'].canvas.update();
  };
}
