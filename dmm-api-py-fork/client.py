import requests

API_BASE_URL = "https://api.dmm.com/affiliate/"


class DMMApiClient:
    """DMM WebAPI client class."""

    def __init__(self, api_id, affiliate_id):
        """Initialize client."""
        self.api_id = api_id
        self.affiliate_id = affiliate_id
        self.api_version = "v3"

    def _get_common_params(self):
        """Get common parameters for request."""
        return {
            "api_id": self.api_id,
            "affiliate_id": self.affiliate_id,
            "output": "json",  # デフォルトでJSON形式を指定
        }

    def _get_url(self, path):
        """Get API URL."""
        return f"{API_BASE_URL}{self.api_version}/{path}"

    def _request_get(self, path, params=None, **kwargs):
        """Request with GET method."""
        req_params = self._get_common_params()
        if params:
            req_params.update({k: v for k, v in params.items() if v is not None})
        return requests.get(self._get_url(path), params=req_params, **kwargs)

    def get_item_list(self, **kwargs):
        """Search item API."""
        return self._request_get("ItemList", params=kwargs)

    def get_floor(self, **kwargs):
        """Get floor list API."""
        return self._request_get("FloorList", params=kwargs)

    def search_actress(self, **kwargs):
        """Search actress API."""
        return self._request_get("ActressSearch", params=kwargs)

    def search_genre(self, **kwargs):
        """Search genre API."""
        return self._request_get("GenreSearch", params=kwargs)

    def search_maker(self, **kwargs):
        """Search maker API."""
        return self._request_get("MakerSearch", params=kwargs)

    def search_series(self, **kwargs):
        """Search series API."""
        return self._request_get("SeriesSearch", params=kwargs)

    def search_author(self, **kwargs):
        """Search author API."""
        return self._request_get("AuthorSearch", params=kwargs)
