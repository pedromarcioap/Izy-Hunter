import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, JSON, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.pool import StaticPool
import time

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')

# Configure engine with better connection handling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=3600,   # Recycle connections after 1 hour
    pool_size=5,         # Connection pool size
    max_overflow=10,     # Maximum overflow connections
    connect_args={
        "options": "-c timezone=utc"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class SearchHistory(Base):
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, nullable=False)
    engines = Column(JSON)  # Store list of search engines used
    results_count = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_session = Column(String, index=True)  # For session-based tracking
    
class SavedSearch(Base):
    __tablename__ = "saved_searches"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    source = Column(String)
    type = Column(String)
    description = Column(Text)
    location = Column(String)
    deadline = Column(DateTime)
    tocantins_eligible = Column(Boolean, default=False)
    url = Column(String)
    search_engine = Column(String)
    published_date = Column(DateTime)
    saved_at = Column(DateTime, default=datetime.utcnow)
    user_session = Column(String, index=True)

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_session = Column(String, unique=True, index=True)
    custom_keywords = Column(JSON)  # Store custom keywords as JSON
    preferred_engines = Column(JSON)  # Store preferred search engines
    default_filters = Column(JSON)  # Store default filter settings
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Database Manager
class DatabaseManager:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
        self.db_available = True
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database with retry logic"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                # Test connection first
                with self.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                
                # Create tables if connection is successful
                Base.metadata.create_all(bind=self.engine)
                self.db_available = True
                return
                
            except (SQLAlchemyError, OperationalError) as e:
                print(f"Database connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    print("Database initialization failed. Running in mock mode.")
                    self.db_available = False
    
    def get_session(self):
        """Get database session"""
        if not self.db_available:
            return None
        return self.SessionLocal()
    
    def save_search_history(self, query, engines, results_count, user_session):
        """Save search to history"""
        if not self.db_available:
            return False
            
        session = self.get_session()
        if not session:
            return False
            
        try:
            search_entry = SearchHistory(
                query=query,
                engines=engines,
                results_count=results_count,
                user_session=user_session
            )
            session.add(search_entry)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error saving search history: {e}")
            return False
        finally:
            session.close()
    
    def get_search_history(self, user_session, limit=10):
        """Get search history for user"""
        if not self.db_available:
            return []
            
        session = self.get_session()
        if not session:
            return []
            
        try:
            history = session.query(SearchHistory)\
                .filter(SearchHistory.user_session == user_session)\
                .order_by(SearchHistory.timestamp.desc())\
                .limit(limit)\
                .all()
            
            return [{
                'id': h.id,
                'query': h.query,
                'engines': h.engines,
                'results_count': h.results_count,
                'timestamp': h.timestamp.strftime("%d/%m/%Y %H:%M")
            } for h in history]
        except SQLAlchemyError as e:
            print(f"Error getting search history: {e}")
            return []
        finally:
            session.close()
    
    def save_opportunity(self, opportunity_data, user_session):
        """Save opportunity to saved searches"""
        if not self.db_available:
            return False
            
        session = self.get_session()
        if not session:
            return False
            
        try:
            # Check if already saved
            existing = session.query(SavedSearch)\
                .filter(SavedSearch.title == opportunity_data['title'])\
                .filter(SavedSearch.user_session == user_session)\
                .first()
            
            if existing:
                return False  # Already saved
            
            saved_search = SavedSearch(
                title=opportunity_data['title'],
                source=opportunity_data.get('source'),
                type=opportunity_data.get('type'),
                description=opportunity_data.get('description'),
                location=opportunity_data.get('location'),
                deadline=opportunity_data.get('deadline'),
                tocantins_eligible=opportunity_data.get('tocantins_eligible', False),
                url=opportunity_data.get('url'),
                search_engine=opportunity_data.get('search_engine'),
                published_date=opportunity_data.get('published_date'),
                user_session=user_session
            )
            session.add(saved_search)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error saving opportunity: {e}")
            return False
        finally:
            session.close()
    
    def get_saved_opportunities(self, user_session):
        """Get saved opportunities for user"""
        if not self.db_available:
            return []
            
        session = self.get_session()
        if not session:
            return []
            
        try:
            saved = session.query(SavedSearch)\
                .filter(SavedSearch.user_session == user_session)\
                .order_by(SavedSearch.saved_at.desc())\
                .all()
            
            return [{
                'id': s.id,
                'title': s.title,
                'source': s.source,
                'type': s.type,
                'description': s.description,
                'location': s.location,
                'deadline': s.deadline,
                'tocantins_eligible': s.tocantins_eligible,
                'url': s.url,
                'search_engine': s.search_engine,
                'published_date': s.published_date,
                'saved_at': s.saved_at
            } for s in saved]
        except SQLAlchemyError as e:
            print(f"Error getting saved opportunities: {e}")
            return []
        finally:
            session.close()
    
    def remove_saved_opportunity(self, opportunity_id, user_session):
        """Remove saved opportunity"""
        if not self.db_available:
            return False
            
        session = self.get_session()
        if not session:
            return False
            
        try:
            opportunity = session.query(SavedSearch)\
                .filter(SavedSearch.id == opportunity_id)\
                .filter(SavedSearch.user_session == user_session)\
                .first()
            
            if opportunity:
                session.delete(opportunity)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error removing saved opportunity: {e}")
            return False
        finally:
            session.close()
    
    def save_user_preferences(self, user_session, custom_keywords=None, preferred_engines=None, default_filters=None):
        """Save or update user preferences"""
        if not self.db_available:
            return False
            
        session = self.get_session()
        if not session:
            return False
            
        try:
            # Check if preferences exist
            prefs = session.query(UserPreferences)\
                .filter(UserPreferences.user_session == user_session)\
                .first()
            
            if prefs:
                # Update existing preferences
                if custom_keywords is not None:
                    prefs.custom_keywords = custom_keywords
                if preferred_engines is not None:
                    prefs.preferred_engines = preferred_engines
                if default_filters is not None:
                    prefs.default_filters = default_filters
                prefs.updated_at = datetime.utcnow()
            else:
                # Create new preferences
                prefs = UserPreferences(
                    user_session=user_session,
                    custom_keywords=custom_keywords,
                    preferred_engines=preferred_engines,
                    default_filters=default_filters
                )
                session.add(prefs)
            
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error saving user preferences: {e}")
            return False
        finally:
            session.close()
    
    def get_user_preferences(self, user_session):
        """Get user preferences"""
        if not self.db_available:
            return None
            
        session = self.get_session()
        if not session:
            return None
            
        try:
            prefs = session.query(UserPreferences)\
                .filter(UserPreferences.user_session == user_session)\
                .first()
            
            if prefs:
                return {
                    'custom_keywords': prefs.custom_keywords,
                    'preferred_engines': prefs.preferred_engines,
                    'default_filters': prefs.default_filters
                }
            return None
        except SQLAlchemyError as e:
            print(f"Error getting user preferences: {e}")
            return None
        finally:
            session.close()
    
    def clear_search_history(self, user_session):
        """Clear search history for user"""
        if not self.db_available:
            return False
            
        session = self.get_session()
        if not session:
            return False
            
        try:
            session.query(SearchHistory)\
                .filter(SearchHistory.user_session == user_session)\
                .delete()
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error clearing search history: {e}")
            return False
        finally:
            session.close()
    
    def get_database_stats(self):
        """Get database statistics"""
        if not self.db_available:
            return None
            
        session = self.get_session()
        if not session:
            return None
            
        try:
            stats = {
                'total_searches': session.query(SearchHistory).count(),
                'total_saved_opportunities': session.query(SavedSearch).count(),
                'total_users': session.query(UserPreferences).count(),
                'recent_searches': session.query(SearchHistory)\
                    .order_by(SearchHistory.timestamp.desc())\
                    .limit(5)\
                    .all()
            }
            return stats
        except SQLAlchemyError as e:
            print(f"Error getting database stats: {e}")
            return None
        finally:
            session.close()