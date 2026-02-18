import quadprog
import numpy as np


def quadprog_fit(x,y):
    # Create Vandermonde matrix for quadratic fitting
    A = np.vander(x, N=3)

    # Calculate G and a for the quadratic programming formulation
    G = 2 * np.array(np.dot(A.T, A),dtype = np.float64)
    a = 2 * np.array(np.dot(A.T, y),dtype = np.float64)

    # Constraint matrix and vector
    C = np.array([[2*np.min(x),1,0]], dtype=np.float64).T  # Example linear constraint
    b = -np.array([0], dtype=np.float64)  # Ensure constraints dimension matches

    # Solve the quadratic programming problem
    result = quadprog.solve_qp(G, a, C, b)

    solution_vector = result[0]
    # lagrange_multipliers = result[1]
    # minimum_function_value = result[2]
    # iterations = result[3]
    # active_constraints = result[4]

    xval = np.linspace(min(x),max(x),1000)
    quadval = np.polyval(solution_vector,np.linspace(min(x),max(x),1000))

    return solution_vector, xval, quadval


# import matplotlib.pyplot as plt
# import time
# x0s = np.array([ 7.20615237,  8.63650181,  9.68983508, 10.63960361],dtype=np.float64)
# Nss = np.array([750, 1500, 6000, 12000],dtype=np.float64)

# x0s = [1,2,3,4,5,6]
# Nss = [1,4,9,16,25,36]

# solution_vector, xval, quadval = quadprog_fit(x0s,Nss)

# plt.figure()
# plt.title(time.time())
# plt.plot(xval,quadval)
# plt.plot(x0s,Nss)
# plt.savefig("deneme.pdf")


# print("hello")