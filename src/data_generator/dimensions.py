import logging
import pandas as pd
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from typing import Optional, List, Literal
# from faker import Faker


# Configuração básica do logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# instanciando o Faker para português do Brasil
# fake = Faker('pt_BR')


def generate_dim_date(
    n_days: Optional[int] = None,
    n_months: Optional[int] = None,
    n_years: Optional[int] = None,
    begining_align_to: Optional[Literal['month', 'year']] = None,
    end_align_to: Optional[Literal['month', 'year']] = None,
    closed_range: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Gera uma dimensão de data (dim_date) como um DataFrame Pandas.

    A data de início é calculada para trás a partir de hoje,
    com precedência: n_days > n_months > n_years.
    Se nada for passado, o default é 1 ano atrás alinhado ao início do ano.

    Args:
        n_days: Número de dias para trás.
        n_months: Número de meses para trás.
        n_years: Número de anos para trás.
        begining_align_to: Trunca a data de início.
                  'month': Trunca para o primeiro dia do mês.
                  'year': Trunca para o primeiro dia do ano.
                  None: Usa a data exata calculada.
        end_align_to: Trunca a data para o fim.
                  'month': trunca para o fim do mês atual
                  'year': trunca para o fim do ano atual.

    Returns:
        pd.DataFrame: Um DataFrame indexado por data (DatetimeIndex)
                      com colunas de atributos de data (ano, mês, dia, etc.).
    """

    if closed_range is not None:
        logging.info(
            f"--- Starting date generation in closed date range ---")
        if len(closed_range) != 2:
            raise ValueError(
                f"closed_range parameter has expected 2 itens and currenlty we have {len(closed_range)}")

        try:
            start_date = datetime.strptime(closed_range[0], "%Y-%m-%d").date()
            end_date = datetime.strptime(closed_range[1], "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError(
                f"Invalid date format in closed_range. Use 'yyy-mm-dd'. Erro: {e}")

    else:
        logging.info(
            f"--- Starting date generation (Begining Align = {begining_align_to}  |  End Align = {end_align_to}) ---")

        today = date.today()

        if end_align_to == 'month':
            end_date = today.replace(
                day=1) + relativedelta(months=1) - timedelta(days=1)
            logging.info(f"End date aligned to END OF MONTH: {end_date}")

        elif end_align_to == 'year':
            # Mais simples e direto para o fim do ano
            end_date = today.replace(month=12, day=31)
            logging.info(f"End date aligned to END OF YEAR: {end_date}")

        else:
            end_date = today
            logging.info(f"End date used: {end_date}")

        if n_days:
            start_date = end_date - timedelta(days=n_days)
        elif n_months:
            start_date = end_date - relativedelta(months=n_months)
        elif n_years:
            start_date = end_date - relativedelta(years=n_years)
        else:
            start_date = end_date - relativedelta(years=1)
            if begining_align_to is None:
                begining_align_to = 'year'
                logging.info(
                    "Default behavior: 1 year back, aligned to the beginning of the year.")

        logging.info(
            f"Calculated start date (before alignment): {start_date}")

        if begining_align_to == 'month':
            start_date = start_date.replace(day=1)
            logging.info(f"Start date aligned to BEGINING OF THE MONTH.")
        elif begining_align_to == 'year':
            start_date = start_date.replace(month=1, day=1)
            logging.info(f"Start date aligned to BEGINING OF THE YEAR.")

    logging.info(
        f"Range final: Start = {start_date} | End = {end_date}")

    if start_date > end_date:
        logging.warning(
            f"Start date ({start_date}) is after end date ({end_date}). Returning empty DataFrame.")
        return pd.DataFrame()

    date_range = pd.date_range(start=start_date, end=end_date)

    if date_range.empty:
        logging.warning("Date range is empty. Returning empty DataFrame.")
        return pd.DataFrame()

    df_date = pd.DataFrame(index=date_range)
    df_date.index.name = 'date'

    # Usando vetorização do DatetimeIndex (performático)
    df_date['date_key'] = df_date.index.strftime('%Y%m%d').astype(int)
    df_date['year'] = df_date.index.year
    df_date['month'] = df_date.index.month
    df_date['day'] = df_date.index.day
    df_date['weekday'] = df_date.index.weekday  # Segunda=0, Domingo=6
    df_date['day_name'] = df_date.index.day_name()
    df_date['week'] = df_date.index.isocalendar().week.astype(int)
    df_date['quarter'] = df_date.index.quarter

    # Cálculo de semestre (esperto, gostei)
    df_date['semester'] = (df_date['quarter'] - 1) // 2 + 1

    df_date['is_month_end'] = df_date.index.is_month_end
    df_date['is_year_end'] = df_date.index.is_year_end

    logging.info(f"dim_date generated with {len(df_date)} rows.")
    return df_date
