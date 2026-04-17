import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { EconomicIndicator } from '../types/indicator';

interface IndicatorChartProps {
  indicators: EconomicIndicator[];
  indicatorType: string;
  indicatorName: string;
  chartType?: 'line' | 'bar';
}

export default function IndicatorChart({
  indicators,
  indicatorType,
  indicatorName,
  chartType = 'line'
}: IndicatorChartProps) {
  // Filter and sort indicators by type
  const typeIndicators = indicators
    .filter(ind => ind.indicator_type === indicatorType)
    .sort((a, b) => new Date(a.recorded_at).getTime() - new Date(b.recorded_at).getTime());

  if (typeIndicators.length === 0) {
    return null;
  }

  // Prepare chart data
  const chartData = typeIndicators.map(ind => ({
    period: ind.period,
    value: ind.value,
    unit: ind.unit,
  }));

  // Determine color based on indicator type
  const getColor = (type: string) => {
    switch (type) {
      case 'exchange_rate':
        return '#3b82f6'; // blue
      case 'gdp_growth':
        return '#10b981'; // green
      case 'inflation':
        return '#f97316'; // orange
      case 'interest_rate':
        return '#8b5cf6'; // purple
      case 'trade_balance':
        return '#06b6d4'; // cyan
      case 'unemployment_rate':
        return '#ef4444'; // red
      default:
        return '#6b7280'; // gray
    }
  };

  const color = getColor(indicatorType);

  return (
    <div className="bg-white p-4 border border-gray-200 rounded-lg">
      <h4 className="text-sm font-semibold text-gray-800 mb-4">{indicatorName} 추이</h4>
      <ResponsiveContainer width="100%" height={250}>
        {chartType === 'line' ? (
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="period"
              tick={{ fontSize: 12 }}
              stroke="#6b7280"
            />
            <YAxis
              tick={{ fontSize: 12 }}
              stroke="#6b7280"
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#fff',
                border: '1px solid #e5e7eb',
                borderRadius: '0.375rem',
                fontSize: '12px'
              }}
              formatter={(value: number, name: string, props: any) => {
                return [`${value.toLocaleString()} ${props.payload.unit || ''}`, '수치'];
              }}
            />
            <Legend
              wrapperStyle={{ fontSize: '12px' }}
            />
            <Line
              type="monotone"
              dataKey="value"
              stroke={color}
              strokeWidth={2}
              dot={{ fill: color, r: 4 }}
              activeDot={{ r: 6 }}
              name={indicatorName}
            />
          </LineChart>
        ) : (
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="period"
              tick={{ fontSize: 12 }}
              stroke="#6b7280"
            />
            <YAxis
              tick={{ fontSize: 12 }}
              stroke="#6b7280"
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#fff',
                border: '1px solid #e5e7eb',
                borderRadius: '0.375rem',
                fontSize: '12px'
              }}
              formatter={(value: number, name: string, props: any) => {
                return [`${value.toLocaleString()} ${props.payload.unit || ''}`, '수치'];
              }}
            />
            <Legend
              wrapperStyle={{ fontSize: '12px' }}
            />
            <Bar
              dataKey="value"
              fill={color}
              name={indicatorName}
            />
          </BarChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}
