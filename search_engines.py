import requests
import os
import json
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

class SearchEngines:
    def __init__(self, mock_data=None):
        self.mock_data = mock_data  # Manter para fallback ou testes

    def _search_google(self, query, custom_keywords):
        api_key = os.environ.get("GOOGLE_API_KEY", "")
        cse_id = os.environ.get("GOOGLE_CSE_ID", "")
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": cse_id,
            "q": query + " " + " ".join(custom_keywords or [])
        }
        try:
            resp = requests.get(search_url, params=params)
            resp.raise_for_status()
            data = resp.json()
            results = []
            for item in data.get("items", []):
                results.append({
                    "title": item.get("title"),
                    "url": item.get("link"),
                    "description": item.get("snippet"),
                    "search_engine": "Google",
                    "is_real_data": True
                })
            return results
        except Exception as e:
            print(f"Google Search error: {e}")
            return []

    def _search_duckduckgo(self, query, custom_keywords):
        # DuckDuckGo API não oficial. Limite: só retorna instant answers (não resultados web completos)
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query + " " + " ".join(custom_keywords or []),
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        }
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            results = []
            if "RelatedTopics" in data:
                for topic in data["RelatedTopics"]:
                    if "Text" in topic and "FirstURL" in topic:
                        results.append({
                            "title": topic["Text"][:80],
                            "url": topic["FirstURL"],
                            "description": topic["Text"],
                            "search_engine": "DuckDuckGo",
                            "is_real_data": True
                        })
            # fallback para Abstract se houver
            if data.get("AbstractText"):
                results.insert(0, {
                    "title": data.get("Heading") or query,
                    "url": data.get("AbstractURL") or "",
                    "description": data.get("AbstractText"),
                    "search_engine": "DuckDuckGo",
                    "is_real_data": True
                })
            return results
        except Exception as e:
            print(f"DuckDuckGo Search error: {e}")
            return []

    def _search_yahoo(self, query, custom_keywords):
        # OAuth2 Token fetch
        client_id = os.environ.get("YAHOO_CLIENT_ID", "")
        client_secret = os.environ.get("YAHOO_CLIENT_SECRET", "")
        app_id = os.environ.get("YAHOO_APP_ID", "")
        token_url = "https://api.login.yahoo.com/oauth2/get_token"
        search_url = "https://yboss.yahooapis.com/ysearch/web"
        try:
            # Passo 1: Obtenha um token OAuth2
            auth = HTTPBasicAuth(client_id, client_secret)
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "grant_type": "client_credentials",
                "redirect_uri": "oob"
            }
            token_resp = requests.post(token_url, data=data, headers=headers, auth=auth)
            token_resp.raise_for_status()
            token_info = token_resp.json()
            access_token = token_info["access_token"]

            # Passo 2: Consulte a Search API com Bearer Token
            headers = {
                "Authorization": f"Bearer {access_token}",
                "X-Yahoo-App-Id": app_id
            }
            params = {
                "q": query + " " + " ".join(custom_keywords or []),
                "format": "json"
            }
            resp = requests.get(search_url, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            results = []
            for doc in data.get("web", {}).get("results", []):
                results.append({
                    "title": doc.get("title"),
                    "url": doc.get("url"),
                    "description": doc.get("abstract"),
                    "search_engine": "Yahoo!",
                    "is_real_data": True
                })
            return results
        except Exception as e:
            print(f"Yahoo! Search error: {e}")
            return []

    def _search_bravo(self, query, custom_keywords):
        api_key = os.environ.get("BRAVO_API_KEY", "")
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": api_key
        }
        params = {
            "q": query + " " + " ".join(custom_keywords or [])
        }
        try:
            resp = requests.get(url, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            results = []
            for item in data.get("web", {}).get("results", []):
                results.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "description": item.get("description", ""),
                    "search_engine": "Bravo Search",
                    "is_real_data": True
                })
            return results
        except Exception as e:
            print(f"Bravo Search error: {e}")
            return []

    def search_all(self, engines, query, custom_keywords):
        results = []
        if "Google" in engines:
            results.extend(self._search_google(query, custom_keywords))
        if "DuckDuckGo" in engines:
            results.extend(self._search_duckduckgo(query, custom_keywords))
        if "Yahoo!" in engines:
            results.extend(self._search_yahoo(query, custom_keywords))
        if "Bravo Search" in engines:
            results.extend(self._search_bravo(query, custom_keywords))
        return results
