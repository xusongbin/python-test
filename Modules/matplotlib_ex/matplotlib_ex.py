
# matplotlib图表演示


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from matplotlib import cm, rcParams
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import axes3d


class Plt(object):
    def class0(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.show()

    def class_line_plot(self):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
        z = np.linspace(-2, 2, 100)
        r = z ** 2 + 1
        x = r * np.sin(theta)
        y = r * np.cos(theta)
        ax.plot(x, y, z)
        ax.legend()
        plt.show()

    def randrange(self, n, vmin, vmax):
        # Helper function to make an array of random numbers having shape (n, )
        # with each number distributed Uniform(vmin, vmax).
        return (vmax - vmin) * np.random.rand(n) + vmin

    def class_scatter_plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # n = 100
        # for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', 'o', -30, -5)]:
        #     xs = self.randrange(n, 23, 32)
        #     ys = self.randrange(n, 0, 100)
        #     zs = self.randrange(n, zlow, zhigh)
        #     ax.scatter(xs, ys, zs, c=c, marker=m)
        x, y, z = axes3d.get_test_data(0.3)
        ax.scatter(x, y, z+10, c='r', marker='o')
        ax.scatter(x, y, -z-10, c='b', marker='o')

        # ax.set_xlabel('X Label')
        # ax.set_ylabel('Y Label')
        # ax.set_zlabel('Z Label')

        plt.show()

    def class_wireframe_plots(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x, y, z = axes3d.get_test_data(0.05)
        ax.plot_wireframe(x, y, z, rstride=10, cstride=10)
        plt.show()

    def class_surface_plots(self):
        fig = plt.figure()
        ax = fig.gca(projection='3d')

        # Make data.
        x = np.arange(-10, 10, 0.25)
        y = np.arange(-10, 10, 0.25)
        x, y = np.meshgrid(x, y)
        r = np.sqrt(x**2 + y**2)
        z = np.sin(r)

        # Plot the surface.
        surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)

        # Customize the z axis.
        ax.set_zlim(-1.01, 1.01)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.savefig('t.png')

        plt.show()

    def class_tri_surface_plots(self):
        n_radii = 8
        n_angles = 36

        # Make radii and angles spaces (radius r=0 omitted to eliminate duplication).
        radii = np.linspace(0.125, 1.0, n_radii)
        angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)

        # Repeat all angles for each radius.
        angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)

        # Convert polar (radii, angles) coords to cartesian (x, y) coords.
        # (0, 0) is manually added at this stage,  so there will be no duplicate
        # points in the (x, y) plane.
        x = np.append(0, (radii * np.cos(angles)).flatten())
        y = np.append(0, (radii * np.sin(angles)).flatten())

        # Compute z to make the pringle surface.
        z = np.sin(-x * y)

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        ax.plot_trisurf(x, y, z, linewidth=0.2, antialiased=True)

        plt.show()

    def class_contour_plots(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        X, Y, Z = axes3d.get_test_data(0.05)
        cset = ax.contour(X, Y, Z, cmap=cm.coolwarm)
        ax.clabel(cset, fontsize=9, inline=1)

        plt.show()

    def class_contour_plots1(self):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        X, Y, Z = axes3d.get_test_data(0.05)
        ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
        cset = ax.contour(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
        cset = ax.contour(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
        cset = ax.contour(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)

        # ax.set_xlabel('X')
        ax.set_xlim(-40, 40)
        # ax.set_ylabel('Y')
        ax.set_ylim(-40, 40)
        # ax.set_zlabel('Z')
        ax.set_zlim(-100, 100)

        plt.show()

    def class_contour_plots2(self):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        X, Y, Z = axes3d.get_test_data(0.05)
        ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
        cset = ax.contourf(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
        cset = ax.contourf(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
        cset = ax.contourf(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)

        # ax.set_xlabel('X')
        ax.set_xlim(-40, 40)
        # ax.set_ylabel('Y')
        ax.set_ylim(-40, 40)
        # ax.set_zlabel('Z')
        ax.set_zlim(-100, 100)

        plt.show()

    def class_bar_plots(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for c, z in zip(['r', 'g', 'b', 'y'], [30, 20, 10, 0]):
            xs = np.arange(20)
            ys = np.random.rand(20)

            # You can provide either a single color or an array. To demonstrate this,
            # the first bar of each set will be colored cyan.
            cs = [c] * len(xs)
            # cs[0] = 'c'
            ax.bar(xs, ys, zs=z, zdir='y', color=cs, alpha=0.8, width=0.5)

        # ax.set_xlabel('X')
        # ax.set_ylabel('Y')
        # ax.set_zlabel('Z')

        plt.show()

    def class_subplot(self):
        fig = plt.figure()
        ax = fig.gca(projection='3d')

        # Plot a sin curve using the x and y axes.
        x = np.linspace(0, 1, 100)
        y = np.sin(x * 2 * np.pi) / 2 + 0.5
        ax.plot(x, y, zs=0, zdir='z', label='curve in (x,y)')

        # Plot scatterplot data (20 2D points per colour) on the x and z axes.
        num = 20
        colors = ('r', 'g', 'b', 'k')
        x = np.random.sample(num * len(colors))
        y = np.random.sample(num * len(colors))
        c_list = []
        for c in colors:
            for _ in range(num):
                c_list.append(c)
        # By using zdir='y', the y value of these points is fixed to the zs value 0
        # and the (x,y) points are plotted on the x and z axes.
        ax.scatter(x, y, zs=0, zdir='y', c=c_list, label='points in (x,z)')

        # Make legend, set axes limits and labels
        ax.legend()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_zlim(0, 1)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

    def class_subplots(self):
        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        # ===============
        #  First subplot
        # ===============
        # set up the axes for the first plot
        ax = fig.add_subplot(2, 2, 1, projection='3d')

        # plot a 3D surface like in the example mplot3d/surface3d_demo
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.sin(R)
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)
        ax.set_zlim(-1.01, 1.01)
        fig.colorbar(surf, shrink=0.5, aspect=10)

        # ===============
        # Second subplot
        # ===============
        # set up the axes for the second plot
        ax = fig.add_subplot(2, 1, 2, projection='3d')

        # plot a 3D wireframe like in the example mplot3d/wire3d_demo
        X, Y, Z = axes3d.get_test_data(0.05)
        ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

        plt.show()

    def class_histogram(self):
        # 设置matplotlib正常显示中文和负号
        rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
        rcParams['axes.unicode_minus'] = False  # 正常显示负号
        # 随机生成（10000,）服从正态分布的数据
        data = np.random.randn(10000)
        """
        绘制直方图
        data:必选参数，绘图数据
        bins:直方图的长条形数目，可选项，默认为10
        normed:是否将得到的直方图向量归一化，可选项，默认为0，代表不归一化，显示频数。normed=1，表示归一化，显示频率。
        facecolor:长条形的颜色
        edgecolor:长条形边框的颜色
        alpha:透明度
        """
        plt.hist(data, bins=40, normed=0, facecolor="blue", edgecolor="black", alpha=0.7)
        # 显示横轴标签
        plt.xlabel('区间')
        # 显示纵轴标签
        plt.ylabel("频数/频率")
        # 显示图标题
        plt.title("频数/频率分布直方图")
        plt.show()

    def class_bar_chart(self):
        rcParams['font.sans-serif'] = ['SimHei']
        rcParams['axes.unicode_minus'] = False

        label_list = ['2014', '2015', '2016', '2017']  # 横坐标刻度显示值
        num_list1 = [20, 30, 15, 35]  # 纵坐标值1
        num_list2 = [15, 30, 40, 20]  # 纵坐标值2
        x = range(len(num_list1))
        """
        绘制条形图
        left:长条形中点横坐标
        height:长条形高度
        width:长条形宽度，默认值0.8
        label:为后面设置legend准备
        """
        rects1 = plt.bar([i + 0.0 for i in x], height=num_list1, width=0.4, alpha=0.8, color='red', label="一部门")
        rects2 = plt.bar([i + 0.4 for i in x], height=num_list2, width=0.4, alpha=0.8, color='green', label="二部门")
        plt.ylim(0, 50)  # y轴取值范围
        plt.ylabel("数量")
        """
        设置x轴刻度显示值
        参数一：中点坐标
        参数二：显示值
        """
        plt.xticks([index + 0.2 for index in x], label_list)
        plt.xlabel("年份")
        plt.title("某某公司")
        plt.legend()  # 设置题注
        # 编辑文本
        for rect in rects1:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
        for rect in rects2:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
        plt.show()

    def class_text_tips(self):
        fig = plt.figure()
        ax = fig.gca(projection='3d')

        # Demo 1: zdir
        zdirs = (None, 'x', 'y', 'z', (1, 1, 0), (1, 1, 1))
        xs = (1, 4, 4, 9, 4, 1)
        ys = (2, 5, 8, 10, 1, 2)
        zs = (10, 3, 8, 9, 1, 8)

        for zdir, x, y, z in zip(zdirs, xs, ys, zs):
            label = '(%d, %d, %d), dir=%s' % (x, y, z, zdir)
            ax.text(x, y, z, label, zdir)

        # Demo 2: color
        ax.text(9, 0, 0, "red", color='red')

        # Demo 3: text2D
        # Placement 0, 0 would be the bottom left, 1, 1 would be the top right.
        ax.text2D(0.05, 0.95, "2D Text", transform=ax.transAxes)

        # Tweaking display region and labels
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_zlim(0, 10)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')

        plt.show()

    def class1(self):
        x = np.array([[0, 0.5, 1], [0, 0.5, 1]])
        y = np.array([[0, 0, 0], [1, 1, 1]])
        plt.plot(x, y, 'o--')
        plt.grid(True)
        # plt.show()
        plt.savefig('t.png')

    def class2(self):
        x = np.arange(-3, 5, 0.1)
        y = np.exp(x)
        plt.plot(x, y, c='r')
        xs = np.ones(160)
        ys = np.arange(-10, 150, 1)
        plt.plot(xs, ys, c='black')
        plt.grid(True)
        plt.show()


if __name__ == '__main__':
    tt = Plt()
    tt.class_text_tips()
