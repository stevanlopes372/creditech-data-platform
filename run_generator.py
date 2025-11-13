import pandas as pd
import logging
from pathlib import Path

from src.data_generator.dimensions import generate_dim_date

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("--- Starting fake data generation pipeline ---")

    df_default = generate_dim_date(end_align_to='year')
    print(df_default.head(3))
    print("")
    print(df_default.tail(3))


if __name__ == "__main__":
    main()
