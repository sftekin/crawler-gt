import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def analyze():
    file_path = "stats.csv"
    rows = []
    with open(file_path, "r", newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            rows.append([float(r) for r in row])

    stat_df = pd.DataFrame(rows, columns=["time", "url_count", "keyword_count"])
    stat_df["time"] = stat_df["time"] - stat_df["time"].iloc[0]
    stat_df.set_index("time")
    print(stat_df.head(10))

    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    x_axis = stat_df.index
    ax[0].plot(x_axis, stat_df["url_count"], lw=3, c="navy", label="URL count")
    ax[0].set_ylabel("URL count")
    y_ticks = np.linspace(0, np.max(stat_df["url_count"]), 10)
    y_ticklabels = [f"{int(y)}" for y in y_ticks]
    ax[0].set_yticks(y_ticks)
    ax[0].set_yticklabels(y_ticklabels)
    ax[1].plot(x_axis, stat_df["keyword_count"], lw=3, c="firebrick", label="keyword count")
    ax[1].set_ylabel("Keyword count")
    y_ticks = np.linspace(0, np.max(stat_df["keyword_count"]), 10)
    y_ticklabels = [f"{int(y)}" for y in y_ticks]
    ax[1].set_yticks(y_ticks)
    ax[1].set_yticklabels(y_ticklabels)
    for i in range(2):
        ax[i].set_xlabel("time (s)")
        ax[i].grid()
        ax[i].legend()
    plt.suptitle("Crawler analysis")
    plt.savefig("crawler_analysis.png", dpi=200, bbox_inches="tight")
    print("Saved under crawler_analysis.png")


if __name__ == '__main__':
    analyze()
