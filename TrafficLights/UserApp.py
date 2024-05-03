import json
import os

from kivy.app import App
from kivy_garden.mapview import MapMarker, MapView
from kivy_garden.mapview.clustered_marker_layer import ClusteredMarkerLayer

TIMISOARA_LAT = 45.747231774279214
TIMISOARA_LON = 21.231679569701775


class UserApp(App):

    def build(self):
        # Create a MapView

        mapview = MapView(zoom=10, lat=TIMISOARA_LAT, lon=TIMISOARA_LON)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        black_tl_png = os.path.join(script_dir, 'venv', 'icons', 'BlackTL3.png')

        with open('filtered_trafficlight_response.json', 'r') as f:
            trafficlight_data = json.load(f)

        clustered_layer = ClusteredMarkerLayer()

        for feature in trafficlight_data["features"]:
            if "geometry" in feature and "coordinates" in feature["geometry"]:
                coordinates = feature["geometry"]["coordinates"]
                if len(coordinates) == 2:
                    marker = MapMarker(lat=coordinates[1], lon=coordinates[0], source=black_tl_png)
                    clustered_layer.add_marker(marker.lon, marker.lat, cls=MapMarker, options={'source': marker.source})

        mapview.add_layer(clustered_layer)

        return mapview
