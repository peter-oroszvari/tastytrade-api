import json

class Quote:

    def __init__(self, symbol, event_time, sequence, time_nano_part, bid_time, bid_exchange_code, bid_price, bid_size, ask_time, ask_exchange_code, ask_price, ask_size):
        """
        Initializes an instance of the class with the given parameters.

        Args:
            symbol (str): The symbol of the event.
            event_time (int): The time of the event.
            sequence (int): The sequence of the event.
            time_nano_part (int): The nano part of the time of the event.
            bid_time (int): The time of the bid.
            bid_exchange_code (str): The exchange code of the bid.
            bid_price (float): The price of the bid.
            bid_size (int): The size of the bid.
            ask_time (int): The time of the ask.
            ask_exchange_code (str): The exchange code of the ask.
            ask_price (float): The price of the ask.
            ask_size (int): The size of the ask.
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
    def from_list(cls, data_list):
        """
        Creates a list of Quote objects from a list of data.

        Args:
            cls (class): The class object.
            data_list (list): The list of data to convert into Quote objects.

        Returns:
            list: The list of Quote objects created from the data.
        """ 
        quotes = []
        if not data_list:
            print("Invalid data list received")
            return quotes

        # Check if the first element is a header, if yes, skip it
        if isinstance(data_list[0], list) and len(data_list[0]) > 1 and data_list[0][0] == 'Quote' and data_list[0][1][0] == 'eventSymbol':
            data_list = data_list[1:]

        for i in range(0, len(data_list)):
            quote_data = data_list[i]
            if len(quote_data) != 12:
                continue

            symbol, event_time, sequence, time_nano_part, bid_time, bid_exchange_code, bid_price, bid_size, ask_time, ask_exchange_code, ask_price, ask_size = quote_data
            bid_size = float(bid_size) if bid_size != 'NaN' else None
            ask_size = float(ask_size) if ask_size != 'NaN' else None
            quote = cls(symbol, event_time, sequence, time_nano_part, bid_time, bid_exchange_code, bid_price, bid_size, ask_time, ask_exchange_code, ask_price, ask_size)
            quotes.append(quote)
        return quotes



    def __str__(self):
        """
        Return a string representation of the object.

        Returns:
            str: A string representing the object, including the symbol, event time,
                sequence, time nano part, bid time, bid exchange code, bid price,
                bid size, ask time, ask exchange code, ask price, and ask size.
        """
        return f"Symbol: {self.symbol}, Event time: {self.event_time}, Sequence: {self.sequence}, Time nano part: {self.time_nano_part}, Bid time: {self.bid_time}, Bid exchange code: {self.bid_exchange_code}, Bid price: {self.bid_price}, Bid size: {self.bid_size}, Ask time: {self.ask_time}, Ask exchange code: {self.ask_exchange_code}, Ask price: {self.ask_price}, Ask size: {self.ask_size}"
