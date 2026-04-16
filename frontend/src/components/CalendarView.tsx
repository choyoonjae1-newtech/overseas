import { useState } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import { Event } from '../types/event';

interface CalendarViewProps {
  events: Event[];
}

export default function CalendarView({ events }: CalendarViewProps) {
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);

  // 이벤트 타입별 색상
  const getEventColor = (eventType: string | null) => {
    switch (eventType) {
      case 'holiday':
        return '#ef4444'; // 빨강 (공휴일)
      case 'regulation':
        return '#3b82f6'; // 파랑 (규제)
      case 'deadline':
        return '#f97316'; // 주황 (마감일)
      default:
        return '#6b7280'; // 회색 (기타)
    }
  };

  // 이벤트 타입 한글 라벨
  const getEventTypeLabel = (eventType: string | null) => {
    switch (eventType) {
      case 'holiday':
        return '공휴일';
      case 'regulation':
        return '규제';
      case 'deadline':
        return '마감일';
      default:
        return '기타';
    }
  };

  // FullCalendar용 이벤트 데이터 변환
  const calendarEvents = events.map((event) => ({
    id: event.id.toString(),
    title: event.title,
    date: event.event_date,
    backgroundColor: getEventColor(event.event_type),
    borderColor: getEventColor(event.event_type),
    extendedProps: {
      ...event,
    },
  }));

  // 이벤트 클릭 핸들러
  const handleEventClick = (clickInfo: any) => {
    const event = clickInfo.event.extendedProps as Event;
    setSelectedEvent(event);
  };

  return (
    <div className="relative">
      <FullCalendar
        plugins={[dayGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        events={calendarEvents}
        eventClick={handleEventClick}
        height="auto"
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: '',
        }}
        locale="ko"
        buttonText={{
          today: '오늘',
        }}
        eventDisplay="block"
        eventTimeFormat={{
          hour: '2-digit',
          minute: '2-digit',
          hour12: false,
        }}
        dayCellClassNames="hover:bg-gray-50 cursor-pointer"
        eventClassNames="cursor-pointer hover:opacity-80 transition"
      />

      {/* 이벤트 상세 모달 */}
      {selectedEvent && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          onClick={() => setSelectedEvent(null)}
        >
          <div
            className="bg-white rounded-lg p-6 max-w-md w-full mx-4 shadow-xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-bold text-gray-800">{selectedEvent.title}</h3>
              <button
                onClick={() => setSelectedEvent(null)}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                ×
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <span className="text-sm font-semibold text-gray-600">날짜:</span>
                <p className="text-gray-800">
                  {new Date(selectedEvent.event_date).toLocaleDateString('ko-KR', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    weekday: 'long',
                  })}
                </p>
              </div>

              <div>
                <span className="text-sm font-semibold text-gray-600">유형:</span>
                <span
                  className="ml-2 px-2 py-1 rounded text-xs text-white"
                  style={{ backgroundColor: getEventColor(selectedEvent.event_type) }}
                >
                  {getEventTypeLabel(selectedEvent.event_type)}
                </span>
              </div>

              {selectedEvent.description && (
                <div>
                  <span className="text-sm font-semibold text-gray-600">설명:</span>
                  <p className="text-gray-700 mt-1">{selectedEvent.description}</p>
                </div>
              )}

              {selectedEvent.source && (
                <div>
                  <span className="text-sm font-semibold text-gray-600">출처:</span>
                  <p className="text-gray-700">{selectedEvent.source}</p>
                </div>
              )}

              {selectedEvent.url && (
                <div>
                  <a
                    href={selectedEvent.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline text-sm"
                  >
                    자세히 보기 →
                  </a>
                </div>
              )}
            </div>

            <div className="mt-6 flex justify-end">
              <button
                onClick={() => setSelectedEvent(null)}
                className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 transition"
              >
                닫기
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 범례 */}
      <div className="mt-4 flex flex-wrap gap-4 text-sm">
        <div className="flex items-center">
          <div className="w-4 h-4 bg-red-500 rounded mr-2"></div>
          <span>공휴일</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-blue-500 rounded mr-2"></div>
          <span>규제</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-orange-500 rounded mr-2"></div>
          <span>마감일</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-gray-500 rounded mr-2"></div>
          <span>기타</span>
        </div>
      </div>
    </div>
  );
}
