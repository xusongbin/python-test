
import tracemalloc


tracemalloc.start()

'''
do user thing
'''

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats:
	print(stat)