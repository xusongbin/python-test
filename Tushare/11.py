
import tushare as ts

wd = ts.get_k_data('sh000001', ktype='5')

row, col = wd.shape
print(row, col)
for i in range(len(wd.columns)):
    print(wd.columns[i], end='\t')
print('')
for i in range(row):
    for j in range(col):
        print(wd.values[i][j], end='\t')
    print('')
