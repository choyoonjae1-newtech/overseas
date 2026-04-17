import { useState, useEffect } from 'react';
import { schedulerAPI } from '../api/scheduler';
import { SchedulerConfig } from '../types/scheduler';

export default function SchedulerManagement() {
  const [configs, setConfigs] = useState<SchedulerConfig[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editForm, setEditForm] = useState<{
    interval_hours: number;
    keywords: string;
  }>({ interval_hours: 3, keywords: '' });
  const [triggering, setTriggering] = useState<string | null>(null);
  const [triggeringIndicators, setTriggeringIndicators] = useState(false);
  const [collectingReal, setCollectingReal] = useState(false);
  const [populatingSample, setPopulatingSample] = useState(false);
  const [cleaningDuplicates, setCleaningDuplicates] = useState(false);
  const [crawlingNews, setCrawlingNews] = useState(false);

  useEffect(() => {
    loadConfigs();
  }, []);

  const loadConfigs = async () => {
    setLoading(true);
    try {
      const data = await schedulerAPI.getConfigs();
      setConfigs(data);
    } catch (error) {
      console.error('설정 로딩 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (id: number, enabled: boolean) => {
    try {
      const updated = await schedulerAPI.updateConfig(id, { enabled: !enabled });
      setConfigs(configs.map((c) => (c.id === id ? updated : c)));
    } catch (error) {
      console.error('토글 실패:', error);
      alert('설정 변경에 실패했습니다.');
    }
  };

  const handleEdit = (config: SchedulerConfig) => {
    setEditingId(config.id);
    setEditForm({
      interval_hours: config.interval_hours,
      keywords: config.keywords.join(', '),
    });
  };

  const handleSave = async (id: number) => {
    try {
      const keywords = editForm.keywords
        .split(',')
        .map((k) => k.trim())
        .filter((k) => k);

      const updated = await schedulerAPI.updateConfig(id, {
        interval_hours: editForm.interval_hours,
        keywords,
      });

      setConfigs(configs.map((c) => (c.id === id ? updated : c)));
      setEditingId(null);
    } catch (error) {
      console.error('저장 실패:', error);
      alert('설정 저장에 실패했습니다.');
    }
  };

  const handleTrigger = async (countryCode: string) => {
    if (!confirm(`${countryCode} 뉴스를 지금 수집하시겠습니까?`)) return;

    setTriggering(countryCode);
    try {
      const result = await schedulerAPI.triggerCollection(countryCode);
      alert(`${result.message}\n수집된 뉴스: ${result.collected_count}개`);
      loadConfigs(); // 설정 새로고침
    } catch (error: any) {
      console.error('수동 수집 실패:', error);
      alert(`수집 실패: ${error.response?.data?.detail || error.message}`);
    } finally {
      setTriggering(null);
    }
  };

  const handleTriggerIndicators = async () => {
    if (!confirm('모든 국가의 경제 지표를 지금 수집하시겠습니까?')) return;

    setTriggeringIndicators(true);
    try {
      const result = await schedulerAPI.triggerIndicatorsCollection();
      alert(result.message);
    } catch (error: any) {
      console.error('경제 지표 수집 실패:', error);
      alert(`수집 실패: ${error.response?.data?.detail || error.message}`);
    } finally {
      setTriggeringIndicators(false);
    }
  };

  const handleCollectRealData = async () => {
    if (!confirm('⭐ 실제 데이터를 수집하시겠습니까?\n\nWorld Bank API 및 Exchange Rate API에서 실제 경제 지표를 가져옵니다.')) return;

    setCollectingReal(true);
    try {
      const result = await schedulerAPI.collectRealIndicators();
      alert(`✅ ${result.message}\n\n` +
            `수집된 지표: ${result.data.collected}개\n` +
            `미얀마: ${result.data.myanmar_total}개\n` +
            `인도네시아: ${result.data.indonesia_total}개\n\n` +
            `출처: ${result.sources.join(', ')}`);
    } catch (error: any) {
      console.error('실제 데이터 수집 실패:', error);
      alert(`❌ 수집 실패: ${error.response?.data?.detail || error.message}`);
    } finally {
      setCollectingReal(false);
    }
  };

  const handlePopulateSampleData = async () => {
    if (!confirm('⚠️ 샘플 데이터를 추가하시겠습니까?\n\n이 데이터는 하드코딩된 샘플 데이터이며 실제 데이터가 아닙니다.\n\n프로덕션 환경에서는 "실제 데이터 수집"을 사용하세요.')) return;

    setPopulatingSample(true);
    try {
      const result = await schedulerAPI.populateSampleIndicators();
      alert(`⚠️ ${result.message}\n\n` +
            `미얀마: ${result.data.myanmar}개\n` +
            `인도네시아: ${result.data.indonesia}개\n` +
            `총합: ${result.data.total}개\n\n` +
            `${result.warning}`);
    } catch (error: any) {
      console.error('샘플 데이터 추가 실패:', error);
      alert(`❌ 실패: ${error.response?.data?.detail || error.message}`);
    } finally {
      setPopulatingSample(false);
    }
  };

  const handleCleanDuplicates = async () => {
    if (!confirm('🧹 중복 데이터를 제거하시겠습니까?\n\n동일한 뉴스, 이벤트, 경제 지표의 중복을 제거합니다.\n(최신 데이터만 유지)')) return;

    setCleaningDuplicates(true);
    try {
      const result = await schedulerAPI.cleanDuplicates();
      alert(`✅ ${result.message}\n\n` +
            `제거된 데이터:\n` +
            `- 뉴스: ${result.removed.news}개\n` +
            `- 이벤트: ${result.removed.events}개\n` +
            `- 경제 지표: ${result.removed.indicators}개\n\n` +
            `남은 데이터:\n` +
            `- 뉴스: ${result.remaining.news}개\n` +
            `- 이벤트: ${result.remaining.events}개\n` +
            `- 경제 지표: ${result.remaining.indicators}개`);
    } catch (error: any) {
      console.error('중복 제거 실패:', error);
      alert(`❌ 실패: ${error.response?.data?.detail || error.message}`);
    } finally {
      setCleaningDuplicates(false);
    }
  };

  const handleCrawlNews = async (countryCode?: string) => {
    const countryName = countryCode === 'MM' ? '미얀마 CBM' :
                        countryCode === 'ID' ? '인도네시아 OJK' : '전체';

    if (!confirm(`🌐 ${countryName}에서 뉴스/공시를 크롤링하시겠습니까?\n\n웹사이트에서 최신 뉴스와 규제 공시를 수집합니다.`)) return;

    setCrawlingNews(true);
    try {
      const result = await schedulerAPI.crawlNews(countryCode);

      if (countryCode) {
        alert(`✅ ${result.message}\n\n` +
              `수집된 뉴스: ${result.count}개\n` +
              `출처: ${result.source}`);
      } else {
        alert(`✅ ${result.message}\n\n` +
              `미얀마 CBM: ${result.cbm_count}개\n` +
              `인도네시아 OJK: ${result.ojk_count}개\n` +
              `총합: ${result.total_count}개\n\n` +
              `출처: ${result.sources.join(', ')}`);
      }
    } catch (error: any) {
      console.error('웹 크롤링 실패:', error);
      alert(`❌ 크롤링 실패: ${error.response?.data?.detail || error.message}`);
    } finally {
      setCrawlingNews(false);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-blue-100 text-blue-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'running':
        return '수집 중';
      case 'error':
        return '오류';
      default:
        return '대기';
    }
  };

  const formatDateTime = (dateStr: string | null) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleString('ko-KR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <p className="text-gray-500">로딩 중...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-6"> 뉴스 수집 자동화 관리</h2>

        <div className="space-y-6">
          {configs.map((config) => {
            const countryName = config.country_code === 'MM' ? '미얀마 🇲🇲' : '인도네시아 🇮🇩';
            const isEditing = editingId === config.id;

            return (
              <div key={config.id} className="border rounded-lg p-6">
                {/* 헤더 */}
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-bold">{countryName}</h3>
                    <span className={`inline-block mt-2 px-3 py-1 rounded text-sm ${getStatusBadge(config.status)}`}>
                      {getStatusText(config.status)}
                    </span>
                  </div>
                  <div className="flex items-center gap-4">
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={config.enabled}
                        onChange={() => handleToggle(config.id, config.enabled)}
                        className="w-5 h-5 text-blue-600"
                      />
                      <span className="ml-2 font-semibold">{config.enabled ? '활성화' : '비활성화'}</span>
                    </label>
                  </div>
                </div>

                {/* 설정 정보 */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-600 mb-1">수집 간격</label>
                    {isEditing ? (
                      <input
                        type="number"
                        min="1"
                        max="24"
                        value={editForm.interval_hours}
                        onChange={(e) => setEditForm({ ...editForm, interval_hours: parseInt(e.target.value) })}
                        className="w-full px-3 py-2 border rounded"
                      />
                    ) : (
                      <p className="text-gray-800">{config.interval_hours}시간마다</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-600 mb-1">마지막 수집</label>
                    <p className="text-gray-800">{formatDateTime(config.last_run_at)}</p>
                  </div>

                  <div className="col-span-2">
                    <label className="block text-sm font-semibold text-gray-600 mb-1">다음 수집 예정</label>
                    <p className="text-gray-800">{formatDateTime(config.next_run_at)}</p>
                  </div>
                </div>

                {/* 키워드 */}
                <div className="mb-4">
                  <label className="block text-sm font-semibold text-gray-600 mb-2">검색 키워드</label>
                  {isEditing ? (
                    <textarea
                      value={editForm.keywords}
                      onChange={(e) => setEditForm({ ...editForm, keywords: e.target.value })}
                      className="w-full px-3 py-2 border rounded"
                      rows={3}
                      placeholder="쉼표로 구분하여 입력 (예: regulation, economy, trade)"
                    />
                  ) : (
                    <div className="flex flex-wrap gap-2">
                      {config.keywords.map((keyword, idx) => (
                        <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* 에러 메시지 */}
                {config.last_error && (
                  <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded">
                    <p className="text-sm text-red-800">
                      <strong>마지막 오류:</strong> {config.last_error}
                    </p>
                  </div>
                )}

                {/* 버튼 */}
                <div className="flex gap-2">
                  {isEditing ? (
                    <>
                      <button
                        onClick={() => handleSave(config.id)}
                        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                      >
                        저장
                      </button>
                      <button
                        onClick={() => setEditingId(null)}
                        className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                      >
                        취소
                      </button>
                    </>
                  ) : (
                    <>
                      <button
                        onClick={() => handleEdit(config)}
                        className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
                      >
                        설정 수정
                      </button>
                      <button
                        onClick={() => handleTrigger(config.country_code)}
                        disabled={triggering === config.country_code}
                        className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-400"
                      >
                        {triggering === config.country_code ? '수집 중...' : '지금 수집'}
                      </button>
                    </>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 데이터 정리 */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="mb-4">
          <h2 className="text-2xl font-bold mb-2">🧹 데이터 정리</h2>
          <p className="text-gray-600 text-sm">중복된 데이터를 제거하여 데이터베이스를 깨끗하게 유지합니다.</p>
        </div>

        <div className="border-2 border-orange-200 bg-orange-50 rounded-lg p-5">
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-2xl">🧹</span>
                <h3 className="font-bold text-xl text-orange-900">중복 데이터 제거</h3>
              </div>
              <p className="text-orange-800 text-sm mb-3">
                동일한 뉴스, 이벤트, 경제 지표의 중복을 제거합니다. 최신 데이터만 유지됩니다.
              </p>
              <div className="bg-orange-100 border border-orange-300 rounded p-2 text-sm text-orange-900">
                <strong>💡 팁:</strong> 데이터가 여러 번 표시되는 경우 이 버튼을 클릭하세요!
              </div>
            </div>
            <button
              onClick={handleCleanDuplicates}
              disabled={cleaningDuplicates}
              className="px-6 py-3 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:bg-gray-400 font-semibold whitespace-nowrap ml-4"
            >
              {cleaningDuplicates ? '제거 중...' : '중복 제거'}
            </button>
          </div>
        </div>
      </div>

      {/* 웹 크롤링 */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="mb-4">
          <h2 className="text-2xl font-bold mb-2">🌐 웹 크롤링</h2>
          <p className="text-gray-600 text-sm">미얀마 중앙은행(CBM)과 인도네시아 금융감독청(OJK) 웹사이트에서 최신 뉴스와 규제 공시를 수집합니다.</p>
        </div>

        <div className="border-2 border-purple-200 bg-purple-50 rounded-lg p-5">
          <div className="flex flex-col gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-2xl">🌐</span>
                <h3 className="font-bold text-xl text-purple-900">금융 규제 공시 크롤링</h3>
              </div>
              <p className="text-purple-800 text-sm mb-3">
                중앙은행 및 금융감독청 공식 웹사이트에서 최신 규제 공시, 정책 발표, 금융 뉴스를 자동으로 수집합니다.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                {/* 미얀마 CBM */}
                <div className="bg-white border border-purple-200 rounded p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <span>🇲🇲</span>
                    <h4 className="font-semibold text-purple-900">미얀마 중앙은행 (CBM)</h4>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">Central Bank of Myanmar</p>
                  <ul className="text-xs text-gray-700 space-y-1 mb-3">
                    <li>• 통화정책 발표</li>
                    <li>• 금융규제 지침</li>
                    <li>• 환율 정책</li>
                  </ul>
                  <button
                    onClick={() => handleCrawlNews('MM')}
                    disabled={crawlingNews}
                    className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400 text-sm font-semibold"
                  >
                    {crawlingNews ? '크롤링 중...' : 'CBM 크롤링'}
                  </button>
                </div>

                {/* 인도네시아 OJK */}
                <div className="bg-white border border-purple-200 rounded p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <span>🇮🇩</span>
                    <h4 className="font-semibold text-purple-900">인도네시아 금융감독청 (OJK)</h4>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">Otoritas Jasa Keuangan</p>
                  <ul className="text-xs text-gray-700 space-y-1 mb-3">
                    <li>• 금융규제 공시</li>
                    <li>• 감독정책</li>
                    <li>• 허가/인가 정보</li>
                  </ul>
                  <button
                    onClick={() => handleCrawlNews('ID')}
                    disabled={crawlingNews}
                    className="w-full px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-400 text-sm font-semibold"
                  >
                    {crawlingNews ? '크롤링 중...' : 'OJK 크롤링'}
                  </button>
                </div>
              </div>

              {/* 전체 크롤링 버튼 */}
              <div className="flex justify-center">
                <button
                  onClick={() => handleCrawlNews()}
                  disabled={crawlingNews}
                  className="px-8 py-3 bg-purple-700 text-white rounded-lg hover:bg-purple-800 disabled:bg-gray-400 font-semibold shadow-lg"
                >
                  {crawlingNews ? '크롤링 중...' : '🌐 전체 크롤링 (CBM + OJK)'}
                </button>
              </div>
            </div>

            <div className="mt-3 p-3 bg-white rounded border border-purple-300">
              <p className="text-sm text-purple-900">
                <strong>📡 크롤링 대상:</strong> CBM (www.cbm.gov.mm), OJK (www.ojk.go.id)
              </p>
              <p className="text-xs text-purple-700 mt-1">
                💡 크롤링 결과는 "주요 소식" 탭에서 확인할 수 있습니다.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* 경제 지표 수집 관리 */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold mb-2">경제 지표 데이터 관리</h2>
          <p className="text-gray-600 text-sm">실제 API에서 데이터를 수집하거나 테스트용 샘플 데이터를 사용할 수 있습니다.</p>
        </div>

        {/* 실제 데이터 수집 섹션 */}
        <div className="border-2 border-green-200 bg-green-50 rounded-lg p-5 mb-4">
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-2xl">⭐</span>
                <h3 className="font-bold text-xl text-green-900">실제 데이터 수집 (권장)</h3>
              </div>
              <p className="text-green-800 text-sm mb-3">
                World Bank API, Exchange Rate API 등에서 실제 경제 지표를 가져옵니다.
              </p>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                  <span>환율 (실시간)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                  <span>GDP 성장률</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                  <span>인플레이션</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                  <span>무역수지</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                  <span>실업률</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                  <span>외환보유액</span>
                </div>
              </div>
            </div>
            <button
              onClick={handleCollectRealData}
              disabled={collectingReal}
              className="px-6 py-3 bg-green-700 text-white rounded-lg hover:bg-green-800 disabled:bg-gray-400 font-semibold whitespace-nowrap ml-4 shadow-lg"
            >
              {collectingReal ? '수집 중...' : '실제 데이터 수집'}
            </button>
          </div>
          <div className="mt-3 p-3 bg-white rounded border border-green-300">
            <p className="text-sm text-green-900">
              <strong>📡 데이터 출처:</strong> World Bank API, Exchange Rate API
            </p>
          </div>
        </div>

        {/* 샘플 데이터 섹션 */}
        <div className="border-2 border-yellow-300 bg-yellow-50 rounded-lg p-5 mb-4">
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-2xl">⚠️</span>
                <h3 className="font-bold text-xl text-yellow-900">샘플 데이터 (데모/테스트용)</h3>
              </div>
              <p className="text-yellow-800 text-sm mb-2">
                하드코딩된 샘플 데이터입니다. <strong>실제 경제 상황을 반영하지 않습니다.</strong>
              </p>
              <div className="bg-yellow-100 border border-yellow-400 rounded p-2 text-sm text-yellow-900">
                <strong>⚠️ 경고:</strong> 프로덕션 환경이나 업무 담당자에게 보여줄 때는 사용하지 마세요!
              </div>
            </div>
            <button
              onClick={handlePopulateSampleData}
              disabled={populatingSample}
              className="px-6 py-3 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 disabled:bg-gray-400 font-semibold whitespace-nowrap ml-4"
            >
              {populatingSample ? '추가 중...' : '샘플 데이터 추가'}
            </button>
          </div>
        </div>

        {/* 자동 수집 스케줄 */}
        <div className="border rounded-lg p-4 bg-blue-50">
          <h3 className="font-semibold text-blue-900 mb-3">자동 수집 스케줄</h3>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-800">
                매일 오전 9시에 자동으로 실제 경제 지표를 수집합니다.
              </p>
              <p className="text-xs text-blue-600 mt-1">
                (백엔드 스케줄러가 실행 중이어야 합니다)
              </p>
            </div>
            <button
              onClick={handleTriggerIndicators}
              disabled={triggeringIndicators}
              className="px-4 py-2 bg-blue-700 text-white rounded hover:bg-blue-800 disabled:bg-gray-400 text-sm"
            >
              {triggeringIndicators ? '수집 중...' : '지금 수집'}
            </button>
          </div>
        </div>
      </div>

      {/* 도움말 */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-bold text-blue-900 mb-2">안내: 사용 안내</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• 뉴스 자동 수집이 활성화되면 설정한 간격마다 뉴스를 자동으로 수집합니다.</li>
          <li>• 경제 지표는 매일 오전 9시에 자동으로 수집됩니다.</li>
          <li>• 검색 키워드를 수정하여 원하는 주제의 뉴스를 수집할 수 있습니다.</li>
          <li>• "지금 수집" 버튼으로 예정 시간을 기다리지 않고 즉시 수집할 수 있습니다.</li>
          <li>• 수집 간격은 1~24시간 사이로 설정할 수 있습니다.</li>
        </ul>
      </div>
    </div>
  );
}
