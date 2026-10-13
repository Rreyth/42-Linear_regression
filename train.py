from numpy import array as npArray
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

NB_ITER = 1500


def get_data():
    try:
        with open("data.csv") as f:
            lines = f.readlines()
    except OSError as e:
        print(f"Error: cannot read data.csv: {e}")
        exit(1)

    mileages, prices = [], []
    first_line = True
    for n, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        values = line.strip().split(',')
        if len(values) != 2:
            print(f"Error: wrong number of values on line {n}: {line.strip()}")
            exit(1)
        try:
            mileage, price = int(values[0]), int(values[1])
        except ValueError:
            if first_line:
                first_line = False
                continue
            print(f"Error: invalid data on line {n}: {line.strip()}")
            exit(1)
        first_line = False
        mileages.append(mileage)
        prices.append(price)

    if not mileages:
        print("Error: no data found in data.csv")
        exit(1)
    return npArray(mileages), npArray(prices)


def gradient_descent(theta0, theta1, learning_rate, pred, mileages,
                     norm_prices, norm_mileages):
    theta0 -= learning_rate * 1 / len(mileages) * sum(pred - norm_prices)
    theta1 -= learning_rate * 1 / len(mileages) * sum((pred - norm_prices)
                                                      * norm_mileages)
    pred = theta0 + theta1 * norm_mileages
    return theta0, theta1, pred


def save_weights(theta0, theta1):
    save = f"{theta0}\n{theta1}"
    try:
        file = open("weights", 'w')
        file.write(save)
        file.close()
    except Exception as e:
        print(f"ERROR: could not save final weights: {str(e)}")
    print(f"Final weights:\ntheta0: {theta0}\ntheta1: {theta1}")


def linear_regression(theta0, theta1, learning_rate, mileages, prices):
    norm_mileages = mileages / max(mileages)
    norm_prices = prices / max(prices)
    pred = theta0 + theta1 * norm_mileages

    theta0_history = [theta0]
    theta1_history = [theta1]
    loss_history = []

    for i in range(NB_ITER):
        theta0, theta1, pred = gradient_descent(
            theta0, theta1, learning_rate,
            pred, mileages, norm_prices, norm_mileages
        )
        theta0_history.append(theta0)
        theta1_history.append(theta1)

        mse = sum((pred - norm_prices) ** 2) / len(mileages)
        loss_history.append(mse)

    theta0_real = [t0 * max(prices) for t0 in theta0_history]
    theta1_real = [t1 * (max(prices) / max(mileages)) for t1 in theta1_history]

    end0 = theta0 * max(prices)
    end1 = theta1 * (max(prices) / max(mileages))

    save_weights(end0, end1)

    return theta0_real, theta1_real, loss_history


def display_plot(mileages, prices,
                 theta0_histo, theta1_histo, loss_histo):
    fig, (ax_reg, ax_loss) = plt.subplots(2, 1, figsize=(8, 8))
    plt.subplots_adjust(bottom=0.25)

    ax_reg.scatter(mileages, prices, label='Cars')
    ax_reg.set_xlabel("Mileages")
    ax_reg.set_ylabel("Prices")

    line, = ax_reg.plot(
        mileages,
        theta0_histo[NB_ITER] + theta1_histo[NB_ITER] * mileages,
        color="red",
        label="Regression"
    )

    ax_reg.legend()

    ax_loss.plot(loss_histo, label="MSE loss")
    ax_loss.set_xlabel("Iterations")
    ax_loss.set_ylabel("Loss")
    ax_loss.legend()

    ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])

    slider = Slider(
        ax=ax_slider,
        label='Iteration',
        valmin=0,
        valmax=len(theta0_histo) - 1,
        valinit=NB_ITER,
        valstep=1
    )

    def update_slider(val):
        i = int(slider.val)
        y = theta0_histo[i] + theta1_histo[i] * mileages
        line.set_ydata(y)
        fig.canvas.draw_idle()

    slider.on_changed(update_slider)
    plt.show()


def main():
    mileages, prices = get_data()
    learning_rate = 0.1
    theta0 = 0
    theta1 = 0

    theta0_histo, theta1_histo, loss_histo = (
        linear_regression(theta0, theta1, learning_rate, mileages, prices))

    display_plot(mileages, prices,
                 theta0_histo, theta1_histo, loss_histo)


if __name__ == "__main__":
    main()
