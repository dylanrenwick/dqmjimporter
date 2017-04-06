import urllib.request
import re

with open('names.txt') as f:
	names = f.readlines()

content = [x.strip().replace(' ', '-').replace('\'', '').lower() for x in names]

baseurl = "http://www.woodus.com/den/games/dqm4ds/dqmjinfo/monsters/";

i = 0
monsters = []
for monster in content:
	i += 1
	pageurl = '%s%s.html' % (baseurl, monster)
	print('[%s/%s] %s' % (i, len(content), pageurl))
	page = urllib.request.urlopen(pageurl).read().decode("utf-8")
	statsreg = re.compile('Wis</th>\n(.+\n){2}<td>([0-9]{1,3})<\/td>\n.+>([a-zA-Z]{5,8})<\/a>.+\n.+>([a-zA-Z]{1,7})<\/a>.+\n.+\n<td>([0-9]{1,3})<\/td>\n<td>([0-9]{1,3})<\/td>\n<td>([0-9]{1,3})<\/td>\n<td>([0-9]{1,3})<\/td>\n<td>([0-9]{1,3})<\/td>\n<td>([0-9]{1,3})<\/td>')
	m = statsreg.search(page)
	if m:
		monsters.append(m)

i = 0
with open('output.txt', 'w') as f:
	f.write("%s | %s | %s | %s | %s | %s | %s | %s | %s | %s\n" % ("ID".ljust(3), "Name".ljust(18), "F", "R", "HP".ljust(3), "MP".ljust(3), "Atk", "Def", "Agi", "Wis"))
	f.write("%s-+-%s-+-%s-+-%s-+-%s-+-%s-+-%s-+-%s-+-%s-+-%s\n" % ("".ljust(3, '-'), "".ljust(18, '-'), "".ljust(1, '-'), "".ljust(1, '-'), "".ljust(3, '-'), "".ljust(3, '-'), "".ljust(3, '-'), "".ljust(3, '-'), "".ljust(3, '-'), "".ljust(3, '-')))
	for x in monsters:
		fam = x.group(3)
		fam_id = 0
		if fam == "Slime":
			fam_id = 0
		elif fam == "Dragon":
			fam_id = 1
		elif fam == "Nature":
			fam_id = 2
		elif fam == "Beast":
			fam_id = 3
		elif fam == "Material":
			fam_id = 4
		elif fam == "Demon":
			fam_id = 5
		elif fam == "Undead":
			fam_id = 6
		elif fam == "Incarnus":
			fam_id = 7
		else:
			fam_id = 8
		rank = x.group(4)
		rank_id = 0
		if rank == "F":
			rank_id = 0
		elif rank == "E":
			rank_id = 1
		elif rank == "D":
			rank_id = 2
		elif rank == "C":
			rank_id = 3
		elif rank == "B":
			rank_id = 4
		elif rank == "A":
			rank_id = 5
		elif rank == "S":
			rank_id = 6
		elif rank == "X":
			rank_id = 7
		elif rank == "Incarnus":
			rank_id = 8
		else:
			rank_id = 9
		f.write("%s | %s | %s | %s | %s | %s | %s | %s | %s | %s\n" % (x.group(2).ljust(3), names[i].strip().ljust(18), fam_id, rank_id, x.group(5).ljust(3), x.group(6).ljust(3), x.group(7).ljust(3), x.group(8).ljust(3), x.group(9).ljust(3), x.group(10).ljust(3)))
		i += 1

i = 0
with open('add-monsters.sql', 'w') as f:
	for x in monsters:
		f.write("INSERT INTO monsters (id, name, family, rank, hp, mp, atk, def, agi, wis) VALUES (%s, \"%s\", %s, %s, %s, %s, %s, %s, %s, %s)\n" % (x.group(2), names[i].strip().replace("'", "''"), x.group(3), x.group(4), x.group(5), x.group(6), x.group(7), x.group(8), x.group(9), x.group(10)))
		i += 1
