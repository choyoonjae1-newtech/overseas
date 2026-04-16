import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import UserApproval from './UserApproval';
import NewsManagement from './NewsManagement';
import SchedulerManagement from './SchedulerManagement';

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'users' | 'news' | 'scheduler'>('users');

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <button
            onClick={() => navigate('/')}
            className="text-blue-600 hover:text-blue-800"
          >
            ← 홈으로
          </button>
          <h1 className="text-2xl font-bold text-gray-800">관리자 대시보드</h1>
          <div className="w-20"></div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setActiveTab('users')}
            className={`px-6 py-3 rounded-lg font-semibold transition ${
              activeTab === 'users'
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            사용자 관리
          </button>
          <button
            onClick={() => setActiveTab('news')}
            className={`px-6 py-3 rounded-lg font-semibold transition ${
              activeTab === 'news'
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            뉴스 관리
          </button>
          <button
            onClick={() => setActiveTab('scheduler')}
            className={`px-6 py-3 rounded-lg font-semibold transition ${
              activeTab === 'scheduler'
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            자동 수집
          </button>
        </div>

        {activeTab === 'users' && <UserApproval />}
        {activeTab === 'news' && <NewsManagement />}
        {activeTab === 'scheduler' && <SchedulerManagement />}
      </div>
    </div>
  );
}
