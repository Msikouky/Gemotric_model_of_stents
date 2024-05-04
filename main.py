from svgPathReader import SvgPathReader
from curvatureSampler import CurvatureSampler
from equidistantSampler import EquidistantSampler
from visualiser import Visualiser
from svgPathOperator import SvgPathOperator
from ui import InterfaceUtilisateur
import tkinter as tk

root = tk.Tk()
Interface = InterfaceUtilisateur(root)
root.mainloop()

svg_file_path = Interface.get_file_path()
sampler_type = Interface.get_sampler_type()
plot_number = Interface.get_plot_number()

if svg_file_path and sampler_type and plot_number:
    # Create SVG file reader
    reader = SvgPathReader(svg_file_path)
    operator = SvgPathOperator(reader)

    if sampler_type == "Equidistant Sampler":
        sampler = EquidistantSampler(operator)
    elif sampler_type == "Curvature Sampler":
        sampler = CurvatureSampler(operator)

    # Visualize sampling
    visualiser = Visualiser(sampler)
    visualiser.plot_shape(plot_number)
