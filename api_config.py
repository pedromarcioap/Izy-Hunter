import streamlit as st
import os
import json
from typing import Dict, Optional

class APIConfigManager:
    """Manages API keys and configuration for search engines"""
    
    def __init__(self):
        self.config_file = "api_config.json"
        self.supported_engines = {
            'Google': {
                'keys': ['GOOGLE_API_KEY', 'GOOGLE_CSE_ID'],
                'description': 'Google Custom Search API',
                'docs': 'https://developers.google.com/custom-search/v1/introduction'
            },
            'Bing': {
                'keys': ['BING_API_KEY'],
                'description': 'Bing Search API',
                'docs': 'https://www.microsoft.com/en-us/bing/apis/bing-web-search-api'
            },
            'DuckDuckGo': {
                'keys': [],
                'description': 'DuckDuckGo (Sem API key necessária)',
                'docs': 'https://duckduckgo.com/api'
            },
            'Perplexity': {
                'keys': ['PERPLEXITY_API_KEY'],
                'description': 'Perplexity API',
                'docs': 'https://perplexity.ai/api'
            }
        }
    
    def load_config(self) -> Dict:
        """Load API configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            st.error(f"Erro ao carregar configuração: {e}")
            return {}
    
    def save_config(self, config: Dict) -> bool:
        """Save API configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Erro ao salvar configuração: {e}")
            return False
    
    def get_api_key(self, engine: str, key_name: str) -> Optional[str]:
        """Get API key for specific engine"""
        # First check environment variables
        env_key = os.getenv(key_name)
        if env_key:
            return env_key
        
        # Then check saved configuration
        config = self.load_config()
        return config.get(engine, {}).get(key_name)
    
    def set_api_key(self, engine: str, key_name: str, key_value: str) -> bool:
        """Set API key for specific engine"""
        config = self.load_config()
        if engine not in config:
            config[engine] = {}
        config[engine][key_name] = key_value
        return self.save_config(config)
    
    def remove_api_key(self, engine: str, key_name: str) -> bool:
        """Remove API key for specific engine"""
        config = self.load_config()
        if engine in config and key_name in config[engine]:
            del config[engine][key_name]
            if not config[engine]:  # Remove empty engine config
                del config[engine]
            return self.save_config(config)
        return False
    
    def get_engine_status(self, engine: str) -> Dict:
        """Get status of API configuration for an engine"""
        if engine not in self.supported_engines:
            return {'configured': False, 'error': 'Engine not supported'}
        
        required_keys = self.supported_engines[engine]['keys']
        if not required_keys:  # No API key required (like DuckDuckGo)
            return {'configured': True, 'keys_status': {}}
        
        keys_status = {}
        all_configured = True
        
        for key in required_keys:
            api_key = self.get_api_key(engine, key)
            keys_status[key] = {
                'configured': bool(api_key),
                'source': 'environment' if os.getenv(key) else 'saved' if api_key else 'none'
            }
            if not api_key:
                all_configured = False
        
        return {
            'configured': all_configured,
            'keys_status': keys_status
        }
    
    def render_config_ui(self):
        """Render the API configuration UI"""
        st.subheader("🔑 Configuração de APIs")
        
        # Configuration tabs
        tab1, tab2, tab3 = st.tabs(["Configurar APIs", "Status", "Documentação"])
        
        with tab1:
            st.write("Configure as chaves API para ativar a busca real:")
            
            # Create form for each engine
            for engine, info in self.supported_engines.items():
                with st.expander(f"{engine} - {info['description']}"):
                    required_keys = info['keys']
                    
                    if not required_keys:
                        st.success("✅ Não requer API key - Pronto para uso")
                        continue
                    
                    # Form for this engine
                    with st.form(f"form_{engine}"):
                        st.write(f"**Chaves necessárias para {engine}:**")
                        
                        form_data = {}
                        for key in required_keys:
                            current_value = self.get_api_key(engine, key)
                            placeholder = "***********" if current_value else "Cole sua API key aqui"
                            
                            form_data[key] = st.text_input(
                                key,
                                value="",
                                placeholder=placeholder,
                                type="password",
                                help=f"API key para {key}"
                            )
                        
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            if st.form_submit_button("💾 Salvar"):
                                success = True
                                for key, value in form_data.items():
                                    if value.strip():  # Only save if user entered something
                                        if not self.set_api_key(engine, key, value.strip()):
                                            success = False
                                            break
                                
                                if success:
                                    st.success(f"Configuração salva para {engine}")
                                    st.rerun()
                                else:
                                    st.error("Erro ao salvar configuração")
                        
                        with col2:
                            if st.form_submit_button("🗑️ Remover"):
                                success = True
                                for key in required_keys:
                                    if not self.remove_api_key(engine, key):
                                        success = False
                                        break
                                
                                if success:
                                    st.success(f"Configuração removida para {engine}")
                                    st.rerun()
                                else:
                                    st.error("Erro ao remover configuração")
        
        with tab2:
            st.write("Status das configurações de API:")
            
            for engine in self.supported_engines:
                status = self.get_engine_status(engine)
                
                if status['configured']:
                    st.success(f"✅ {engine} - Configurado")
                else:
                    st.error(f"❌ {engine} - Não configurado")
                
                # Show detailed status
                if 'keys_status' in status and status['keys_status']:
                    for key, key_status in status['keys_status'].items():
                        source_icon = "🌍" if key_status['source'] == 'environment' else "💾" if key_status['source'] == 'saved' else "❌"
                        st.write(f"  {source_icon} {key}: {key_status['source']}")
        
        with tab3:
            st.write("Documentação e links úteis:")
            
            for engine, info in self.supported_engines.items():
                with st.expander(f"Como obter API key para {engine}"):
                    st.write(f"**Serviço:** {info['description']}")
                    st.write(f"**Documentação:** {info['docs']}")
                    
                    if engine == 'Google':
                        st.write("**Passos:**")
                        st.write("1. Acesse Google Cloud Console")
                        st.write("2. Crie um projeto ou selecione um existente")
                        st.write("3. Ative a API Custom Search")
                        st.write("4. Crie credenciais (API Key)")
                        st.write("5. Configure um Custom Search Engine")
                    
                    elif engine == 'Bing':
                        st.write("**Passos:**")
                        st.write("1. Acesse Azure Portal")
                        st.write("2. Crie um recurso Bing Search")
                        st.write("3. Obtenha a chave da API")
                    
                    elif engine == 'DuckDuckGo':
                        st.write("**Informações:**")
                        st.write("- Não requer API key")
                        st.write("- Uso gratuito com limitações")
                        st.write("- Busca através de scraping web")
                    
                    elif engine == 'Perplexity':
                        st.write("**Passos:**")
                        st.write("1. Acesse perplexity.ai")
                        st.write("2. Crie uma conta")
                        st.write("3. Acesse área de API")
                        st.write("4. Gere uma API key")
    
    def get_available_engines(self) -> list:
        """Get list of engines that are properly configured"""
        available = []
        for engine in self.supported_engines:
            status = self.get_engine_status(engine)
            if status['configured']:
                available.append(engine)
        return available
    
    def clear_all_config(self):
        """Clear all API configuration"""
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            return True
        except Exception as e:
            st.error(f"Erro ao limpar configuração: {e}")
            return False