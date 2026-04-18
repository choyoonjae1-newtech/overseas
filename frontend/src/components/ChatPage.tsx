import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import client from '../api/client';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function ChatPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatAvailable, setChatAvailable] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // 채팅 서비스 상태 확인
    checkChatStatus();

    // 환영 메시지 추가
    setMessages([
      {
        role: 'assistant',
        content: `안녕하세요, ${user?.username}님! 👋\n\n저는 JB우리캐피탈의 해외사업 모니터링 전문 AI 어시스턴트입니다.\n\n**제가 도와드릴 수 있는 분야:**\n- 🏦 미얀마/인도네시아 금융규제 분석\n- 📊 경제 지표 해석 및 전망\n- ⚠️ 지정학적 리스크 평가\n- 💼 투자 및 운영 전략 조언\n- 📈 시장 동향 분석\n\n무엇이 궁금하신가요?`,
        timestamp: new Date()
      }
    ]);
  }, [user]);

  const checkChatStatus = async () => {
    try {
      const response = await client.get('/api/chat/status');
      setChatAvailable(response.data.available);
    } catch (error) {
      console.error('채팅 상태 확인 실패:', error);
      setChatAvailable(false);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || loading) return;

    const userMessage: Message = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      // 채팅 히스토리 준비 (assistant 메시지만)
      const history = messages.map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      const response = await client.post('/api/chat/message', {
        message: inputMessage,
        history: history
      });

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error: any) {
      console.error('채팅 오류:', error);

      let errorMessage = '죄송합니다. 응답을 생성하는 중 오류가 발생했습니다.';

      if (error.response?.status === 503) {
        errorMessage = '채팅 서비스가 현재 이용 불가능합니다. 관리자에게 문의하세요.';
      }

      const errorMsg: Message = {
        role: 'assistant',
        content: `❌ ${errorMessage}\n\n${error.response?.data?.detail || ''}`,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const suggestedQuestions = [
    "미얀마의 최근 금융규제 변화는?",
    "인도네시아 경제 전망은 어때?",
    "미얀마와 인도네시아 중 어느 시장이 더 안정적인가요?",
    "환율 변동이 우리 사업에 미치는 영향은?"
  ];

  const askSuggestion = (question: string) => {
    setInputMessage(question);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <nav className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex justify-between items-center">
          <button
            onClick={() => navigate('/')}
            className="text-blue-700 hover:text-blue-800 text-sm"
          >
            ← 홈으로
          </button>
          <div className="text-center">
            <h1 className="text-lg sm:text-xl font-semibold text-gray-800">🤖 AI 어시스턴트</h1>
            <p className="text-xs text-gray-600 hidden sm:block">해외사업 모니터링 전문가</p>
          </div>
          <div className="w-20"></div>
        </div>
      </nav>

      {/* Chat Container */}
      <div className="flex-1 max-w-5xl w-full mx-auto flex flex-col">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-4 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white border border-gray-200 text-gray-800'
                }`}
              >
                <div className="whitespace-pre-wrap text-sm">{message.content}</div>
                <div
                  className={`text-xs mt-2 ${
                    message.role === 'user' ? 'text-blue-100' : 'text-gray-400'
                  }`}
                >
                  {message.timestamp.toLocaleTimeString('ko-KR', {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 rounded-lg p-4">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <span className="text-sm text-gray-600 ml-2">응답 생성 중...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Questions (shown when no messages) */}
        {messages.length === 1 && (
          <div className="p-4 bg-white border-t border-gray-200">
            <p className="text-sm text-gray-600 mb-3">💡 추천 질문:</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {suggestedQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => askSuggestion(question)}
                  className="text-left px-3 py-2 text-sm bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded transition"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="bg-white border-t border-gray-200 p-4">
          <div className="max-w-5xl mx-auto">
            {!chatAvailable && (
              <div className="mb-3 p-3 bg-yellow-50 border border-yellow-200 rounded text-sm text-yellow-800">
                ⚠️ 채팅 서비스가 현재 이용 불가능합니다. 관리자에게 Claude API 키 설정을 요청하세요.
              </div>
            )}

            <div className="flex gap-2">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="메시지를 입력하세요... (Shift+Enter: 줄바꿈, Enter: 전송)"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 resize-none"
                rows={2}
                disabled={!chatAvailable || loading}
              />
              <button
                onClick={sendMessage}
                disabled={!inputMessage.trim() || loading || !chatAvailable}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition font-semibold"
              >
                {loading ? '전송 중...' : '전송'}
              </button>
            </div>

            <p className="text-xs text-gray-500 mt-2">
              AI가 생성한 정보는 참고용입니다. 중요한 의사결정은 전문가와 상담하세요.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
