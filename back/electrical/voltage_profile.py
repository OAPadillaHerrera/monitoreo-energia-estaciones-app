

import random

MIN_120V = 114
MAX_120V = 126
MIN_240V = 228
MAX_240V = 252

class VoltageProfile:

    def __init__(self):

        self.profile_120v = {}
        self.profile_240v = {}

    def generate_daily_profile(self):

        for hour in range(24):

            self.profile_120v[hour] = random.uniform(MIN_120V, MAX_120V)
            self.profile_240v[hour] = random.uniform(MIN_240V, MAX_240V)
    
    def get_voltage_120v(self, hour):

        return self.profile_120v[hour]
    
    def get_voltage_240v(self, hour):

        return self.profile_240v[hour]