from .common import get_dict_value


class Crawler:
    """DMM WebAPI crawler."""

    def __init__(self, api_func, keys, params, hits=100, offset=1, limit=None):
        """Initialize the crawler.

        Args:
            api_func (Callable): API function to fetch data.
            keys (list): Keys to access records in the response.
            params (dict): API request parameters.
            hits (int): Number of records to fetch per request. Defaults to 100.
            offset (int): Starting offset for fetching records. Defaults to 1.
            limit (int): Maximum number of records to fetch. Defaults to None.
        """
        self.api_func = api_func
        self.keys = keys
        self.params = params
        self.hits = min(hits, limit) if limit else hits
        self.offset = offset
        self.limit = limit
        self.records = []
        self.records_idx = 0

        self._update_records()

    def __iter__(self):
        """Make the crawler an iterable."""
        return self

    def __next__(self):
        """Fetch the next record."""
        if self.records_idx >= len(self.records):
            self.offset += self.hits
            if self.limit is not None and self.offset > self.limit:
                raise StopIteration()
            self._update_records()

        self.records_idx += 1
        return self.records[self.records_idx - 1]

    def _update_records(self):
        """Fetch the next set of records from the API."""
        response = self.api_func(**self.params, hits=self.hits, offset=self.offset)
        response.raise_for_status()
        data = response.json()

        status_code = data.get("result", {}).get("status")
        if str(status_code) != "200":
            raise StopIteration(f"Unexpected status code: {status_code}")

        # Set the total limit if it is not already set
        if self.limit is None:
            self.limit = int(data["result"]["total_count"])

        # Update records and reset the index
        self.records = get_dict_value(data, self.keys)
        self.records_idx = 0
