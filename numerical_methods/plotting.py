"""Graph an interpolating polynomial. Needs matplotlib."""


def plot_polynomial(polynomial, xs, ys, title, output=None, samples=500):
    """Show the graph, or save it when output is a file name."""
    import matplotlib

    if output:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    low, high = min(xs), max(xs)
    margin = 0.025 * (high - low) or 1
    low, high = low - margin, high + margin
    grid = [low + (high - low) * i / (samples - 1) for i in range(samples)]

    figure, axes = plt.subplots()
    axes.plot(grid, [polynomial(x) for x in grid], label="polynomial")
    axes.plot(xs, ys, "o", color="tab:red", label="data")
    axes.axhline(0, color="black", linewidth=0.5)
    axes.set(title=title, xlabel="x", ylabel="y")
    axes.legend()
    if output:
        figure.savefig(output, dpi=150)
    else:
        plt.show()
    plt.close(figure)
