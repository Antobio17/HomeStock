from dotenv import load_dotenv
from src.shared.service_container.infrastructure.domain.service.service_container import ServiceContainer

load_dotenv(dotenv_path='.env')
load_dotenv(dotenv_path='.env.local', override=True)

service_container = ServiceContainer()