function drawRisksChart() {
  fetch("stats/risks.json?processor=risk_averages&days=365", {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then((resp) => resp.json())
  .then(function(resp_json) {
    let ctx_risks_info = document.getElementById("canvas-risks-info").getContext("2d");
    let ctx_risks_op = document.getElementById("canvas-risks-op").getContext("2d");

    let configInfoRisks = cloneDeep(config_base_bar_chart_risks);
    let configOPRisks = cloneDeep(config_base_bar_chart_risks);

    // Display data for informational risks
    configInfoRisks.data.datasets.push({
      label: "Current Risks",
      backgroundColor: ['rgb(214, 241, 7)', 'rgb(255, 188, 28)','rgb(253, 102, 31)'],
      data: [
        resp_json["current"]["informational"]["Low risks"],
        resp_json["current"]["informational"]["Medium risks"],
        resp_json["current"]["informational"]["High risks"]
      ]
    });
    configInfoRisks.data.datasets.push({
      label: "Residual Risks",
      backgroundColor: ['rgb(214, 241, 7, 0.5)', 'rgb(255, 188, 28, 0.5)', 'rgb(253, 102, 31, 0.5)'],
      data: [
        resp_json["residual"]["informational"]["Low risks"],
        resp_json["residual"]["informational"]["Medium risks"],
        resp_json["residual"]["informational"]["High risks"]
      ]
    })

    let chartInfoRisks = new Chart(ctx_risks_info, configInfoRisks);

    // Display data for operational risks
    configOPRisks.data.datasets.push({
      label: "Current Risks",
      backgroundColor: ['rgb(214, 241, 7)', 'rgb(255, 188, 28)','rgb(253, 102, 31)'],
      data: [
        resp_json["current"]["operational"]["Low risks"],
        resp_json["current"]["operational"]["Medium risks"],
        resp_json["current"]["operational"]["High risks"]
      ]
    })
    configOPRisks.data.datasets.push({
      label: "Residual Risks",
      backgroundColor: ['rgb(214, 241, 7, 0.5)', 'rgb(255, 188, 28, 0.5)', 'rgb(253, 102, 31, 0.5)'],
      data: [
        resp_json["residual"]["operational"]["Low risks"],
        resp_json["residual"]["operational"]["Medium risks"],
        resp_json["residual"]["operational"]["High risks"]
      ]
    })
    let chartOpRisks = new Chart(ctx_risks_op, configOPRisks);

  }).catch((error) => {
    console.error('Error:', error);
  });
}
