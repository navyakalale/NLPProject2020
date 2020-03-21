
# class bag:
# 	def __init__(self):
# 		self.words = {}
# 		self.line = ""
# 		self.similarity = 0

def makebag(line):
	ans = {}
	for word in line.split(" "):
		if word in ans:
			ans[word]+= 1
		else:
			ans[word] = 1
	return ans

def similarity(databag, line, questionbag):
	val = 0
	for key in questionbag:
		if key in databag:
			if databag[key] >= questionbag[key]:
				val += questionbag[key]

	return (databag, line, val)

def findmax(bags):
	m = 0
	ans = ""
	for (_, line, val) in bags:
		if (val > m):
			m = val
			ans = line
	return (ans, m)

datafile = "Development_data/set1/a1.txt"
questionfile = "Development_data/set1/a1q.txt"

data = open(datafile, "r")
questions = open(questionfile, "r") 

bags = []

for line in data.read().split("."):
	curr = makebag(line)
	bags.append((curr, line, 0))

for q in questions:
	curr = makebag(q)
	bags = [similarity(bag,line,curr) for (bag,line,_) in bags]
	(ans, val) = findmax(bags)
	print(ans + " " + str(val) + "\n")
	# print(ans + "\n")






