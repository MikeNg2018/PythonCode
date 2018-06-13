import matplotlib.pyplot as plt
import openpyxl

wb = openpyxl.load_workbook('test.xlsx')
mySheet = wb['Sheet1']

x = []
y = []
for i in range(1, mySheet.max_row + 1):
    x.append(mySheet["A%s" % i].value)
    y.append(mySheet["B%s" % i].value)

plt.plot(x, y)
plt.show()