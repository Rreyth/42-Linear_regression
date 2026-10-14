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
    return mileages, prices


def predict_all(mileages, theta0, theta1):
    res = []
    for mileage in mileages:
        res.append(theta0 + theta1 * mileage)

    return res


def r_squared(real_prices, predicted_prices):
    mean_real = sum(real_prices) / len(real_prices)
    Ssquare_total = sum((value - mean_real) ** 2 for value in real_prices)
    Ssquare_err = sum((pred_value - real_value) ** 2
                      for pred_value, real_value
                      in zip(predicted_prices, real_prices))
    rsquared = 1 - (Ssquare_err / Ssquare_total)

    return rsquared


def main():
    theta0 = 0
    theta1 = 0

    try:
        file = open("weights")
        content = file.readlines()
        theta0 = float(content[0])
        theta1 = float(content[1])
        file.close()
    except Exception:
        print("Error: weights are needed to compute precision,",
              "please launch train.py")
        exit(1)

    mileages, real_prices = get_data()
    predicted_prices = predict_all(mileages, theta0, theta1)
    precision = r_squared(real_prices, predicted_prices) * 100
    print(f"prediction precision is: {precision:0.2f}%")


if __name__ == "__main__":
    main()
