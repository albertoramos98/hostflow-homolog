
import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTrainingMode, setIsTrainingMode] = useState(false);
  const [showStats, setShowStats] = useState(false);
  const [stats, setStats] = useState(null);
  const messagesEndRef = useRef(null);

  const personaName = "HostFlow Assistant";
  const personaDescription = "Olá! Eu sou o HostFlow Assistant, seu guia amigável para todas as suas necessidades de gerenciamento de propriedades. Como posso ajudar você hoje?";

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      setMessages([{ sender: 'bot', text: personaDescription, timestamp: new Date() }]);
    }
  }, [isOpen]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (input.trim() === '') return;

    const userMessage = input.trim();
    const newMessages = [...messages, { sender: 'user', text: userMessage, timestamp: new Date() }];
    setMessages(newMessages);
    setInput('');

    try {
      const response = await fetch('/api/ai/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });
      const data = await response.json();
      
      const botMessage = {
        sender: 'bot',
        text: data.response,
        intent: data.intent,
        confidence: data.confidence,
        timestamp: new Date(),
        showFeedback: true
      };
      
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Erro ao comunicar com o chatbot:', error);
      setMessages((prevMessages) => [...prevMessages, { 
        sender: 'bot', 
        text: 'Desculpe, não consegui me conectar ao serviço de chatbot. Por favor, tente novamente mais tarde.',
        timestamp: new Date()
      }]);
    }
  };

  const handleFeedback = async (messageIndex, score) => {
    const message = messages[messageIndex];
    const userMessage = messages[messageIndex - 1]?.text;
    
    if (!userMessage || !message.text) return;

    try {
      await fetch('/api/ai/chatbot/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          response: message.text,
          score: score
        }),
      });

      // Atualizar a mensagem para remover os botões de feedback
      setMessages(prevMessages => 
        prevMessages.map((msg, idx) => 
          idx === messageIndex ? { ...msg, showFeedback: false, feedbackGiven: score } : msg
        )
      );
    } catch (error) {
      console.error('Erro ao enviar feedback:', error);
    }
  };

  const handleTrainingSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const trainingData = {
      message: formData.get('message'),
      intent: formData.get('intent'),
      response: formData.get('response')
    };

    try {
      const response = await fetch('/api/ai/chatbot/train', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(trainingData),
      });
      
      if (response.ok) {
        alert('Exemplo de treinamento adicionado com sucesso!');
        e.target.reset();
      }
    } catch (error) {
      console.error('Erro ao adicionar exemplo de treinamento:', error);
      alert('Erro ao adicionar exemplo de treinamento.');
    }
  };

  const loadStats = async () => {
    try {
      const response = await fetch('/api/ai/chatbot/stats');
      const data = await response.json();
      setStats(data);
      setShowStats(true);
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    }
  };

  const retrain = async () => {
    try {
      const response = await fetch('/api/ai/chatbot/retrain', {
        method: 'POST',
      });
      
      if (response.ok) {
        alert('Retreinamento concluído com sucesso!');
        loadStats(); // Recarregar estatísticas
      }
    } catch (error) {
      console.error('Erro durante o retreinamento:', error);
      alert('Erro durante o retreinamento.');
    }
  };

  return (
    <div className="chatbot-container">
      <button className="chatbot-toggle-button" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? 'X' : 'Chat'}
      </button>
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <h3>{personaName}</h3>
            <div className="chatbot-controls">
              <button 
                className="control-button"
                onClick={() => setIsTrainingMode(!isTrainingMode)}
                title="Modo de Treinamento"
              >
                🎓
              </button>
              <button 
                className="control-button"
                onClick={loadStats}
                title="Estatísticas"
              >
                📊
              </button>
              <button 
                className="control-button"
                onClick={retrain}
                title="Retreinar"
              >
                🔄
              </button>
            </div>
          </div>
          
          {showStats && stats && (
            <div className="chatbot-stats">
              <h4>Estatísticas do Treinamento</h4>
              <p>Intenções: {stats.total_intents}</p>
              <p>Padrões: {stats.total_patterns}</p>
              <p>Respostas: {stats.total_responses}</p>
              <p>Feedbacks: {stats.total_feedback_entries}</p>
              <p>Vocabulário: {stats.vocabulary_size} palavras</p>
              <button onClick={() => setShowStats(false)}>Fechar</button>
            </div>
          )}
          
          {isTrainingMode && (
            <div className="chatbot-training">
              <h4>Adicionar Exemplo de Treinamento</h4>
              <form onSubmit={handleTrainingSubmit}>
                <input name="message" placeholder="Mensagem do usuário" required />
                <input name="intent" placeholder="Intenção" required />
                <input name="response" placeholder="Resposta do bot" required />
                <button type="submit">Adicionar</button>
              </form>
              <button onClick={() => setIsTrainingMode(false)}>Fechar</button>
            </div>
          )}
          
          <div className="chatbot-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                <div className="message-content">
                  {msg.text}
                  {msg.intent && (
                    <div className="message-metadata">
                      <small>Intenção: {msg.intent} | Confiança: {(msg.confidence * 100).toFixed(1)}%</small>
                    </div>
                  )}
                </div>
                {msg.showFeedback && (
                  <div className="feedback-buttons">
                    <button onClick={() => handleFeedback(index, 1.0)} title="Muito bom">👍</button>
                    <button onClick={() => handleFeedback(index, 0.5)} title="Neutro">👌</button>
                    <button onClick={() => handleFeedback(index, 0.0)} title="Muito ruim">👎</button>
                  </div>
                )}
                {msg.feedbackGiven !== undefined && (
                  <div className="feedback-given">
                    <small>Feedback: {msg.feedbackGiven === 1.0 ? '👍' : msg.feedbackGiven === 0.5 ? '👌' : '👎'}</small>
                  </div>
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <form onSubmit={handleSendMessage} className="chatbot-input-form">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Digite sua mensagem..."
            />
            <button type="submit">Enviar</button>
          </form>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
