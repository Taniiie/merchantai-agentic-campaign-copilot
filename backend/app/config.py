from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Database
    database_url: str = "sqlite:///./data/merchantai.db"
    
    # AI Provider
    ai_provider: str = "demo"  # demo, openai, anthropic
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    llm_model_name: str = "gpt-3.5-turbo"  # Renamed to avoid conflict
    
    # RAG Configuration
    embeddings_provider: str = "local"  # local, openai
    vector_store_path: str = "./data/vector_store"
    knowledge_base_path: str = "./data/knowledge_base"
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001,http://192.168.1.69:3000,http://192.168.1.69:3001"  # Allow all possible origins
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        protected_namespaces = ('settings_',)  # Fix model_name conflict


settings = Settings()
