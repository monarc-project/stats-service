function drawVulnerabilitiesChart() {
  let myChart;
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
          var activePoints = myChart.getElementsAtEventForMode(evt, 'point', myChart.options);
          var firstPoint = activePoints[0];
          var object_label = myChart.data.labels[firstPoint.index];
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

      updateChart();

  }).catch((error) => {
      console.error('Error:', error);
  });

  function  updateChart() {
      let vulnerabilities_by_uuid = {};
      let chart_data = {};
      let resp_json_sorted = allVulnerabilities.slice(0, parseInt(valueTop));

      var promises = resp_json_sorted.map(function(vulnerability) {
        return retrieve_information_from_mosp(vulnerability.object)
        .then(function(result_mosp) {
          vulnerabilities_by_uuid[vulnerability.object] = {"object": vulnerability}
          if (result_mosp) {
            vulnerabilities_by_uuid[vulnerability.object]["translated_label"] = result_mosp
          } else {
            vulnerabilities_by_uuid[vulnerability.object]["translated_label"] = vulnerability.labels.label2;
          }
          return vulnerability.object;
        })
      })

      // wait that we have all responses from MOSP
      Promise.all(promises).then(function() {
          resp_json_sorted.map(function(elem) {
            chart_data[vulnerabilities_by_uuid[elem["object"]].translated_label] = elem['averages']['averageRate'];
          });

          let data = {
            labels: Object.keys(chart_data),
            datasets: [{
                data: Object.values(chart_data),
                borderWidth: 1,
                backgroundColor: chartColors
            }]
          };

          if (myChart) {
            myChart.config.data = data;
            myChart.update();
          }else {
            config.data = data;
            myChart = new Chart(ctx,config);
          }
      });
  };

  topVulnerabilitiesInput.onchange = function() {
      valueTop = topVulnerabilitiesInput.value;
      updateChart();
  }
}
