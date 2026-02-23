from plotter import plotter
from plotter_gamma import plotter_gamma


# group variable değerleri değiştirilmeli.
# plotter(model = "mmd",
#              ind_variable_name = "layer",
#              group_variable_name = "Ns",
#              group_variables = [30000, 36000, 42000, 54000],
#              y0s = [0.7, 0.75, 0.8],
#              automatic=True)

# plotter(model = "mmd",
#              ind_variable_name = "dim",
#              group_variable_name = "Ms",
#              group_variables = [117,234,351,819],
#              y0s = [0.5, 0.55, 0.6],
#              automatic=False)

# plotter(model = "mmd",
#              ind_variable_name = "layer",
#              group_variable_name = "Ms",
#              group_variables = [117,234,351,819],
#              y0s = [0.55, 0.6, 0.65],
#              automatic=False)


# plotter(model = "adv",
#              ind_variable_name = "layer",
#              ind_variables = [4,5,6,7,8,9,10],
#              group_variable_name = "Ms",
#              group_variables = [60,120,180,240],
#              y0s = [0.35, 0.4, 0.45],
#              automatic=True)

# plotter(model = "adv",
#              ind_variable_name = "layer",
#              group_variable_name = "Ns",
#              group_variables = [750,1500,6000,12000],
#              y0s = [0.3, 0.35, 0.4],
#              automatic=True)

# plotter(model = "adv",
#              ind_variable_name = "dcm",
#              ind_variables = [1, 4, 8, 16, 24, 32],
#              group_variable_name = "Ms",
#              group_variables = [120,180,240,300,360],
#              y0s = [0.4, 0.45, 0.5],
#              automatic=True)

# plotter(model = "adv",
#              ind_variable_name = "dcm",
#              ind_variables = [1, 4, 8, 16, 24, 32],
#              group_variable_name = "Ns",
#              group_variables = [750,1500,3000,6000],
#              y0s = [0.35, 0.4, 0.45],
#              automatic=True)


plotter_gamma(Mts = [60, 120, 210, 240],
              Mss = [240, 360, 480],
              type = "adv")

plotter_gamma(Mts = [115, 345, 460, 575],
              Mss = [234, 819, 1755],
              type = "mmd")


