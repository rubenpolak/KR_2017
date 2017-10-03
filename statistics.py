import numpy as np
from matplotlib.pyplot import *

if (__name__ == '__main__'):
	results_file = open('results.txt')
	data = []
	for line in results_file:
		text = line.strip().split(' ')
		data.append((81 - int(text[0]), int(text[1]), int(text[2]), float(text[3])))
	results_file.close()

	stats = dict()
	for i in range(31, 65):
		stats[i] = ([], [])

	for x in data:
		stats[x[0]][0].append(x[2])
		stats[x[0]][1].append(x[3])

	avg_decs = []
	avg_time = []
	for i in range(31, 65):
		avg_decs.append(np.mean(stats[i][0]))
		avg_time.append(np.mean(stats[i][1]))
	empty = list(range(31, 65))

	figure(1)

	subplot(121)
	plot(empty, avg_decs, 'b-', empty, avg_decs, 'k.')
	axes = gca()
	x0, x1 = axes.get_xlim()
	y0, y1 = axes.get_ylim()
	axes.set_aspect((x1 - x0) / ( y1 - y0))
	xlabel('# of empty cells')
	ylabel('average # of decisions')
	
	subplot(122)
	plot(empty, avg_time, 'b-', empty, avg_time, 'k.')
	axes = gca()
	x0, x1 = axes.get_xlim()
	y0, y1 = axes.get_ylim()
	axes.set_aspect((x1 - x0) / ( y1 - y0))
	xlabel('# of empty cells')
	ylabel('average CPU time')

	show()