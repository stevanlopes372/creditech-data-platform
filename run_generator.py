import logging
from pathlib import Path

from src.data_generator.dimensions import generate_dim_date

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("--- Starting fake data generation pipeline ---")
    # df = generate_dim_date(n_days=20)
    # df = generate_dim_date(n_months=2)
    # df = generate_dim_date(n_years=2)
    df = generate_dim_date()

    print('\n' + '#'*50 + '  DataFrame head:  ' + '#'*50)
    print(df.head())
    print('\n')

    print('\n' + '#'*50 + '  DataFrame info:  ' + '#'*50)
    df.info()


if __name__ == "__main__":
    main()
