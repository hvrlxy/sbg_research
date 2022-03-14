import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class AUC_reduction:
	def __init__(self, orig_components: int, n_components: int):
		self.orig_components = orig_components
		self.n_components = n_components

	def find_ys(self, reduced_y, ys):
		for i in range(len(ys) - 1):
			if reduced_y >= ys[i] and reduced_y <= ys[i + 1]:
				return i, i + 1

	def reduce(self, x):
		if len(x) != self.orig_components:
			return None 
		ys = [i for i in range(self.orig_components)]
		reduced_ys = [i for i in range (self.n_components)]
		reduced_ys = [i * self.n_components/self.orig_components for i in reduced_ys]

		reduced_xs = []

		for i in range(self.n_components):
			y1, y2 = self.find_ys(reduced_ys[i], ys)

			slope = (x[y1] - x[y2])/(ys[y1] - ys[y2])
			print(slope)
			new_x = slope * reduced_ys[i] + x[y1]

			reduced_xs.append(new_x)

		return reduced_xs
# AUC = AUC_reduction(orig_components=14, n_components=13)

# old_xs = [0, 2, 1, 2, 7, 2, 4, 1, 4, 4, 1, 3, 6, 20]
# new_xs = AUC.reduce(old_xs)





