import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import hashlib
from search_engines import SearchEngineManager
from mock_data import MockDataGenerator
from filters import FilterManager
from styles import get_custom_css
from database import DatabaseManager
from api_config import APIConfigManager

# Configure page
st.set_page_config(
    page_title="Oportunidades Literárias Tocantins",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state and user session tracking
if 'user_session' not in st.session_state:
    # Create unique session ID based on timestamp and random component
    session_data = str(datetime.now()) + str(hash(id(st.session_state)))
    st.session_state.user_session = hashlib.md5(session_data.encode()).hexdigest()

if 'search_results' not in st.session_state:
    st.session_state.search_results = []

# Initialize managers
search_manager = SearchEngineManager()
mock_data = MockDataGenerator()
filter_manager = FilterManager()
db_manager = DatabaseManager()
api_config = APIConfigManager()

# Load user preferences from database
user_prefs = db_manager.get_user_preferences(st.session_state.user_session)
if user_prefs:
    default_keywords = user_prefs.get('custom_keywords', [
        "concurso literário", "prêmio literatura", "antologia", "contos",
        "poesia", "edital cultural", "chamada pública", "festival literário"
    ])
    default_engines = user_prefs.get('preferred_engines', ["Google", "You", "Perplexity", "Bing"])
else:
    default_keywords = [
        "concurso literário", "prêmio literatura", "antologia", "contos",
        "poesia", "edital cultural", "chamada pública", "festival literário"
    ]
    # Atualize a lista de buscadores disponíveis na sidebar:
default_engines = ["Google", "DuckDuckGo", "Yandex", "Yahoo!", "Bravo Search"]

if 'custom_keywords' not in st.session_state:
    st.session_state.custom_keywords = default_keywords

def get_eligibility_tag(eligible):
    """Generate eligibility tag HTML"""
    if eligible:
        return '<span class="eligibility-tag eligible">✅ Elegível TO</span>'
    else:
        return '<span class="eligibility-tag not-eligible">❌ Não Elegível TO</span>'

# Main header
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("🌳 Oportunidades Literárias - Tocantins")
st.markdown("*Encontre concursos, editais e oportunidades culturais disponíveis para residentes do Tocantins*")
st.markdown('</div>', unsafe_allow_html=True)

# Data disclaimer banner
st.warning("⚠️ **IMPORTANTE:** Esta aplicação atualmente utiliza dados simulados para demonstração. Para obter informações reais de concursos e editais, é necessário integrar com APIs oficiais dos motores de busca. Todos os links e informações mostrados são exemplos gerados por IA para fins de demonstração.")

# Sidebar for filters and settings
with st.sidebar:
    st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
    st.header("🔍 Configurações de Busca")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Search engines selection
    st.subheader("Plataformas de Busca")
    available_engines = ["Google", "You", "Perplexity", "Bing", "DuckDuckGo"]
    search_engines = st.multiselect(
        "Selecione as plataformas:",
        available_engines,
        default=default_engines if all(engine in available_engines for engine in default_engines) else ["Google", "DuckDuckGo"]
    )
    
    # Real data option
    use_real_search = st.checkbox(
        "🔍 Tentar busca real (experimental)", 
        value=False,
        help="Ativa busca em sites reais. Ainda em desenvolvimento e pode ter resultados limitados."
    )
    
    # Regional filtering
    st.subheader("Filtros Regionais")
    include_tocantins = st.checkbox("Incluir oportunidades para Tocantins", value=True)
    exclude_other_states = st.checkbox("Excluir oportunidades restritas a outros estados", value=False)
    national_only = st.checkbox("Apenas oportunidades nacionais", value=False)
    
    # Opportunity types
    st.subheader("Tipos de Oportunidade")
    opportunity_types = st.multiselect(
        "Selecione os tipos:",
        ["Concursos Literários", "Editais Culturais", "Antologias", "Festivais", "Prêmios", "Chamadas Públicas"],
        default=["Concursos Literários", "Editais Culturais", "Antologias"]
    )
    
    # Deadline filter
    st.subheader("Prazos")
    deadline_filter = st.selectbox(
        "Filtrar por prazo:",
        ["Todos", "Próximos 7 dias", "Próximos 30 dias", "Próximos 90 dias"]
    )
    
    # Keywords management
    st.subheader("Palavras-chave")
    with st.expander("Gerenciar palavras-chave"):
        # Display current keywords
        st.write("**Palavras-chave atuais:**")
        for i, keyword in enumerate(st.session_state.custom_keywords):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(keyword)
            with col2:
                if st.button("❌", key=f"remove_{i}"):
                    st.session_state.custom_keywords.pop(i)
                    # Save to database
                    db_manager.save_user_preferences(
                        st.session_state.user_session,
                        custom_keywords=st.session_state.custom_keywords
                    )
                    st.rerun()
        
        # Add new keyword
        new_keyword = st.text_input("Nova palavra-chave:")
        if st.button("Adicionar"):
            if new_keyword and new_keyword not in st.session_state.custom_keywords:
                st.session_state.custom_keywords.append(new_keyword)
                # Save to database
                db_manager.save_user_preferences(
                    st.session_state.user_session,
                    custom_keywords=st.session_state.custom_keywords
                )
                st.rerun()
    
    # API Configuration Section
    st.markdown("---")
    with st.expander("⚙️ Configuração de APIs"):
        api_config.render_config_ui()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Search bar
    search_query = st.text_input(
        "🔍 Buscar oportunidades literárias:",
        placeholder="Digite termos específicos ou deixe vazio para busca geral...",
        key="search_input"
    )
    
    # Search button
    if st.button("🚀 Buscar Oportunidades", type="primary"):
        if search_engines:
            with st.spinner("Buscando oportunidades..."):
                # Update search manager with real data option
                search_manager.use_real_data = use_real_search
                
                # Search across selected engines
                results = search_manager.search_all_engines(
                    search_engines, 
                    search_query, 
                    st.session_state.custom_keywords
                )
                
                # Apply filters
                filtered_results = filter_manager.apply_filters(
                    results,
                    include_tocantins=include_tocantins,
                    exclude_other_states=exclude_other_states,
                    national_only=national_only,
                    opportunity_types=opportunity_types,
                    deadline_filter=deadline_filter
                )
                
                st.session_state.search_results = filtered_results
                
                # Save to database
                db_manager.save_search_history(
                    search_query or "Busca geral",
                    search_engines,
                    len(filtered_results),
                    st.session_state.user_session
                )
                
                # Save engine preferences
                db_manager.save_user_preferences(
                    st.session_state.user_session,
                    preferred_engines=search_engines
                )
        else:
            st.error("Por favor, selecione pelo menos uma plataforma de busca.")

with col2:
    # Quick stats
    if st.session_state.search_results:
        st.markdown('<div class="stats-container">', unsafe_allow_html=True)
        st.metric("Total de Oportunidades", len(st.session_state.search_results))
        
        # Count by eligibility
        eligible_count = len([r for r in st.session_state.search_results if r.get('tocantins_eligible', False)])
        st.metric("Elegíveis para Tocantins", eligible_count)
        
        # Count by type
        type_counts = {}
        for result in st.session_state.search_results:
            opp_type = result.get('type', 'Outros')
            type_counts[opp_type] = type_counts.get(opp_type, 0) + 1
        
        if type_counts:
            st.write("**Por tipo:**")
            for opp_type, count in sorted(type_counts.items()):
                st.write(f"• {opp_type}: {count}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Results display
if st.session_state.search_results:
    st.markdown("---")
    st.header("📋 Resultados da Busca")
    
    # Sort options
    sort_col1, sort_col2 = st.columns([1, 1])
    with sort_col1:
        sort_by = st.selectbox(
            "Ordenar por:",
            ["Relevância", "Data de Publicação", "Prazo", "Tipo"]
        )
    with sort_col2:
        sort_order = st.selectbox("Ordem:", ["Crescente", "Decrescente"])
    
    # Display results
    for i, result in enumerate(st.session_state.search_results):
        with st.container():
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            
            # Header with title and eligibility tag
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {result['title']}")
            with col2:
                eligibility_tag = get_eligibility_tag(result.get('tocantins_eligible', False))
                st.markdown(eligibility_tag, unsafe_allow_html=True)
            
            # Content with proper citations and disclaimers
            st.markdown(f"**Fonte:** {result['source']} | **Motor:** {result['search_engine']}")
            st.markdown(f"**Tipo:** {result['type']}")
            st.markdown(f"**Descrição:** {result['description']}")
            
            # Add disclaimer and citation information
            if result.get('is_mock_data', True):
                st.markdown("**⚠️ AVISO:** *Dados simulados para demonstração. Para informações reais, é necessário integrar com APIs de busca oficiais.*", 
                           help="Esta aplicação atualmente utiliza dados simulados para demonstrar funcionalidades. Dados reais requerem integração com APIs de motores de busca.")
            else:
                if result.get('citation'):
                    st.markdown(f"**📖 Fonte:** {result['citation']}")
                st.markdown("**ℹ️ Nota:** *Dados obtidos via busca web - sempre verifique informações diretamente na fonte oficial.*")
            
            # Deadline and location info
            col1, col2 = st.columns([1, 1])
            with col1:
                if result.get('deadline'):
                    deadline_str = result['deadline'].strftime("%d/%m/%Y")
                    days_left = (result['deadline'] - datetime.now()).days
                    if days_left > 0:
                        st.markdown(f"**Prazo:** {deadline_str} ({days_left} dias)")
                    else:
                        st.markdown(f"**Prazo:** {deadline_str} (Expirado)")
            with col2:
                if result.get('location'):
                    st.markdown(f"**Localização:** {result['location']}")
            
            # Action buttons
            btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
            with btn_col1:
                if st.button("🔗 Ver Detalhes", key=f"details_{i}"):
                    url = result.get('url', 'URL não disponível')
                    if url.startswith('https://example.com'):
                        st.error("⚠️ AVISO: Esta é uma URL de exemplo (dados simulados). Para obter links reais, é necessário integrar com APIs de busca reais.")
                    else:
                        st.info(f"Redirecionando para: {url}")
            with btn_col2:
                if st.button("💾 Salvar", key=f"save_{i}"):
                    if db_manager.save_opportunity(result, st.session_state.user_session):
                        st.success("Oportunidade salva!")
                    else:
                        st.info("Oportunidade já foi salva anteriormente.")
            with btn_col3:
                if st.button("📤 Compartilhar", key=f"share_{i}"):
                    st.info("Link copiado para a área de transferência!")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")

# Search history and saved searches
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📚 Histórico de Buscas", "💾 Buscas Salvas", "📊 Estatísticas"])

with tab1:
    st.subheader("Histórico de Buscas")
    search_history = db_manager.get_search_history(st.session_state.user_session)
    
    if search_history:
        for entry in search_history:
            with st.expander(f"{entry['query']} - {entry['timestamp']}"):
                st.write(f"**Plataformas:** {', '.join(entry['engines'])}")
                st.write(f"**Resultados encontrados:** {entry['results_count']}")
        
        # Add clear history button
        if st.button("🗑️ Limpar Histórico"):
            if db_manager.clear_search_history(st.session_state.user_session):
                st.success("Histórico limpo com sucesso!")
                st.rerun()
    else:
        st.info("Nenhuma busca realizada ainda.")

with tab2:
    st.subheader("Oportunidades Salvas")
    saved_opportunities = db_manager.get_saved_opportunities(st.session_state.user_session)
    
    if saved_opportunities:
        for saved in saved_opportunities:
            with st.expander(f"{saved['title']} - {saved['type']}"):
                st.write(f"**Descrição:** {saved['description']}")
                st.write(f"**Fonte:** {saved['source']}")
                if saved.get('deadline'):
                    st.write(f"**Prazo:** {saved['deadline'].strftime('%d/%m/%Y')}")
                if saved.get('location'):
                    st.write(f"**Localização:** {saved['location']}")
                
                # Eligibility tag
                eligibility_tag = get_eligibility_tag(saved.get('tocantins_eligible', False))
                st.markdown(eligibility_tag, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("🗑️ Remover", key=f"remove_saved_{saved['id']}"):
                        if db_manager.remove_saved_opportunity(saved['id'], st.session_state.user_session):
                            st.success("Oportunidade removida!")
                            st.rerun()
                with col2:
                    if st.button("🔗 Ver Detalhes", key=f"details_saved_{saved['id']}"):
                        st.info(f"Redirecionando para: {saved.get('url', 'URL não disponível')}")
    else:
        st.info("Nenhuma oportunidade salva ainda.")

with tab3:
    st.subheader("Estatísticas do Sistema")
    stats = db_manager.get_database_stats()
    
    if stats:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Buscas", stats['total_searches'])
        with col2:
            st.metric("Oportunidades Salvas", stats['total_saved_opportunities'])
        with col3:
            st.metric("Usuários Ativos", stats['total_users'])
        
        if stats['recent_searches']:
            st.subheader("Buscas Recentes no Sistema")
            for search in stats['recent_searches']:
                st.write(f"• {search.query} - {search.timestamp.strftime('%d/%m/%Y %H:%M')}")
    else:
        st.info("Estatísticas não disponíveis no momento.")



# Footer with citations and disclaimers
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        <p>🌳 <strong>Oportunidades Literárias Tocantins</strong> - Conectando escritores do Tocantins com oportunidades culturais</p>
        <p><em>Desenvolvido para a comunidade literária tocantinense</em></p>
        
        <div style="margin-top: 20px; font-size: 12px; color: #666;">
            <h4>Fontes de Informação e Citações:</h4>
            <ul>
                <li><strong>Dados Simulados:</strong> Gerados por IA para demonstração de funcionalidades</li>
                <li><strong>Busca Web:</strong> Resultados extraídos de sites públicos quando disponível</li>
                <li><strong>Fontes Oficiais:</strong> Ministério da Cultura, Funarte, Secretarias Estaduais</li>
                <li><strong>Organizações Culturais:</strong> Itaú Cultural, SESC, Academia Brasileira de Letras</li>
            </ul>
            <p><strong>Importante:</strong> Todas as informações devem ser verificadas diretamente nas fontes oficiais antes de qualquer inscrição ou participação.</p>
            <p><strong>Desenvolvido com:</strong> Streamlit, PostgreSQL, Python | <strong>Dados:</strong> Mock Data para demonstração</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
