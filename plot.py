import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import os


def rastrigin_fitness(genome: str, size: int) -> float:
    val = genome - size
    return (10 + np.power(val, 2)) - (10 * np.cos(2 * np.pi * val))


def square_fitness(val, size: int) -> float:
    v = val - size
    return np.power(v, 2)


def read_data(elems: "list[str]") -> "pd.DataFrame":
    dataframes = []
    for e in elems:
        path = e.split("€")[0]
        label = e.split("€")[1]
        d = pd.read_csv(path)
        d["type"] = label
        dataframes.append(d)
    return pd.concat(dataframes)


def generate_image(arguments: "list[str]", **kwargs):
    df = read_data(arguments)
    length = len(arguments)
    fontsize = 10 + (length**2)
    path = kwargs.get("path", None)
    sb.set_palette(palette="plasma", n_colors=length)
    sb.set_style(style="whitegrid")
    fig, ax = plt.subplots(figsize=(6 * length, 4 + (2 * length)))

    bpdict = sb.boxplot(
        data=df,
        x="type",
        hue="type",
        y="iterations",
        width=0.5,
        ax=ax,
        whis=6,
        fliersize=0,
        dodge=False,
        notch=True,
        showmeans=True,
        meanline=True,
        showbox=False,
        showfliers=False,
        showcaps=False,
        medianprops={"linewidth": 0},
        whiskerprops={"linewidth": 0},
        meanprops={"linewidth": 1, "color": "black"},
    )
    fig.canvas.draw()
    bpdict.tick_params(labelsize=fontsize)
    means = df.groupby(["type"])["iterations"].mean()
    vertical_offset = df["iterations"].max() * 0.01
    print(ax.get_xticklabels())
    for i, xtick in enumerate(ax.get_xticklabels()):
        y = means[xtick.get_text()]
        bpdict.text(
            i + 0.2,
            y + vertical_offset,
            y,
            horizontalalignment="center",
            size=fontsize,
            color="black",
            weight="normal",
        )
    ylims = ax.get_ylim()
    ax = sb.violinplot(
        data=df,
        y="iterations",
        x="type",
        hue="type",
        dodge=False,
        legend=False,
        linewidth=0,
        ax=ax,
    )
    for violin in ax.collections:
        violin.set_alpha(0.45)
    ax = sb.stripplot(
        data=df,
        y="iterations",
        x="type",
        hue="type",
        zorder=1,
        jitter=0.1,
        size=4 * length,
        legend=False,
        ax=ax,
        alpha=0.5,
    )

    ax.set(ylim=ylims)
    ax.set_ylabel("Generations", fontsize=fontsize)
    ax.set_xlabel("")
    plt.legend([], [], frameon=False)
    plt.tight_layout()
    # os.makedirs(path, exist_ok=True)
    if path is not None:
        plt.savefig(path)
    plt.show()
    # else:


def regenerate_all():
    generate_image(
        [
            r"results\knapsack_7\diffusion_recombined_poly.csv,EQDR",
            r"results\knapsack_7\not_recombined.csv,BBHT",
        ],
        path=r"C:\Users\matteo\Documents\UniTn\Tesi\assets\boxplots_7_knapsack.svg",
    )
    generate_image(
        [
            r"results\recombination_type\square_contribution.csv,RCD",
            r"results\recombination_type\square_proportional.csv,SPD",
            r"results\recombination_type\square_uniform.csv,UD",
        ],
        path=r"C:\Users\matteo\Documents\UniTn\Tesi\assets\recombination_square.svg",
    )
    generate_image(
        [
            r"results\recombination_type\multimodal_contribution.csv,RCD",
            r"results\recombination_type\multimodal_proportional.csv,SPD",
            r"results\recombination_multimodal\multimodal_uniform.csv,UD",
        ],
        path=r"C:\Users\matteo\Documents\UniTn\Tesi\assets\recombination_multimodal.svg",
    )
    generate_image(
        [
            r"results\rastrigin_4\recombined.csv,EQDR",
            r"results\rastrigin_4\not_recombined.csv,BBHT",
        ],
        path=r"C:\Users\matteo\Documents\UniTn\Tesi\assets\4_qubits.svg",
    )
    generate_image(
        [
            r"results\rastrigin\recombined_tweaked.csv,EQDR",
            r"results\rastrigin\not_recombined.csv,BBHT",
        ],
        path=r"C:\Users\matteo\Documents\UniTn\Tesi\assets\8_qubits.svg",
    )
    generate_image(
        [
            r"results\alpha\gaussian_highalpha.csv,$\alpha_g = 0.775$",
            r"results\alpha\gaussian_lowalpha.csv,$\alpha_g = 0.055$",
        ],
        path=r"C:\Users\matteo\Documents\UniTn\Tesi\assets\gaussian_alpha.svg",
    )
    generate_image(
        [
            r"results\alpha\poly_highalpha.csv,$\alpha_p = 0.975$",
            r"results\alpha\poly_lowalpha.csv,$\alpha_p = 0.75$",
        ],
        path=r"C:\Users\matteo\Documents\UniTn\Tesi\assets\poly_alpha.svg",
    )


if __name__ == "__main__":
    generate_image(
        [
            r"C:\Users\matteo\Documents\UniTn\Tesi\eqiro\results\knapsack_recombination\rcd.csv€RCD",
            r"C:\Users\matteo\Documents\UniTn\Tesi\eqiro\results\knapsack_recombination\spd.csv€SPD",
            r"C:\Users\matteo\Documents\UniTn\Tesi\eqiro\results\knapsack_recombination\ud.csv€UD",
        ],
        path=r"C:\Users\matteo\Documents\UniTn\Tesi\assets\knapsack.svg",
    )
    # generate_image(
    #     [
    #         r"results\exploration\poly_high_exp.csv€$\alpha_p=0.975, |B|=14$",
    #         r"results\exploration\poly_low_exp.csv€$\alpha_p=0.5, |B|=4$",
    #     ],
    #     path=r"C:\Users\matteo\Documents\UniTn\Tesi\assets\poly_gamma.svg",
    # )
    exit(1)
    arguments = sys.argv.copy()
    arguments.pop(0)
    sb.set_style(style="whitegrid")

    if arguments[0] == "all":
        regenerate_all()
    elif arguments[0] == "multimodal_func":
        fig, ax = plt.subplots(figsize=(12, 8))
        size = float(arguments[1])
        if len(arguments) > 1:
            path = arguments[2]
        x = np.linspace(0, 2 * size, 1000)
        x_i = np.array([int(i) for i in range(int(size) * 2 + 1)])
        y = rastrigin_fitness(x, size)
        y_i = rastrigin_fitness(x_i, size)
        # plt.plot(x, y)
        ax = sb.lineplot(x=x, y=y)
        ax.axvline(size, ls="--")
        ax.tick_params(labelsize=14)
        ax.plot(x_i, y_i)
        for w, z in zip(x_i, y_i):
            ax.plot(w, z, "o", color="#bf3982")
        plt.tight_layout()
        if path is not None:
            plt.savefig(path)
        plt.show()

    elif arguments[0] == "square":
        fig, ax = plt.subplots(figsize=(12, 8))
        size = float(arguments[1])
        if len(arguments) > 1:
            path = arguments[2]
        x = np.linspace(0, 3 * size, 1000)
        y = square_fitness(x, size)
        # plt.plot(x, y)
        ax = sb.lineplot(x=x, y=y)
        ax.axvline(size, color="orange", ls="--")
        ax.tick_params(labelsize=14)
        plt.tight_layout()
        if path is not None:
            plt.savefig(path)
        else:
            plt.show()
    else:
        generate_image(arguments)
