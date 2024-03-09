import math
import os
import json
import random
import re
from math import radians, cos, sin, sqrt
from kivy.clock import Clock
from kivy.app import App
from kivy_garden.mapview import MapView, MapMarker
from pathfinder import RouteView as rv


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def find_nearest_building(victim_lat, victim_lon, victim_type):
    with open('markers_data.json') as f:
        markers_data = json.load(f)

    nearest_building_name = None
    nearest_building_distance = float('inf')

    for building in markers_data['features'][victim_type]:
        building_lat = building['lat']
        building_lon = building['lon']
        distance = calculate_distance(victim_lat, victim_lon, building_lat, building_lon)
        if distance < nearest_building_distance:
            nearest_building_distance = distance
            nearest_building_name = building['name']

    return nearest_building_name

class MapApp(App):
    def build(self):
        # Create a MapView on Timisoara
        mapview = MapView(zoom=20, lat=45.74801789330893, lon=21.231333561092747, map_source='osm')
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_test = os.path.join(script_dir, 'image.png')

        marker_test = MapMarker(lat=45.74801789330893, lon=21.231333561092747, source=img_test)
        mapview.add_marker(marker_test)

        # Load the JSON data from the file
        with open('markers_data.json', 'r') as infile:
            data = json.load(infile)

        # Loop through each location type (hospital, police, firemen)
        for location_type, locations in data['features'].items():
            # Check the location type and display different information based on it
            if location_type == 'hospital':
                img_hospital = os.path.join(script_dir, 'hospital.png')
                print("Hospital Locations:")
                for location in locations:
                    name = location['name']
                    lat = location['lat']
                    lon = location['lon']
                    print(f"Name: {name}")
                    print(f"Latitude: {lat}, Longitude: {lon}")
                    marker_hospital = MapMarker(lat=lat, lon=lon, source=img_hospital)
                    mapview.add_marker(marker_hospital)
            elif location_type == 'police':
                img_police = os.path.join(script_dir, 'police.png')
                print("Police Locations:")
                for location in locations:
                    name = location['name']
                    lat = location['lat']
                    lon = location['lon']
                    print(f"Name: {name}")
                    print(f"Latitude: {lat}, Longitude: {lon}")
                    marker_police = MapMarker(lat=lat, lon=lon, source=img_police)
                    mapview.add_marker(marker_police)
            elif location_type == 'firemen':
                img_firemen = os.path.join(script_dir, 'firemen.png')
                print("Firemen Locations:")
                for location in locations:
                    name = location['name']
                    lat = location['lat']
                    lon = location['lon']
                    print(f"Name: {name}")
                    print(f"Latitude: {lat}, Longitude: {lon}")
                    marker_firemen = MapMarker(lat=lat, lon=lon, source=img_firemen)
                    mapview.add_marker(marker_firemen)
            else:
                print(f"Unknown Location Type: {location_type}")



        def add_random_marker(dt):
            # Center coordinates
            lat_center = 45.74801789330893
            lon_center = 21.231333561092747

            # Radius in meters
            radius = 10000

            # Generate random coordinates within the specified radius
            r = radius * sqrt(random.uniform(0, 1))
            theta = random.uniform(0, 2 * 3.141592653589793)  # Random angle in radians

            # Convert to Cartesian coordinates
            x = r * cos(theta)
            y = r * sin(theta)

            # Convert Cartesian coordinates to latitude and longitude offsets
            lat_offset = y / 111111  # Approx. 111111 meters per degree latitude
            lon_offset = x / (111111 * cos(radians(lat_center)))  # Approx. 111111 meters per degree longitude at equator

            # Calculate the random coordinates
            lat = lat_center + lat_offset
            lon = lon_center + lon_offset

            # Choose a random marker type
            victim_type = random.choice(["police_victim", "firemen_victim", "hospital_victim"])

            # Create a map marker based on the chosen type
            if victim_type == "police_victim":
                script_dir = os.path.dirname(os.path.abspath(__file__))
                img_police_victim = os.path.join(script_dir, 'police_victim.png')
                marker_victim = MapMarker(lat=lat, lon=lon, source=img_police_victim)
            elif victim_type == "firemen_victim":
                script_dir = os.path.dirname(os.path.abspath(__file__))
                img_firemen_victim = os.path.join(script_dir, 'firemen_victim.png')
                marker_victim = MapMarker(lat=lat, lon=lon,source=img_firemen_victim)
            else:  # "hospital_victim"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                img_hospital_victim = os.path.join(script_dir, 'hospital_victim.png')
                marker_victim = MapMarker(lat=lat, lon=lon, source=img_hospital_victim)
            mapview.add_marker(marker_victim)



            nearest_building = find_nearest_building(lat,lon,re.sub(r'_victim$', '', victim_type))
            print("Nearest building for the victim:", nearest_building)

        Clock.schedule_interval(add_random_marker, 5)

        return mapview

if __name__ == '__main__':
    MapApp().run()
