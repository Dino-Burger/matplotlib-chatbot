import matplotlib
import matplotlib.colors

sentences = [
    "Change the color of the markers to $color",
    "plot column $columnname from variable $variable",

]

variable_train_values = {
    'color': list(matplotlib.colors.CSS4_COLORS.keys()),
    'columnname': [],
    'variable': [],
}

