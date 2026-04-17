import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function HomePage() {
  const navigate = useNavigate();
  const { user, logout, isAdmin } = useAuth();

  const countries = [
    { code: 'MM', name: '미얀마', fullName: 'Myanmar', borderColor: 'border-blue-600' },
    { code: 'ID', name: '인도네시아', fullName: 'Indonesia', borderColor: 'border-blue-600' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-3 sm:px-6 py-3 sm:py-4">
          <div className="flex justify-between items-center mb-3 sm:mb-0">
            <div>
              <h1 className="text-lg sm:text-xl font-semibold text-gray-800">JB우리캐피탈</h1>
              <p className="text-xs text-gray-600 hidden sm:block">해외사업 모니터링 시스템</p>
            </div>
            <div className="flex items-center gap-2 sm:gap-4">
              <span className="text-xs sm:text-sm text-gray-700 hidden md:block">
                {user?.username} {isAdmin && <span className="text-blue-700 font-medium">(관리자)</span>}
              </span>
              {isAdmin && (
                <button
                  onClick={() => navigate('/admin')}
                  className="px-2 sm:px-4 py-1.5 sm:py-2 bg-blue-700 text-white text-xs sm:text-sm hover:bg-blue-800 transition whitespace-nowrap"
                >
                  <span className="hidden sm:inline">관리자 페이지</span>
                  <span className="sm:hidden">관리자</span>
                </button>
              )}
              <button
                onClick={logout}
                className="px-2 sm:px-4 py-1.5 sm:py-2 border border-gray-300 text-gray-700 text-xs sm:text-sm hover:bg-gray-50 transition"
              >
                로그아웃
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-3 sm:px-6 py-6 sm:py-12">
        <div className="mb-6 sm:mb-12">
          <h2 className="text-xl sm:text-2xl font-semibold text-gray-800 mb-2">
            국가별 현황 조회
          </h2>
          <p className="text-xs sm:text-sm text-gray-600">
            모니터링할 국가를 선택하세요
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 max-w-4xl">
          {countries.map((country) => (
            <button
              key={country.code}
              onClick={() => navigate(`/countries/${country.code}`)}
              className={`bg-white border-l-4 ${country.borderColor} p-4 sm:p-6 shadow hover:shadow-md transition text-left`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg sm:text-xl font-semibold text-gray-800 mb-1">{country.name}</h3>
                  <p className="text-xs sm:text-sm text-gray-500">{country.fullName}</p>
                </div>
                <svg className="w-5 h-5 sm:w-6 sm:h-6 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
              <div className="mt-3 sm:mt-4 flex flex-wrap gap-2 sm:gap-4 text-xs text-gray-600">
                <span>뉴스 · 공시</span>
                <span>주요 일정</span>
                <span>규제 현황</span>
              </div>
            </button>
          ))}
        </div>

        {/* 국가 비교 버튼 */}
        <div className="mt-6 sm:mt-8 max-w-4xl">
          <button
            onClick={() => navigate('/comparison')}
            className="w-full bg-gradient-to-r from-blue-600 to-green-600 text-white p-4 sm:p-5 shadow hover:shadow-md transition flex items-center justify-between rounded-lg"
          >
            <div className="flex items-center gap-3">
              <div className="text-2xl">📊</div>
              <div className="text-left">
                <h3 className="text-base sm:text-lg font-semibold">국가 비교 분석</h3>
                <p className="text-xs sm:text-sm opacity-90">미얀마 vs 인도네시아 경제 지표 비교</p>
              </div>
            </div>
            <svg className="w-5 h-5 sm:w-6 sm:h-6 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        {/* AI 채팅 어시스턴트 버튼 */}
        <div className="mt-4 max-w-4xl">
          <button
            onClick={() => navigate('/chat')}
            className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 text-white p-4 sm:p-5 shadow hover:shadow-md transition flex items-center justify-between rounded-lg"
          >
            <div className="flex items-center gap-3">
              <div className="text-2xl">🤖</div>
              <div className="text-left">
                <h3 className="text-base sm:text-lg font-semibold">AI 어시스턴트</h3>
                <p className="text-xs sm:text-sm opacity-90">해외사업 전문가에게 무엇이든 물어보세요</p>
              </div>
            </div>
            <svg className="w-5 h-5 sm:w-6 sm:h-6 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
