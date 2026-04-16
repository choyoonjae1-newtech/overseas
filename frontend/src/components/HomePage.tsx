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
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-xl font-semibold text-gray-800">JB우리캐피탈</h1>
            <p className="text-xs text-gray-600">해외사업 모니터링 시스템</p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-700">
              {user?.username} {isAdmin && <span className="text-blue-700 font-medium">(관리자)</span>}
            </span>
            {isAdmin && (
              <button
                onClick={() => navigate('/admin')}
                className="px-4 py-2 bg-blue-700 text-white text-sm hover:bg-blue-800 transition"
              >
                관리자 페이지
              </button>
            )}
            <button
              onClick={logout}
              className="px-4 py-2 border border-gray-300 text-gray-700 text-sm hover:bg-gray-50 transition"
            >
              로그아웃
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="mb-12">
          <h2 className="text-2xl font-semibold text-gray-800 mb-2">
            국가별 현황 조회
          </h2>
          <p className="text-sm text-gray-600">
            모니터링할 국가를 선택하세요
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 max-w-4xl">
          {countries.map((country) => (
            <button
              key={country.code}
              onClick={() => navigate(`/countries/${country.code}`)}
              className={`bg-white border-l-4 ${country.borderColor} p-6 shadow hover:shadow-md transition text-left`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-semibold text-gray-800 mb-1">{country.name}</h3>
                  <p className="text-sm text-gray-500">{country.fullName}</p>
                </div>
                <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
              <div className="mt-4 flex gap-4 text-xs text-gray-600">
                <span>뉴스 · 공시</span>
                <span>주요 일정</span>
                <span>규제 현황</span>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
