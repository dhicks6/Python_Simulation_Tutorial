import random
import simpy
import numpy as np

# Constants for the simulation
NUM_EMPLOYEES = 2
AVG_SUPPORT_TIME = 5
CUSTOMER_INTERVAL = 2
SIM_TIME = 120

# Counter for how many customers have been handled
customers_handled = 0

# the env that is passed is used in simpy for the environment for the simulation
class CallCenter:

    def __init__(self, env, num_employees, support_time):
        self.env = env
        self.staff = simpy.Resource(env, num_employees)
        self.support_time = support_time

    def support(self, customer):
        random_time = max(1, np.random.normal(self.support_time, 4))
        yield self.env.timeout(random_time)
        print(f"Support finished for {customer} at {self.env.now:.2f}")


def customer(env, name, call_center):
    global customers_handled
    print(f"Customer {name} enters waiting queue at {env.now:.2f}!")
    with call_center.staff.request() as request:
        yield request
        print(f"customer {name} enters call at {env.now:.2f}")
        yield env.process(call_center.support(name))
        print(f"Customer {name} left call at {env.now:.2f}")
        customers_handled += 1

def setup(env, num_employees, support_time, customer_interval):
    call_center = CallCenter(env, num_employees, support_time)

    for i in range(1, 6):
        env.process(customer(env, num_employees, call_center))

    while True:
        yield env.timeout


