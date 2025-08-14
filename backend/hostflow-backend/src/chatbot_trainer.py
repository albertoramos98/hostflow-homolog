import json
import os
import pickle
from datetime import datetime
from typing import List, Dict, Any
import re
from collections import defaultdict, Counter
import sqlite3

class ChatbotTrainer:
    """
    Classe responsável pelo treinamento e aprendizado do chatbot.
    Implementa algoritmos de aprendizado supervisionado e por reforço.
    """
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), 'database', 'app.db')
        self.training_data_path = os.path.join(os.path.dirname(__file__), 'training_data.json')
        self.model_path = os.path.join(os.path.dirname(__file__), 'chatbot_model.pkl')
        self.feedback_path = os.path.join(os.path.dirname(__file__), 'feedback_data.json')
        
        # Estruturas de dados para o modelo
        self.intent_patterns = {}
        self.response_templates = {}
        self.word_frequency = Counter()
        self.intent_confidence = defaultdict(float)
        self.feedback_scores = defaultdict(list)
        
        # Carregar dados existentes
        self.load_training_data()
        self.load_model()
        self.load_feedback_data()
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Pré-processa o texto para análise.
        """
        # Converter para minúsculas
        text = text.lower()
        
        # Remover pontuação e caracteres especiais
        text = re.sub(r'[^\w\s]', '', text)
        
        # Dividir em palavras
        words = text.split()
        
        # Remover palavras muito curtas
        words = [word for word in words if len(word) > 2]
        
        return words
    
    def extract_intent(self, message: str) -> str:
        """
        Extrai a intenção da mensagem usando análise de palavras-chave.
        """
        words = self.preprocess_text(message)
        intent_scores = defaultdict(float)
        
        # Calcular pontuação para cada intenção baseada nas palavras
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                pattern_words = self.preprocess_text(pattern)
                common_words = set(words) & set(pattern_words)
                if common_words:
                    intent_scores[intent] += len(common_words) / len(pattern_words)
        
        # Retornar a intenção com maior pontuação
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = intent_scores[best_intent]
            
            # Só retornar se a confiança for suficiente
            if confidence > 0.3:
                return best_intent
        
        return "unknown"
    
    def generate_response(self, intent: str, message: str) -> str:
        """
        Gera uma resposta baseada na intenção identificada.
        """
        if intent in self.response_templates:
            responses = self.response_templates[intent]
            
            # Escolher resposta baseada no feedback histórico
            if intent in self.feedback_scores:
                # Usar resposta com melhor feedback médio
                best_response = max(responses, key=lambda r: self.get_response_score(intent, r))
                return best_response
            else:
                # Escolher primeira resposta se não há feedback
                return responses[0] if responses else "Desculpe, não entendi sua pergunta."
        
        return "Desculpe, não entendi sua pergunta. Pode reformular?"
    
    def get_response_score(self, intent: str, response: str) -> float:
        """
        Calcula a pontuação média de uma resposta baseada no feedback.
        """
        key = f"{intent}:{response}"
        if key in self.feedback_scores:
            scores = self.feedback_scores[key]
            return sum(scores) / len(scores) if scores else 0.0
        return 0.0
    
    def add_training_example(self, message: str, intent: str, response: str):
        """
        Adiciona um novo exemplo de treinamento.
        """
        # Atualizar padrões de intenção
        if intent not in self.intent_patterns:
            self.intent_patterns[intent] = []
        
        if message not in self.intent_patterns[intent]:
            self.intent_patterns[intent].append(message)
        
        # Atualizar templates de resposta
        if intent not in self.response_templates:
            self.response_templates[intent] = []
        
        if response not in self.response_templates[intent]:
            self.response_templates[intent].append(response)
        
        # Atualizar frequência de palavras
        words = self.preprocess_text(message)
        self.word_frequency.update(words)
        
        # Salvar dados atualizados
        self.save_training_data()
        self.save_model()
    
    def add_feedback(self, message: str, response: str, score: float):
        """
        Adiciona feedback para uma resposta (aprendizado por reforço).
        Score: 1.0 = muito bom, 0.5 = neutro, 0.0 = muito ruim
        """
        intent = self.extract_intent(message)
        key = f"{intent}:{response}"
        
        self.feedback_scores[key].append(score)
        
        # Manter apenas os últimos 100 feedbacks por resposta
        if len(self.feedback_scores[key]) > 100:
            self.feedback_scores[key] = self.feedback_scores[key][-100:]
        
        # Salvar feedback
        self.save_feedback_data()
        
        # Re-treinar se necessário
        if len(self.feedback_scores[key]) % 10 == 0:
            self.retrain_from_feedback()
    
    def retrain_from_feedback(self):
        """
        Re-treina o modelo baseado no feedback recebido.
        """
        # Atualizar confiança das intenções baseado no feedback
        for key, scores in self.feedback_scores.items():
            if ':' in key:
                intent = key.split(':')[0]
                avg_score = sum(scores) / len(scores) if scores else 0.0
                self.intent_confidence[intent] = avg_score
        
        # Salvar modelo atualizado
        self.save_model()
    
    def train_from_conversations(self):
        """
        Treina o modelo a partir de conversas armazenadas no banco de dados.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Buscar conversas (assumindo que existe uma tabela de logs)
            # Como não temos essa tabela, vamos criar dados de exemplo
            self.create_default_training_data()
            
            conn.close()
        except Exception as e:
            print(f"Erro ao treinar a partir de conversas: {e}")
            self.create_default_training_data()
    
    def create_default_training_data(self):
        """
        Cria dados de treinamento padrão para o HostFlow.
        """
        default_data = {
            "greeting": {
                "patterns": [
                    "olá", "oi", "bom dia", "boa tarde", "boa noite", "hey", "e aí"
                ],
                "responses": [
                    "Olá! Eu sou o HostFlow Assistant. Como posso ajudar você hoje?",
                    "Oi! Bem-vindo ao HostFlow. Em que posso ajudá-lo?",
                    "Olá! Estou aqui para ajudar com suas necessidades de gerenciamento de propriedades."
                ]
            },
            "reservas": {
                "patterns": [
                    "reservas", "booking", "reservar", "agendar", "disponibilidade"
                ],
                "responses": [
                    "Para gerenciar suas reservas, acesse a seção de Reservas no painel de controle. Lá você pode ver, editar e adicionar novas reservas.",
                    "Posso ajudar com reservas! Você pode visualizar e gerenciar todas as suas reservas através do painel administrativo.",
                    "As reservas podem ser gerenciadas facilmente através da nossa interface. Precisa de ajuda com alguma reserva específica?"
                ]
            },
            "propriedades": {
                "patterns": [
                    "propriedades", "imóveis", "casas", "apartamentos", "acomodações"
                ],
                "responses": [
                    "Na seção de Propriedades, você pode listar e gerenciar todos os seus imóveis. Adicione fotos, descrições e detalhes importantes.",
                    "Você pode gerenciar suas propriedades através do painel de controle. Adicione, edite ou remova propriedades conforme necessário.",
                    "O HostFlow permite gerenciar múltiplas propriedades de forma eficiente. Que tipo de ajuda você precisa com suas propriedades?"
                ]
            },
            "ajuda": {
                "patterns": [
                    "ajuda", "suporte", "help", "socorro", "não sei", "como"
                ],
                "responses": [
                    "Estou aqui para ajudar! Posso responder perguntas sobre reservas, propriedades, hóspedes e funcionalidades do sistema.",
                    "Se precisar de ajuda adicional, entre em contato com nosso suporte técnico ou continue conversando comigo.",
                    "Posso ajudar com diversas questões do HostFlow. Sobre o que você gostaria de saber mais?"
                ]
            },
            "precos": {
                "patterns": [
                    "preço", "custo", "valores", "planos", "quanto custa"
                ],
                "responses": [
                    "As informações sobre preços e planos estão disponíveis em nossa página de Planos e Preços.",
                    "Oferecemos diferentes planos para atender suas necessidades. Gostaria de saber mais sobre algum plano específico?",
                    "Os preços variam conforme o plano escolhido. Posso ajudar a encontrar o melhor plano para você."
                ]
            },
            "funcionalidades": {
                "patterns": [
                    "funcionalidades", "recursos", "o que faz", "características"
                ],
                "responses": [
                    "O HostFlow oferece gerenciamento de reservas, propriedades, comunicação com hóspedes, relatórios e muito mais!",
                    "Nossas principais funcionalidades incluem: gestão de propriedades, controle de reservas, comunicação automatizada e relatórios detalhados.",
                    "O sistema oferece uma solução completa para gerenciamento de propriedades de aluguel temporário."
                ]
            },
            "login": {
                "patterns": [
                    "login", "acessar", "entrar", "fazer login", "conectar"
                ],
                "responses": [
                    "Para fazer login, clique no botão Login no canto superior direito da tela e insira suas credenciais.",
                    "Você pode acessar sua conta através do botão de login na página principal.",
                    "Para entrar no sistema, use suas credenciais de acesso na tela de login."
                ]
            },
            "cadastro": {
                "patterns": [
                    "cadastro", "registrar", "criar conta", "sign up", "registro"
                ],
                "responses": [
                    "Para se cadastrar, clique no botão Registrar e preencha o formulário com suas informações.",
                    "O cadastro é rápido e fácil! Clique em Registrar e siga as instruções.",
                    "Você pode criar sua conta gratuitamente através do formulário de registro."
                ]
            },
            "obrigado": {
                "patterns": [
                    "obrigado", "obrigada", "valeu", "thanks", "muito obrigado"
                ],
                "responses": [
                    "De nada! Fico feliz em ajudar. Se tiver mais alguma dúvida, é só perguntar.",
                    "Por nada! Estou sempre aqui para ajudar.",
                    "Foi um prazer ajudar! Volte sempre que precisar."
                ]
            }
        }
        
        # Adicionar dados padrão ao modelo
        for intent, data in default_data.items():
            self.intent_patterns[intent] = data["patterns"]
            self.response_templates[intent] = data["responses"]
            
            # Atualizar frequência de palavras
            for pattern in data["patterns"]:
                words = self.preprocess_text(pattern)
                self.word_frequency.update(words)
        
        # Salvar dados
        self.save_training_data()
        self.save_model()
    
    def save_training_data(self):
        """
        Salva os dados de treinamento em arquivo JSON.
        """
        data = {
            "intent_patterns": self.intent_patterns,
            "response_templates": self.response_templates,
            "word_frequency": dict(self.word_frequency),
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(self.training_data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar dados de treinamento: {e}")
    
    def load_training_data(self):
        """
        Carrega os dados de treinamento do arquivo JSON.
        """
        try:
            if os.path.exists(self.training_data_path):
                with open(self.training_data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.intent_patterns = data.get("intent_patterns", {})
                self.response_templates = data.get("response_templates", {})
                self.word_frequency = Counter(data.get("word_frequency", {}))
        except Exception as e:
            print(f"Erro ao carregar dados de treinamento: {e}")
    
    def save_model(self):
        """
        Salva o modelo treinado em arquivo pickle.
        """
        model_data = {
            "intent_patterns": self.intent_patterns,
            "response_templates": self.response_templates,
            "word_frequency": dict(self.word_frequency),
            "intent_confidence": dict(self.intent_confidence),
            "version": "1.0",
            "last_trained": datetime.now().isoformat()
        }
        
        try:
            with open(self.model_path, 'wb') as f:
                pickle.dump(model_data, f)
        except Exception as e:
            print(f"Erro ao salvar modelo: {e}")
    
    def load_model(self):
        """
        Carrega o modelo treinado do arquivo pickle.
        """
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                
                self.intent_patterns = model_data.get("intent_patterns", {})
                self.response_templates = model_data.get("response_templates", {})
                self.word_frequency = Counter(model_data.get("word_frequency", {}))
                self.intent_confidence = defaultdict(float, model_data.get("intent_confidence", {}))
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
    
    def save_feedback_data(self):
        """
        Salva os dados de feedback em arquivo JSON.
        """
        data = {
            "feedback_scores": {k: v for k, v in self.feedback_scores.items()},
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(self.feedback_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar dados de feedback: {e}")
    
    def load_feedback_data(self):
        """
        Carrega os dados de feedback do arquivo JSON.
        """
        try:
            if os.path.exists(self.feedback_path):
                with open(self.feedback_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                feedback_data = data.get("feedback_scores", {})
                self.feedback_scores = defaultdict(list, feedback_data)
        except Exception as e:
            print(f"Erro ao carregar dados de feedback: {e}")
    
    def get_training_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do treinamento.
        """
        total_patterns = sum(len(patterns) for patterns in self.intent_patterns.values())
        total_responses = sum(len(responses) for responses in self.response_templates.values())
        total_feedback = sum(len(scores) for scores in self.feedback_scores.values())
        
        return {
            "total_intents": len(self.intent_patterns),
            "total_patterns": total_patterns,
            "total_responses": total_responses,
            "total_feedback_entries": total_feedback,
            "vocabulary_size": len(self.word_frequency),
            "most_common_words": self.word_frequency.most_common(10),
            "intent_confidence": dict(self.intent_confidence)
        }
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Processa uma mensagem e retorna resposta com metadados.
        """
        intent = self.extract_intent(message)
        response = self.generate_response(intent, message)
        confidence = self.intent_confidence.get(intent, 0.5)
        
        return {
            "message": message,
            "intent": intent,
            "response": response,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }

# Instância global do trainer
chatbot_trainer = ChatbotTrainer()

# Inicializar com dados padrão se necessário
if not chatbot_trainer.intent_patterns:
    chatbot_trainer.create_default_training_data()

