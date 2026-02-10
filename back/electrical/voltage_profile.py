
"""
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
"""


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

OUTAGE_DAY_RANGE = (1, 28)
OUTAGE_HOUR_RANGE = (0, 23)
OUTAGE_DURATION_RANGE = (1, 24)

BROWNOUT_DAY_RANGE = (1, 28)
BROWNOUT_HOUR_RANGE = (0, 23)
BROWNOUT_DURATION_RANGE = (1, 24)

SEVERE_BROWNOUT_DAY_RANGE = (1, 28)
SEVERE_BROWNOUT_HOUR_RANGE = (0, 23)
SEVERE_BROWNOUT_DURATION_RANGE = (1, 24)

class VoltageProfile:

    def __init__(self):

        self.profile_120v = {}
        self.profile_240v = {}
        self.quality_flags = {}

        self.current_outage_month = None
        self.outage_start = None
        self.outage_end = None

        self.current_brownout_month = None
        self.brownout_start = None
        self.brownout_end = None

        self.current_severe_brownout_month = None
        self.severe_brownout_start = None
        self.severe_brownout_end = None

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

    def is_fully_within_outage(self, start, end):

        if not self.outage_start or not self.outage_end:
            return False

        return start >= self.outage_start and end <= self.outage_end

    def generate_monthly_brownout_if_needed(self, simulation_date):

        month_key = (simulation_date.year, simulation_date.month)

        if self.current_brownout_month != month_key:

            self.current_brownout_month = month_key

            MAX_RETRIES = 5

            for _ in range(MAX_RETRIES):

                brownout_day = random.randint(*BROWNOUT_DAY_RANGE)
                brownout_hour = random.randint(*BROWNOUT_HOUR_RANGE)
                brownout_duration = random.randint(*BROWNOUT_DURATION_RANGE)

                start = datetime.datetime(
                    simulation_date.year,
                    simulation_date.month,
                    brownout_day,
                    brownout_hour
                )

                end = start + datetime.timedelta(hours=brownout_duration)

                if self.is_fully_within_outage(start, end):
                    continue

                self.brownout_start = start
                self.brownout_end = end

                print(
                    f"[BROWNOUT] {self.brownout_start} "
                    f"-> {self.brownout_end} "
                    f"({brownout_duration}h)"
                )

                return

            self.brownout_start = start
            self.brownout_end = end

            print(
                f"[BROWNOUT - OVERLAP] {self.brownout_start} "
                f"-> {self.brownout_end} "
                f"({brownout_duration}h)"
            )

    def generate_monthly_severe_brownout_if_needed(self, simulation_date):

        month_key = (simulation_date.year, simulation_date.month)

        if self.current_severe_brownout_month != month_key:

            self.current_severe_brownout_month = month_key

            MAX_RETRIES = 5

            for _ in range(MAX_RETRIES):

                day = random.randint(*SEVERE_BROWNOUT_DAY_RANGE)
                hour = random.randint(*SEVERE_BROWNOUT_HOUR_RANGE)
                duration = random.randint(*SEVERE_BROWNOUT_DURATION_RANGE)

                start = datetime.datetime(
                    simulation_date.year,
                    simulation_date.month,
                    day,
                    hour
                )

                end = start + datetime.timedelta(hours=duration)

                if self.is_fully_within_outage(start, end):
                    continue

                self.severe_brownout_start = start
                self.severe_brownout_end = end

                print(
                    f"[BROWNOUT_SEVERE] {self.severe_brownout_start} "
                    f"-> {self.severe_brownout_end} "
                    f"({duration}h)"
                )

                return

            self.severe_brownout_start = start
            self.severe_brownout_end = end

            print(
                f"[BROWNOUT_SEVERE - OVERLAP] {self.severe_brownout_start} "
                f"-> {self.severe_brownout_end} "
                f"({duration}h)"
            )

    def is_grid_outage(self, timestamp):

        if not self.outage_start or not self.outage_end:
            return False

        return self.outage_start <= timestamp < self.outage_end

    def is_severe_brownout(self, timestamp):

        if not self.severe_brownout_start or not self.severe_brownout_end:
            return False

        return self.severe_brownout_start <= timestamp < self.severe_brownout_end

    def is_brownout(self, timestamp):

        if not self.brownout_start or not self.brownout_end:
            return False

        return self.brownout_start <= timestamp < self.brownout_end

    def generate_daily_profile(self, simulation_date):

        self.generate_monthly_grid_outage_if_needed(simulation_date)
        self.generate_monthly_severe_brownout_if_needed(simulation_date)
        self.generate_monthly_brownout_if_needed(simulation_date)

        for hour in range(24):

            timestamp = datetime.datetime.combine(
                simulation_date,
                datetime.time(hour=hour)
            )

            if self.is_grid_outage(timestamp):

                self.profile_120v[hour] = 0.0
                self.profile_240v[hour] = 0.0
                self.quality_flags[hour] = "grid_outage"

            elif self.is_severe_brownout(timestamp):

                self.profile_120v[hour] = random.uniform(
                    SEVERE_BROWNOUT_MIN_120V, SEVERE_BROWNOUT_MAX_120V
                )

                self.profile_240v[hour] = random.uniform(
                    SEVERE_BROWNOUT_MIN_240V, SEVERE_BROWNOUT_MAX_240V
                )

                self.quality_flags[hour] = "brownout_severe"

            elif self.is_brownout(timestamp):

                self.profile_120v[hour] = random.uniform(
                    BROWNOUT_MIN_120V, BROWNOUT_MAX_120V
                )

                self.profile_240v[hour] = random.uniform(
                    BROWNOUT_MIN_240V, BROWNOUT_MAX_240V
                )

                self.quality_flags[hour] = "brownout"

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
