import math
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy
import seaborn as sb
import matplotlib as mat


def ma(interval, window_size):
    window = numpy.ones(int(window_size)) / float(window_size)
    return numpy.convolve(interval, window, "same")


def annotate_boxplot(
    bpdict,
    annotate_params=None,
    x_loc=0,
    text_offset_x=100,
    text_offset_y=-2.5,
):
    """Annotates a matplotlib boxplot with labels marking various centile levels.

    Parameters:
    - bpdict: The dict returned from the matplotlib `boxplot` function. If you're using pandas you can
    get this dict by setting `return_type='dict'` when calling `df.boxplot()`.
    - annotate_params: Extra parameters for the plt.annotate function. The default setting uses standard arrows
    and offsets the text based on other parameters passed to the function
    - x_offset: The offset from the centre of the boxplot to place the heads of the arrows, in x axis
    units (normally just 0-n for n boxplots). Values between around -0.15 and 0.15 seem to work well
    - x_loc: The x axis location of the boxplot to annotate. Usually just the number of the boxplot, counting
    from the left and starting at zero.
    text_offset_x: The x offset from the arrow head location to place the associated text, in 'figure points' units
    text_offset_y: The y offset from the arrow head location to place the associated text, in 'figure points' units
    """
    if annotate_params is None:
        annotate_params = dict(
            xytext=(text_offset_x, text_offset_y),
            fontsize=12,
            weight="bold",
            textcoords="offset points",
        )

    plt.annotate(
        bpdict["means"][x_loc].get_ydata()[0],
        (x_loc + 1, bpdict["means"][x_loc].get_ydata()[0]),
        **annotate_params
    )


if __name__ == "__main__":
    sb.set_palette(palette="magma", n_colors=2)
    sb.set_style(style="ticks")

    # df = pd.DataFrame()
    # df["recombined"] = pd.read_csv(r"results\square_7\diffusion_recombined_poly.csv")
    # df["not_recombined"] = pd.read_csv(r"results\square_7\not_recombined.csv")
    # df = [
    #     pd.read_csv(r"results\square_7\diffusion_recombined_poly.csv"),
    #     pd.read_csv(r"results\square_7\not_recombined.csv"),
    # ]

    df0 = pd.read_csv(r"results\knapsack_7\diffusion_recombined_poly.csv").assign(
        type="EQDR"
    )
    df1 = pd.read_csv(r"results\knapsack_7\not_recombined.csv").assign(type="BBHT")
    cdf = pd.concat([df0, df1])
    # mdf = pd.melt(cdf, id_vars=["type"], var_name=["typology"])
    print(cdf)
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot()
    # print(mdf)
    bpdict = ax.boxplot(
        x=[df0["iterations"], df1["iterations"]],
        notch=False,
        widths=0.5,
        sym="",
        labels=["EQDR", "BBHT"],
        showmeans=True,
        meanline=True,
        showcaps=False,
        boxprops={"linewidth": 2},
        medianprops={"color": (0, 0.2, 1, 1), "linewidth": 0},
        whiskerprops={"color": (0.15, 0.15, 0.15, 1), "linewidth": 2},
        meanprops={"color": (0, 0.35, 1, 1), "linewidth": 2},
    )
    ax.set_ylabel("Generations")
    annotate_boxplot(bpdict, x_loc=1)
    annotate_boxplot(bpdict, x_loc=0)
    # sb.boxplot(
    #     y=cdf["iterations"],
    #     x=cdf["type"],
    #     fliersize=2,
    #     showfliers=False,
    # ).set(xlabel=None, ylabel="Iterations")
    # sb.boxplot(y=df["iterations"])

    plt.savefig(r"C:\Users\matteo\Documents\UniTn\Tesi\assets\boxplots_7_knapsack.svg")
    plt.show()
