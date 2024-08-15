import json
import pprint

from staketaxcsv.common.ibc.MsgInfoIBC import MsgInfoIBC
from staketaxcsv.osmo.constants import MSG_TYPE_EXECUTE_CONTRACT
from staketaxcsv.osmo import denoms as denoms_osmo


class MsgInfoOsmo(MsgInfoIBC):

    def __init__(self, wallet_address, msg_index, message, log, lcd_node):
        super().__init__(wallet_address, msg_index, message, log, lcd_node)
        self.events_by_type = self._events_by_type()
        self.execute_contract_message = self._execute_contract_message()

    def amount_currency_single(self, amount_raw, currency_raw):
        return denoms_osmo.amount_currency_from_raw(amount_raw, currency_raw, self.lcd_node)

    def _execute_contract_message(self):
        if self.msg_type == MSG_TYPE_EXECUTE_CONTRACT:
            m = self.message
            if "msg" in m:
                return m["msg"]
            elif "msg__@stringify" in m:
                return json.loads(m["msg__@stringify"])

        return {}

    def print(self):
        super().print()
        print("\n\texecute_contract_message:")
        pprint.pprint(self.execute_contract_message)


    # def amount_currency_single(self, amount_raw, currency_raw):
    #     amount, currency = denoms.amount_currency_from_raw(
    #         amount_raw, currency_raw, self.lcd_node)
    #
    #     if currency.startswith("unknown_"):
    #         # try osmosis api
    #         currency = denoms_osmo.symbol(currency_raw)
    #         if currency:
    #             exponent = denoms_osmo.exponent(currency)
    #             if exponent:
    #                 amount = float(amount_raw) / float(10 ** exponent)
    #                 return amount, currency
    #
    #     return amount, currency
