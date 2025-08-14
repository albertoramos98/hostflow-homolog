from flask import Blueprint, jsonify, request
from src.ai_agent import insight_ai
from src.chatbot_trainer import chatbot_trainer

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/agent/info', methods=['GET'])
def get_agent_info():
    """Retorna informações sobre o agente de IA"""
    return jsonify({
        'name': insight_ai.name,
        'personality': insight_ai.personality,
        'tone': insight_ai.tone,
        'capabilities': [
            'Coleta e Processamento de Dados',
            'Análise de Desempenho Comercial',
            'Análise de Desempenho de Marketing',
            'Análises Preditivas e Previsões',
            'Geração de Insights Acionáveis',
            'Relatórios e Visualização de Dados',
            'Análise de LTV e Vendas Proativas'
        ],
        'status': 'Ativo e operacional'
    }), 200

@ai_bp.route('/agent/analysis/complete', methods=['GET'])
def get_complete_analysis():
    """Executa análise completa do agente de IA"""
    try:
        analysis = insight_ai.get_comprehensive_analysis()
        return jsonify(analysis), 200
    except Exception as e:
        return jsonify({'error': f'Erro na análise: {str(e)}'}), 500

@ai_bp.route('/agent/briefing/daily', methods=['GET'])
def get_daily_briefing():
    """Retorna briefing diário do agente"""
    try:
        briefing = insight_ai.get_daily_briefing()
        return jsonify(briefing), 200
    except Exception as e:
        return jsonify({'error': f'Erro no briefing: {str(e)}'}), 500

@ai_bp.route('/agent/data/collection', methods=['GET'])
def get_data_collection():
    """Executa coleta e processamento de dados"""
    try:
        result = insight_ai.collect_and_process_data()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Erro na coleta de dados: {str(e)}'}), 500

@ai_bp.route('/agent/analysis/commercial', methods=['GET'])
def get_commercial_analysis():
    """Executa análise de desempenho comercial"""
    try:
        result = insight_ai.analyze_commercial_performance()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Erro na análise comercial: {str(e)}'}), 500

@ai_bp.route('/agent/analysis/marketing', methods=['GET'])
def get_marketing_analysis():
    """Executa análise de desempenho de marketing"""
    try:
        result = insight_ai.analyze_marketing_performance()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Erro na análise de marketing: {str(e)}'}), 500

@ai_bp.route('/agent/predictions', methods=['GET'])
def get_predictions():
    """Executa análises preditivas"""
    try:
        result = insight_ai.generate_predictive_analysis()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Erro nas previsões: {str(e)}'}), 500

@ai_bp.route('/agent/insights', methods=['GET'])
def get_insights():
    """Retorna insights acionáveis"""
    try:
        insights = insight_ai.generate_actionable_insights()
        return jsonify(insights), 200
    except Exception as e:
        return jsonify({'error': f'Erro nos insights: {str(e)}'}), 500

@ai_bp.route('/agent/reports', methods=['GET'])
def get_reports():
    """Gera relatórios e visualizações"""
    try:
        result = insight_ai.generate_reports_and_visualization()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Erro nos relatórios: {str(e)}'}), 500

@ai_bp.route('/agent/ltv-analysis', methods=['GET'])
def get_ltv_analysis():
    """Executa análise de LTV e vendas proativas"""
    try:
        result = insight_ai.analyze_ltv_and_proactive_sales()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Erro na análise de LTV: {str(e)}'}), 500

@ai_bp.route("/chatbot", methods=["POST"])
def chatbot_response():
    """Recebe uma mensagem do chatbot e retorna uma resposta usando o sistema de treinamento."""
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Mensagem não fornecida"}), 400

    try:
        # Usar o sistema de treinamento para processar a mensagem
        result = chatbot_trainer.process_message(user_message)
        
        return jsonify({
            "response": result["response"],
            "intent": result["intent"],
            "confidence": result["confidence"]
        }), 200
    except Exception as e:
        return jsonify({
            "response": "Desculpe, ocorreu um erro interno. Tente novamente mais tarde.",
            "error": str(e)
        }), 500

@ai_bp.route("/chatbot/feedback", methods=["POST"])
def chatbot_feedback():
    """Recebe feedback sobre uma resposta do chatbot para aprendizado por reforço."""
    data = request.get_json()
    message = data.get("message")
    response = data.get("response")
    score = data.get("score")  # 1.0 = muito bom, 0.5 = neutro, 0.0 = muito ruim

    if not all([message, response, score is not None]):
        return jsonify({"error": "Dados incompletos"}), 400

    try:
        # Adicionar feedback ao sistema de treinamento
        chatbot_trainer.add_feedback(message, response, float(score))
        
        return jsonify({
            "message": "Feedback recebido com sucesso",
            "status": "ok"
        }), 200
    except Exception as e:
        return jsonify({
            "error": f"Erro ao processar feedback: {str(e)}"
        }), 500

@ai_bp.route("/chatbot/train", methods=["POST"])
def chatbot_train():
    """Adiciona um novo exemplo de treinamento ao chatbot."""
    data = request.get_json()
    message = data.get("message")
    intent = data.get("intent")
    response = data.get("response")

    if not all([message, intent, response]):
        return jsonify({"error": "Dados incompletos"}), 400

    try:
        # Adicionar exemplo de treinamento
        chatbot_trainer.add_training_example(message, intent, response)
        
        return jsonify({
            "message": "Exemplo de treinamento adicionado com sucesso",
            "status": "ok"
        }), 200
    except Exception as e:
        return jsonify({
            "error": f"Erro ao adicionar exemplo de treinamento: {str(e)}"
        }), 500

@ai_bp.route("/chatbot/stats", methods=["GET"])
def chatbot_stats():
    """Retorna estatísticas do treinamento do chatbot."""
    try:
        stats = chatbot_trainer.get_training_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({
            "error": f"Erro ao obter estatísticas: {str(e)}"
        }), 500

@ai_bp.route("/chatbot/retrain", methods=["POST"])
def chatbot_retrain():
    """Força o retreinamento do chatbot com base no feedback."""
    try:
        chatbot_trainer.retrain_from_feedback()
        return jsonify({
            "message": "Retreinamento concluído com sucesso",
            "status": "ok"
        }), 200
    except Exception as e:
        return jsonify({
            "error": f"Erro durante o retreinamento: {str(e)}"
        }), 500

