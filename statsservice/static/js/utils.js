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
    infoRisks: {
      canvas: undefined
    },
    opRisks: {
      canvas: undefined
    },
    threatsEvolution: {
      by_uuid: [],
      canvas: undefined
    },
    vulnerabilitiesEvolution: {
      by_uuid: [],
      canvas: undefined
    },
};

// basic configuration of the charts (threats and vulnerabilities)
var config_base_bar_chart = {
    type: 'bar',
    data: {},
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      scales: {
        y: {
            ticks: {
                mirror: 'true',
                z: 100,
                color: 'black',
                callback: function(value) {
                    let label = this.getLabelForValue(value);
                    return truncateText(label,100);
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
  height: 171,
  data: {
    labels: ["Low", "Medium", "High"],
    datasets: []
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
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
          },
          tooltipFormat: 'MMMM DD YYYY'
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
        },
        onHover: function(ev, legendItem, legend){
          let index = legendItem.datasetIndex;
          let dataset = legend.chart.getDatasetMeta(index)._dataset;
          let tooltip = document.getElementById(`legendTooltip-${dataset.chart}`);
          let windowsSize = window.innerWidth;
          if (windowsSize <= 780 || dataset.label.length != dataset.longLabel.length) {
            let y = ev.y - 40;
            tooltip.style.visibility  = 'visible';
            tooltip.textContent  = dataset.longLabel;
            tooltip.style.left = ev.x + "px";
            tooltip.style.top = y + "px";
          }
        },
        onLeave: function(ev, legendItem, legend){
          let index = legendItem.datasetIndex;
          let dataset = legend.chart.getDatasetMeta(index)._dataset;
          let tooltip = document.getElementById(`legendTooltip-${dataset.chart}`);
          tooltip.style.visibility  = 'hidden';
        }
      }
    }
  }
}

var languageIndex = {fr:1,en:2,de:3, nl:4};

var language = userLanguage();

function userLanguage() {
  let language;
  try {
    language = navigator.language.split("-")[0].toUpperCase()
    if (!Object.keys(languageIndex).includes(language.toLowerCase())) {
      language = 'EN';
    }
  } catch (e) {
    language = 'EN';
  }
  return language;
}

function getLabel(labels){
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
        resolve(getLabel(query.labels));
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
 * @param {object} sortParams sort params of chart display.
 * @param {string} chart Name of items (threats,vulnerabilities).
 * @param {object} ctx Canvas context.
 * @param {object} config Chart config.
 */

function updateChart(allData, sortParams, chart, ctx, config) {
  let chart_data = {};
  let promises = [];
  if (sortParams.valueTop > allData.length) {
    sortParams.valueTop = allData.length
  }
  let dataSorted = allData
    .filter(data => data.averages[sortParams.valueDisplay] > 0)
    .sort(function(a, b) {
      if (sortParams.valueOrder == 'lowest') {
        config.options.scales.y.reverse = true;
        return a.averages[sortParams.valueDisplay] - b.averages[sortParams.valueDisplay];
      }
      config.options.scales.y.reverse = false;
      return b.averages[sortParams.valueDisplay] - a.averages[sortParams.valueDisplay];
    })
    .slice(0, parseInt(sortParams.valueTop));

  dataSorted.forEach((item,index) => {
    if (!Object.keys(charts[chart].by_uuid).includes(item.object) ) {
      promises.push(
        retrieve_information_from_mosp(item)
          .then(function(result_mosp) {
              charts[chart].by_uuid[item.object] = {object: item}
              charts[chart].by_uuid[item.object].translated_label = result_mosp;
          })
      );
    }

    Promise.all(promises).then(function() {
        if (!chart_data[charts[chart].by_uuid[item.object].translated_label]) {
          chart_data[charts[chart].by_uuid[item.object].translated_label] = item.averages[sortParams.valueDisplay];
        }
        if (index == sortParams.valueTop - 1) {
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

/**
 * Update evolution charts
 *
 * @param {Array} chartData elements sorted from MOSP query.
 * @param {object} sortParams sort params of chart display.
 * @param {string} chart Name of items (threatsEvolution,vulnerabilitiesEvolution).
 * @param {object} ctx Canvas context.
 * @param {object} config Chart config.
 */

function updateEvolutionCharts (allData, sortParams, chart, ctx, config){
  let limitDatasets = 20; // we limit the datasets to 20
  let promises = [];
  let datasets = [];

  if (limitDatasets > allData.length) {
    limitDatasets = allData.length
  }

  allData.map(data =>
    data.rate = data.values
      .map(value => value[sortParams.valueDisplay])
      .reduce((a, b) => a + b) / data.values.length
  );

  let dataSorted = allData
    .filter(data => data.rate > 0)
    .sort(function(a, b) {
      if (sortParams.valueOrder == 'lowest') {
        config.options.plugins.legend.reverse = true;
        return a.rate - b.rate;
      }
      config.options.plugins.legend.reverse = false;
      return b.rate - a.rate;
    })
    .slice(0, limitDatasets);

  dataSorted.forEach((item,index) => {
    let data = [];

    if (!Object.keys(charts[chart].by_uuid).includes(item.object) ) {
      promises.push(
        // retrieve the labels from MOSP corresponding to the UUID in the result with a promise
        retrieve_information_from_mosp(item)
          .then(function(result_mosp) {
              charts[chart].by_uuid[item.object] = {object: item};
              charts[chart].by_uuid[item.object].translated_label = result_mosp;
          })
      );
    }

    Promise.all(promises)
    .then(function() {
        // construct the datasets
        let dataset = {
          chart : chart,
          longLabel :  charts[chart].by_uuid[item.object].translated_label,
          label: truncateText(charts[chart].by_uuid[item.object].translated_label, 40),
          backgroundColor: colors[index],
          borderColor: colors[index],
        };

        charts[chart].by_uuid[item.object].object.values
        .sort(function(a, b) {
          return new Date(a.date) - new Date(b.date) ;
        })
        .map(function(elem) {
          data.push({
            x: elem.date,
            y: elem[sortParams.valueDisplay]
          });
        });

        dataset.data = data;
        datasets.push(dataset);

        // finally set the datasets in the config variable
        if (index + 1 == limitDatasets) {
            if (charts[chart].canvas) {
              charts[chart].canvas.config.data.datasets = datasets;
              charts[chart].canvas.update();
            }else {
              document.getElementById("spinner-" + chart).remove();
              document.getElementById(`inverse${chart}Selection`).style.display = 'inline-block';
              config.data.datasets = datasets;
              charts[chart].canvas = new Chart(ctx,config);
            }
        }
    })
  });
}

function truncateText(text,width) {
    let label = text;
    if (text.length > width) {
      return label.substr(0, width) + '...';
    }
    return label;
}

function exportPNG(chart,filename) {
    let file = document.createElement('a');
    file.href = charts[chart].canvas.toBase64Image();
    file.download = filename;
    file.click();
}

function exportCSV(json,filename){
    let file = document.createElement("a");
    let csvContent = "data:text/csv;charset=UTF-8,\uFEFF";
    let replace = (key, value) => value === null ? '' : value;
    let header = Object.keys(json[0])

    let csv = [
      header.join(','), // header row first
      ...json.map(row => header.map(fieldName => JSON.stringify(row[fieldName], replace)).join(','))
    ].join('\r\n')

    file.href = encodeURI(csvContent + csv);
    file.download = filename;
    file.click();
}
