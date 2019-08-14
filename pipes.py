# -​- coding: utf-8 -​-
# salberico
from __future__ import print_function
from random import randint
from time import sleep
import sys
from data import *
import argparse

def parse_args():
	parser = argparse.ArgumentParser(description='Pythonpipes')
	parser.add_argument('-w', dest='width', help='Width of random pipe output. [80]', default=80, type=int)
	parser.add_argument('-l', dest='lines', help='Number of lines in random pipe output, -1 for infinite. [-1]', default=-1, type=int)
	parser.add_argument('-d', dest='delay', help='Delay between subsequent printing of lines. [0]', default=0, type=float)
	parser.add_argument('-s', dest='save', help='Save to file if specified otherwise just print. [none] (overides delay)', type=str)
	args = parser.parse_args()
	return args

def rand_char(s):
	return s[randint(0,len(s)-1)]

def find_pipe(p):
	for x in range(2):
		for y in range(2):
			for z in range(len(pipe_rd[x][y])):
				if pipe_rd[x][y][z] == p: return (x,y)
	return (0,0)
	
def find_lu(p):
	for x in range(2):
		for y in range(2):
			for z in range(len(pipe_lu[x][y])):
				if pipe_lu[x][y][z] == p: return (x,y)
	return (0,0)
	
def gen_start(w):
	pline = []
	pline.append(pipes[0])
	for x in range(1,w-1):
		if x == w - 2:	
			pline.append(rand_char(pipe_b[find_pipe(pline[x-1])[0]][0]))
		else:
			pline.append(rand_char(pipe_lu[find_pipe(pline[x-1])[0]][0]))
	pline.append("╗")
	return pline

def gen_cap(pline, w, h):
	for z in range(1,3):
		for x in range(0,w):
			if z == 1 and x == 0:
				pline[h-z][x] = "╚"
			elif z == 1 and x == w-1:
				pline[h-z][x] = "╝"
			elif z == 1 and x == w-2:
				pline[h-z][x] = rand_char(pipe_bb[find_pipe(pline[h-z][x-1])[0]])
			elif z == 1:
				pline[h-z][x] = rand_char(pipe_nd[find_pipe(pline[h-z][x-1])[0]])
			elif z == 2:
				if x == 0:
					pline[h-z][x] = rand_char(pipe_u[find_pipe(pline[h-3][0])[1]])
				elif x == w-2:
					pline[h-z][x+1] = rand_char(pipe_unor[find_pipe(pline[h-3][w-1])[1]])
				elif x == w-1:
					c = (find_pipe(pline[h-2][w-3])[0]) + (find_pipe(pline[h-3][w-2])[1]) + (find_lu(pline[h-2][w-1])[0]) + (find_lu(pline[h-1][w-2])[1])
					if c == 1:
						if pline[h-2][w-1] == u'╣':
							pline[h-2][w-1] = u'║'
						else:
							pline[h-2][w-1] = u'╣'
					pline[h-z][x-1] = rand_char(pipe_lurd[find_pipe(pline[h-2][w-3])[0]][find_pipe(pline[h-3][w-2])[1]][find_lu(pline[h-2][w-1])[0]][find_lu(pline[h-1][w-2])[1]])
				else: pline[h-z][x] = rand_char(pipe_lud[find_pipe(pline[h-2][x-1])[0]][find_pipe(pline[h-3][x])[1]][find_lu(pline[h-1][x])[1]])
	return 

def gen_pipeline(w, h, p=0, delay=0):
	if w < 3 or (h < 3 and h != -1):
		return 
	pline = [[]]
	pline[0] = gen_start(w)
	if (p):
		print(''.join(pline[0]))

	y = 1
	while (y != h):
		sleep(delay)
		pline.append([])
		pline[y].append(rand_char(pipe_lu[0][find_pipe(pline[y-1][0])[1]]))
		for x in range(1,w-2):
			pline[y].append(rand_char(pipe_lu[find_pipe(pline[y][x-1])[0]][find_pipe(pline[y-1][x])[1]]))
		pline[y].append("x")
		pline[y].append(rand_char(pipe_eu[find_pipe(pline[y-1][w-1])[1]]))
		pline[y][w-2] = rand_char(pipe_lur[find_pipe(pline[y][w-3])[0]][find_pipe(pline[y-1][w-2])[1]][find_lu(pline[y][w-1])[0]])
		if (h == -1 or y < h-2):
			print(''.join(pline[y]))
		y += 1
	gen_cap(pline, w, h)
	for z in range(h-2, h):
		sleep(delay)
		print(''.join(pline[z]))
	return pline

def save_pline(width, lines, name):
	p = gen_pipeline(width,lines)
	f = open(name, 'wb')
	z = []
	for y in range(len(p)):
		z.append("")
		for x in range(len(p[y])): 
			z[y] += p[y][x]
		if not y==len(p)-1:
			z[y] += "\n"
	for i,x in enumerate(z):
		z[i] = x.encode("utf-8")
	f.writelines(z)
	f.close()
	
def print_pline(width, lines, delay):
	gen_pipeline(width,lines,p=1,delay=delay)
	
if __name__ == "__main__":
	args = parse_args()
	print(args)
	if args.save:
		save_pline(args.width, args.lines, args.save)
	else:
		try:
			print_pline(args.width, args.lines, args.delay)
		except KeyboardInterrupt:
			exit(0)
		
