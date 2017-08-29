import numpy as np
import random

class Perceptron:

	def __init__(self):
		self.weights = np.random.rand(3,1)

	def train(self,X,Y, iterations):
		for i in range iterations:
			choice = random.randint(0, X.shape[0])
			x = X[choice]
			result = self.weights[0] + self.weights[1:3]*
			expected
			error



	def predict(self,x):
		result
		expected
		return output