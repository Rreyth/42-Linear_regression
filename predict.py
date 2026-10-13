def main():
    theta0 = 0
    theta1 = 0

    mileage = input("Enter a mileage: ")

    try:
        mileage = int(mileage)
    except Exception:
        print("Error: mileage must be an integer")
        exit(1)

    try:
        file = open("weights")
        content = file.readlines()
        theta0 = float(content[0])
        theta1 = float(content[1])
        file.close()
    except Exception as e:
        print(f"Error: {e}")
        print("Using default weights instead (theta0 = 0 and theta1 = 0)")
        theta0 = 0
        theta1 = 0

    estimate_price = theta0 + (theta1 * mileage)
    print("\nEstimated price =", estimate_price)


if __name__ == "__main__":
    main()
