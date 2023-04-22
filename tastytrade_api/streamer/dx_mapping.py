import json

class Quote:
   
    def __init__(self, symbol, event_time, sequence, time_nano_part, bid_time, bid_exchange_code, bid_price, bid_size, ask_time, ask_exchange_code, ask_price, ask_size):
        """
        Initializes a new instance of the class.

        Args:
            symbol (Any): The symbol.
            event_time (Any): The event time.
            sequence (Any): The sequence.
            time_nano_part (Any): The time nano part.
            bid_time (Any): The bid time.
            bid_exchange_code (Any): The bid exchange code.
            bid_price (Any): The bid price.
            bid_size (Any): The bid size.
            ask_time (Any): The ask time.
            ask_exchange_code (Any): The ask exchange code.
            ask_price (Any): The ask price.
            ask_size (Any): The ask size.
        """
        self.symbol = symbol
        self.event_time = event_time
        self.sequence = sequence
        self.time_nano_part = time_nano_part
        self.bid_time = bid_time
        self.bid_exchange_code = bid_exchange_code
        self.bid_price = bid_price
        self.bid_size = bid_size
        self.ask_time = ask_time
        self.ask_exchange_code = ask_exchange_code
        self.ask_price = ask_price
        self.ask_size = ask_size
        
    @classmethod
    def from_json(cls, json_message):
        try:
            data_list = json.loads(json_message)[0]["data"][1]
        except (KeyError, ValueError, IndexError):
            raise ValueError("Invalid JSON message")
        quotes = []
        for i in range(0, len(data_list), 12):
            quote_data = data_list[i:i+12]
            quote = cls(*quote_data)
            quotes.append(quote)
        return quotes
    
    def __str__(self):
        return f"Symbol: {self.symbol}, Event time: {self.event_time}, Sequence: {self.sequence}, Time nano part: {self.time_nano_part}, Bid time: {self.bid_time}, Bid exchange code: {self.bid_exchange_code}, Bid price: {self.bid_price}, Bid size: {self.bid_size}, Ask time: {self.ask_time}, Ask exchange code: {self.ask_exchange_code}, Ask price: {self.ask_price}, Ask size: {self.ask_size}"

"""
data1 = [{'data': ['Quote', ['AAPL', 0, 0, 0, 0, 'Q', 167.1, 439.0, 0, 'Q', 167.12, 602.0, 'TSLA', 0, 0, 0, 0, 'Q', 162.07, 100.0, 0, 'Q', 162.09, 100.0]], 'channel': '/service/data'}]
data2 = [{'data': ['Quote', ['AAPL', 0, 0, 0, 0, 'Q', 167.11, 200.0, 0, 'Q', 167.12, 302.0]], 'channel': '/service/data'}]

quotes1 = Quote.from_json(json.dumps(data1))
for quote in quotes1:
    print(quote)
"""