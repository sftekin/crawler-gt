import matplotlib.pyplot as plt


def analyze():
    K_values = list(range(100, 900, 100))
    creation_time = [0.4199, 0.7471, 0.9908, 1.306, 1.3752, 1.4001, 1.9707, 2.1588]
    response_time = [0.0168, 0.0176, 0.0178, 0.0192, 0.0194, 0.0187, 0.0215, 0.0186]

    # create plot
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    ax[0].bar(K_values, creation_time, 50,
              color='b',
              label='Creation Time')
    ax[0].set_xlabel('number of documents (K)')
    ax[0].set_xticks(K_values)
    ax[0].set_ylabel('time (s)')
    ax[0].legend()
    ax[0].grid()

    ax[1].bar(K_values, response_time, 50,
              color='g',
              label='Response Time')
    ax[1].set_xlabel('number of documents')
    ax[1].set_ylabel('time (s)')
    ax[1].set_xticks(K_values)
    ax[1].legend()
    ax[1].grid()

    plt.suptitle("Creation & Response time by number of documents")
    plt.savefig("se_analysis.png", dpi=200, bbox_inches="tight")
    print("Saved under se_analysis.png")


if __name__ == '__main__':
    analyze()
