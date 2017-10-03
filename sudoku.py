import sys
import subprocess
import random

def var2prop(r, c, v):
	return r * N*N + c * N + v

def prop2var(i):
	j = i - 1
	r = j // (N*N)
	c = j // N % N
	v = j % N + 1
	return r, c, v

def min_one_per_cell(clauses):
	for r in range(N):
		for c in range(N):
			clauses.append([ var2prop(r, c, v) for v in range(1, N+1) ])

def max_one_per_cell(clauses):
	for r in range(N):
		for c in range(N):
			for v1 in range(1, N):
				for v2 in range(v1+1, N+1):
					clauses.append([-var2prop(r, c, v1), -var2prop(r, c, v2)])

def min_one_per_row(clauses):
	for r in range(N):
		for v in range(1, N+1):
				clauses.append([ var2prop(r, c, v) for c in range(N) ])

def max_one_per_row(clauses):
	for r in range(N):
		for v in range(1, N+1):
			for c1 in range(N-1):
				for c2 in range(c1+1, N):
					clauses.append([-var2prop(r, c1, v), -var2prop(r, c2, v)])

def min_one_per_column(clauses):
	for c in range(N):
		for v in range(1, N+1):
				clauses.append([ var2prop(r, c, v) for r in range(N) ])

def max_one_per_column(clauses):
	for c in range(N):
		for v in range(1, N+1):
			for r1 in range(N-1):
				for r2 in range(r1+1, N):
					clauses.append([-var2prop(r1, c, v), -var2prop(r2, c, v)])

def min_one_per_region(clauses):
	for a in range(n):
		for b in range(n):
			for v in range(1, N+1):
				clauses.append([ var2prop(a*n + r, b*n + c, v) for r in range(n) for c in range(n) ])

def max_one_per_region(clauses):
	for a in range(n):
		for b in range(n):
			for v in range(1, N+1):
				for i in range(N-1):
					for j in range(i+1, N):
						clauses.append([ -var2prop(a*n + (i // n), b*n + (i % n), v),
						                 -var2prop(a*n + (j // n), b*n + (j % n), v)])

def form_clauses(clauses):
	min_one_per_cell(clauses)
	max_one_per_cell(clauses)
	min_one_per_row(clauses)
	max_one_per_row(clauses)
	min_one_per_column(clauses)
	max_one_per_column(clauses)
	min_one_per_region(clauses)
	max_one_per_region(clauses)


if (__name__ == '__main__'):
	
	global n, N
	n = 3 #int(sys.argv[1])
	N = n * n
	
	with open(sys.argv[1], 'r') as input_file, open(sys.argv[2], 'w') as output_file:
		
		input_lines = list(input_file)
		sample = [ [ int(v) for v in input_lines[i].strip() ] for i in random.sample(range(len(input_lines)), 2400) ]
		for e in range(17, 51):
			count = 1
			for sudoku in sample:
				print(str(e) + ' empty cells, ' + 'sudoku no. ' + str(count))
				empty = []
				clauses = []
				for i in range(len(sudoku)):
					v = sudoku[i]
					r = i // N
					c = i % N
					#print(r, c, v)
					if (v > 0):
						clauses.append([var2prop(r, c, v)])
					else:
						empty.append((r, c))
	
				form_clauses(clauses)
				cnf_file = open('clauses.txt', 'w')
				cnf_file.write('p cnf ' + str(var2prop(N-1, N-1, N)) + ' ' + str(len(clauses)) + '\n')
				for clause in clauses[:-1]:
					cnf_file.write(' '.join([ str(l) for l in clause ]) + ' 0\n')
				cnf_file.write(' '.join([ str(l) for l in clauses[-1] ]) + ' 0')
				cnf_file.close()
		
				output = str(subprocess.run(['minisat', 'clauses.txt', 'solution.txt'], stdout=subprocess.PIPE).stdout)
		
				solution_file = open('solution.txt', 'r')
				solution_lines = list(solution_file)
				if (solution_lines[0].startswith('SAT')):
		
					solution = solution_lines[1].split(' ')
			
					"""
					for i in range(len(solution)):
						if (int(solution[i]) > 0):
							print(str(i // (N*N)) + ' ' + str(i // N % N) + ' ' + str(i % N + 1))
			
					for u in range(N):
						for v in range(N):
							print(sudoku[u*N + v], end = '')
						print()
					"""
			
					r, c = random.choice(empty)
					start = r * N*N + c * N
					end = start + 9
					i = 0
					found = False
					while ((start + i < end) and (not found)):
						if (int(solution[start + i]) > 0):
							sudoku[r * N + c] = i + 1
							found = True
						else:
							i += 1
					if (not found):
						error('NOT FOUND')
			
					"""
					for u in range(N):
						for v in range(N):
							print(sudoku[u*N + v], end = '')
						print()
					"""
			
					output_lines = output.split('\\n')
					restarts = next((line for line in output_lines if line.startswith('restarts')), None).split(': ')[1]
					decisions = next((line for line in output_lines if line.startswith('decisions')), None).split(': ')[1].split(' ')[0]
					cpu_time = next((line for line in output_lines if line.startswith('CPU time')), None).split(': ')[1].split(' ')[0]
					output_file.write(str(e) + ' ' + restarts + ' ' + decisions + ' ' + cpu_time + '\n')
					print('restarts: ' + restarts + ', ' + 'decisions: ' + decisions + ', ' + 'time: ' + cpu_time + '\n')
				else:
					error('UNSAT')
				solution_file.close()
				count += 1