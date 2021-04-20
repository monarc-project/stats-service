function drawRisksChart() {
  fetch("stats/risks.json?processor=risk_averages&days=365", {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then((resp) => resp.json())
  .then(function(resp_json) {
    // Display data for informational risks
    config_base_bar_chart_informational_risks["data"]["datasets"].push({
      label: "Current Risks",
      backgroundColor: ['rgb(214, 241, 7)', 'rgb(255, 188, 28)','rgb(253, 102, 31)'],
      data: [
        resp_json["current"]["informational"]["Low risks"],
        resp_json["current"]["informational"]["Medium risks"],
        resp_json["current"]["informational"]["High risks"]
      ]
    })
    config_base_bar_chart_informational_risks["data"]["datasets"].push({
      label: "Residual Risks",
      backgroundColor: ['rgb(214, 241, 7, 0.5)', 'rgb(255, 188, 28, 0.5)', 'rgb(253, 102, 31, 0.5)'],
      data: [
        resp_json["residual"]["informational"]["Low risks"],
        resp_json["residual"]["informational"]["Medium risks"],
        resp_json["residual"]["informational"]["High risks"]
      ]
    })

    var ctx_risks_info = document.getElementById("canvas-risks-info").getContext("2d");
    var chart_risks = new Chart(ctx_risks_info, config_base_bar_chart_informational_risks);

    // Display data for operational risks
    config_base_bar_chart_operational_risks["data"]["datasets"].push({
      label: "Current Risks",
      backgroundColor: ['rgb(214, 241, 7)', 'rgb(255, 188, 28)','rgb(253, 102, 31)'],
      data: [
        resp_json["current"]["operational"]["Low risks"],
        resp_json["current"]["operational"]["Medium risks"],
        resp_json["current"]["operational"]["High risks"]
      ]
    })
    config_base_bar_chart_operational_risks["data"]["datasets"].push({
      label: "Residual Risks",
      backgroundColor: ['rgb(214, 241, 7, 0.5)', 'rgb(255, 188, 28, 0.5)', 'rgb(253, 102, 31, 0.5)'],
      data: [
        resp_json["residual"]["operational"]["Low risks"],
        resp_json["residual"]["operational"]["Medium risks"],
        resp_json["residual"]["operational"]["High risks"]
      ]
    })
    var ctx_risks_op = document.getElementById("canvas-risks-op").getContext("2d");
    var chart_risks = new Chart(ctx_risks_op, config_base_bar_chart_operational_risks);

  }).catch((error) => {
    console.error('Error:', error);
  });
}
