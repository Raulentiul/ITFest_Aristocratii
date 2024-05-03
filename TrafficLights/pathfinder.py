import math
from time import sleep

import keyboard
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Line, Color, InstructionGroup
import requests
from kivy_garden.mapview import MapMarker
from numpy import double


class ImageMarker(MapMarker):
    def __init__(self, **kwargs):
        super(ImageMarker, self).__init__(**kwargs)
        self.source = 'dot.png'
        self.size = (15, 15)
        self.offset = (0, 0)


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
            distance = data['features'][0]['properties']['segments'][0]['distance']
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
        return map_line

    def animate_marker(self, mapview, marker, marker2, map_line, route_coordinates, intersections_arr, intersection_dict):
        # try:
        print("IntersectingArray")
        print(intersections_arr)
        print(route_coordinates)
        print(len(route_coordinates))
        if marker is None:
            print("Marker is None")
            return False

        for lon, lat in route_coordinates:
            def update_marker(dt):
                marker.lon, marker.lat = lon, lat
                i = 0
                # curr_intersection = intersections_arr[i]
                # intersection_lat = intersection_dict[intersection][0]
                # intersection_lon = intersection_dict[intersection][1]
                if i < len(intersections_arr):
                    distance = double(((marker.lat - intersection_dict[intersections_arr[i]][1]) ** 2
                                 + (marker.lon - intersection_dict[intersections_arr[i]][0]) ** 2) ** 0.5)
                    print(marker.lat, marker.lon)
                    print(intersection_dict[intersections_arr[i]][1], intersection_dict[intersections_arr[i]][0])
                    print(distance)
                    if distance < 0.002:
                        delta_x = marker.lat - intersection_dict[intersections_arr[i]][0]
                        delta_y = marker.lon - intersection_dict[intersections_arr[i]][1]
                        #
                        # # Calculate the angle in radians using arctangent
                        angle_rad = math.atan2(delta_y, delta_x)
                        #
                        # # Convert angle to degrees
                        angle_deg = math.degrees(angle_rad)
                        #
                        # # Map the angle to the corresponding direction
                        angle_deg -= 90
                        if angle_deg < 0:
                            angle_deg += 360  # Ensure positive angle
                        if angle_deg > 360:
                            angle_deg -= 360
                        orientation = round(angle_deg / 90) % 4


                        #the connection to the arduino part
                        #stupid_arr = [0,1,2,3]
                        #requests.get(f"http://192.168.251.63/semaphore?s{stupid_arr[orientation]}={2}")
                        #print(orientation)
                        #stupid_arr.remove(orientation)
                        #for x in stupid_arr:
                            #requests.get(f"http://192.168.251.63/semaphore?s{x}={1}")
                        #end of connection


                        # if intersection_dict[intersections_arr[i]]  == 49:
                        #     stupid_arr = [0,1,2,3]
                        #     requests.get(f"http://192.168.251.63/semaphore?s{stupid_arr[orientation]}={2}")
                        #     print(orientation)
                        #     stupid_arr.remove(orientation)
                        #     for x in stupid_arr:
                        #         requests.get(f"http://192.168.251.63/semaphore?s{x}={1}")
                    print(intersections_arr[i])

                    if distance <= 0.0007:
                        i += 1

                    mapview.trigger_update(full=True)

            if keyboard.is_pressed('s'):
                while True:
                    if keyboard.is_pressed('p'):
                        break

            Clock.schedule_once(update_marker, 0.1)
            sleep(0.1)  # Adjust this value to control the speed of the animation
        Clock.schedule_once(lambda dt: mapview.remove_marker(marker))
        Clock.schedule_once(lambda dt: mapview.remove_marker(marker2))
        Clock.schedule_once(lambda dt: mapview.canvas.remove(map_line))
        Clock.schedule_once(lambda dt: mapview.trigger_update(full=True), 0.05)

    def create_marker(self, mapview, marker1):
        marker = ImageMarker(lat=marker1['lat'], lon=marker1['lon'])
        mapview.add_marker(marker)
        return marker
