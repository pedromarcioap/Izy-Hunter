import requests
from datetime import datetime, timedelta
import random
from mock_data import MockDataGenerator
from real_search import RealSearchEngine, APISearchEngine

class SearchEngineManager:
    def __init__(self, use_real_data=False):
        self.mock_data = MockDataGenerator()
        self.real_search = RealSearchEngine()
        self.api_search = APISearchEngine()
        self.use_real_data = use_real_data
        
        self.engines = {
            'Google': self._search_google,
            'You': self._search_you,
            'Perplexity': self._search_perplexity,
            'Bing': self._search_bing,
            'DuckDuckGo': self._search_duckduckgo
        }
    
    def search_all_engines(self, selected_engines, query, custom_keywords):
        """Search across all selected engines"""
        all_results = []
        
        for engine in selected_engines:
            if engine in self.engines:
                try:
                    results = self.engines[engine](query, custom_keywords)
                    all_results.extend(results)
                except Exception as e:
                    print(f"Error searching {engine}: {e}")
                    continue
        
        return all_results
    
    def _search_google(self, query, custom_keywords):
        """Search Google - real or mock data based on configuration"""
        if self.use_real_data:
            # Use real search engine
            results = self.real_search.search_google_web(query, custom_keywords)
            for result in results:
                result['search_engine'] = 'Google'
            return results
        else:
            # Use mock data with clear labeling
            results = self.mock_data.generate_google_results(query, custom_keywords)
            for result in results:
                result['search_engine'] = 'Google (Dados Simulados)'
                result['is_mock_data'] = True
            return results
    
    def _search_you(self, query, custom_keywords):
        """Search You.com - mock data with clear labeling"""
        results = self.mock_data.generate_you_results(query, custom_keywords)
        for result in results:
            result['search_engine'] = 'You.com (Dados Simulados)'
            result['is_mock_data'] = True
        return results
    
    def _search_perplexity(self, query, custom_keywords):
        """Search Perplexity - mock data with clear labeling"""
        results = self.mock_data.generate_perplexity_results(query, custom_keywords)
        for result in results:
            result['search_engine'] = 'Perplexity (Dados Simulados)'
            result['is_mock_data'] = True
        return results
    
    def _search_bing(self, query, custom_keywords):
        """Search Bing - mock data with clear labeling"""
        results = self.mock_data.generate_bing_results(query, custom_keywords)
        for result in results:
            result['search_engine'] = 'Bing (Dados Simulados)'
            result['is_mock_data'] = True
        return results
    
    def _search_duckduckgo(self, query, custom_keywords):
        """Search DuckDuckGo - real or mock data based on configuration"""
        if self.use_real_data:
            # Use real DuckDuckGo search
            results = self.real_search.search_duckduckgo(query, custom_keywords)
            for result in results:
                result['search_engine'] = 'DuckDuckGo'
            return results
        else:
            # Use mock data with clear labeling
            results = self.mock_data.generate_bing_results(query, custom_keywords)  # Reuse Bing mock data
            for result in results:
                result['search_engine'] = 'DuckDuckGo (Dados Simulados)'
                result['is_mock_data'] = True
            return results
    
    def _make_search_request(self, engine, query, api_key=None):
        """Make actual search request to external API"""
        # This method would contain the actual API calls
        # For now, it's a placeholder for future implementation
        pass
