import math
from os import environ
from sys import exit
from manim import config, GraphScene, VGroup, ShowCreation, BLUE, GRAY, DOWN, LEFT
from numpy import clip, arange
from sympy import symbols, lambdify, Interval, Union, latex
from sympy.calculus.util import continuous_domain
from sympy.parsing.maxima import parse_maxima

x, e = symbols("x e")

try:
    path = environ['PLOT_DIR']
except KeyError:
    print("Error: you need to specify PLOT_DIR env var")
    exit(1)


def plot(function_str, filename, x_min, x_max, y_min, y_max):
    expr = parse_maxima(function_str)
    config.output_file = path + filename
    config.frame_rate = 25
    config.pixel_width = 1280
    config.pixel_height = 720
    scene = FunctionPlot(expr=expr, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
    scene.render()
    return filename


class FunctionPlot(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            num_graph_anchor_points=100,
            axes_color=GRAY,
            **kwargs
        )

        self.graph_origin = (clip(self.y_max / (self.y_max - self.y_min), 0, 1) * 5 - 2.5) * DOWN + \
                            (clip(self.x_max / (self.x_max - self.x_min), 0, 1) * 8 - 4) * LEFT

        x_steps = max((self.x_max - self.x_min) // 8, 1)
        self.x_labeled_nums = arange(self.x_min, self.x_max, x_steps)
        y_steps = max((self.y_max - self.y_min) // 5, 1)
        self.y_labeled_nums = arange(self.y_min, self.y_max, y_steps)

        self.function_color = BLUE
        self.expr = kwargs['expr']

    def construct(self):
        expr2 = self.expr.subs(e, math.e)
        f = lambdify(x, expr2, 'numpy')

        domains = continuous_domain(self.expr, x, Interval(self.x_min, self.x_max))

        if type(domains) is Union:
            domains = domains.args
        else:
            domains = [domains]

        self.setup_axes(animate=True)

        func_graph = VGroup()

        for domain in domains:
            graph = self.get_graph(f, self.function_color, get_left_bound(domain), get_right_bound(domain))
            func_graph.add(graph)

        graph_lab = self.get_graph_label(func_graph[0], label=latex(self.expr))
        self.play(ShowCreation(func_graph, run_time=3))
        self.play(ShowCreation(graph_lab))
        self.wait(5)


epsilon = 0.1


def get_right_bound(domain):
    if domain.right_open:
        return float(domain.right) - epsilon
    else:
        return float(domain.right)


def get_left_bound(domain):
    if domain.left_open:
        return float(domain.left) + epsilon
    else:
        return float(domain.left)
