function drawThreatsChart() {
  let myChart;
  let ctx = document.getElementById("threats-chart").getContext('2d');
  let topThreatsInput = document.getElementById("topThreats")
  let valueTop = topThreatsInput.value;
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
      allThreats = resp_json;
      allThreats.sort(function(a, b) {
          return b.averages.averageRate - a.averages.averageRate;
      });

      updateChart();

  }).catch((error) => {
      console.error('Error:', error);
  });

  function  updateChart() {
    let threats_by_uuid = {};
    let chart_data = {};
    let resp_json_sorted = allThreats.slice(0, parseInt(valueTop));

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
        });
    });

    // wait that we have all responses from MOSP
    Promise.all(promises).then(function() {
        resp_json_sorted.map(function(elem) {
          chart_data[threats_by_uuid[elem["object"]].translated_label] = elem['averages']['averageRate'];
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
  }

  topThreatsInput.onchange = function() {
      valueTop = topThreatsInput.value;
      updateChart();
  }
}
