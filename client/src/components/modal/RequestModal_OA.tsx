import React, { useState } from 'react';
import { nanoid } from "nanoid";


interface GroupRow {
  id: number;
  country: string;
  status: string;
  appNumber: string;
  result: string;
}

interface Group {
  id: number;
  title: string;
  rows: GroupRow[];
}

interface ModalProps {
  isOpen: boolean;
  groups: Group[];
  closeModal: () => void;
  addRow: (groupId: number) => void;
  addGroup: () => void;
  handleInputChange: (groupId: number, rowId: number, field: string, value: string) => void;
  handleSubmit: () => void;
}

const RequestModal_OA = () => {

    const [groups, setGroups] = useState([
      {
        id: nanoid(),
        title: "제1그룹",
        rows: [{ id: 1, country: 'KR', status: '공개', appNumber: '12345678', result: '' }],
      },
    ]);

    const addGroup = () => {
      const newGroupNumber = groups.length + 1;
      setGroups([
        ...groups,
        {
          id: nanoid(),
          title: `제${newGroupNumber}그룹`,
          rows: [{ id: nanoid(), country: 'KR', status: '공개', appNumber: '12345678', result: '' }],
        },
      ]);
    };
    const addRow = (groupId) => {
      setGroups(
        groups.map(group =>
          group.id === groupId
            ? { ...group, rows: [...group.rows, { id: 1, country: 'KR', status: '공개', appNumber: '12345678', result: '' }] }
            : group
        )
      );
    };

    const handleInputChange = (groupId, rowId, field, value) => {
      setGroups(
        groups.map(group =>
          group.id === groupId
            ? {
                ...group,
                rows: group.rows.map(row =>
                  row.id === rowId ? { ...row, [field]: value } : row
                ),
              }
            : group
        )
      );
    };

    const handleSubmit = async () => {
        console.log("submit");
      // const userId = 1;  // 실제 애플리케이션에서는 로그인된 사용자의 ID를 가져옴
      // const requestData = {
      //     user_id : userId.toString(),
      //     request_key: `${new Date().toISOString().replace(/[-:.]/g, '')}_${userId}`, // yyyyMMddHHmmss_userId 형식
      //     patent_documents: groups.flatMap(group =>
      //         group.rows.map(row => ({
      //             group: group.title,
      //             country: row.country,
      //             status: row.status,
      //             app_number: row.appNumber,
      //         }))
      //     ),
      // };

      // try {
      //     const response = await axios.post('http://localhost:8000/api/create-request-document/', requestData);
      //     console.log('Request submitted:', response.data);
      // } catch (error) {
      //     console.error('Failed to submit request:', error);
      // }
  };


  return (
    
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg w-auto">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Request Job</h2>
        {groups.map((group) => (
          <div key={group.id} className="mb-6">
            <table className="min-w-full bg-white dark:bg-gray-700">
              <thead>
                <tr>
                  <th className="border px-4 py-2">Group</th>
                  <th className="border px-4 py-2">Country</th>
                  <th className="border px-4 py-2">Status</th>
                  <th className="border px-4 py-2">App_Number</th>
                  <th className="border px-4 py-2">조회결과</th>
                </tr>
              </thead>
              <tbody>
                {group.rows.map((row, rowIndex) => (
                  <tr key={row.id}>
                    {rowIndex === 0 ? (
                      <td className="border px-4 py-2" rowSpan={group.rows.length}>
                        {group.title}
                      </td>
                    ) : null}
                    <td className="border px-4 py-2">
                      <select
                        value={row.country}
                        onChange={(e) =>
                          handleInputChange(group.id, row.id, 'country', e.target.value)
                        }
                        className="w-full px-2 py-1 border rounded dark:bg-gray-600 dark:text-white"
                      >
                        <option value="">Select Country</option>
                        <option value="KR">KR</option>
                        <option value="UR">UR</option>
                        <option value="JR">JR</option>
                        <option value="CN">CN</option>
                      </select>
                    </td>
                    <td className="border px-4 py-2">
                      <select
                        value={row.status}
                        onChange={(e) =>
                          handleInputChange(group.id, row.id, 'status', e.target.value)
                        }
                        className="w-full px-2 py-1 border rounded dark:bg-gray-600 dark:text-white"
                      >
                        <option value="">Select Status</option>
                        <option value="공개">공개</option>
                        <option value="출원">출원</option>
                      </select>
                    </td>
                    <td className="border px-4 py-2">
                      <input
                        type="text"
                        value={row.appNumber}
                        onChange={(e) =>
                          handleInputChange(group.id, row.id, 'appNumber', e.target.value)
                        }
                        className="w-full px-2 py-1 border rounded dark:bg-gray-600 dark:text-white"
                      />
                    </td>
                    <td className="border px-4 py-2">
                      <input
                        type="text"
                        value={row.result}
                        readOnly
                        className="w-full px-2 py-1 border rounded dark:bg-gray-600 dark:text-white bg-gray-200 dark:bg-gray-700"
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <button
              onClick={() => addRow(group.id)}
              className="mt-2 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
            >
              + 행 추가
            </button>
          </div>
        ))}

        <div className="mt-4">
          <button
            onClick={addGroup}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            + 그룹 추가
          </button>
        </div>

        <div className="flex justify-end gap-x-2 mt-4">
          <button
            type="submit"
            onClick={handleSubmit}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Submit
          </button>
        </div>
      </div>
  );
};

export default RequestModal_OA;