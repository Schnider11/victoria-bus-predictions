from dataclasses import dataclass

import numpy as np


@dataclass
class Vector:
    x: np.float32
    y: np.float32

    def dot(self, other: Vector) -> np.float32:
        return self.x * other.x + self.y * other.y
    
    def length(self) -> np.float32:
        return math.sqrt(self.dot(self))

    def proj(self, other: Vector) -> Vector:
        # Projection of `self` onto `other`
        other_squared = pow(other.length(), 2)
        return Vector(
            other.x * self.dot(other) / other_squared,
            other.y  * self.dot(other) / other_squared
        )

@dataclass
class Point:
    x: np.float32
    y: np.float32

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        # Also is distance from self to other
        return Point(other.x - self.x, other.y - self.y)

    def distance(self, other: Point) -> np.int16:
        return math.sqrt(
            pow(other.x - self.x, 2) + pow(other.y - self.y, 2)
        )

@dataclass
class GCS:
    lat: np.float32
    lon: np.float32

    def to_point(self) -> Point:
        R = 6367 # Earth's radius in KM

        # Longitude and latitude are given in degrees, convert to radians
        self.lat = self.lat * np.pi / 180
        self.lon = self.lon * np.pi / 180

        return Point(
            R * np.cos(self.lat) * np.cos(self.lon),
            R * np.cos(self.lat) * np.sin(self.lon)
        )

@dataclass
class AbstractStop:
    stop_sequence: str
    arrival_timestamp: np.int64
    departure_timestamp: np.int64
    stop_id: str
    
    def __eq__(self, other) -> bool:
        return self.stop_sequence == other.stop_sequence \
            and self.stop_id == other.stop_id

    def to_csv(self) -> str:
        return ",".join(
            [
                self.stop_sequence,
                self.arrival_timestamp,
                self.departure_timestamp,
                self.stop_id,
            ]
        )

@dataclass
class AbstractTrip:
    trip_id: str
    start_time: str
    start_date: str
    route_id: str
    direction_id: int
    stops: list[Stop]

    def __eq__(self, other) -> bool:
        return self.trip_id == other.trip_id \
            and self.start_date == other.start_date
        
    def len(self) -> int:
        return len(self.stops)

    def to_csv(self) -> str:
        csv_str = ""
        for s in self.stops:
            csv_str += ",".join(
                [
                    self.trip_id,
                    self.start_time,
                    self.start_date,
                    self.route_id,
                    self.direction_id,
                    s.to_csv()
                ]
            ) + "\n"

        return csv_str

def create_base_abstract_trip(df_row):
    return TripUpdate(
        df_row.trip_id,
        df_row.start_time,
        df_row.start_date,
        df_row.route_id,
        df_row.direction_id,
        []
    )

def process_abstract_trip(df_slice):
    t = None

    for row in df_slice.itertuples(index=False):
        if t is None:
            t = create_base_trip(row)

        t.stops.append(
            AbstractStop(
                row.stop_sequence,
                row.arrival_timestamp,
                row.departure_timestamp,
                row.stop_id,
            )
        )

    return t

@dataclass
class Stop:
    stop_sequence: str
    arrival_timestamp: str
    arrival_delay: str
    departure_timestamp: str
    departure_delay: str
    stop_id: str
    stop_schedule_relationship: str

    def to_csv(self) -> str:
        return ",".join(
            [
                self.stop_sequence,
                self.arrival_timestamp,
                self.arrival_delay,
                self.departure_timestamp,
                self.departure_delay,
                self.stop_id,
                self.stop_schedule_relationship
            ]
        )

@dataclass
class TripUpdate:
    trip_id: str
    fetch_time: str
    start_time: str
    start_date: str
    schedule_relationship: str
    route_id: str
    direction_id: int
    stops: list[Stop]

    def __eq__(self, other) -> bool:
        return self.trip_id == other.trip_id \
            and self.fetch_time == other.fetch_time \
            and self.start_date == other.start_date

    def to_csv(self) -> str:
        csv_str = ""
        for s in self.stops:
            csv_str += ",".join(
                [
                    self.trip_id,
                    self.fetch_time,
                    self.start_time,
                    self.start_date,
                    self.schedule_relationship,
                    self.route_id,
                    self.direction_id,
                    s.to_csv()
                ]
            ) + "\n"

        return csv_str

def create_base_trip(df_row):
    return TripUpdate(
        df_row.trip_id,
        df_row.fetch_time,
        df_row.start_time,
        df_row.start_date,
        df_row.schedule_relationship,
        df_row.route_id,
        df_row.direction_id,
        []
    )

def process_trip(df_slice):
    t = None
    stops = []

    for row in df_slice.itertuples(index=False):
        if t is None:
            t = create_base_trip(row)

        t.stops.append(
            Stop(
                row.stop_sequence,
                row.arrival_timestamp,
                row.arrival_delay,
                row.departure_timestamp,
                row.departure_delay,
                row.stop_id,
                row.stop_schedule_relationship
            )
        )

    return t

@dataclass
class VehicleUpdate:
    speed: np.float32
    pos: GCS
    current_stop_sequence: np.int8
    current_status: str
    timestamp: np.int64
    congestion_level: str
    stop_id: str

@dataclass
class VehicleUpdates:
    trip_id: str
    vehicle_id: str
    start_time: str
    start_date: str
    route_id: str
    direction_id: int
    updates: list[VehicleUpdate]

def create_base_vehicle_updates(df_row):
    return VehicleUpdates(
        df_row.trip_id,
        df_row.vehicle_id,
        df_row.start_time,
        df_row.start_date,
        df_row.route_id,
        df_row.direction_id,
        []
    )

def process_vehicle_updates(df_slice):
    t = None
    stops = []

    for row in df_slice.itertuples(index=False):
        if t is None:
            t = create_base_vehicle_updates(row)

        t.updates.append(
            VehicleUpdate(
                row.speed,
                GCS(lat=row.latitude, lon=row.longiutde),
                row.current_stop_sequence,
                row.current_status,
                row.timestamp,
                row.congestion_level,
                row.stop_id
            )
        )

    return t


@dataclass
class InterpolatedStop:
    stop_sequence: np.int8
    arrival_timestamp: np.int64
    arrival_delay: np.int64
    departure_timestamp: np.int64
    departure_delay: np.int64
    stop_id: str

    # Automatically reject sets that would not make sense where
    # the arrival time is after the departure time and vice-versa
    # def __setattr__(self, prop, val):
    #     if prop == "arrival_timestamp":
    #         if val <= self.departure_timestamp:
    #             super().__setattr__(prop, val)
    #     elif prop == "departure_timestamp":
    #         if val >= self.arrival_timestamp:
    #             super().__setattr__(prop, val)
    #     else:
    #         super().__setattr__(prop, val)
    
    def to_csv(self) -> str:
        return ",".join(
            [
                str(self.stop_sequence),
                str(self.arrival_timestamp),
                str(self.arrival_delay),
                str(self.departure_timestamp),
                str(self.departure_delay),
                self.stop_id
            ]
        )

def create_base_interpolated_stop(stop_sequence: np.int8, stop_id: str):
    return InterpolatedStop(
        stop_sequence,
        np.inf,
        np.inf,
        stop_id
    )

@dataclass
class ActualTrip:
    trip_id: str
    vehicle_id: str
    start_time: str
    start_date: str
    route_id: str
    direction_id: int
    stops: list[InterpolatedStop]
    
    def to_csv(self) -> str:
        csv_str = ""
        for s in self.stops:
            csv_str += ",".join(
                [
                    self.trip_id,
                    self.vehicle_id,
                    self.start_time,
                    self.start_date,
                    self.route_id,
                    self.direction_id,
                    s.to_csv()
                ]
            ) + "\n"

        return csv_str

def create_base_actual_trip(vechileupdates: VehicleUpdates):
    return ActualTrip(
        vechileupdates.trip_id,
        vechileupdates.vehicle_id,
        vechileupdates.start_time,
        vechileupdates.start_date,
        vechileupdates.route_id,
        vechileupdates.direction_id,
        []
    )

def process_actual_trip(
    at: ActualTrip,
    interpolated_stops: list[InterpolatedStop]
):
    for stop in interpolated_stops:
        at.stops.append(
            InterpolatedStops(
                np.int8(stop.stop_sequence),
                np.int64(stop.arrival_timestamp),
                np.int64(stop.departure_timestamp),
                stop.stop_id
            )
        )