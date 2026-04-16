import { useState, useEffect } from 'react';
import { User } from '../types/user';
import { usersAPI } from '../api/users';

export default function UserApproval() {
  const [pendingUsers, setPendingUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPendingUsers();
  }, []);

  const loadPendingUsers = async () => {
    setLoading(true);
    try {
      const users = await usersAPI.getPendingUsers();
      setPendingUsers(users);
    } catch (error) {
      console.error('사용자 목록 로딩 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (userId: number) => {
    if (!confirm('이 사용자를 승인하시겠습니까?')) return;

    try {
      await usersAPI.approveUser(userId);
      alert('사용자가 승인되었습니다.');
      loadPendingUsers();
    } catch (error) {
      alert('승인에 실패했습니다.');
    }
  };

  const handleReject = async (userId: number) => {
    if (!confirm('이 사용자를 거절하시겠습니까?')) return;

    try {
      await usersAPI.rejectUser(userId);
      alert('사용자가 거절되었습니다.');
      loadPendingUsers();
    } catch (error) {
      alert('거절에 실패했습니다.');
    }
  };

  if (loading) {
    return <div className="text-center py-8">로딩 중...</div>;
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6">승인 대기 사용자</h2>

      {pendingUsers.length === 0 ? (
        <p className="text-gray-500 text-center py-8">승인 대기 중인 사용자가 없습니다.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left">사용자명</th>
                <th className="px-4 py-3 text-left">이메일</th>
                <th className="px-4 py-3 text-left">가입일</th>
                <th className="px-4 py-3 text-center">작업</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {pendingUsers.map((user) => (
                <tr key={user.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3">{user.username}</td>
                  <td className="px-4 py-3">{user.email}</td>
                  <td className="px-4 py-3">
                    {user.created_at ? new Date(user.created_at).toLocaleDateString('ko-KR') : '-'}
                  </td>
                  <td className="px-4 py-3 text-center">
                    <button
                      onClick={() => handleApprove(user.id)}
                      className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 mr-2"
                    >
                      승인
                    </button>
                    <button
                      onClick={() => handleReject(user.id)}
                      className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                    >
                      거절
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
