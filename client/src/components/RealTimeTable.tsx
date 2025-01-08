import React, { useState, useEffect } from 'react';
import axios from 'axios';





// TableData 타입 정의
interface TableData {
    id: number;
    tx_key: string;
    hospital_name: string;
    hospital_number: string;
    doctor_name: string;
    place_name: string;
    doctor_exist: string;
    hospital_address: string;
    searched_address: string;
    distance: number;
}

interface TableDataProps {
    taskId: string;
}


// 테이블 컴포넌트 정의 및 React.memo로 감싸기
const RealTimeTable: React.FC<TableDataProps> = React.memo(({ taskId }) => {
    const [data, setData] = useState<TableData[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [tx_key, setTxKey] = useState<string | null>(null);

    const fetchData = async () => {
        if (!tx_key) return;  // tx_key가 설정되지 않으면 데이터를 요청하지 않음
    
        try {
          const response = await axios.get(`http://localhost:8000/api/request-transactions/${tx_key}/`);  // 서버의 실제 엔드포인트 사용
          setData(response.data);
          console.log(response.data);
          setLoading(false);
        } catch (err) {
          // setError('데이터를 가져오는 중 오류가 발생했습니다.');
          setLoading(false);
        }
      };
    
      // taskId가 변경될 때 tx_key 설정
      useEffect(() => {
        console.log("taskId:", taskId);
        setTxKey(taskId);  // taskId가 변경되면 tx_key 설정
      }, [taskId]);
    
      // tx_key가 설정되면 데이터를 가져오는 로직
      useEffect(() => {
        fetchData();  // tx_key가 설정되면 데이터 가져오기
    
        const intervalId = setInterval(() => {
          fetchData();  // 5초마다 데이터를 갱신
        }, 5000);
    
        return () => clearInterval(intervalId);  // 컴포넌트가 언마운트될 때 인터벌 해제
      }, [tx_key]);  // tx_key가 변경될 때마다 fetchData 실행
    // 테이블 렌더링
    return (
        <div className="container mx-auto px-4">
            <h2 className="text-xl font-bold mb-4">지출결의서 확인 결과</h2>

            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}

            <table className="min-w-full bg-white dark:bg-gray-800">
                <thead>
                    <tr>
                        <th className="px-6 py-3 border-b-2 border-gray-300 text-left leading-4 text-gray-600 dark:text-gray-400 tracking-wider">소속</th>
                        <th className="px-6 py-3 border-b-2 border-gray-300 text-left leading-4 text-gray-600 dark:text-gray-400 tracking-wider">요양기관번호</th>
                        <th className="px-6 py-3 border-b-2 border-gray-300 text-left leading-4 text-gray-600 dark:text-gray-400 tracking-wider">성명</th>
                        <th className="px-6 py-3 border-b-2 border-gray-300 text-left leading-4 text-gray-600 dark:text-gray-400 tracking-wider">지출장소</th>
                        <th className="px-6 py-3 border-b-2 border-gray-300 text-left leading-4 text-gray-600 dark:text-gray-400 tracking-wider">요양기관확인</th>
                        <th className="px-6 py-3 border-b-2 border-gray-300 text-left leading-4 text-gray-600 dark:text-gray-400 tracking-wider">의료인확인</th>
                        <th className="px-6 py-3 border-b-2 border-gray-300 text-left leading-4 text-gray-600 dark:text-gray-400 tracking-wider">지출장소확인</th>
                        <th className="px-6 py-3 border-b-2 border-gray-300 text-left leading-4 text-gray-600 dark:text-gray-400 tracking-wider">거리</th>
                        
      
                        
                    </tr>
                </thead>
                <tbody>
                    {!loading && data.length > 0 ? (
                        data.map((item) => (
                            <tr key={item.id}>
                                <td className="px-6 py-4 border-b border-gray-200">{item.hospital_name}</td>
                                <td className="px-6 py-4 border-b border-gray-200">{item.hospital_number}</td>
                                <td className="px-6 py-4 border-b border-gray-200">{item.doctor_name}</td>
                                <td className={`px-6 py-4 border-b border-gray-200`}>{item.place_name}</td>
                                <td className={`px-6 py-4 border-b border-gray-200 ${item.medical_exist == "미확인" ? "" : (item.medical_exist == "확인 실패" ? 'bg-red-200' : 'bg-green-200')}`}>{item.medical_exist}</td>
                                <td className={`px-6 py-4 border-b border-gray-200 ${item.doctor_exist == "미확인" ? "" : (item.doctor_exist =="확인 불가" ? 'bg-red-300': 'bg-green-300')}`}>{item.doctor_exist}</td>
                                <td className={`px-6 py-4 border-b border-gray-200 ${item.place_exist == "미확인" ? "" : (item.place_exist =="확인 불가" ? 'bg-red-400': 'bg-green-400')}`}>{item.place_exist}</td>
                                <td className={`px-6 py-4 border-b border-gray-200 ${item.distance == -1 ? "" : (item.distance >= 10 ? (item.distance >= 20 ? 'bg-red-500' : 'bg-yellow-300') : 'bg-green-500')}`}> {item.distance.toFixed(2)} km</td>
                                

                                
                                
                                
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan={7} className="px-6 py-4 text-center">
                                No data available
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
});

export default RealTimeTable
