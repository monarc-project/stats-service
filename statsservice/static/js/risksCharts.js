function drawRisksChart() {
  let allRisks = [];

  let ctx_risks_info = document.getElementById("canvas-risks-info").getContext("2d");
  let configInfoRisks = cloneDeep(config_base_bar_chart_risks);
  let exportInfoRisksPNG = document.getElementById("exportInfoRisksPNG");
  let exportInfoRisksCSV = document.getElementById("exportInfoRisksCSV");

  let ctx_risks_op = document.getElementById("canvas-risks-op").getContext("2d");
  let configOPRisks = cloneDeep(config_base_bar_chart_risks);
  let exportOpRisksPNG = document.getElementById("exportOpRisksPNG");
  let exportOpRisksCSV = document.getElementById("exportOpRisksCSV");

  fetch("stats/risks.json?processor=risk_averages&days=365", {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then((resp) => resp.json())
  .then(function(resp_json) {
    allRisks = resp_json;
    // Display data for informational risks
    configInfoRisks.data.datasets.push({
      label: "Current Risks",
      backgroundColor: ['rgb(214, 241, 7)', 'rgb(255, 188, 28)','rgb(253, 102, 31)'],
      data: [
        allRisks["current"]["informational"]["Low risks"],
        allRisks["current"]["informational"]["Medium risks"],
        allRisks["current"]["informational"]["High risks"]
      ]
    });
    configInfoRisks.data.datasets.push({
      label: "Residual Risks",
      backgroundColor: ['rgb(214, 241, 7, 0.5)', 'rgb(255, 188, 28, 0.5)', 'rgb(253, 102, 31, 0.5)'],
      data: [
        allRisks["residual"]["informational"]["Low risks"],
        allRisks["residual"]["informational"]["Medium risks"],
        allRisks["residual"]["informational"]["High risks"]
      ]
    })

    ctx_risks_info.canvas.height = configInfoRisks.height;
    charts.infoRisks.canvas = new Chart(ctx_risks_info, configInfoRisks);

    // Display data for operational risks
    configOPRisks.data.datasets.push({
      label: "Current Risks",
      backgroundColor: ['rgb(214, 241, 7)', 'rgb(255, 188, 28)','rgb(253, 102, 31)'],
      data: [
        allRisks["current"]["operational"]["Low risks"],
        allRisks["current"]["operational"]["Medium risks"],
        allRisks["current"]["operational"]["High risks"]
      ]
    })
    configOPRisks.data.datasets.push({
      label: "Residual Risks",
      backgroundColor: ['rgb(214, 241, 7, 0.5)', 'rgb(255, 188, 28, 0.5)', 'rgb(253, 102, 31, 0.5)'],
      data: [
        allRisks["residual"]["operational"]["Low risks"],
        allRisks["residual"]["operational"]["Medium risks"],
        allRisks["residual"]["operational"]["High risks"]
      ]
    })
    ctx_risks_op.canvas.height = configOPRisks.height;
    charts.opRisks.canvas = new Chart(ctx_risks_op, configOPRisks);

  }).catch((error) => {
    console.error('Error:', error);
  });

  exportInfoRisksPNG.onclick = function() {
    let filename = `information_Risks.png`;
    exportPNG('infoRisks',filename)
  }
  exportInfoRisksCSV.onclick = function() {
    let filename = 'information_Risks.csv';
    let currentValues = {}
    let residualValues = {}

    Object.keys(allRisks.current.informational).forEach(risk => {
      currentValues[risk] = allRisks.current.informational[risk].toString().replace(/\./g, ',');
      residualValues[risk] = allRisks.residual.informational[risk].toString().replace(/\./g, ',');
    });

    let currentRisks = { risks: 'Current Risks', ...currentValues};
    let residualRisks = { risks: 'Residual Risks', ...residualValues};
    let jsonFormatted = [currentRisks,residualRisks];
    exportCSV(jsonFormatted,filename)
  }
  exportOpRisksPNG.onclick = function() {
    let filename = `operational_Risks.png`;
    exportPNG('opRisks',filename)
  }
  exportOpRisksCSV.onclick = function() {
    let filename = 'operational_Risks.csv';
    let currentValues = {}
    let residualValues = {}

    Object.keys(allRisks.current.operational).forEach(risk => {
      currentValues[risk] = allRisks.current.operational[risk].toString().replace(/\./g, ',');
      residualValues[risk] = allRisks.residual.operational[risk].toString().replace(/\./g, ',');
    });

    let currentRisks = { risks: 'Current Risks', ...currentValues};
    let residualRisks = { risks: 'Residual Risks', ...residualValues};
    let jsonFormatted = [currentRisks,residualRisks];
    exportCSV(jsonFormatted,filename)
  }
}
