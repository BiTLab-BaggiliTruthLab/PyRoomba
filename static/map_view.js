fetch('/map_json')
    .then(response => response.json())
    .then(data => {
        const borderLayer = data.umf.maps[0].points2d;
        const borderNums = data.umf.maps[0].borders[0].geometry.ids;

        const idToCoord = {};
        for (const point of borderLayer) {
            idToCoord[point.id] = point.coordinates;
        }

        const borderCoords = borderNums[0].map(id => idToCoord[id]);

        const traceBorder = {
            x: borderCoords.map(coord => coord[0]),
            y: borderCoords.map(coord => coord[1]),
            mode: 'lines',
            name: 'Border'
        };

        const layout = {
            title: 'Map View',
            xaxis: { title: 'X' },
            yaxis: { title: 'Y' }
        };

        const mapData = [traceBorder];

        Plotly.newPlot('map', mapData, layout);
    });
