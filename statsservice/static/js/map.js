function drawMap() {
  let map = L.map('cyberweathermap').setView([49.5, 6.175], 7);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  var monarcIcon = L.icon({
      iconUrl: '/static/img/monarc-logo.png',
      // shadowUrl: 'leaf-shadow.png',
      iconSize:     [42, 42], // size of the icon
      // shadowSize:   [50, 64], // size of the shadow
      // iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
      // shadowAnchor: [4, 62],  // the same for the shadow
      popupAnchor:  [-3, -20] // point from which the popup should open relative to the iconAnchor
  });

  let translations = {};

  fetch("/map/clients.json", {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
      },
  })
  .then((resp) => resp.json())
  .then(function(resp_json) {
    resp_json.map(function(client){
      let promises = [];
      // sets UUIDs in labels as a fallback value
      var queries = [
        {"object": client.max_threat[1], "labels": client.max_threat[1]},
        {"object": client.max_vulnerability[1], "labels": client.max_vulnerability[1]}
      ];
      queries.map(function(item) {
        if (!(item.uuid in translations)) {
          // if not already translated
          promises.push(
            retrieve_information_from_mosp(item)
              // get the translation
              .then(function(result_mosp) {
                translations[item.object] = result_mosp;
              })
          );
        }
      })
      Promise.all(promises).then(function() {
        L.marker([client.latitude, client.longitude], {icon: monarcIcon})
        .addTo(map)
        .bindPopup('<b>#1 Threat:</b> ' +
                   translations[client.max_threat[1]] +
                   '<br /><b>#1 Vulnerability:</b> ' +
                   translations[client.max_vulnerability[1]]);
      })
    })
  })
}
