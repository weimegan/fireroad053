import numpy as np

def generate_utility_dist(num_students, num_classes, mu=4, sigma=1.5):
    dist = np.random.normal(mu, sigma, [num_students, num_classes])
    dist = np.rint(dist)
    dist = np.where(dist < 1, 1, dist)
    dist = np.where(dist > 7, 7, dist)
    return dist

print(generate_utility_dist(3, 2))