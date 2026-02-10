

import random
import datetime

MIN_120V = 114
MAX_120V = 126
MIN_240V = 228
MAX_240V = 252

BROWNOUT_MIN_120V = 108
BROWNOUT_MAX_120V = 113.5
BROWNOUT_MIN_240V = 216
BROWNOUT_MAX_240V = 227

SEVERE_BROWNOUT_MIN_120V = 95
SEVERE_BROWNOUT_MAX_120V = 107.9
SEVERE_BROWNOUT_MIN_240V = 190
SEVERE_BROWNOUT_MAX_240V = 215.9

OVERVOLT_MIN_120V = 126.1
OVERVOLT_MAX_120V = 132.0
OVERVOLT_MIN_240V = 252.1
OVERVOLT_MAX_240V = 264.0

SEVERE_OVERVOLT_MIN_120V = 132.1
SEVERE_OVERVOLT_MAX_120V = 140.0
SEVERE_OVERVOLT_MIN_240V = 264.1
SEVERE_OVERVOLT_MAX_240V = 280.0

OUTAGE_DAY_RANGE = (1, 28)
OUTAGE_HOUR_RANGE = (0, 23)
OUTAGE_DURATION_RANGE = (1, 24)

EVENT_DAY_RANGE = (1, 28)
EVENT_HOUR_RANGE = (0, 23)
EVENT_DURATION_RANGE = (1, 24)

class VoltageProfile:

    def __init__(self):

        self.profile_120v = {}
        self.profile_240v = {}
        self.quality_flags = {}

        self.current_month = None

        self.outage_start = None
        self.outage_end = None

        self.brownout_start = None
        self.brownout_end = None

        self.severe_brownout_start = None
        self.severe_brownout_end = None

        self.overvolt_start = None
        self.overvolt_end = None

        self.severe_overvolt_start = None
        self.severe_overvolt_end = None

    def overlaps_any_event(self, start, end):

        events = [
            (self.outage_start, self.outage_end),
            (self.brownout_start, self.brownout_end),
            (self.severe_brownout_start, self.severe_brownout_end),
            (self.overvolt_start, self.overvolt_end),
            (self.severe_overvolt_start, self.severe_overvolt_end),
        ]

        for ev_start, ev_end in events:
            if ev_start and ev_end:
                if start < ev_end and end > ev_start:
                    return True

        return False

    def is_in_range(self, ts, start, end):
        return start and end and start <= ts < end

    def reset_month_if_needed(self, simulation_date):

        month_key = (simulation_date.year, simulation_date.month)

        if self.current_month != month_key:
            self.current_month = month_key

            self.outage_start = self.outage_end = None
            self.brownout_start = self.brownout_end = None
            self.severe_brownout_start = self.severe_brownout_end = None
            self.overvolt_start = self.overvolt_end = None
            self.severe_overvolt_start = self.severe_overvolt_end = None

    def generate_event_once(self, label):

        for _ in range(10):

            day = random.randint(*EVENT_DAY_RANGE)
            hour = random.randint(*EVENT_HOUR_RANGE)
            duration = random.randint(*EVENT_DURATION_RANGE)

            start = datetime.datetime(self.current_month[0], self.current_month[1], day, hour)
            end = start + datetime.timedelta(hours=duration)

            if not self.overlaps_any_event(start, end):
                print(f"[{label}] {start} -> {end} ({duration}h)")
                return start, end

        print(f"[{label} - FORCED OVERLAP]")
        return start, end

    def generate_monthly_events_if_needed(self):

        if not self.outage_start:
            self.outage_start, self.outage_end = self.generate_event_once("GRID_OUTAGE")

        if not self.severe_brownout_start:
            self.severe_brownout_start, self.severe_brownout_end = self.generate_event_once("BROWNOUT_SEVERE")

        if not self.brownout_start:
            self.brownout_start, self.brownout_end = self.generate_event_once("BROWNOUT")

        if not self.severe_overvolt_start:
            self.severe_overvolt_start, self.severe_overvolt_end = self.generate_event_once("OVERVOLTAGE_SEVERE")

        if not self.overvolt_start:
            self.overvolt_start, self.overvolt_end = self.generate_event_once("OVERVOLTAGE")

    def is_grid_outage(self, ts):
        return self.is_in_range(ts, self.outage_start, self.outage_end)

    def is_brownout(self, ts):
        return self.is_in_range(ts, self.brownout_start, self.brownout_end)

    def is_severe_brownout(self, ts):
        return self.is_in_range(ts, self.severe_brownout_start, self.severe_brownout_end)

    def is_overvolt(self, ts):
        return self.is_in_range(ts, self.overvolt_start, self.overvolt_end)

    def is_severe_overvolt(self, ts):
        return self.is_in_range(ts, self.severe_overvolt_start, self.severe_overvolt_end)

    def generate_daily_profile(self, simulation_date):

        self.reset_month_if_needed(simulation_date)
        self.generate_monthly_events_if_needed()

        for hour in range(24):

            timestamp = datetime.datetime.combine(simulation_date, datetime.time(hour=hour))

            if self.is_grid_outage(timestamp):

                self.profile_120v[hour] = 0.0
                self.profile_240v[hour] = 0.0
                self.quality_flags[hour] = "grid_outage"

            elif self.is_severe_brownout(timestamp):

                dev_120 = random.uniform(
                    SEVERE_BROWNOUT_MIN_120V / 120.0,
                    SEVERE_BROWNOUT_MAX_120V / 120.0
                )

                self.profile_120v[hour] = 120 * dev_120
                self.profile_240v[hour] = 240 * dev_120
                self.quality_flags[hour] = "brownout_severe"

            elif self.is_brownout(timestamp):

                dev_120 = random.uniform(
                    BROWNOUT_MIN_120V / 120.0,
                    BROWNOUT_MAX_120V / 120.0
                )

                self.profile_120v[hour] = 120 * dev_120
                self.profile_240v[hour] = 240 * dev_120
                self.quality_flags[hour] = "brownout"

            elif self.is_severe_overvolt(timestamp):

                dev_120 = random.uniform(
                    SEVERE_OVERVOLT_MIN_120V / 120.0,
                    SEVERE_OVERVOLT_MAX_120V / 120.0
                )

                self.profile_120v[hour] = 120 * dev_120
                self.profile_240v[hour] = 240 * dev_120
                self.quality_flags[hour] = "overvoltage_severe"

            elif self.is_overvolt(timestamp):

                dev_120 = random.uniform(
                    OVERVOLT_MIN_120V / 120.0,
                    OVERVOLT_MAX_120V / 120.0
                )

                self.profile_120v[hour] = 120 * dev_120
                self.profile_240v[hour] = 240 * dev_120
                self.quality_flags[hour] = "overvoltage"

            else:

                dev_120 = random.uniform(
                    MIN_120V / 120.0,
                    MAX_120V / 120.0
                )

                self.profile_120v[hour] = 120 * dev_120
                self.profile_240v[hour] = 240 * dev_120
                self.quality_flags[hour] = "normal"

    def get_voltage_120v(self, hour):
        return self.profile_120v[hour]

    def get_voltage_240v(self, hour):
        return self.profile_240v[hour]

    def get_quality_flag(self, hour):
        return self.quality_flags.get(hour, "normal")





