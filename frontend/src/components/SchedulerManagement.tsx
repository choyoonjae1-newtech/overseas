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

      {/* 경제 지표 수집 관리 */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h2 className="text-2xl font-bold mb-2">경제 지표 자동 수집</h2>
            <p className="text-gray-600 text-sm">매일 오전 9시에 자동으로 경제 지표를 수집합니다.</p>
          </div>
          <button
            onClick={handleTriggerIndicators}
            disabled={triggeringIndicators}
            className="px-6 py-3 bg-blue-700 text-white rounded hover:bg-blue-800 disabled:bg-gray-400 font-semibold"
          >
            {triggeringIndicators ? '수집 중...' : '지금 수집'}
          </button>
        </div>

        <div className="border rounded-lg p-4">
          <h3 className="font-semibold text-gray-800 mb-3">수집 항목</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
              <span className="text-sm">환율 (USD 기준)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
              <span className="text-sm">GDP 성장률 (%)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
              <span className="text-sm">인플레이션율 (%)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
              <span className="text-sm">기준금리 (%)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
              <span className="text-sm">외환보유고 (billion USD)</span>
            </div>
          </div>

          <div className="mt-4 p-3 bg-gray-50 rounded">
            <p className="text-sm text-gray-700">
              <strong>데이터 소스:</strong> World Bank API, 각국 중앙은행 공식 사이트
            </p>
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
