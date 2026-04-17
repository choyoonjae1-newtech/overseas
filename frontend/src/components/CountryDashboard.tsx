import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { News } from '../types/news';
import { Event } from '../types/event';
import { newsAPI } from '../api/news';
import { eventsAPI } from '../api/events';
import CalendarView from './CalendarView';
import IndicatorsView from './IndicatorsView';

type TabType = 'schedule' | 'news' | 'indicators';
type DateRangeType = '1week' | '1month' | '3months' | 'all';

export default function CountryDashboard() {
  const { countryCode } = useParams<{ countryCode: string }>();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<TabType>('schedule');
  const [news, setNews] = useState<News[]>([]);
  const [events, setEvents] = useState<Event[]>([]);
  const [category, setCategory] = useState<string>('all');
  const [dateRange, setDateRange] = useState<DateRangeType>('all');
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

  const getDateRangeLabel = (range: DateRangeType) => {
    switch (range) {
      case '1week':
        return '최근 1주일';
      case '1month':
        return '최근 1개월';
      case '3months':
        return '최근 3개월';
      default:
        return '전체';
    }
  };

  const filterNewsByDateRange = (newsItems: News[]) => {
    if (dateRange === 'all') return newsItems;

    const now = new Date();
    const cutoffDate = new Date();

    switch (dateRange) {
      case '1week':
        cutoffDate.setDate(now.getDate() - 7);
        break;
      case '1month':
        cutoffDate.setMonth(now.getMonth() - 1);
        break;
      case '3months':
        cutoffDate.setMonth(now.getMonth() - 3);
        break;
    }

    return newsItems.filter((item) => {
      if (!item.published_at) return true; // 날짜 없는 항목은 항상 표시
      const publishedDate = new Date(item.published_at);
      return publishedDate >= cutoffDate;
    });
  };

  const filteredNews = filterNewsByDateRange(news);

  const tabs: { id: TabType; label: string }[] = [
    { id: 'schedule', label: '주요 일정' },
    { id: 'news', label: '주요 소식' },
    { id: 'indicators', label: '관련 지표' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-3 sm:px-6 py-3 sm:py-4 flex justify-between items-center">
          <button
            onClick={() => navigate('/')}
            className="text-blue-700 hover:text-blue-800 text-xs sm:text-sm whitespace-nowrap"
          >
            ← 홈으로
          </button>
          <div className="text-center flex-1 mx-2">
            <h1 className="text-lg sm:text-xl font-semibold text-gray-800">{countryName}</h1>
            <p className="text-xs text-gray-600 hidden sm:block">{countryFullName}</p>
          </div>
          <div className="w-12 sm:w-20"></div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-3 sm:px-6 py-4 sm:py-6">
        {/* 탭 메뉴 */}
        <div className="bg-white border-b border-gray-200 mb-4 sm:mb-6 overflow-x-auto">
          <div className="flex gap-1 min-w-max">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 sm:px-6 py-2 sm:py-3 text-xs sm:text-sm font-medium transition border-b-2 whitespace-nowrap ${
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
            <div className="bg-white p-3 sm:p-6 border border-gray-200">
              <div className="mb-4 sm:mb-6">
                <h2 className="text-base sm:text-lg font-semibold text-gray-800 mb-2">일정 캘린더</h2>
                {!loading && events.length > 0 && (
                  <div className="flex items-center gap-2 text-xs text-gray-500">
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>최종 업데이트: {new Date().toLocaleDateString('ko-KR')} (실시간 연동 아님)</span>
                  </div>
                )}
              </div>
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
            <div className="bg-white p-3 sm:p-6 border border-gray-200">
              <div className="mb-4 sm:mb-6">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-3">
                  <h2 className="text-base sm:text-lg font-semibold text-gray-800">뉴스 · 공시</h2>
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="px-2 sm:px-3 py-1.5 sm:py-2 border border-gray-300 text-xs sm:text-sm focus:outline-none focus:ring-1 focus:ring-blue-600 w-full sm:w-auto"
                  >
                    <option value="all">전체</option>
                    <option value="regulation">금융규제</option>
                    <option value="geopolitical">지정학적 리스크</option>
                    <option value="economic">경제</option>
                    <option value="other">기타</option>
                  </select>
                </div>

                {/* 날짜 범위 필터 */}
                <div className="mb-3">
                  <div className="flex flex-wrap gap-2">
                    {(['1week', '1month', '3months', 'all'] as DateRangeType[]).map((range) => (
                      <button
                        key={range}
                        onClick={() => setDateRange(range)}
                        className={`px-3 py-1.5 text-xs sm:text-sm font-medium transition ${
                          dateRange === range
                            ? 'bg-blue-700 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }`}
                      >
                        {getDateRangeLabel(range)}
                      </button>
                    ))}
                  </div>
                </div>

                {!loading && news.length > 0 && (
                  <div className="flex items-center gap-2 text-xs text-gray-500">
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>최종 업데이트: {new Date().toLocaleDateString('ko-KR')} (실시간 연동 아님)</span>
                    {dateRange !== 'all' && (
                      <span className="ml-2 text-blue-600">• {getDateRangeLabel(dateRange)} 필터 적용 중 ({filteredNews.length}건)</span>
                    )}
                  </div>
                )}
              </div>

              {loading ? (
                <p className="text-center py-8 sm:py-12 text-gray-500 text-sm">로딩 중...</p>
              ) : filteredNews.length > 0 ? (
                <div className="space-y-3 sm:space-y-4">
                  {filteredNews.map((item) => (
                    <div key={item.id} className="border-b border-gray-200 pb-3 sm:pb-4 last:border-0">
                      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-2 gap-2 sm:gap-0">
                        <h3 className="text-sm sm:text-base font-medium flex-1 text-gray-900 pr-0 sm:pr-2">{item.title}</h3>
                        <span className={`text-xs px-2 py-1 whitespace-nowrap self-start ${getCategoryColor(item.category)}`}>
                          {getCategoryLabel(item.category)}
                        </span>
                      </div>
                      {item.content && (
                        <p className="text-gray-600 text-xs sm:text-sm mb-2 line-clamp-2">{item.content}</p>
                      )}
                      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center text-xs text-gray-500 gap-2 sm:gap-0">
                        <span className="text-xs">
                          {item.source} • {item.published_at ? new Date(item.published_at).toLocaleDateString('ko-KR') : '날짜 미상'}
                        </span>
                        {item.url && (
                          <a
                            href={item.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-700 hover:text-blue-800 text-xs whitespace-nowrap"
                          >
                            원문 보기 →
                          </a>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 sm:py-12">
                  <p className="text-gray-500 text-sm">
                    {news.length > 0 && filteredNews.length === 0
                      ? `${getDateRangeLabel(dateRange)} 기간의 뉴스가 없습니다.`
                      : '뉴스가 없습니다.'}
                  </p>
                  {news.length > 0 && filteredNews.length === 0 && (
                    <button
                      onClick={() => setDateRange('all')}
                      className="mt-3 text-blue-700 hover:text-blue-800 text-sm"
                    >
                      전체 뉴스 보기 →
                    </button>
                  )}
                </div>
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
