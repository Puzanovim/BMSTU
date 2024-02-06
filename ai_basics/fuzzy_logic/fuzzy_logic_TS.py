import time
from math import sin, exp
import random
from typing import Tuple, Dict
import numpy as np

from matplotlib import pyplot as plt
from simpful import *


def func(x, y):
	return x / (2 * exp(y / 10)) * sin(x / 2)


def compare(start_x, finish_x, start_y, finish_y, param_func) -> float:
	total_error = 0
	count = 0

	for x in range(start_x * 10, finish_x * 10):
		for y in range(start_y * 10, finish_y * 10):
			norm_x = x / 10
			norm_y = y / 10
			orig_z = func(norm_x, norm_y)
			current_z = param_func(norm_x, norm_y)
			total_error += abs(orig_z - current_z)
			count += 1

	return total_error / count


def get_coefficients(start_x, finish_x, start_y, finish_y) -> Tuple[float, float, float]:
	t = 100_000_000
	t_end = 100

	a = random.randint(-6, 6)
	b = random.randint(-6, 6)
	c = random.randint(-6, 6)
	current_a, current_b, current_c = best_a, best_b, best_c = a, b, c
	current_error = best_error = compare(start_x, finish_x, start_y, finish_y, lambda x, y: a * x + b * y + c)
	work_a, work_b, work_c = current_a, current_b, current_c

	while t > t_end:
		work_a = work_a + random.choice((-1, 1)) * random.uniform(0, 5)
		work_b = work_b + random.choice((-1, 1)) * random.uniform(0, 5)
		work_c = work_c + random.choice((-1, 1)) * random.uniform(0, 5)

		work_error: float = compare(start_x, finish_x, start_y, finish_y, lambda x, y: work_a * x + work_b * y + work_c)

		print(f't={t}, {best_error}, {current_error}, {work_error}')
		if work_error < current_error:
			current_a, current_b, current_c = work_a, work_b, work_c
			current_error = work_error

			if current_error < best_error:
				best_a, best_b, best_c = current_a, current_b, current_c
				best_error = current_error
		else:
			p = exp(-work_error / t)
			value = random.random()

			if value <= p:
				current_a, current_b, current_c = work_a, work_b, work_c
				current_error = work_error

				if current_error < best_error:
					best_a, best_b, best_c = current_a, current_b, current_c
					best_error = current_error
			else:
				work_a, work_b, work_c = current_a, current_b, current_c

		t = t * 0.9

	return best_a, best_b, best_c


def gen_params(count_x, count_y) -> Tuple[Dict, Dict, Dict, Dict, Dict]:
	x_params = {}
	y_params = {}

	step_x = 13 // count_x
	for i in range(count_x):
		x_params[f'x_{i}'] = (i * step_x, random.uniform(0.1, 6))

	step_y = 13 // count_y
	for i in range(count_y):
		y_params[f'y_{i}'] = (i * step_y, random.uniform(0.1, 6))

	x_step = 13 // count_x
	y_step = 13 // count_y

	pre_rules = {}
	coefficients = {}
	coefficients_indexes = {}

	name_z = 0
	x_i = -6
	for x_name in x_params.keys():
		y_i = -6
		for y_name in y_params.keys():
			pre_rules[(x_name, y_name)] = f'z_{name_z}'
			a, b, c = get_coefficients(x_i, x_i + x_step, y_i, y_i + y_step)
			coefficients[f'z_{name_z}'] = a, b, c
			coefficients_indexes[f'z_{name_z}'] = x_i, x_i + x_step, y_i, y_i + y_step
			name_z += 1
			y_i += y_step
		x_i += x_step

	return x_params, y_params, pre_rules, coefficients, coefficients_indexes


def change_params(current_params: Tuple[Dict, Dict]) -> Tuple[Dict, Dict]:
	x_params, y_params = current_params
	new_x_params = {}
	new_y_params = {}

	for k, v in x_params.items():
		new_x_params[k] = (v[0] + random.uniform(-1, 1), abs(v[1] + random.choice((-1, 1)) * random.uniform(0.1, 1)))

	for k, v in y_params.items():
		new_y_params[k] = (v[0] + random.uniform(-1, 1), abs(v[1] + random.choice((-1, 1)) * random.uniform(-1, 1)))

	return new_x_params, new_y_params



def get_gaussian_params(x_count: int, y_count: int):
	t = 10_000_000
	t_end = 100

	x_params, y_params, pre_rules, coefficients, coefficients_indexes = gen_params(x_count, y_count)
	current_params = best_params = x_params, y_params
	current_error = best_error = fuzzy_logic(*current_params, pre_rules=pre_rules, coefficients=coefficients)
	work_params = current_params

	while t > t_end:
		work_params = change_params(work_params)
		work_error = fuzzy_logic(*work_params, pre_rules=pre_rules, coefficients=coefficients)

		print(f't={t}, {best_error}, {current_error}, {work_error}')
		if work_error < current_error:
			current_params = work_params
			current_error = work_error

			if current_error < best_error:
				best_params = current_params
				best_error = current_error

		else:
			p = exp(-work_error / t)
			value = random.random()

			if value <= p:
				current_params = work_params
				current_error = work_error

				if current_error < best_error:
					best_params = current_params
					best_error = current_error
			else:
				work_params = current_params

		t = t * 0.9

	return best_params, pre_rules, coefficients, coefficients_indexes


def fuzzy_logic(x_params: Dict, y_params: Dict, pre_rules: Dict, coefficients: Dict) -> float:
	fs = FuzzySystem()

	x_sets = []
	for name, params in x_params.items():
		x_sets.append(GaussianFuzzySet(params[0], params[1], term=name))

	y_sets = []
	for name, params in y_params.items():
		y_sets.append(GaussianFuzzySet(params[0], params[1], term=name))

	fs.add_linguistic_variable('x', LinguisticVariable(x_sets, universe_of_discourse=[-6, 6]))
	fs.add_linguistic_variable('y', LinguisticVariable(y_sets, universe_of_discourse=[-6, 6]))

	rules = []
	for k, v in pre_rules.items():
		rules.append(f'IF (x IS {k[0]}) AND (y IS {k[1]}) THEN (z IS {v})')
	fs.add_rules(rules)

	for z_name, v in coefficients.items():
		fs.set_output_function(z_name, f'{v[0]} * x + {v[1]} * y + {v[2]}')

	total_error = 0
	count = 0

	for y in range(-6, 7):
		for x in range(-6, 7):
			fs.set_variable('x', x)
			fs.set_variable('y', y)

			result = fs.Sugeno_inference(['z'])['z']
			real_result = func(x, y)

			error = (real_result - result) ** 2
			total_error += error
			count += 1

	total_error /= count
	return total_error


def main_fuzzy_logic(
	x_params: Dict, y_params: Dict, pre_rules: Dict, coefficients: Dict, coefficients_indexes: Dict
) -> float:
	fs = FuzzySystem()

	x_sets = []
	for name, params in x_params.items():
		x_sets.append(GaussianFuzzySet(params[0], params[1], term=name))

	y_sets = []
	for name, params in y_params.items():
		y_sets.append(GaussianFuzzySet(params[0], params[1], term=name))

	fs.add_linguistic_variable('x', LinguisticVariable(x_sets, universe_of_discourse=[-6, 6]))
	fs.add_linguistic_variable('y', LinguisticVariable(y_sets, universe_of_discourse=[-6, 6]))

	rules = []
	for k, v in pre_rules.items():
		values = coefficients[v]
		rules.append(f'IF (x IS {k[0]}) AND (y IS {k[1]}) THEN (z IS {v})')
		print(f'IF (x IS {k[0]}) AND (y IS {k[1]}) THEN {values[0]} * x + {values[1]} * y + {values[2]}')
	fs.add_rules(rules)

	for z_name, v in coefficients.items():
		fs.set_output_function(z_name, f'{v[0]} * x + {v[1]} * y + {v[2]}')

	total_error = 0
	count = 0

	z = []
	real_z = []
	clear_z = []

	for y in range(-6, 7):
		for x in range(-6, 7):
			fs.set_variable('x', x)
			fs.set_variable('y', y)
			result = fs.Sugeno_inference(['z'])['z']
			real_result = func(x, y)
			error = (real_result - result) ** 2
			total_error += error
			count += 1

			current_clear_z: float = 0
			for k, indexes in coefficients_indexes.items():
				if indexes[0] <= x < indexes[1] and indexes[2] <= y < indexes[3]:
					values = coefficients.get(k)
					current_clear_z = values[0] * x + values[1] * y + values[2]

			z.append(result)
			real_z.append(real_result)
			clear_z.append(current_clear_z)

	total_error /= count
	print(f'TOTAL ERROR: {total_error}')


	fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(10, 10))
	X = np.arange(-6, 7)
	Y = np.arange(-6, 7)
	X, Y = np.meshgrid(X, Y)
	Z = np.array(z).reshape((13, 13))
	ax.plot_surface(X, Y, Z, linewidth=0, antialiased=False)
	ax.zaxis.set_major_formatter('{x:.02f}')
	plt.show()

	fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(10, 10))
	X = np.arange(-6, 7)
	Y = np.arange(-6, 7)
	X, Y = np.meshgrid(X, Y)
	Z = np.array(clear_z).reshape((13, 13))
	ax.plot_surface(X, Y, Z, linewidth=0, antialiased=False)
	ax.zaxis.set_major_formatter('{x:.02f}')
	plt.show()

	# fs.plot_variable('x')
	# fs.plot_variable('y')

	fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(10, 10))
	X = np.arange(-6, 7)
	Y = np.arange(-6, 7)
	X, Y = np.meshgrid(X, Y)
	Z = np.array(real_z).reshape((13, 13))
	ax.plot_surface(X, Y, Z, linewidth=0, antialiased=False)
	ax.zaxis.set_major_formatter('{x:.02f}')
	plt.show()

	return total_error


if __name__ == '__main__':
	times = {}
	errors = {}

	for x, y in ((1, 1), (4, 2), (4, 3), (6, 6), (13, 13)):
		t_start = time.monotonic()

		standard_params, raw_rules, coeffs, coeffs_indexes = get_gaussian_params(x, y)
		error = main_fuzzy_logic(*standard_params, pre_rules=raw_rules, coefficients=coeffs, coefficients_indexes=coeffs_indexes)
		t_finish = time.monotonic()

		diff = t_finish - t_start
		times[(x, y)] = diff
		errors[(x, y)] = error

	print(f'ALL TIMES {times}')
	print(f'ALL ERRORS {errors}')

