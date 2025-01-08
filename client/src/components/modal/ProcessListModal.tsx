import React, { useState } from "react";
import RequestModal_OA from "./RequestModal_OA"; // Process 1 컴포넌트 import
import ExcelUploadModal from "./RequestModal_Health"


interface ModalProps {
    isOpen: boolean;

}


const ModalComponent: React.FC<{ isOpen: boolean; closeModal: () => void }> = (
    { isOpen, 
    closeModal 
    }) => 
  {
  // 현재 모달에서 보여줄 UI를 결정하는 상태
  const [selectedProcess, setSelectedProcess] = useState<string | null>(null);

  // 프로세스 리스트
  const processes = ["OA Automation", "Health Automation", "Process 3"];

  // 모달의 UI를 변경하는 함수
  const handleProcessClick = (processName: string) => {
    setSelectedProcess(processName);
  };

  // 모달 Close
  const handleCloseModal = () => {
    setSelectedProcess(null); // 모달을 닫을 때 selectedProcess 값을 초기화
    closeModal(); // 부모 컴포넌트에 있는 closeModal 함수 호출
  };


  // 선택된 프로세스에 따른 다른 UI를 렌더링하는 함수
  const renderContent = () => {
    switch (selectedProcess) {
        case "OA Automation":
            return <RequestModal_OA/>; // Process 1 컴포넌트 호출
        case "Health Automation":
            return <ExcelUploadModal handleCloseModal={handleCloseModal}/>;
      default:
        return (
          <div>
            <h2>프로세스를 선택하세요</h2>
            {processes.map((process) => (
            <button
                key={process}
                onClick={() => handleProcessClick(process)}
                className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                {process}
              </button>
            ))}
          </div>
        );
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50 overflow-auto">
        <div className="relative bg-white dark:bg-gray-800 p-6 rounded-lg w-auto">
        {/* X 닫기 버튼: 오른쪽 상단에 고정 */}
        <button
          onClick={handleCloseModal}
          className="absolute top-2 right-2 text-gray-600 hover:text-gray-800 dark:text-white dark:hover:text-gray-400"
        >
          ✕
        </button>

        {/* 모달 내용 */}
        {renderContent()}
      </div>
    </div>
  );
};

export default ModalComponent;