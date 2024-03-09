from kivy.app import App
from kivy.graphics import Line, Color, InstructionGroup
import requests

class MapLine(InstructionGroup):
    def __init__(self, mapview, route_coordinates, **kwargs):
        super(MapLine, self).__init__(**kwargs)
        self.mapview = mapview
        self.route_coordinates = route_coordinates
        self.line = Line(points=[], width=2)
        self.add(Color(0, 0, 0.5, 1))
        self.add(self.line)
        self.update_line()
        mapview.bind(zoom=self.update_line, center=self.update_line, on_touch_down=self.update_line,
                     on_touch_up=self.update_line, on_touch_move=self.update_line, on_map_relocated=self.update_line)

    def update_line(self, *args):
        self.line.points = []
        for lon, lat in self.route_coordinates:
            x, y = self.mapview.get_window_xy_from(lat, lon, self.mapview.zoom)
            self.line.points.extend([x, y])


class RouteView(App):
    def fetch_route_distance(self, lat1, lon1, lat2, lon2):
        # Use OpenRouteService API to fetch the route
        api_key = "5b3ce3597851110001cf62483878a54e67844685a1beda093eac41af"
        url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={lon1},{lat1}&end={lon2},{lat2}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            distance = distance = data['features'][0]['properties']['segments'][0]['distance']
            return distance
        else:
            print("Failed to fetch route")
            return -1

    def fetch_route(self, lat1, lon1, lat2, lon2):
        # Use OpenRouteService API to fetch the route
        api_key = "5b3ce3597851110001cf62483878a54e67844685a1beda093eac41af"
        url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={lon1},{lat1}&end={lon2},{lat2}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            route = data["features"][0]["geometry"]["coordinates"]
            return route
        else:
            print("Failed to fetch route")
            return []

    def draw_route(self, mapview, route_coordinates):
        map_line = MapLine(mapview, route_coordinates)
        mapview.canvas.add(map_line)


if __name__ == "__main__":
    RouteView().run()
