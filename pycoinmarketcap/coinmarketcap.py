from typing import Dict
from requests import Session
from requests.models import Response
from .errors import *

from __future__ import annotations

API_DOMAIN = "https://pro-api.coinmarketcap.com/v1/"
SANDBOX_API = "https://sandbox-api.coinmarketcap.com/v1/"
SANDBOX_API_KEY = "b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c"


class CoinMarketCap:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.__session = Session()
        self.__headers = {"Accept": "application/json", "X-CMC_PRO_API_KEY": api_key}

    def __cleanNoneItems(self, d: Dict):
        # https://betterprogramming.pub/how-to-remove-null-none-values-from-a-dictionary-in-python-1bedf1aab5e4
        return {k: v for k, v in d.items() if v is not None}

    def __get(self, url: str, **params) -> Dict:
        """Internal function url request getter

        Args:
            url (str): url to request
            params (Dict): url parameters

        Returns:
            [type]: Dict
        """

        r: Response = self.__session.get(
            API_DOMAIN + url,
            params=self.__cleanNoneItems(params),
            headers=self.__headers,
        )
        data = r.json()

        if r.status_code != 200:
            self.__raise_error(r.status_code, data["status"])

        return data

    def __raise_error(self, code: int, status: Dict) -> None:
        """Function of raising errors depending on status code.

        Args:
            code (int): the status code
            status (Dict): the response status object

        Raises:
            ErrorUnauthorized: 401 Unauthorized
            ErrorForbidden: 403 Forbidden
            ErrorTooManyRequests: 429 Too Many Requests
            ErrorInternalServerError: 500 Internal Server Error
            ErrorBadRequest: 400 Bad Request
        """

        if code == 401:
            raise ErrorUnauthorized(status)
        elif code == 403:
            raise ErrorForbidden(status)
        elif code == 429:
            raise ErrorTooManyRequests(status)
        elif code == 500:
            raise ErrorInternalServerError(status)

        raise ErrorBadRequest(status)

    def crypto_airdrop(self, id: str):
        """Returns information about a single airdrop available on CoinMarketCap.
        Includes the cryptocurrency data.

        Args:
            id (str): Airdrop Unique ID. This can be found using the Aidrops API.
        """
        return self.__get(f"/cryptocurrency/airdrop", id=id)

    def crypto_airdrops(
        self,
        start: int = 1,
        limit: int = None,
        status: str = "ONGOING",
        id: str = None,
        slug: str = None,
        symbol: str = None,
    ):
        """Returns a list of past, present, or future airdrops which have run on CoinMarketCap.

        Args:
            start (int): Optionally offset the start (1-based index) of the paginated list
                        of items to return. [>=1] (default: 1)
            limit (int): Optionally specify the number of results to return. Use this parameter
                        and the "start" parameter to determine your own pagination size.
            status (str): What status of airdrops.
                        Valid Values: ["ENDED", "ONGOING", "UPCOMING"] (default: "ONGOING")
            id (str): Filtered airdrops by one cryptocurrency CoinMarketCap IDs.
                        Example: 1
            slug (str): Alternatively filter airdrops by a cryptocurrency slug.
                        Example: "bitcoin"
            symbol (str): Alternatively filter airdrops one cryptocurrency symbol.
                        Example: "BTC".
        """
        return self.__get(
            f"/cryptocurrency/airdrops",
            start=start,
            limit=limit,
            status=status,
            id=id,
            slug=slug,
            symbol=symbol,
        )

    def crypto_categories(
        self,
        start: int = 1,
        limit: int = None,
        id: str = None,
        slug: str = None,
        symbol: str = None,
    ):
        return self.__get(
            f"/cryptocurrency/categories",
            start=start,
            limit=limit,
            id=id,
            slug=slug,
            symbol=symbol,
        )

    def crypto_category(
        self,
        id: str,
        start: int = 1,
        limit: int = 100,
        convert: str = None,
        convert_id: str = None,
    ):
        return self.__get(
            f"/cryptocurrency/category",
            id=id,
            start=start,
            limit=limit,
            convert=convert,
            convert_id=convert_id,
        )

    def crypto_metadata(
        self,
        id: str = None,
        slug: str = None,
        symbol: str = None,
        address: str = None,
        aux: str = "urls,logo,description,tags,platform,date_added,notice",
    ):
        return self.__get(
            "/cryptocurrency/info",
            id=id,
            slug=slug,
            symbol=symbol,
            address=address,
            aux=aux,
        )

    def crypto_map(
        self,
        listing_status: str = "active",
        start: int = 1,
        limit: int = None,
        sort: str = "id",
        symbol: str = None,
        aux: str = "platform,first_historical_data,last_historical_data,is_active",
    ):
        return self.__get(
            "/cryptocurrency/map",
            listing_status=listing_status,
            start=start,
            limit=limit,
            sort=sort,
            symbol=symbol,
            aux=aux,
        )

    def crypto_listings_historical(
        self,
        date: str,
        start: int = 1,
        limit: int = 100,
        convert: str = None,
        convert_id: str = None,
        sort: str = "cmc_rank",
        sort_dir: str = "asc",
        cryptocurrency_type: str = "all",
        aux: str = "platform,tags,date_added,circulating_supply,total_supply,max_supply,cmc_rank,num_market_pairs",
    ):
        return self.__get(
            "/cryptocurrency/listings/historical",
            date=date,
            start=start,
            limit=limit,
            convert=convert,
            convert_id=convert_id,
            sort=sort,
            sort_dir=sort_dir,
            cryptocurrency_type=cryptocurrency_type,
            aux=aux,
        )

    def crypto_listings_latest(
        self,
        start: int = 1,
        limit: int = 1,
        price_min: float = None,
        price_max: float = None,
        market_cap_min: float = None,
        volume_24h_min: float = None,
        volume_24h_max: float = None,
        circulating_supply_min: float = None,
        circulating_supply_max: float = None,
        percent_change_24h_min: float = None,
        percent_change_24h_max: float = None,
        convert: str = None,
        convert_id: str = None,
        sort: str = "market_cap",
        cryptocurrency_type: str = "all",
        tag: str = "all",
        aux: str = "num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply",
    ):
        return self.__get(
            "/cryptocurrency/listings/latest",
            start=start,
            limit=limit,
            price_min=price_min,
            price_max=price_max,
            market_cap_min=market_cap_min,
            volume_24h_min=volume_24h_min,
            volume_24h_max=volume_24h_max,
            circulating_supply_min=circulating_supply_min,
            circulating_supply_max=circulating_supply_max,
            percent_change_24h_min=percent_change_24h_min,
            percent_change_24h_max=percent_change_24h_max,
            convert=convert,
            convert_id=convert_id,
            sort=sort,
            cryptocurrency_type=cryptocurrency_type,
            tag=tag,
            aux=aux,
        )

    def crypto_marketpairs_latest(
        self,
        id: str = None,
        slug: str = None,
        symbol: str = None,
        start: int = 1,
        limit: int = 100,
        sort_dir: str = "desc",
        sort: str = "volume_24h_strict",
        aux: str = "num_market_pairs,category,fee_type",
        matched_id: str = None,
        matched_symbol: str = None,
        category: str = "all",
        fee_type: str = "all",
        convert: str = None,
        convert_id: str = None,
    ):
        return self.__get(
            "/cryptocurrency/market-pairs/latest",
            id=id,
            slug=slug,
            symbol=symbol,
            start=start,
            limit=limit,
            sort_dir=sort_dir,
            sort=sort,
            aux=aux,
            matched_id=matched_id,
            matched_symbol=matched_symbol,
            category=category,
            fee_type=fee_type,
            convert=convert,
            convert_id=convert_id,
        )

    def crypto_ohlcv_historical(
        self,
        id: str = None,
        slug: str = None,
        symbol: str = None,
        time_period: str = "daily",
        time_start: str = None,
        time_end: str = None,
        count: int = 10,
        interval: str = "daily",
        convert: str = None,
        convert_id: str = None,
        skip_invalid: bool = False,
    ):
        return self.__get(
            "/cryptocurrency/ohlcv/historical",
            id=id,
            slug=slug,
            symbol=symbol,
            time_period=time_period,
            time_start=time_start,
            time_end=time_end,
            count=count,
            interval=interval,
            convert=convert,
            convert_id=convert_id,
            skip_invalid=skip_invalid,
        )

    def crypto_ohlcv_latest(
        self,
        id: str = None,
        symbol: str = None,
        convert: str = None,
        convert_id: str = None,
        skip_invalid: bool = False,
    ):
        return self.__get(
            "/cryptocurrency/ohlvc/latest",
            id=id,
            symbol=symbol,
            convert=convert,
            convert_id=convert_id,
            skip_invalid=skip_invalid,
        )

    def crypto_price_performance_stats_latest(
        self,
        id: str = None,
        slug: str = None,
        symbol: str = None,
        time_period: str = "all_time",
        convert: str = None,
        convert_id: str = None,
        skip_invalid: bool = False,
    ):
        return self.__get(
            "/cryptocurrency/price-performance-stats/latest",
            id=id,
            slug=slug,
            symbol=symbol,
            time_period=time_period,
            convert=convert,
            convert_id=convert_id,
            skip_invalid=skip_invalid,
        )

    def crypto_quotes_historical(
        self,
        id: str = None,
        symbol: str = None,
        time_start: str = None,
        time_end: str = None,
        count: int = 10,
        interval: str = "5m",
        convert: str = None,
        convert_id: str = None,
        aux: str = "price,volume,market_cap,quote_timestamp,is_active,is_fiat",
        skip_invalid: bool = False,
    ):
        return self.__get(
            "/cryptocurrency/quotes/historical",
            id=id,
            symbol=symbol,
            time_start=time_start,
            time_end=time_end,
            count=count,
            interval=interval,
            convert=convert,
            convert_id=convert_id,
            aux=aux,
            skip_invalid=skip_invalid,
        )

    def crypto_quotes_latest(
        self,
        id: str = None,
        slug: str = None,
        symbol: str = None,
        convert: str = None,
        convert_id: str = None,
        aux: str = "num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply,is_active,is_fiat",
        skip_invalid: bool = False,
    ):
        return self.__get(
            "/cryptocurrency/quotes/latest",
            id=id,
            slug=slug,
            symbol=symbol,
            convert=convert,
            convert_id=convert_id,
            aux=aux,
            skip_invalid=skip_invalid,
        )

    def crypto_trending_gainers_losers(
        self,
        start: int = 1,
        limit: int = 100,
        time_period: str = "24h",
        convert: str = None,
        convert_id: str = None,
    ):
        return self.__get(
            "/cryptocurrency/trending/gainers-losers",
            start=start,
            limit=limit,
            time_period=time_period,
            convert=convert,
            convert_id=convert_id,
        )

    def crypto_trending_latest(
        self,
        start: int = 1,
        limit: int = 100,
        convert: str = None,
        convert_id: str = None,
    ):
        return self.__get(
            "/cryptocurrency/trending/latest",
            start=start,
            limit=limit,
            convert=convert,
            convert_id=convert_id,
        )

    def crypto_trending_most_visited(
        self,
        start: int = 1,
        limit: int = 100,
        time_period: str = "24h",
        convert: str = None,
        convert_id: str = None,
    ):
        return self.__get(
            "/cryptocurrency/trending/most-visited",
            start=start,
            limit=limit,
            time_period=time_period,
            convert=convert,
            convert_id=convert_id,
        )

    def fiat_map(
        self,
        start: int = 1,
        limit: int = None,
        sort: str = "id",
        include_metals: bool = False,
    ):
        return self.__get(
            "/fiat/map",
            start=start,
            limit=limit,
            sort=sort,
            include_metals=include_metals,
        )

    def exchange_metadata(
        self,
        id: str = None,
        slug: str = None,
        aux: str = "urls,logo,description,date_launched,notice",
    ):
        return self.__get("/exchange/info", id=id, slug=slug, aux=aux)

    def exchange_map(
        self,
        listing_status: str = "active",
        slug: str = None,
        start: int = 1,
        limit: int = None,
        sort: str = "id",
        aux: str = "first_historical_data,last_historical_data,is_active",
        crypto_id: str = "",
    ):
        return self.__get(
            "/exchange/map",
            listing_status=listing_status,
            slug=slug,
            start=start,
            limit=limit,
            sort=sort,
            aux=aux,
            crypto_id=crypto_id,
        )

    def exchange_listings_latest(
        self,
        start: int = 1,
        limit: int = 100,
        sort: str = "volume_24h",
        sort_dir: str = None,
        market_type: str = "all",
        category: str = "all",
        aux: str = "num_market_pairs,traffic_score,rank,exchange_score,effective_liquidity_24h",
        convert: str = None,
        convert_id: str = None,
    ):
        return self.__get(
            "/exchange/listings/latest",
            start=start,
            limit=limit,
            sort=sort,
            sort_dir=sort_dir,
            market_type=market_type,
            category=category,
            aux=aux,
            convert=convert,
            convert_id=convert_id,
        )

    def exchange_marketpairs_latest(
        self,
        id: str = None,
        slug: str = None,
        start: int = 1,
        limit: int = 100,
        aux: str = "num_market_pairs,category,fee_type",
        matched_id: str = None,
        matched_symbol: str = None,
        category: str = "all",
        fee_type: str = "all",
        convert: str = None,
        convert_id: str = None,
    ):
        return self.__get(
            "/exchange/market-pairs/latest",
            id=id,
            slug=slug,
            start=start,
            limit=limit,
            aux=aux,
            matched_id=matched_id,
            matched_symbol=matched_symbol,
            category=category,
            fee_type=fee_type,
            convert=convert,
            convert_id=convert_id,
        )

    def exchange_quotes_historical(
        self,
        id: str = None,
        slug: str = None,
        time_start: str = None,
        count: float = 10,
        interval: str = "5m",
        convert: str = None,
        convert_id: str = None,
    ):
        return self.__get(
            "/exchange/quotes/historical",
            id=id,
            slug=slug,
            time_start=time_start,
            count=count,
            interval=interval,
            convert=convert,
            convert_id=convert_id,
        )

    def exchange_quotes_latest(
        self,
        id: str = None,
        slug: str = None,
        convert: str = None,
        convert_id: str = None,
        aux: str = "num_market_pairs,traffic_score,rank,exchange_score,liquidity_score,effective_liquidity_24h",
    ):
        return self.__get(
            "/exchange/quotes/latest",
            id=id,
            slug=slug,
            convert=convert,
            convert_id=convert_id,
            aux=aux,
        )

    def globalmetrics_quotes_historical(
        self,
        time_start: str = None,
        time_end: str = None,
        count: int = 10,
        interval: str = "1d",
        convert: str = None,
        convert_id: str = None,
        aux: str = "btc_dominance,active_cryptocurrencies,active_exchanges,active_market_pairs,total_volume_24h,total_volume_24h_reported,altcoin_market_cap,altcoin_volume_24h,altcoin_volume_24h_reported",
    ):
        return self.__get(
            "/global-metrics/quotes/historical",
            time_start=time_start,
            time_end=time_end,
            count=count,
            interval=interval,
            convert=convert,
            convert_id=convert_id,
            aux=aux,
        )

    def globalmetrics_quotes_latest(self, convert: str = None, convert_id: str = None):
        return self.__get(
            "/global-metrics/quotes/latest", convert=convert, convert_id=convert_id
        )

    def tools_price_conversion(
        self,
        amount: float,
        id: str = None,
        symbol: str = None,
        time: str = None,
        convert: str = None,
        convert_id: str = None,
    ):
        return self.__get(
            "/tools/price-conversion",
            amount=amount,
            id=id,
            symbol=symbol,
            time=time,
            convert=convert,
            convert_id=convert_id,
        )

    def blockchain_statistics_latest(
        self, id: str = None, symbol: str = None, slug: str = None
    ):
        return self.__get(
            "/blockchain/statistics/latest", id=id, symbol=symbol, slug=slug
        )

    def partners_fsc_fcas_listings_latest(
        self,
        start: int = 1,
        limit: int = 100,
        aux: str = "point_change_24h,percent_change_24h",
    ):
        return self.__get(
            "/partners/flipside-crypto/fcas/listings/latest",
            start=start,
            limit=limit,
            aux=aux,
        )

    def partners_fsc_fcas_lquotes_latest(
        self,
        id: str = None,
        slug: str = None,
        symbol: str = None,
        aux: str = "point_change_24h,percent_change_24h",
    ):
        return self.__get(
            "/partners/flipside-crypto/fcas/quotes/latest",
            slug=slug,
            symbol=symbol,
            id=id,
            aux=aux,
        )

    def key_info(self):
        return self.__get("/key/info")
