import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, Tooltip, Legend, ArcElement } from "chart.js";
import { useAppSelector } from "../../hooks";
import { memo } from "react";


ChartJS.register(Tooltip, Legend, ArcElement);

interface PieChartProps {
  labels: string[];
  data: number[];
  backgroundColor: string[];
  borderColor?: string[];
}

const PieChart_Task: React.FC<PieChartProps> = memo(({labels, data, backgroundColor, borderColor}) => {

  const chartData = {
    labels: labels,  // 부모 컴포넌트에서 받은 labels
    datasets: [
      {
        label: 'Dataset',
        data: data,  // 부모 컴포넌트에서 받은 데이터
        backgroundColor: backgroundColor || [
          '#4bc055',
          'rgba(255, 99, 132, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
        ],
        borderColor: borderColor || [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,  // 범례 위치
      },
      tooltip: {
        enabled: true,  // 툴팁 활성화
      },
    },
  };
  

  const { darkMode } = useAppSelector((state) => state.darkMode);
  if (darkMode) {
    ChartJS.defaults.color = "#fff";
    ChartJS.defaults.backgroundColor = '#fff';
    ChartJS.defaults.borderColor = '#fff';
    ChartJS.defaults.color = '#fff';
  } else {
    ChartJS.defaults.color = "#000";
    ChartJS.defaults.backgroundColor = '#000';
    ChartJS.defaults.borderColor = '#000';
    ChartJS.defaults.color = '#000';
  }



  return <Pie data={chartData} options={options} />;
});
export default PieChart_Task;
