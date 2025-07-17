import random
from datetime import datetime, timedelta

class MockDataGenerator:
    def __init__(self):
        self.contest_titles = [
            "Concurso Nacional de Contos Brasileiros",
            "Prêmio Literário Amazônia",
            "Festival de Poesia do Cerrado",
            "Edital de Apoio à Literatura Regional",
            "Antologia Vozes do Norte",
            "Concurso de Crônicas Urbanas",
            "Prêmio Jovem Escritor Brasil",
            "Festival Nacional de Cordel",
            "Concurso de Literatura Infantil",
            "Prêmio de Poesia Contemporânea"
        ]
        
        self.sources = [
            "Ministério da Cultura",
            "Fundação Cultural Palmares",
            "Instituto Brasileiro de Museus",
            "Secretaria de Cultura do Tocantins",
            "Fundação Cultural do Tocantins",
            "Editora Moderna",
            "Academia Brasileira de Letras",
            "Fundação Biblioteca Nacional",
            "SESC Nacional",
            "Itaú Cultural"
        ]
        
        self.locations = [
            "Palmas, TO",
            "Araguaína, TO",
            "Gurupi, TO",
            "Nacional (todos os estados)",
            "Região Norte",
            "Brasília, DF",
            "São Paulo, SP",
            "Rio de Janeiro, RJ",
            "Belo Horizonte, MG",
            "Salvador, BA"
        ]
        
        self.types = [
            "Concursos Literários",
            "Editais Culturais",
            "Antologias",
            "Festivais",
            "Prêmios",
            "Chamadas Públicas"
        ]
        
        self.descriptions = [
            "Concurso aberto para escritores de todo o Brasil com temática livre",
            "Edital para apoio à produção literária regional com foco na cultura local",
            "Festival que celebra a diversidade da literatura brasileira",
            "Prêmio destinado a jovens talentos da literatura nacional",
            "Chamada para participação em antologia de autores contemporâneos",
            "Concurso de contos com temática voltada para a preservação ambiental",
            "Edital para publicação de obras de autores estreantes",
            "Festival que promove a cultura popular através da literatura",
            "Prêmio para obras que retratam a realidade do interior brasileiro",
            "Concurso de poesia com temática sobre identidade cultural"
        ]
    
    def generate_google_results(self, query, custom_keywords):
        """Generate mock Google search results"""
        return self._generate_base_results(3, 7, query)
    
    def generate_you_results(self, query, custom_keywords):
        """Generate mock You.com search results"""
        return self._generate_base_results(2, 5, query)
    
    def generate_perplexity_results(self, query, custom_keywords):
        """Generate mock Perplexity search results"""
        return self._generate_base_results(2, 6, query)
    
    def generate_bing_results(self, query, custom_keywords):
        """Generate mock Bing search results"""
        return self._generate_base_results(2, 4, query)
    
    def _generate_base_results(self, min_count, max_count, query):
        """Generate base mock results"""
        results = []
        count = random.randint(min_count, max_count)
        
        for i in range(count):
            # Determine if opportunity is eligible for Tocantins
            location = random.choice(self.locations)
            tocantins_eligible = self._determine_tocantins_eligibility(location)
            
            # Generate deadline
            deadline = datetime.now() + timedelta(days=random.randint(1, 180))
            
            result = {
                'title': random.choice(self.contest_titles),
                'source': random.choice(self.sources),
                'type': random.choice(self.types),
                'description': random.choice(self.descriptions),
                'location': location,
                'deadline': deadline,
                'tocantins_eligible': tocantins_eligible,
                'url': f"https://example.com/opportunity/{i+1}",
                'published_date': datetime.now() - timedelta(days=random.randint(1, 30))
            }
            
            results.append(result)
        
        return results
    
    def _determine_tocantins_eligibility(self, location):
        """Determine if an opportunity is eligible for Tocantins residents"""
        if "TO" in location or "Tocantins" in location:
            return True
        elif "Nacional" in location or "todos os estados" in location:
            return True
        elif "Região Norte" in location:
            return True
        else:
            # Some random eligibility for other locations
            return random.choice([True, False])
    
    def generate_trending_opportunities(self):
        """Generate trending opportunities for the homepage"""
        trending = []
        for i in range(5):
            result = {
                'title': random.choice(self.contest_titles),
                'source': random.choice(self.sources),
                'type': random.choice(self.types),
                'description': random.choice(self.descriptions)[:100] + "...",
                'deadline': datetime.now() + timedelta(days=random.randint(1, 60)),
                'tocantins_eligible': random.choice([True, False])
            }
            trending.append(result)
        return trending
