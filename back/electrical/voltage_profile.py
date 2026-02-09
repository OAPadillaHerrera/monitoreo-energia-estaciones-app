

import random
import datetime

MIN_120V = 114
MAX_120V = 126
MIN_240V = 228
MAX_240V = 252

OUTAGE_DAY_RANGE = (1, 28)
OUTAGE_HOUR_RANGE = (0, 23)
OUTAGE_DURATION_RANGE = (1, 24)

class VoltageProfile:

    def __init__(self):

        self.profile_120v = {}
        self.profile_240v = {}
        self.quality_flags = {}

        self.current_outage_month = None
        self.outage_start = None
        self.outage_end = None

    def generate_monthly_grid_outage_if_needed(self, simulation_date):
        
        month_key = (simulation_date.year, simulation_date.month)

        if self.current_outage_month != month_key:
            self.current_outage_month = month_key

            outage_day = random.randint(*OUTAGE_DAY_RANGE)
            outage_hour = random.randint(*OUTAGE_HOUR_RANGE)
            outage_duration = random.randint(*OUTAGE_DURATION_RANGE)

            self.outage_start = datetime.datetime(
                simulation_date.year,
                simulation_date.month,
                outage_day,
                outage_hour
            )

            self.outage_end = self.outage_start + datetime.timedelta(
                hours=outage_duration
            )

            print(
                f"[GRID OUTAGE] {self.outage_start} "
                f"-> {self.outage_end} "
                f"({outage_duration}h)"
            )

    def is_grid_outage(self, timestamp):
        if not self.outage_start or not self.outage_end:
            return False

        return self.outage_start <= timestamp < self.outage_end

    def generate_daily_profile(self, simulation_date):
        self.generate_monthly_grid_outage_if_needed(simulation_date)

        for hour in range(24):
            timestamp = datetime.datetime.combine(
                simulation_date,
                datetime.time(hour=hour)
            )

            if self.is_grid_outage(timestamp):
                self.profile_120v[hour] = 0.0
                self.profile_240v[hour] = 0.0
                self.quality_flags[hour] = "grid_outage"
            else:
                self.profile_120v[hour] = random.uniform(MIN_120V, MAX_120V)
                self.profile_240v[hour] = random.uniform(MIN_240V, MAX_240V)
                self.quality_flags[hour] = "normal"

    def get_voltage_120v(self, hour):
        return self.profile_120v[hour]

    def get_voltage_240v(self, hour):
        return self.profile_240v[hour]

    def get_quality_flag(self, hour):
        return self.quality_flags.get(hour, "normal")
