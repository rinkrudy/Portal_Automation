// *********************
// Role of the component: Order table component that displays the orders in a table
// Name of the component: OrderTable.tsx
// Developer: Aleksandar Kuzmanovic
// Version: 1.0
// Component call: <OrderTable />
// Input parameters: no input parameters
// Output: OrderTable component that displays the orders in a table
// *********************

import { nanoid } from "nanoid";
import { Link } from "react-router-dom";
import { HiOutlinePencil } from "react-icons/hi";
import { HiOutlineTrash } from "react-icons/hi";
import { HiOutlineEye } from "react-icons/hi";
import { orderAdminItems } from "../utils/data";
import { useEffect, useState } from "react";
import axios from "axios";



const JobTable = () => {

  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // 데이터 가져오기
    const fetchRequestDocuments = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/request-documents/');
        setDocuments(response.data); // 가져온 데이터를 상태에 저장
        console.log(response.data);
        setLoading(false); // 로딩 상태를 false로 설정
      } catch (error) {
        setError('데이터를 가져오는 중 오류가 발생했습니다.');
        setLoading(false);
      }
    };

    fetchRequestDocuments();

    const intervalId = setInterval(fetchRequestDocuments, 5000); // 5초마다 데이터 요청

    return () => clearInterval(intervalId);


  }, []); // 빈 배열로 설정하여 컴포넌트가 마운트될 때 한 번만 실행

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <table className="mt-6 w-full whitespace-nowrap text-center max-lg:block max-lg:overflow-x-scroll">
      <colgroup>
        <col className="lg:w-1/12" />
        <col className="lg:w-3/12" />
        <col className="lg:w-1/12" />
        <col className="lg:w-2/12" />
        <col className="lg:w-2/12" />
        <col className="lg:w-2/12" />
        <col className="lg:w-2/12" />
      </colgroup>
      <thead className="border-b border-white/10 text-sm leading-6 dark:text-whiteSecondary text-blackPrimary">
        <tr>
          <th
            scope="col"
            className="py-2 pl-4 pr-8 font-semibold sm:pl-6 lg:pl-8 "
          >
             
          </th>
          <th
            scope="col"
            className="py-2 pl-4 pr-8 font-semibold sm:pl-6 lg:pl-8 text-center"
          >
            ProcessName
          </th>
          <th
            scope="col"
            className="py-2 pl-0 pr-8 font-semibold table-cell lg:pr-20"
          >
            UserId
          </th>
          <th scope="col" className="py-2 pl-0 pr-8 font-semibold table-cell">
            Status
          </th>
          <th
            scope="col"
            className="py-2 pl-0 pr-8 font-semibold table-cell lg:pr-20"
          >
            Date
          </th>
          <th
            scope="col"
            className="py-2 pl-0 pr-4 text-center font-semibold table-cell sm:pr-6 lg:pr-8"
          >
            Result File
          </th>
          <th
            scope="col"
            className="py-2 pl-0 pr-4 text-center font-semibold table-cell sm:pr-6 lg:pr-8"
          >
            Action
          </th>
        </tr>
      </thead>
      <tbody className="divide-y divide-white/5">
        {documents.map((item) => (
          <tr key={nanoid()}>
            <td className="py-4 pl-4 pr-8 sm:pl-6 lg:pl-8">
              <div className="flex items-center gap-x-4">
                <div className="truncate text-sm font-medium  leading-6 dark:text-whiteSecondary text-blackPrimary">
                  <input type="checkbox"></input>
                </div>
              </div>
            </td>
            <td className="py-4 pl-4 pr-8 sm:pl-6 lg:pl-8">
              <div className="flex items-center gap-x-4">
                <div className="truncate text-sm font-medium leading-6 dark:text-whiteSecondary text-blackPrimary block flex justify-center text-center">
                  {item.process_name}
                </div>
              </div>
            </td>
            <td className="py-4 pl-4 pr-8 sm:pl-6 lg:pl-8">
              <div className="flex items-center gap-x-4">
                <div className="truncate text-sm font-medium leading-6 dark:text-whiteSecondary text-blackPrimary">
                  {item.user_id}
                </div>
              </div>
            </td>
            <td className="py-4 pl-0 pr-4 table-cell pr-8">
              <div className="flex gap-x-3 block flex justify-center items-center">
                <div
                  className={`text-sm leading-6 py-1 px-2 ${
                    item.status === "COMPLETED" &&
                    "dark:bg-green-900 bg-green-700 text-whiteSecondary font-semibold"
                  } ${
                    item.status === "ON_HOLD" &&
                    "dark:bg-yellow-900 bg-yellow-700 text-whiteSecondary font-semibold"
                  } ${
                    item.status === "Cancelled" &&
                    "dark:bg-red-900 bg-red-700 text-whiteSecondary font-semibold"
                  } ${
                    item.status === "PROCESSING" &&
                    "dark:bg-blue-900 bg-blue-700 text-whiteSecondary font-semibold"
                  }`}
                >
                  {item.status}
                </div>
              </div>
            </td>
            <td className="py-4 pl-0 pr-8 text-sm leading-6 dark:text-whiteSecondary text-blackPrimary table-cell lg:pr-20">
              {item.date}
            </td>
            <td className="py-4 pl-0 pr-8 text-sm leading-6 dark:text-whiteSecondary text-blackPrimary table-cell lg:pr-20">
                {item.path_result && (
            <a href={item.path_result} download={item.path_result}>
               <button>엑셀 파일 다운로드</button>
            </a>
             )}
            </td>
            <td className="py-4 pl-0 pr-4 text-right text-sm leading-6 dark:text-whiteSecondary text-blackPrimary table-cell pr-6 lg:pr-8">
              <div className="flex gap-x-1 justify-end">
                <Link
                  to="/job-status"
                  state={{ task_id : item.request_key }}
                  className="dark:bg-blackPrimary bg-whiteSecondary dark:text-whiteSecondary text-blackPrimary border border-gray-600 w-8 h-8 block flex justify-center items-center cursor-pointer dark:hover:border-gray-500 hover:border-gray-400"
                >
                  <HiOutlineEye className="text-lg" />
                </Link>
                <Link
                  to="#"
                  className="dark:bg-blackPrimary bg-whiteSecondary dark:text-whiteSecondary text-blackPrimary border border-gray-600 w-8 h-8 block flex justify-center items-center cursor-pointer dark:hover:border-gray-500 hover:border-gray-400"
                >
                  <HiOutlineTrash className="text-lg" />
                </Link>
              </div>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};
export default JobTable;
