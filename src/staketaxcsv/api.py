import logging

from staketaxcsv.settings_csv import (
    TICKER_ALGO, TICKER_AKT, TICKER_ARCH, TICKER_ATOM, TICKER_BLD, TICKER_BTSG, TICKER_DVPN,
    TICKER_EVMOS, TICKER_FET, TICKER_COSMOSPLUS, TICKER_HUAHUA,
    TICKER_IOTEX, TICKER_JUNO, TICKER_KUJI, TICKER_KYVE, TICKER_LUNA1,
    TICKER_LUNA2, TICKER_MNTL, TICKER_OSMO, TICKER_REGEN,
    TICKER_ROWAN, TICKER_SCRT, TICKER_SOL, TICKER_STARS, TICKER_STRD, TICKER_TIA,
    TICKER_TORI
)
from staketaxcsv.common.ExporterTypes import FORMATS

import staketaxcsv.report_algo
import staketaxcsv.report_akt
import staketaxcsv.report_arch
import staketaxcsv.report_atom
import staketaxcsv.report_bld
import staketaxcsv.report_btsg
import staketaxcsv.report_cosmosplus
import staketaxcsv.report_dvpn
import staketaxcsv.report_evmos
import staketaxcsv.report_fet
import staketaxcsv.report_huahua
import staketaxcsv.report_iotex
import staketaxcsv.report_juno
import staketaxcsv.report_kuji
import staketaxcsv.report_kyve
import staketaxcsv.report_luna1
import staketaxcsv.report_luna2
import staketaxcsv.report_mntl
import staketaxcsv.report_osmo
import staketaxcsv.report_regen
import staketaxcsv.report_rowan
import staketaxcsv.report_scrt
import staketaxcsv.report_sol
import staketaxcsv.report_stars
import staketaxcsv.report_strd
import staketaxcsv.report_tia
import staketaxcsv.report_tori


REPORT_MODULES = {
    TICKER_ALGO: staketaxcsv.report_algo,
    TICKER_AKT: staketaxcsv.report_akt,
    TICKER_ARCH: staketaxcsv.report_arch,
    TICKER_ATOM: staketaxcsv.report_atom,
    TICKER_BLD: staketaxcsv.report_bld,
    TICKER_BTSG: staketaxcsv.report_btsg,
    TICKER_COSMOSPLUS: staketaxcsv.report_cosmosplus,
    TICKER_DVPN: staketaxcsv.report_dvpn,
    TICKER_EVMOS: staketaxcsv.report_evmos,
    TICKER_FET: staketaxcsv.report_fet,
    TICKER_HUAHUA: staketaxcsv.report_huahua,
    TICKER_IOTEX: staketaxcsv.report_iotex,
    TICKER_JUNO: staketaxcsv.report_juno,
    TICKER_KUJI: staketaxcsv.report_kuji,
    TICKER_KYVE: staketaxcsv.report_kyve,
    TICKER_LUNA1: staketaxcsv.report_luna1,
    TICKER_LUNA2: staketaxcsv.report_luna2,
    TICKER_MNTL: staketaxcsv.report_mntl,
    TICKER_OSMO: staketaxcsv.report_osmo,
    TICKER_REGEN: staketaxcsv.report_regen,
    TICKER_ROWAN: staketaxcsv.report_rowan,
    TICKER_SCRT: staketaxcsv.report_scrt,
    TICKER_SOL: staketaxcsv.report_sol,
    TICKER_STARS: staketaxcsv.report_stars,
    TICKER_STRD: staketaxcsv.report_strd,
    TICKER_TIA: staketaxcsv.report_tia,
    TICKER_TORI: staketaxcsv.report_tori,
}


def tickers():
    return sorted(REPORT_MODULES.keys())


def formats():
    return FORMATS


def has_csv(ticker, wallet_address):
    """ Returns True if wallet_address is valid address.

    :param ticker: ALGO|ATOM|LUNA1|LUNA2|...   [see staketaxcsv.tickers()]
    :param wallet_address: <string wallet address>
    """

    module = REPORT_MODULES[ticker]
    return module.wallet_exists(wallet_address)


def csv(ticker, wallet_address, csv_format, path=None, options=None, logs=True):
    """ Writes one CSV file, for this wallet address, in this format.

    :param ticker: ALGO|ATOM|LUNA1|LUNA2|...   [see staketaxcsv.tickers()]
    :param wallet_address: <string wallet address>
    :param csv_format: default|accointing|koinly|cointracking|... [see staketaxcsv.formats()]
    :param path: (optional) <string file path> .  By default, writes to /tmp .
    :param options: (optional) dictionary [documentation not in great state; see parse_args() in
           https://github.com/hodgerpodger/staketaxcsv/blob/main/src/staketaxcsv/common/report_util.py]
    :param logs: (optional) show logging.  Defaults to True.

    """
    path = path if path else "/tmp/{}.{}.{}.csv".format(ticker, wallet_address, csv_format)
    options = options if options else {}
    if logs:
        logging.basicConfig(level=logging.INFO)

    # Run report
    module = REPORT_MODULES[ticker]
    module.read_options(options)
    exporter = module.txhistory(wallet_address)
    exporter.sort_rows()

    # Print transactions table to console
    if logs:
        exporter.export_print()

    # Write CSV
    exporter.export_format(csv_format, path)


def csv_all(ticker, wallet_address, dirpath=None, options=None, logs=True):
    """ Writes CSV files, for this wallet address, in all CSV formats.

    :param ticker: ALGO|ATOM|LUNA1|LUNA2|...   [see staketaxcsv.tickers()]
    :param wallet_address: <string wallet address>
    :param dirpath: (optional) <string directory path> directory to write CSV files to.
                     By default, writes to /tmp .
    :param options: (optional)
    :param logs: (optional) show logging.  Defaults to True.
    """
    dirpath = dirpath if dirpath else "/tmp"
    options = options if options else {}
    if logs:
        logging.basicConfig(level=logging.INFO)

    # Run report
    module = REPORT_MODULES[ticker]
    module.read_options(options)
    exporter = module.txhistory(wallet_address)
    exporter.sort_rows()

    # Print transactions table to console
    if logs:
        exporter.export_print()

    # Write CSVs
    for cur_format in FORMATS:
        path = "{}/{}.{}.{}.csv".format(dirpath, ticker, wallet_address, cur_format)
        exporter.export_format(cur_format, path)


def transaction(ticker, wallet_address, txid, csv_format="", path="", options=None):
    """ Print transaction to console.  If csv_format specified, writes CSV file of single transaction.

    :param ticker: ALGO|ATOM|LUNA1|LUNA2|...   [see staketaxcsv.tickers()]
    :param wallet_address: <string wallet address>
    :param txid: <string transaction id>
    :param csv_format: (optional) default|accointing|koinly|cointracking|... [see staketaxcsv.formats()]
    :param path: (optional) <string file path> .  By default, writes to /tmp .
    :param options: (optional) dictionary [documentation not in great state; see parse_args() in
           https://github.com/hodgerpodger/staketaxcsv/blob/main/src/staketaxcsv/common/report_util.py]
    """
    logging.basicConfig(level=logging.INFO)
    options = options if options else {}

    # Run report for single transaction
    module = REPORT_MODULES[ticker]
    module.read_options(options)
    exporter = module.txone(wallet_address, txid)

    if csv_format == "":
        exporter.export_print()
    elif csv_format == "test":
        return exporter.export_for_test()
    else:
        exporter.export_print()
        path = path if path else "/tmp/{}.{}.csv".format(txid, csv_format)
        exporter.export_format(csv_format, path)


def historical_balances(ticker, wallet_address, path=None, options=None, logs=""):
    """ Writes historical balances CSV file for this wallet_address

        :param ticker: ALGO|ATOM|LUNA1|LUNA2|...   [see staketaxcsv.tickers()]
        :param wallet_address: <string wallet address>
        :param path: (optional) <string file path> .  By default, writes to /tmp .
        :param options: (optional) dictionary [documentation not in great state; see parse_args() in
               https://github.com/hodgerpodger/staketaxcsv/blob/main/src/staketaxcsv/common/report_util.py]
        :param logs: ""|"test"
    """
    path = path if path else f"/tmp/{ticker}.{wallet_address}.balances_historical.csv"
    options = options if options else {}

    module = REPORT_MODULES[ticker]

    if hasattr(module, staketaxcsv.report_akt.balhistory.__name__):
        module.read_options(options)
        bal_exporter = module.balhistory(wallet_address)
        if not bal_exporter:
            raise Exception("balhistory() did not return ExporterBalance object")

        if logs == "test":
            return bal_exporter.export_for_test()
        else:
            bal_exporter.export_csv(path)
    else:
        logging.error("No balhistory() function found for module=%s", str(module))
