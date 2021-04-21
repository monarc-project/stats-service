// modal variables
var MOSPModal;
var unknowObjectModal;

// define some colors for the lines of the chart
var chartColors = [
  'rgba(230, 25, 75, 0.8)',
  'rgba(60, 180, 75, 0.8)',
  'rgba(255, 225, 25, 0.8)',
  'rgba(0, 130, 200, 0.8)',
  'rgba(245, 130, 48, 0.8)',
  'rgba(145, 30, 180, 0.8)',
  'rgba(70, 240, 240, 0.8)',
  'rgba(240, 50, 230, 0.8)',
  'rgba(210, 245, 60, 0.8)',
  'rgba(250, 190, 190, 0.8)',
  'rgba(0, 128, 128, 0.8)',
  'rgba(230, 190, 255, 0.8)',
  'rgba(170, 110, 40, 0.8)',
  'rgba(255, 250, 200, 0.8)',
  'rgba(128, 0, 0, 0.8)',
  'rgba(170, 255, 195, 0.8)',
  'rgba(128, 128, 0, 0.8)',
  'rgba(255, 215, 180, 0.8)',
  'rgba(0, 0, 128, 0.8)',
  'rgba(128, 128, 128, 0.8)',
  'rgba(0, 0, 0, 0.8)'
];

//  Object of charts canvas data
var charts = {
    threats: {
      by_uuid: [],
      canvas: undefined
    },
    vulnerabilities: {
      by_uuid: [],
      canvas: undefined
    },
};


// basic configuration of the charts (threats and vulnerabilities)
var config_base_bar_chart_informational_risks = {
  type: 'bar',
  data: {
    labels: ["Low", "Medium", "High"],
    datasets: []
  },
  options: {
    legend: { display: true },
    title: {
      display: true,
      text: 'Informational risks'
    }
  }
};


var config_base_bar_chart_operational_risks = {
  type: 'bar',
  data: {
    labels: ["Low", "Medium", "High"],
    datasets: []
  },
  options: {
    legend: { display: true },
    title: {
      display: true,
      text: 'Operational risks'
    }
  }
};


let retrieve_information_from_mosp = function(uuid) {
  language = "EN";
  try {
    language = navigator.language.split("-")[0].toUpperCase()
  } catch (e) {
    language = "EN";
  }
  return new Promise(function(resolve, reject) {
    fetch("https://objects.monarc.lu/api/v2/object/?language="+language+"&uuid="+uuid, {
      method: "GET",
      headers: {
        'Content-Type': 'text/plain',
      },
    })
    .then((resp) => resp.json())
    .then(function(mosp_result) {
      if (mosp_result["metadata"].count > 0) {
        resolve(mosp_result["data"][0].name);
      } else {
        resolve();
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      reject(Error(error));
    });;
  });
}

let mosp_lookup_by_label = function(label) {
  return new Promise(function(resolve, reject) {
    fetch("https://objects.monarc.lu/api/v2/object/?page=1&per_page=10&name="+label, {
      method: "GET",
      headers: {
        'Content-Type': 'text/plain',
      },
    })
    .then((resp) => resp.json())
    .then(function(mosp_result) {
      if (mosp_result["metadata"].count > 0) {
        resolve(mosp_result["data"][0].json_object.uuid);
      } else {
        resolve();
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      reject(Error(error));
    });;
  });
}

let let_pie_charts_modals = function(object_uuid) {
  if (object_uuid) {
    MOSPModal.show()
    document.getElementById("MOSPModalClose").onclick = function(){
    };
    document.getElementById("MOSPModalOK").onclick = function(){
      window.location = 'https://objects.monarc.lu/object/'+object_uuid;
    };
  } else {
    unknowObjectModal.show();
  }
}

function getModals() {
  MOSPModal = new bootstrap.Modal(document.getElementById('MOSPModal'), {
    keyboard: false
  })
  unknowObjectModal = new bootstrap.Modal(document.getElementById('unknowObjectModal'), {
    keyboard: false
  })
}

/**
 * Update chart
 *
 * @param {Array} allData All elements from MOSP query.
 * @param {number} valueTop Number of items to display.
 * @param {string} valueDisplay Average name to display.
 * @param {string} chart Name of items (threats,vulnerabilities).
 * @param {object} ctx Canvas context.
 * @param {object} config Chart config.
 */

function  updateChart(allData, valueTop, valueDisplay, chart, ctx, config) {
  let chart_data = {};
  let promises = [];
  if (valueTop > allData.length) {
    valueTop = allData.length
  }
  let resp_json_sorted = allData.slice(0, parseInt(valueTop));
  resp_json_sorted.forEach(item => {
    if (!Object.keys(charts[chart].by_uuid).includes(item.object) ) {
      promises.push(
        retrieve_information_from_mosp(item.object)
            .then(function(result_mosp) {
                charts[chart].by_uuid[item.object] = {"object": item}
                charts[chart].by_uuid[item.object]["translated_label"] = result_mosp

                if (result_mosp) {
                  charts[chart].by_uuid[item.object]["translated_label"] = result_mosp
                } else {
                  charts[chart].by_uuid[item.object]["translated_label"] = item.labels.label2
                }

                return item.object;
            })
      );
    }

    Promise.all(promises).then(function() {
        chart_data[charts[chart].by_uuid[item["object"]].translated_label] = item['averages'][valueDisplay];
          if (Object.keys(chart_data).length == valueTop) {
              let data = {
                labels: Object.keys(chart_data),
                datasets: [{
                    data: Object.values(chart_data),
                    borderWidth: 1,
                    backgroundColor: chartColors
                }]
              };

              if (charts[chart].canvas) {
                charts[chart].canvas.config.data = data;
                charts[chart].canvas.update();
              }else {
                config.data = data;
                charts[chart].canvas = new Chart(ctx,config);
              }
          }


    });
  })
}
