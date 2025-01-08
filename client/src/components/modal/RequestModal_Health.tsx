import React, { useState } from "react";
import * as XLSX from "xlsx";  // 엑셀 파일을 파싱하기 위한 라이브러리
import axios from "axios";
import { useApi } from "../../context/ApiProvider";



interface ModalProps {
    handleCloseModal: () => void;
}

const ExcelUploadModal: React.FC<ModalProps> = ({
    handleCloseModal
}) => {
    const { postData, loading, error } = useApi(); // Axios 호출을 위한 API Hook 사용
    const [file, setFile] = useState<File | null>(null);
    const [requestKey, setRequestKey] = useState('');
    const [backgroundMode, setBackgroundMode] = useState(true);

    // 파일이 선택되었을 때
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setFile(event.target.files[0]);
        }
    };
    const handleRequestKeyChange = (e) => {
        setRequestKey(e.target.value);
    };

    const handleBackgroundModeChange = () => {
        setBackgroundMode(!backgroundMode);
    };

    // 엑셀 파일을 읽고 Axios로 전송
    const handleSubmit = async () => {
        let jsonData = null;
        const formData = new FormData();

        if (file) {
            try {

                const request_info = {
                    "user_id": "User1",
                    "request_key": "Health_Automation_" + Date.now().toString(),
                    "process_name": "Health_Automation"
                };


                formData.append("file", file);
                formData.append("request_info", JSON.stringify(request_info));
                formData.append("background_mode", backgroundMode);

                // 1. 엑셀 파일을 읽기
                const reader = new FileReader();
                reader.onload = (e) => {
                    const data = e.target?.result;
                    if (data) {
                        // 2. 엑셀 파일을 워크북으로 파싱
                        const workbook = XLSX.read(data, { type: "binary" });

                        // 3. 특정 시트의 이름을 지정하여 파싱 (예: "Sheet1")
                        const sheetName = workbook.SheetNames[0];  // 첫 번째 시트 이름
                        const sheet = workbook.Sheets[sheetName];

                        // 4. 시트의 데이터를 JSON 형태로 변환
                        jsonData = XLSX.utils.sheet_to_json(sheet);
                        console.log(jsonData)

                        // 5. Axios를 통해 서버로 데이터 전송

                        // axios.post("/api/upload-excel", jsonData)
                        //   .then((response) => {
                        //     console.log("Response:", response.data);
                        //     // 성공 시 모달 닫기 또는 알림
                        //   })
                        //   .catch((error) => {
                        //     console.error("Error uploading Excel data:", error);
                        //   });
                    }
                };
                // Request data
                try {
                    const response = await postData('http://localhost:8000/api/create-request-document/', formData);
                    console.log('Response data: ', response);
                    handleCloseModal()
                }
                catch {
                    console.error('Error submitting form:', error);
                }
                // 파일 읽기 시작
                reader.readAsBinaryString(file);
            } catch (err) {
                console.error("Failed to parse the file:", err);
            }
        }
    };
    return (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg w-auto">
            <h2 className="text-lg font-semibold mb-4">엑셀 업로드</h2>

            {/* Request Key 입력 필드 */}
            <div className="mb-4">
                <label className="block text-gray-700 dark:text-gray-300 mb-2" htmlFor="requestKey">
                    Request Key
                </label>
                <input
                    type="text"
                    id="requestKey"
                    placeholder="please request key"
                    value={requestKey}
                    onChange={handleRequestKeyChange}
                    className="px-3 py-2 border rounded w-full dark:bg-gray-700 dark:text-white"
                />
            </div>

            {/* Background Mode 체크박스 */}
            <div className="mb-4 flex items-center">
                <input
                    type="checkbox"
                    id="backgroundMode"
                    checked={backgroundMode}
                    onChange={handleBackgroundModeChange}
                    className="mr-2"
                />
                <label htmlFor="backgroundMode" className="text-gray-700 dark:text-gray-300">
                    Background Mode
                </label>
            </div>

            {/* 파일 업로드 */}
            <div className="mb-4">
                <label className="block text-gray-700 dark:text-gray-300 mb-2">Excel Upload</label>
                <input
                    type="file"
                    accept=".xlsx, .xls"
                    onChange={handleFileChange}
                    className="mb-4"
                />
            </div>

            {/* 제출 버튼 */}
            <button
                onClick={handleSubmit}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
                Upload and Submit
            </button>
        </div>
    );
};

export default ExcelUploadModal;