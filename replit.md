# Oportunidades Literárias Tocantins

## Overview

This is a Streamlit-based web application designed to help residents of Tocantins, Brazil find literary opportunities such as contests, cultural grants, and literary festivals. The application provides a centralized platform for searching and filtering various literary opportunities across multiple search engines, with specific focus on opportunities available to Tocantins residents.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

### July 17, 2025 - Database Integration and Data Transparency
- Added PostgreSQL database integration with persistent storage
- Implemented proper citation system for all search results
- Added clear disclaimers for mock data vs real data
- Created framework for real search engine integration
- Added transparency warnings for fake URLs and AI-generated content
- Improved user interface with data source indicators
- Added secure API key management system
- Integrated DuckDuckGo search engine support
- Created comprehensive API configuration interface
- Fixed database connection issues with improved error handling and retry logic
- Enhanced database manager with graceful fallback to mock mode when database is unavailable

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - chosen for rapid prototyping and ease of deployment
- **UI Components**: Custom CSS styling with responsive design
- **State Management**: Streamlit's session state for maintaining search history, saved searches, and custom keywords
- **Layout**: Wide layout with expandable sidebar for filters and settings

### Backend Architecture
- **Application Structure**: Modular Python architecture with separate concerns
- **Search Engine Integration**: Abstracted search engine manager supporting multiple providers
- **Data Processing**: Mock data generation for development and testing
- **Filtering System**: Dedicated filter manager for regional and content-based filtering

## Key Components

### 1. Application Core (`app.py`)
- Main Streamlit application entry point
- Session state initialization and management
- UI layout and navigation structure
- Integration of all system components

### 2. Search Engine Manager (`search_engines.py`)
- Unified interface for multiple search engines (Google, You.com, Perplexity, Bing)
- Currently implements mock data for development
- Designed for easy extension to real API integrations
- Query processing and result aggregation

### 3. Filter Manager (`filters.py`)
- Regional filtering specific to Tocantins requirements
- Opportunity type categorization
- Deadline-based filtering
- Location-based eligibility checking

### 4. Mock Data Generator (`mock_data.py`)
- Generates realistic test data for development
- Simulates various types of literary opportunities
- Provides consistent data structure for testing filters

### 5. Styling System (`styles.py`)
- Custom CSS with Google Fonts integration
- Responsive design with green/nature theme
- Consistent visual hierarchy and branding

### 6. Database Manager (`database.py`)
- PostgreSQL database integration with SQLAlchemy ORM
- User session management for multi-user support
- Persistent storage for search history, saved opportunities, and user preferences
- Database models: SearchHistory, SavedSearch, UserPreferences
- Complete CRUD operations for all data entities

### 7. API Configuration Manager (`api_config.py`)
- Secure API key management system
- Support for multiple search engines (Google, Bing, DuckDuckGo, Perplexity)
- File-based configuration storage with environment variable fallback
- Comprehensive UI for API key configuration and status monitoring
- Engine availability detection and documentation links

### 8. Real Search Engine Integration (`real_search.py`)
- DuckDuckGo web scraping implementation
- Framework for Google, Bing, and Perplexity API integration
- Intelligent content extraction and classification
- Deadline extraction from search results
- Proper citation and source attribution system

## Data Flow

1. **User Input**: Users configure search parameters through the sidebar
2. **Search Execution**: Search manager queries selected engines with custom keywords
3. **Result Aggregation**: Results from multiple engines are combined and normalized
4. **Filtering**: Filter manager applies regional and content-based filters
5. **Display**: Filtered results are presented with consistent formatting
6. **Database Persistence**: Search history, saved opportunities, and user preferences are stored in PostgreSQL
7. **Session Management**: Unique session tracking enables multi-user support

## External Dependencies

### Current Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Requests**: HTTP client for future API integrations (planned)
- **PostgreSQL**: Database for persistent storage
- **SQLAlchemy**: Database ORM for Python
- **psycopg2-binary**: PostgreSQL database adapter

### Database Integration
- **PostgreSQL Database**: Fully integrated with persistent storage
- **Tables**: search_history, saved_searches, user_preferences
- **Features**: Search history persistence, saved opportunities, user preferences storage
- **Session Management**: Unique session tracking for multi-user support

### Planned Integrations
- **Search Engine APIs**: Google Custom Search, Bing Search API, You.com API, Perplexity API
- **Authentication**: Planned user account system for personalized experiences

## Deployment Strategy

### Development Environment
- Local Streamlit development server
- Mock data for testing without external API dependencies
- Modular structure for easy component testing

### Production Considerations
- **Platform**: Designed for deployment on Streamlit Cloud or similar platforms
- **API Keys**: Environment variable configuration for search engine APIs
- **Performance**: Caching strategies for search results and user data
- **Scalability**: Prepared for database integration and user authentication

### Architecture Decisions

1. **Streamlit Choice**: Selected for rapid development and built-in web hosting capabilities, avoiding complex frontend/backend separation
2. **Mock Data Strategy**: Implemented comprehensive mock data system to enable development without immediate API dependencies
3. **Modular Design**: Separated concerns into distinct managers for maintainability and testing
4. **Regional Focus**: Built-in Tocantins-specific filtering to address the unique geographical requirements
5. **Multi-Engine Support**: Designed to aggregate results from multiple search engines to improve opportunity discovery

The application is structured to be easily extensible, with clear separation of concerns and preparation for future enhancements like real API integrations, user authentication, and persistent data storage.