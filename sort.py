with open('output.txt') as f:
	lines = f.readlines()

monsters = [""] * 210
for line in lines:
	if line != lines[0] and line != lines[1]:
		mon_id = int(line[:3])
		print("Processing monster of ID: %s" % mon_id)
		monsters[mon_id - 1] = line

with open('sorted_output.txt', 'w') as f:
	print("Writing back to file in order...")
	f.write(lines[0])
	f.write(lines[1])
	for line in monsters:
		f.write("%s" % line)
	print("Done!")

