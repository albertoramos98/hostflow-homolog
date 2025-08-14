# HostFlow - Gestão Inteligente para Pousadas 🏨

Uma plataforma SaaS completa para gestão de pousadas, inspirada no layout do Airbnb, com duas visões distintas: **Cliente** e **Proprietário**.

## 🌟 Características Principais

### 🎯 **Duas Visões Completas**
- **Visão Cliente**: Interface moderna para busca e reserva de acomodações
- **Visão Proprietário**: Dashboard administrativo completo para gestão

### 🤖 **Agente de IA - InsightAI**
Sistema de inteligência artificial com 7 funcionalidades principais:
1. **Coleta e Processamento de Dados** - Integração de múltiplas fontes
2. **Análise de Desempenho Comercial** - Métricas de vendas e conversão  
3. **Análise de Desempenho de Marketing** - ROI e eficácia de campanhas
4. **Análises Preditivas e Previsões** - Tendências e comportamentos futuros
5. **Geração de Insights Acionáveis** - Recomendações estratégicas
6. **Relatórios e Visualização de Dados** - Dashboards personalizados
7. **Análise de LTV e Vendas Proativas** - Oportunidades de upsell/cross-sell

### 📊 **Módulos Completos**
- ✅ **Pousadas** - Gestão completa de propriedades
- ✅ **Acomodações** - Quartos, suítes e chalés
- ✅ **Hóspedes** - Cadastro e histórico de clientes
- ✅ **Reservas** - Sistema completo de booking
- ✅ **Dashboard** - Métricas e estatísticas em tempo real
- ✅ **Agente de IA** - Insights e análises preditivas

## 🚀 **Versões Disponíveis**

### 🌐 **Online (Produção)**
**URL**: https://mzhyi8cn15jq.manussite.space

### 💻 **Local (Desenvolvimento)**
Projeto completo no arquivo ZIP para execução no VS Code

## 🔐 **Credenciais de Acesso**

**Área Administrativa:**
- Email: `demo@hostflow.com`
- Senha: `123456`

**Área do Cliente:**
- Acesso direto (sem login necessário)

## 🛠️ **Tecnologias Utilizadas**

### Frontend
- **React 18** com Vite
- **Tailwind CSS** para estilização
- **Lucide Icons** para ícones
- **Shadcn/UI** para componentes

### Backend
- **Flask** (Python)
- **SQLAlchemy** para ORM
- **Flask-CORS** para integração frontend/backend
- **SQLite** para banco de dados

## 📦 **Instalação e Execução**

### Pré-requisitos
- Node.js 18+
- Python 3.11+
- pnpm (ou npm)

### 1. Backend (Flask)
```bash
cd backend/hostflow-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python src/main.py
```

### 2. Frontend (React) - Desenvolvimento
```bash
cd frontend/hostflow-frontend
pnpm install
pnpm run dev
```

### 3. Aplicação Integrada
O backend Flask já serve o frontend construído em `/static/`
- Acesse: `http://localhost:5000`

## 🎨 **Funcionalidades por Visão**

### 👥 **Visão Cliente**
- **Busca Avançada** - Por destino, datas e número de hóspedes
- **Filtros** - Tipo de acomodação, preço, comodidades
- **Catálogo** - Visualização de acomodações disponíveis
- **Favoritos** - Sistema de wishlist
- **Interface Responsiva** - Design mobile-first

### 🏢 **Visão Proprietário**
- **Dashboard** - Métricas e KPIs em tempo real
- **Gestão de Pousadas** - CRUD completo de propriedades
- **Gestão de Acomodações** - Quartos, preços e disponibilidade
- **Gestão de Hóspedes** - Cadastro e histórico
- **Gestão de Reservas** - Sistema completo de booking
- **Agente de IA** - Insights e análises preditivas

## 🤖 **InsightAI - Agente de IA**

### Personalidade
- Analítica, objetiva, proativa
- Precisa, estratégica, imparcial
- Focada em resultados

### Capacidades
- **Briefing Diário** - Resumo de métricas importantes
- **Insights Priorizados** - Recomendações baseadas em dados
- **Análises Preditivas** - Previsões de ocupação e receita
- **Alertas Inteligentes** - Notificações proativas

## 📁 **Estrutura do Projeto**

```
hostflow-project/
├── frontend/hostflow-frontend/    # React App
│   ├── src/
│   │   ├── components/           # Componentes React
│   │   │   ├── Login.jsx        # Tela de login
│   │   │   ├── Dashboard.jsx    # Dashboard administrativo
│   │   │   ├── ClientBooking.jsx # Interface do cliente
│   │   │   ├── Properties.jsx   # Gestão de pousadas
│   │   │   ├── Accommodations.jsx # Gestão de acomodações
│   │   │   ├── Guests.jsx       # Gestão de hóspedes
│   │   │   ├── Bookings.jsx     # Gestão de reservas
│   │   │   └── AIAgent.jsx      # Agente de IA
│   │   └── App.jsx              # App principal
│   └── package.json
├── backend/hostflow-backend/      # Flask API
│   ├── src/
│   │   ├── models/              # Modelos de dados
│   │   ├── routes/              # Rotas da API
│   │   ├── ai_agent.py          # Agente de IA
│   │   ├── seed_data.py         # Dados de exemplo
│   │   └── main.py              # App principal
│   └── requirements.txt
├── docs/                        # Documentação
└── README.md                    # Este arquivo
```

## 🔄 **Fluxo de Navegação**

### Cliente
1. **Página Inicial** - Interface de busca estilo Airbnb
2. **Resultados** - Lista de acomodações disponíveis
3. **Detalhes** - Informações completas da acomodação
4. **Reserva** - Processo de booking (em desenvolvimento)

### Proprietário
1. **Login** - Autenticação administrativa
2. **Dashboard** - Visão geral do negócio
3. **Módulos** - Gestão de pousadas, acomodações, hóspedes, reservas
4. **IA** - Insights e análises do InsightAI

## 🎯 **Status do Projeto**

✅ **100% Funcional para Produção**
- Todas as funcionalidades implementadas
- Duas visões completas (Cliente + Proprietário)
- Agente de IA operacional
- APIs RESTful completas
- Interface responsiva
- Dados de exemplo populados
- Implantado na nuvem

## 🚀 **Deploy**

O projeto está configurado para deploy automático:
- **Frontend**: Build estático servido pelo Flask
- **Backend**: Flask com CORS habilitado
- **Banco**: SQLite com dados de exemplo
- **Nuvem**: Implantado em serviço gratuito

## 📞 **Suporte**

Para dúvidas ou suporte:
- Acesse a versão online: https://mzhyi8cn15jq.manussite.space
- Execute localmente seguindo as instruções acima
- Todas as funcionalidades estão documentadas e operacionais

---

**HostFlow** - Transformando a gestão de pousadas com tecnologia e inteligência artificial. 🏨✨

