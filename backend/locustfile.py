"""
Load test for UmlAramigo API using Locust.

Usage:
    locust -f locustfile.py --host=http://localhost:8000
    
Para interface web:
    locust -f locustfile.py --host=http://localhost:8000 --web
    
Para teste em headless:
    locust -f locustfile.py --host=http://localhost:8000 --headless -u 100 -r 10 -t 5m
    
    Onde:
    -u: número de usuários simulados
    -r: taxa de spawn (usuários por segundo)
    -t: duração do teste
"""

from locust import HttpUser, task, between
import json
import random
import string


class UmlAramigoAPIUser(HttpUser):
    """Simula um usuário interagindo com a UmlAramigo API."""

    wait_time = between(1, 5)  # Aguarda 1-5 segundos entre requisições
    
    def on_start(self):
        """Executado quando o usuário inicia."""
        self.auth_token = None
        self.user_id = None
        self.organization_id = None
        self.pet_id = None
        self.authenticate()
    
    def authenticate(self):
        """Realiza autenticação na API."""
        # Gera email e senha únicos para cada usuário
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = f"user_{random_suffix}@test.com"
        password = "TestPassword123!"
        
        # Tenta registrar novo usuário
        user_data = {
            "email": email,
            "password": password,
            "full_name": f"Test User {random_suffix}"
        }
        
        try:
            # Assumindo que existe um endpoint de registro
            response_criacao = self.client.post(
                "/auth/register",
                json=user_data,
                name="/auth/register"
            )
            self.user_id = response_criacao.json().get("id")
            
            if response_criacao.status_code == 200:

                login_data = {
                    "email": email,
                    "password": password
                }
                response_login = self.client.post(
                    "/auth/login",
                    json=login_data,
                    name="/auth/login"
                )
                
                if response_login.status_code == 200:
                    
                    self.auth_token = response_login.json().get("access_token")


        except:
            pass
        

    
    def get_headers(self):
        """Retorna headers com autenticação."""
        headers = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers
    
    @task(5)
    def health_check(self):
        """Verifica saúde da API."""
        self.client.get("/health", name="/health")
    
    @task(3)
    def root_endpoint(self):
        """Acessa endpoint raiz."""
        self.client.get("/", name="/")
    
    @task(4)
    def get_organizations(self):
        """Lista organizações."""
        self.client.get(
            "/organizations/",
            headers=self.get_headers(),
            name="/organizations/"
        )
    
    @task(4)
    def get_pets(self):
        """Lista pets."""
        self.client.get(
            "/pets/",
            headers=self.get_headers(),
            name="/pets/"
        )
    
    @task(3)
    def create_organization(self):
        """Cria nova organização."""
        random_suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
        org_data = {
            "name": f"Org Test {random_suffix}",
            "description": "Organization for load testing",
            "phone": f"11999{random.randint(100000, 999999)}",
        }
        
        response = self.client.post(
            "/organizations/",
            json=org_data,
            headers=self.get_headers(),
            name="/organizations [POST]"
        )
        
        if response.status_code == 200:
            try:
                self.organization_id = response.json().get("id")
            except:
                pass
    
    @task(3)
    def create_pet(self):
        """Cria novo pet."""
        if not self.organization_id:
            return
        
        random_suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
        pet_types = ["dog", "cat"]
        
        pet_data = {
                "name": f"Pet {random_suffix}",
                "pet_type": random.choice(["dog", "cat"]),  # ← Campo correto
                "description": "Pet for adoption",
            }
        url_req = f"/pets/?org_id={self.organization_id}"
        print(pet_data)
        
        response = self.client.post(
            url_req,  # ✅ org_id como query param
            json=pet_data,
            headers=self.get_headers(),
            name="/pets [POST]"
        )
        
        if response.status_code == 200:
            try:
                self.pet_id = response.json().get("id")
            except:
                pass
    
    @task(3)
    def get_pets_detail(self):
        """Obtém detalhes de um pet específico."""
        if self.pet_id:
            self.client.get(
                f"/pets/{self.pet_id}",
                headers=self.get_headers(),
                name="/pets/{id}"
            )
    
    @task(2)
    def create_interest_form(self):
        """Cria formulário de interesse."""
        if not self.pet_id:
            return
        
        interest_data = {
            "full_name": "Interested User",
            "phone": f"11999{random.randint(100000, 999999)}",
        }
        
        response = self.client.post(
            f"/interests/?pet_id={self.pet_id}",
            json=interest_data,
            headers=self.get_headers(),
            name="/interests/ [POST]"
        )

 
        # O FastAPI retorna uma estrutura detalhada
        error_detail = response.json()
        print(f"Validation error details: {json.dumps(error_detail, indent=2)}")
    
    @task(2)
    def get_interest_forms(self):
        """Lista formulários de interesse."""
        self.client.get(
            "/interests/",
            headers=self.get_headers(),
            name="/interests/"
        )


class UmlAramigoSpikesUser(HttpUser):
    """Simula picos de tráfego na API."""
    
    wait_time = between(0.5, 2)  # Mais requisições, menos espera
    
    def on_start(self):
        """Executado quando o usuário inicia."""
        pass
    
    @task(10)
    def health_check(self):
        """Health check frequente durante picos."""
        self.client.get("/health", name="/health")
    
    @task(5)
    def get_organizations(self):
        """Lista organizações durante pico."""
        self.client.get("/organizations/", name="/organizations")
    
    @task(5)
    def get_pets(self):
        """Lista pets durante pico."""
        self.client.get("/pets/", name="/pets")
