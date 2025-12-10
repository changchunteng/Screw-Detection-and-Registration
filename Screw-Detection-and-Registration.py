import numpy as np
from pycpd import RigidRegistration
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
from scipy.optimize import linear_sum_assignment

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Times New Roman'
plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'

def read_columns_from_file(filename):
    data = np.loadtxt(filename, delimiter=" ")
    columns = data[:, 1:3].copy()
    columns[:, 1] = 1 - columns[:, 1]
    return columns

file1 = "DetectionData.txt"
file2 = "PriorData.txt"
data1 = read_columns_from_file(file1)
data2 = read_columns_from_file(file2)

def cpd_registration(X, Y):
    reg = RigidRegistration(X=X, Y=Y)
    TY, (s_reg, R_reg, t_reg) = reg.register()
    return TY, (s_reg, R_reg, t_reg)

data2_transformed, _ = cpd_registration(data1, data2)

dist_matrix = distance_matrix(data1, data2_transformed)
row_ind, col_ind = linear_sum_assignment(dist_matrix)

threshold_distance = 0.2

paired_points = []
anomalous_points = []
matched_data1_indices = set()
matched_data2_indices = set()

for i, j in zip(row_ind, col_ind):
    if dist_matrix[i, j] <= threshold_distance:
        paired_points.append((data2_transformed[j], data1[i]))
        matched_data1_indices.add(i)
        matched_data2_indices.add(j)
    else:
        anomalous_points.append(data2_transformed[j])

unpaired_data1_points = [
    data1[i] for i in range(len(data1)) if i not in matched_data1_indices
]
unpaired_data2_points = [
    data2_transformed[j]
    for j in range(len(data2_transformed))
    if j not in matched_data2_indices
]

plt.figure(figsize=(6, 6))

plt.scatter(data1[:, 0], data1[:, 1], c="#54B345", label="detection results")
plt.scatter(data2[:, 0], data2[:, 1], c="#2878b5", label="Prior screw position")
plt.scatter(
    data2_transformed[:, 0],
    data2_transformed[:, 1],
    c="#9AC9DB",
    label="Registration results",
)

for pt2, pt1 in paired_points:
    plt.plot([pt2[0], pt1[0]], [pt2[1], pt1[1]], "k--")

if len(unpaired_data1_points) > 0:
    unpaired_data1_points = np.array(unpaired_data1_points)
    plt.scatter(
        unpaired_data1_points[:, 0],
        unpaired_data1_points[:, 1],
        c="red",
        label="Extra screws",
    )

if len(unpaired_data2_points) > 0:
    unpaired_data2_points = np.array(unpaired_data2_points)
    plt.scatter(
        unpaired_data2_points[:, 0],
        unpaired_data2_points[:, 1],
        c="purple",
        label="Missing screws",
    )

plt.legend()
plt.title("Point-Set Registration and Screw Matching")
plt.legend(loc="upper left")
plt.show()
