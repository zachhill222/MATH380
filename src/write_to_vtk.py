# Inputs:	1) X - a vector of length N of x-values
# 			2) Y - a vector of length M of y-values
# 			3) U - a vector of length N*M of u-values
#			4) filename - the full name of the file to write to
# 
# Assumptions: U is the numerical approximation of a function u(x,y) such that U[i+N*j] ~ u(X[i],Y[j]) for i=0,...,N-1 and j=0,...,M-1
#
# Output: 	A .vtk file in ASCII format built as an unstructured quad mesh with N*M vertices and (N-1)*(M-1) elements.
# 			The coordinates of the vertices are at (X[i],Y[j],U[i+N*j]) so that the output surface can be viewed as a graph of u(x,y).
# 			The values of U are also stored so that the surface may be colored.
# 			To view the surface, open the file in a program such as Paraview.


import numpy as np

def write_vtk(X: np.ndarray, Y: np.ndarray, filename: str = "output.vtk") -> None:
	# get number of vertices and cells
	N = len(X)
	M = len(Y)
	n_verts = N*M
	n_cells = (N-1)*(M-1)

	# verify that U has the size
	if len(U) != n_verts:
		raise ValueError(f"U must have length N*M = {n_verts}, got {len(U)}")

	# write the file
	with open(filename, "w") as f:
		# header
		f.write("# vtk DataFile Version 3.0\n")
		f.write("PDE solution surface\n")
		f.write("ASCII\n")
		f.write("DATASET UNSTRUCTURED_GRID\n\n")

		# vertices
		f.write(f"POINTS {n_verts} float\n")
		for j in range(M):
			for i in range(N):
				f.write(f"{X[i]:.6e} ")