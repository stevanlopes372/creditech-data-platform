import logging
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from faker import Faker


# Configuração básica do logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# instanciando o Faker para português do Brasil
fake = Faker('pt_BR')


def generate_dim_date(n_days: int = None, n_months: int = None, n_years: int = None, bom: bool = True):

    logging.info(f"Starting date generation")

    # datas_schema = {
    #     date_key: str,
    #     date: datetime,
    #     year: int,
    #     month: int,
    #     day: int,
    #     weekday: int,
    #     week: int,
    #     quarter: int,
    #     half: int
    # }

    # dim_data = pd.DataFrame(columns=datas_schema.keys()).astype(datas_schema)

    end_date = date.today()

    if n_days:
        start_date = end_date - timedelta(days=n_days)

    elif n_months:
        start_date = end_date - relativedelta(months=n_months)

    elif n_years:
        start_date = end_date - relativedelta(years=n_years)

    else:
        start_date = end_date - relativedelta(years=1)
        start_date = start_date.replace(month=1, day=1)

    logging.info(f"Start date = {start_date}  |  End date = {end_date}")

    date_range = pd.date_range(start=start_date, end=end_date)

    df_date = pd.DataFrame(index=date_range)

    return df_date
