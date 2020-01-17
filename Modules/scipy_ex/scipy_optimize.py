
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt


class App(object):
    def __init__(self):
        pass

    @staticmethod
    def this_func1(d):
        return d ** 2 + 10 * np.sin(d)

    @staticmethod
    def this_func2(x, a, b):
        return a * x ** 2 + b * np.sin(x)
    
    def get_yd(self, xd):
        return self.this_func1(xd)

    def show_brute(self):
        # 按区间查找最小值
        grid = (-10, 10, 0.1)
        xmin_global = optimize.brute(self.this_func1, (grid, ))
        if len(xmin_global):
            return xmin_global[0]
        return -1.3

    def show_img(self):
        # 输出图形并标注最小值
        plt.figure(figsize=(10, 5))
        x = np.arange(-10, 10, 0.1)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('optimize')
        plt.plot(x, self.this_func1(x), 'r-', label='$f(x)=x^2+10sin(x)$')

        # x = -1.3
        x = self.show_brute()
        y = self.get_yd(x)
        plt.annotate('min', xy=(x, y), xytext=(3, 40), arrowprops=dict(facecolor='black', shrink=0.05))
        plt.legend()
        plt.show()

    def show_curve_fit(self):
        # 非线性最小二乘拟合
        xdata = np.linspace(-10, 10, num=20)
        ydata = self.this_func1(xdata) + np.random.randn(xdata.size)
        guess = [2, 2]
        params, params_covariance = optimize.curve_fit(self.this_func2, xdata, ydata, guess)
        print(params)

    def leatsq_func(self, p, x):
        # 定义拟合函数形式
        k, b = p
        return k * x + b

    def leatsq_error(self, p, x, y, s):
        # 定义误差函数
        print(s)
        return self.leatsq_func(p, x) - y

    def show_leatsq(self):
        # 最小二乘法拟合
        Xi = np.array([8.19, 2.72, 6.39, 8.71, 4.7, 2.66, 3.78])
        Yi = np.array([7.01, 2.78, 6.47, 6.71, 4.1, 4.23, 4.05])

        # 随机给出参数的初始值
        p = np.array([9, 1])

        # 使用leastsq()函数进行参数估计
        s = '参数估计次数'
        para = optimize.leastsq(self.leatsq_error, p, args=(Xi, Yi, s))
        k, b = para[0]
        print('k={}\nb={}'.format(k, b))

        # 图形可视化
        plt.figure(figsize=(8, 6))
        # 绘制训练数据的散点图
        plt.scatter(Xi, Yi, color='r', label='Sample Point', linewidths=3)
        plt.xlabel('x')
        plt.ylabel('y')
        x = np.linspace(0, 10, 1000)
        y = k * x + b
        plt.plot(x, y, color='orange', label='Fitting Line', linewidth=2)
        plt.legend()
        plt.show()


if __name__ == '__main__':
    app = App()
    app.show_leatsq()
