// modal variables
var MOSPModal;
var unknowObjectModal;

// define some colors for the lines of the chart
var colors = colorSchemeGenerator();

function colorSchemeGenerator() {
    let opacity = 0.5;
    let colorRgbaScheme = [];
    let colorHexScheme = [...d3.schemeCategory10, ...d3.schemeDark2, ...d3.schemePaired];
    colorHexScheme.forEach(colorHex => {
      let rgb = d3.rgb(colorHex);
      let rgba = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${opacity})`;
      colorRgbaScheme.push(rgba);
    })
    return colorRgbaScheme;
}

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
var config_base_bar_chart = {
    data: {},
    type: 'bar',
    options: {
      responsive: true,
      indexAxis: 'y',
      scales: {
        y: {
            ticks: {
                mirror: 'true',
                z: 100,
                color: 'black',
                callback: function(value) {
                    let label = this.getLabelForValue(value);
                    let truncate = 100;
                    if (label.length > truncate) {
                      return label.substr(0, truncate) + '...';
                    }
                    return label;
                },
            }
        },
      },
      plugins : {
        legend: {
          display: false,
        }
      },
    },
};

var config_base_bar_chart_risks = {
  type: 'bar',
  data: {
    labels: ["Low", "Medium", "High"],
    datasets: []
  }
};

var config_base_evolution_chart = {
  type: 'line',
  data: {
    datasets: []
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
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
        position: 'right',
        align: 'start',
        labels: {
          fontFamily: "'Open Sans', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif"
        }
      }
    }
  }
}

var languageIndex = {fr:1,en:2,de:3, nl:4};

function getLabel(language, labels){

  let currentLanguage = languageIndex[language.toLowerCase()];
  if (labels['label' + currentLanguage]) {
    return labels['label' + currentLanguage];
  }else {
    return Object.values(labels).find(label => {
      if(label) {
        return label;
      }
    });
  };
}

function retrieve_information_from_mosp(query) {
  let uuid = query.object;
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
        resolve(getLabel(language, query.labels));
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      reject(Error(error));
    });;
  });
}

function mosp_lookup_by_label(label) {
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

function let_pie_charts_modals(object_uuid) {
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
        retrieve_information_from_mosp(item)
          .then(function(result_mosp) {
              charts[chart].by_uuid[item.object] = {"object": item}
              charts[chart].by_uuid[item.object]["translated_label"] = result_mosp;
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
                  backgroundColor: colors
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
