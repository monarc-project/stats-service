function drawThreatsChart() {
  let myChart;
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

  fetch("stats/threats.json?processor=threat_average_on_date&last_stats=1", {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then((resp) => resp.json())
  .then(function(resp_json) {
      let ctx = document.getElementById("threats-pie-chart").getContext('2d');
      let topThreatsInput = document.getElementById("topThreats")
      let valueTop = topThreatsInput.value;
      topThreatsInput.onchange = function() {
        valueTop = topThreatsInput.value;
        resp_json_sorted = resp_json.slice(0, parseInt(valueTop));
        updateChart();
      }
      var resp_json_sorted = resp_json
        .sort(function(a, b) {
          return b.averages.averageRate - a.averages.averageRate;
        })
        .slice(0, parseInt(valueTop));

      updateChart();

      function  updateChart() {
        let threats_by_uuid = {};
        let pie_chart_data = {};

        var promises = resp_json_sorted.map(function(threat) {
          return retrieve_information_from_mosp(threat.object)
          .then(function(result_mosp) {
            threats_by_uuid[threat.object] = {"object": threat}
            threats_by_uuid[threat.object]["translated_label"] = result_mosp

            if (result_mosp) {
              threats_by_uuid[threat.object]["translated_label"] = result_mosp
            } else {
              threats_by_uuid[threat.object]["translated_label"] = threat.labels.label2
            }
            return threat.object;
          })
        })

        // wait that we have all responses from MOSP
        Promise.all(promises).then(function() {
          resp_json_sorted.map(function(elem) {
            pie_chart_data[threats_by_uuid[elem["object"]].translated_label] = elem['averages']['averageRate'];
          });
          let data = {
            labels: Object.keys(pie_chart_data),
            datasets: [{
                data: Object.values(pie_chart_data),
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
      }
      // retrieve the labels from MOSP corresponding to the UUID in the result with a promise

  }).catch((error) => {
    console.error('Error:', error);
  });
}
