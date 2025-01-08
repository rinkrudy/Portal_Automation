import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// 외부에서 데이터를 받을 수 있도록 컴포넌트 정의
interface RechartsBarChartProps {
  data: { name: string; revenue: number; profit: number }[];
}

const RechartsBarHealth: React.FC<RechartsBarChartProps> = React.memo(({ data }) => {
  const [chartData, setChartData] = useState(data);

  useEffect(() => {
    // 외부 데이터가 변경되면 차트 데이터를 업데이트
    setChartData(data);
  }, [data]);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart
        title='검증실패'
        data={chartData}  // 업데이트된 데이터를 바인딩
        margin={{
          top: 5,
          right: 10,
          left: 10,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis
        domain={[1, 10]}
            tickCount={10}
            allowDecimals={false}
        />
        <Bar dataKey="value" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  );
});

export default RechartsBarHealth;