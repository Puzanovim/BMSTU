from simpful import *


def main():
	FS = FuzzySystem()

	O1 = TriangleFuzzySet(-10, -10, -5, term="negative_big")
	O2 = TriangleFuzzySet(-10, -5, 0, term="negative_medium")
	O3 = TriangleFuzzySet(-5, 0, 5, term="zero")
	O4 = TriangleFuzzySet(0, 5, 10, term="positive_medium")
	O5 = TriangleFuzzySet(5, 10, 10, term="positive_big")

	O1_3 = TriangleFuzzySet(-10, -10, 0, term="negative")
	O2_3 = TriangleFuzzySet(-10, 0, 10, term="zero")
	O3_3 = TriangleFuzzySet(0, 10, 10, term="positive")

	FS.add_linguistic_variable("distance", LinguisticVariable([O1, O2, O3, O4, O5], universe_of_discourse=[-10, 10]))
	FS.add_linguistic_variable("acceleration", LinguisticVariable([O1_3, O2_3, O3_3], universe_of_discourse=[-10, 10]))
	FS.add_linguistic_variable("diff", LinguisticVariable([O1, O2, O3, O4, O5], universe_of_discourse=[-10, 10]))

	# FS.plot_variable('distance')
	FS.plot_variable('acceleration')

	FS.add_rules([
		"IF (distance IS negative_big) AND (acceleration IS negative) THEN (diff IS negative_big)",
		"IF (distance IS negative_big) AND (acceleration IS zero) THEN (diff IS negative_big)",
		"IF (distance IS negative_big) AND (acceleration IS positive) THEN (diff IS negative_medium)",
		"IF (distance IS negative_medium) AND (acceleration IS negative) THEN (diff IS negative_big)",
		"IF (distance IS negative_medium) AND (acceleration IS zero) THEN (diff IS negative_medium)",
		"IF (distance IS negative_medium) AND (acceleration IS positive) THEN (diff IS zero)",
		"IF (distance IS zero) AND (acceleration IS negative) THEN (diff IS negative_medium)",
		"IF (distance IS zero) AND (acceleration IS zero) THEN (diff IS zero)",
		"IF (distance IS zero) AND (acceleration IS positive) THEN (diff IS positive_medium)",
		"IF (distance IS positive_medium) AND (acceleration IS negative) THEN (diff IS zero)",
		"IF (distance IS positive_medium) AND (acceleration IS zero) THEN (diff IS positive_medium)",
		"IF (distance IS positive_medium) AND (acceleration IS positive) THEN (diff IS positive_big)",
		"IF (distance IS positive_big) AND (acceleration IS negative) THEN (diff IS positive_medium)",
		"IF (distance IS positive_big) AND (acceleration IS zero) THEN (diff IS positive_big)",
		"IF (distance IS positive_big) AND (acceleration IS positive) THEN (diff IS positive_big)",
		])


	# FS.plot_variable('distance')
	# FS.plot_variable('acceleration')
	# FS.plot_variable('diff')

	total_average_error = 0
	sum_num_iter = 0
	n = 1
	for e in range(n):
		s = 0
		v = 0
		a = 0
		target_distance = 2
		positions = tuple(4 * i for i in range(1, 150))
		old_diff_distance = positions[0] - s - target_distance

		error = 0
		i = 0
		for i, s_leader in enumerate(positions):
			s = v + s
			distance_to_leader = s_leader - s
			diff_distance = distance_to_leader - target_distance
			acceleration = diff_distance - old_diff_distance

			error += (diff_distance ** 2)

			if diff_distance == 0.0:
				break

			FS.set_variable("distance", diff_distance)
			FS.set_variable("acceleration", acceleration)

			res = FS.Mamdani_inference(subdivisions=2000, aggregation_function=max)
			diff_acceleration = res['diff']

			print(f"№{i} Leader: {s_leader}, SD: {s} DIFF: {diff_distance}, A: {acceleration}, DIFF: {diff_acceleration}")

			a = diff_acceleration
			v = v + a
			old_diff_distance = diff_distance

		average_error = error / (i + 1)
		total_average_error += average_error
		sum_num_iter += (i + 1)

		print(f'AVERAGE ERROR: {average_error}')

	print()
	print(f'TOTAL AVERAGE ERROR: {total_average_error / n}')
	print(sum_num_iter / n)


if __name__ == '__main__':
	main()
