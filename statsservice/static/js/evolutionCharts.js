function drawEvolutionChart() {

  var color = Chart.helpers.color;

  var charts_config = {
    type: 'line',
    data: {
      datasets: []
    },
    options: {
      scales: {
        x: {
          type: 'time',
          max: Date.now(),
          time: {
            unit: 'month',
            displayFormats: {
              quarter: 'MM YYYY'
            }
          }
        }
      },
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          align: 'start',
          labels: {
            fontFamily: "'Open Sans', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif"
          }
        }
      }
    }
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
    // retrieve the labels from MOSP corresponding to the UUID in the result with a promise
    // (we limit the datasets to the number of previously defined colors)
    threats_by_uuid = {}
    var promises = resp_json.slice(0, chartColors.length).map(function(threat) {
      return retrieve_information_from_mosp(threat.object, "EN")
      .then(function(result_mosp) {
        threats_by_uuid[threat.object] = {"object": threat}
        threats_by_uuid[threat.object]["translated_label"] = result_mosp
        return threat.object;
      })
    })

    // wait that we have all responses from MOSP
    Promise.all(promises).then(function(results) {
      // initializes a configuration variable for the chart
      var config_threats = JSON.parse(JSON.stringify(charts_config));
      // construct the datasets
      datasets = [];
      Object.keys(threats_by_uuid)
      .map(function(threat_uuid, index) {
        data = [];
        dataset = {
          "label": threats_by_uuid[threat_uuid]["translated_label"],
          "backgroundColor": color(chartColors[index]).alpha(0.5).rgbString(),
          "borderColor": chartColors[index],
          "fill": false,
        };

        threats_by_uuid[threat_uuid]["object"]['values']
        .sort(function(a, b) {
          return new Date(a.date) - new Date(b.date) ;
        })
        .map(function(elem) {
          data.push({
            x: new Date(elem.date),
            y: elem.averageRate
          })
        });
        dataset["data"] = data;
        datasets.push(dataset);
      })

      // finally set the datasets in the config variable
      config_threats["data"]["datasets"] = datasets;

      document.getElementById("spinner-threats").remove();

      // draw the chart
      var ctx_threats = document.getElementById("canvas-threats").getContext("2d");
      var chart_threats = new Chart(ctx_threats, config_threats);

      // var legend = chart_threats.generateLegend();
      // document.getElementById("my-legend-con").innerHTML = legend;
    })
  }).catch((error) => {
    console.error('Error:', error);
  });;


  // fetch stats for vulnerabilities (averages per vulnerabilities per date)  and display the chart
  fetch("/stats/vulnerabilities.json?processor=vulnerability_average_on_date&days=180", {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then((resp) => resp.json())
  .then(function(resp_json) {
    // retrieve the labels from MOSP corresponding to the UUID in the result with a promise
    // (we limit the datasets to the number of previously defined colors)
    vulnerabilities_by_uuid = {}
    var promises = resp_json.slice(0, chartColors.length).map(function(vulnerability) {
      return retrieve_information_from_mosp(vulnerability.object, "")
      .then(function(result_mosp) {
        vulnerabilities_by_uuid[vulnerability.object] = {"object": vulnerability}
        vulnerabilities_by_uuid[vulnerability.object]["translated_label"] = result_mosp
        return vulnerability.object;
      })
    })

    Promise.all(promises).then(function(results) {
      // initializes a configuration variable for the chart
      var config_vulnerabilities = JSON.parse(JSON.stringify(charts_config));
      // construct the datasets
      datasets = [];
      Object.keys(vulnerabilities_by_uuid).map(function(vulnerability_uuid, index) {
        data = [];
        dataset = {
          "label": vulnerabilities_by_uuid[vulnerability_uuid]["translated_label"],
          "backgroundColor": color(chartColors[index]).alpha(0.5).rgbString(),
          "borderColor": chartColors[index],
          "fill": false,
        };

        vulnerabilities_by_uuid[vulnerability_uuid]["object"]['values']
        .sort(function(a, b) {
          return new Date(a.date) - new Date(b.date) ;
        })
        .map(function(elem) {
          data.push({
            x: new Date(elem.date),
            y: elem.averageRate
          })
        });
        dataset["data"] = data;
        datasets.push(dataset);
      })

      // finally set the datasets in the config variable
      config_vulnerabilities["data"]["datasets"] = datasets;

      document.getElementById("spinner-vulnerabilities").remove();

      // draw the chart
      var ctx_vulnerabilities = document.getElementById("canvas-vulnerabilities").getContext("2d");
      var chart_vulnerabilities = new Chart(ctx_vulnerabilities, config_vulnerabilities);
    })


  }).catch((error) => {
    console.error('Error:', error);
  });;


}
