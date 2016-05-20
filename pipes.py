#salberico 

from random import randint
from time import sleep

pipes = ["╔","║","╗","╝","╚","╣","╩","╦","╠","═","╬"]

#[left[up],left[up]]
#[[0,1],[0,1]]
pipe_lu = [["╔","║╚╠"],["╗╦═","╣╝╩╬"]]

pipe_rd = [["╝","║╗╣"],["╚╩═","╔╦╠╬"]]

pipe_b = [["╔","╚╠"],["╦═","╩╬"]]

pipe_end = [["╔","║╚╠"],["╗╦═","╣╝╩╬"]]
pipe_eu = ["╗","║╣╝"]
pipe_lur = [[[" ","╔"],["║","╚╠"]],[["╗","═╦"],["╝╣","╩╬"]]]

pipe_nd = ["╚","╝╩═"]
pipe_bb = ["╚","╩═"]
#				0000 0001 0010 0011 0100 0101  0110 0111    1000 1001  1010 1011  1100 1101  1110
pipe_lurd = [[[[" "," "],[" ","╔"]],[[" ","║"],["╚","╠"]]],[[[" ","╗"],["═","╦"]],[["╝","╣"],["╩","╬"]]]]

#			 000  001  010   011     100  101    110  111
pipe_lud = [[[" ","╔"],["╚","║╠"]],[["═","╗╦"],["╝╩","╬╣"]]]
pipe_unor = ["╗","║╣"]
pipe_u = ["╔","║╠"]

pipe_nobot = []


def rand_char(s):
	return s[randint(0,len(s)-1)]

def find_pipe(p):
	for x in range(2):
		for y in range(2):
			for z in range(len(pipe_rd[x][y])):
				if pipe_rd[x][y][z] == p:
					return (x,y)
	return (0,0)
	
def find_lu(p):
	for x in range(2):
		for y in range(2):
			for z in range(len(pipe_lu[x][y])):
				if pipe_lu[x][y][z] == p:
					return (x,y)
	return (0,0)
		
def gen_pipeline(w, h, p = 0):
	if w < 3 or h < 3:
		return 
	pline = [[]]
	pline[0].append(pipes[0])
	for x in range(1,w-1):
		if x == w - 2:	
			pline[0].append(rand_char(pipe_b[find_pipe(pline[0][x-1])[0]][0]))
		else:
			pline[0].append(rand_char(pipe_lu[find_pipe(pline[0][x-1])[0]][0]))
	pline[0].append("╗")
	for y in range(1,h):
		pline.append([])
		pline[y].append(rand_char(pipe_lu[0][find_pipe(pline[y-1][0])[1]]))
		for x in range(1,w-2):
			pline[y].append(rand_char(pipe_lu[find_pipe(pline[y][x-1])[0]][find_pipe(pline[y-1][x])[1]]))
		pline[y].append("x")
		pline[y].append(rand_char(pipe_eu[find_pipe(pline[y-1][w-1])[1]]))
		pline[y][w-2] = rand_char(pipe_lur[find_pipe(pline[y][w-3])[0]][find_pipe(pline[y-1][w-2])[1]][find_lu(pline[y][w-1])[0]])
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
						if pline[h-2][w-1] == "╣":
							pline[h-2][w-1] = "║"
						else:
							pline[h-2][w-1] = "╣"
					pline[h-z][x-1] = rand_char(pipe_lurd[find_pipe(pline[h-2][w-3])[0]][find_pipe(pline[h-3][w-2])[1]][find_lu(pline[h-2][w-1])[0]][find_lu(pline[h-1][w-2])[1]])
				else: pline[h-z][x] = rand_char(pipe_lud[find_pipe(pline[h-2][x-1])[0]][find_pipe(pline[h-3][x])[1]][find_lu(pline[h-1][x])[1]])
	return pline
	
def print_pline(width=3, height=3, delay=0):
	p = gen_pipeline(width,height)
	z = []
	for y in range(len(p)):
		z.append([""])
		for x in range(len(p[y])): 
			z[y][0] += p[y][x]
	for x in range(len(z)): 
		sleep(delay)
		print(z[x][0])
	
if __name__ == "__main__":
	while(1):
		i = input("Width Height Delay: ")
		i = i.split(" ")
		if len(i) < 3:
			i.append("0")
		print_pline(int(i[0]),int(i[1]),float(i[2]))
		