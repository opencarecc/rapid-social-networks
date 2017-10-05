# -*- coding:utf-8 -*-

import gender_guesser.detector

dttr = gender_guesser.detector.Detector()
genders = {}

# the logic is simple
# I build a list of user names (one per line) obtained from a Tulip graph

# I go through the list and run gender°guesser
# you first need to deal with the fact that some user names contain spaces (as in Bridget McKenzie),
# or a period (as in silviad.ambrosio)
#
# you ask guesser to guess on all parts of the name
# you need to deal with situations where you'd get both male and female (happens twice on my data)

path = '/Users/albertocottica/Downloads/'
filename = 'names.txt'

with open(path + filename, 'rU') as fp:
	line = fp.readline()
	n = line.strip()
	while line != '':
		if ' ' in n:
			nns = n.split(' ')
			gns = []
			for nn in nns:
				gns.append(dttr.get_gender(nn))
			print('Guessing from ', nns, ' = ', gns)
			if 'male' in gns:
				try:
					genders['male'] += 1
				except KeyError:
					genders['male'] = 1

				if 'female' in gns:
					genders['male'] -= 1

					try:
						genders['hermaphrodite'] += 1
					except KeyError:
						genders['hermaphrodite'] = 1

			elif 'female' in gns:

				try:
					genders['female'] += 1
				except KeyError:
					genders['female'] = 1

			else:
				try:
					genders['unknown'] += 1
				except KeyError:
					genders['unknown'] = 1
		elif '.' in n:
			nns = n.split('.')
			gns = []
			for nn in nns:
				gns.append(dttr.get_gender(nn))
			print('Guessing from ', nns, ' = ', gns)
			if 'male' in gns:
				try:
					genders['male'] += 1
				except KeyError:
					genders['male'] = 1

				if 'female' in gns:
					genders['male'] -= 1

					try:
						genders['hermaphrodite'] += 1
					except KeyError:
						genders['hermaphrodite'] = 1

			elif 'female' in gns:
				try:
					genders['female'] += 1
				except KeyError:
					genders['female'] = 1

			else:
				try:
					genders['unknown'] += 1
				except KeyError:
					genders['unknown'] = 1
		elif '_' in n:
			nns = n.split('_')
			gns = []
			for nn in nns:
				gns.append(dttr.get_gender(nn))
			print('Guessing from ', nns, ' = ', gns)
			if 'male' in gns:
				try:
					genders['male'] += 1
				except KeyError:
					genders['male'] = 1

				if 'female' in gns:
					genders['male'] -= 1

					try:
						genders['hermaphrodite'] += 1
					except KeyError:
						genders['hermaphrodite'] = 1

			elif 'female' in gns:
				try:
					genders['female'] += 1
				except KeyError:
					genders['female'] = 1

			else:
				try:
					genders['unknown'] += 1
				except KeyError:
					genders['unknown'] = 1
		else:
			nns = [n]
			gns = []
			for nn in nns:
				gns.append(dttr.get_gender(nn))
			print('Guessing from ', nns, ' = ', gns)
			if 'male' in gns:
				try:
					genders['male'] += 1
				except KeyError:
					genders['male'] = 1

				if 'female' in gns:
					genders['male'] -= 1

					try:
						genders['hermaphrodite'] += 1
					except KeyError:
						genders['hermaphrodite'] = 1

			elif 'female' in gns:
				try:
					genders['female'] += 1
				except KeyError:
					genders['female'] = 1

			else:
				try:
					genders['unknown'] += 1
				except KeyError:
					genders['unknown'] = 1
		line = fp.readline()
		n = line.strip()
print(genders)
