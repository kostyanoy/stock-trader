import yfinance as yf


def download():
    with open("../stock.txt", "r") as f:
        ticker = f.read().strip()

    print(ticker)

    start_date = "2021-01-01"
    end_date = "2022-01-01"
    csv_file_path = "../data/stock_data.csv"

    stock_data = yf.download(ticker, start=start_date, end=end_date)

    stock_data.to_csv(csv_file_path)


if __name__ == "__main__":
    download()
