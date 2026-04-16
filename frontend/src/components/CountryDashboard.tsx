import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { News } from '../types/news';
import { Event } from '../types/event';
import { newsAPI } from '../api/news';
import { eventsAPI } from '../api/events';
import CalendarView from './CalendarView';
import IndicatorsView from './IndicatorsView';

type TabType = 'schedule' | 'news' | 'indicators';

export default function CountryDashboard() {
  const { countryCode } = useParams<{ countryCode: string }>();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<TabType>('schedule');
  const [news, setNews] = useState<News[]>([]);
  const [events, setEvents] = useState<Event[]>([]);
  const [category, setCategory] = useState<string>('all');
  const [loading, setLoading] = useState(true);

  const countryName = countryCode === 'MM' ? '미얀마' : '인도네시아';
  const countryFullName = countryCode === 'MM' ? 'Myanmar' : 'Indonesia';

  useEffect(() => {
    loadData();
  }, [countryCode, category]);

  const loadData = async () => {
    if (!countryCode) return;

    setLoading(true);
    try {
      const newsData = await newsAPI.getByCountry(
        countryCode,
        category !== 'all' ? { category } : {}
      );
      const eventsData = await eventsAPI.getByCountry(countryCode);

      setNews(newsData);
      setEvents(eventsData);
    } catch (error) {
      console.error('데이터 로딩 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryColor = (cat: string | null) => {
    switch (cat) {
      case 'regulation':
        return 'bg-red-100 text-red-800';
      case 'geopolitical':
        return 'bg-orange-100 text-orange-800';
      case 'economic':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getCategoryLabel = (cat: string | null) => {
    switch (cat) {
      case 'regulation':
        return '금융규제';
      case 'geopolitical':
        return '지정학적';
      case 'economic':
        return '경제';
      default:
        return '기타';
    }
  };

  const tabs: { id: TabType; label: string }[] = [
    { id: 'schedule', label: '주요 일정' },
    { id: 'news', label: '주요 소식' },
    { id: 'indicators', label: '관련 지표' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <button
            onClick={() => navigate('/')}
            className="text-blue-700 hover:text-blue-800 text-sm"
          >
            ← 홈으로
          </button>
          <div className="text-center">
            <h1 className="text-xl font-semibold text-gray-800">{countryName}</h1>
            <p className="text-xs text-gray-600">{countryFullName}</p>
          </div>
          <div className="w-20"></div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-6">
        {/* 탭 메뉴 */}
        <div className="bg-white border-b border-gray-200 mb-6">
          <div className="flex gap-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-3 text-sm font-medium transition border-b-2 ${
                  activeTab === tab.id
                    ? 'border-blue-700 text-blue-700'
                    : 'border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* 탭 컨텐츠 */}
        <div>
          {activeTab === 'schedule' && (
            <div className="bg-white p-6 border border-gray-200">
              <h2 className="text-lg font-semibold mb-6 text-gray-800">일정 캘린더</h2>
              {loading ? (
                <div className="text-center py-12">
                  <p className="text-gray-500">로딩 중...</p>
                </div>
              ) : events.length > 0 ? (
                <CalendarView events={events} />
              ) : (
                <p className="text-gray-500 text-center py-12">일정이 없습니다.</p>
              )}
            </div>
          )}

          {activeTab === 'news' && (
            <div className="bg-white p-6 border border-gray-200">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-lg font-semibold text-gray-800">뉴스 · 공시</h2>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="px-3 py-2 border border-gray-300 text-sm focus:outline-none focus:ring-1 focus:ring-blue-600"
                >
                  <option value="all">전체</option>
                  <option value="regulation">금융규제</option>
                  <option value="geopolitical">지정학적 리스크</option>
                  <option value="economic">경제</option>
                  <option value="other">기타</option>
                </select>
              </div>

              {loading ? (
                <p className="text-center py-12 text-gray-500">로딩 중...</p>
              ) : news.length > 0 ? (
                <div className="space-y-4">
                  {news.map((item) => (
                    <div key={item.id} className="border-b border-gray-200 pb-4 last:border-0">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="text-base font-medium flex-1 text-gray-900">{item.title}</h3>
                        <span className={`text-xs px-2 py-1 ml-2 whitespace-nowrap ${getCategoryColor(item.category)}`}>
                          {getCategoryLabel(item.category)}
                        </span>
                      </div>
                      {item.content && (
                        <p className="text-gray-600 text-sm mb-2 line-clamp-2">{item.content}</p>
                      )}
                      <div className="flex justify-between items-center text-xs text-gray-500">
                        <span>
                          {item.source} • {item.published_at ? new Date(item.published_at).toLocaleDateString('ko-KR') : '날짜 미상'}
                        </span>
                        <a
                          href={item.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-700 hover:text-blue-800"
                        >
                          원문 보기 →
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-12">뉴스가 없습니다.</p>
              )}
            </div>
          )}

          {activeTab === 'indicators' && countryCode && (
            <IndicatorsView countryCode={countryCode} />
          )}
        </div>
      </div>
    </div>
  );
}
