import numpy as np

# dimensions of output: num_students x num_classes

# sample utilities from normal distribution
# utilities must be in between 1 and 10
def generate_normal_utility_dist(num_students, num_classes, mu=5.5, sigma=2.5):
    dist = np.random.normal(mu, sigma, [num_students, num_classes])
    dist = np.rint(dist)
    dist = np.where(dist < 1, 1, dist)
    dist = np.where(dist > 10, 10, dist)
    return dist

# sample utilities from uniform distribution
def generate_unif_utility_dist(num_students, num_classes, a=1, b=10):
    dist = np.random.uniform(a, b, [num_students, num_classes])
    dist = np.rint(dist)
    return dist

def convert_to_csv(arr, path=None):
    if path is None:
        np.savetxt('data/utility.csv', arr, delimiter=",")
    else:
        np.savetxt(path, arr, delimiter=",")

unif_dist = generate_unif_utility_dist(6, 30)
convert_to_csv(unif_dist, 'data/utility_unif.csv')

norm_dist = generate_normal_utility_dist(6, 30)
convert_to_csv(norm_dist, 'data/utility_norm.csv')