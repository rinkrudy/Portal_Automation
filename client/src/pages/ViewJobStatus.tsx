import { useCallback, useEffect, useState } from "react";
import {
    InputWithLabel,
    RealTimeTable,
    Sidebar,
    SimpleInput,
    SingleProgressElementTotalSavings,
    Stepper,
    TextAreaInput,
    WhiteButton,
} from "../components";
import { current } from "@reduxjs/toolkit";
import { useLocation } from "react-router-dom";
import axios from "axios";
import { PieChart_Task } from "../components/chart";
import RechartsBarChart from "../components/chart/RechartsBarChart";
import RechartsBarHealth from "../components/chart/BarChartHealth";







const ViewJobStatus = () => {
    const [data_1, setData] = useState([]);
    const [bar_data, setBarData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const location = useLocation();
    const [step, setStep] = useState("MAPPING_MEDICAL_CARE");
    const [totalProgress, setTotalProgress] = useState({
        current: 0,
        total: 0
    });

    const [progressDoctor, setProgressDoctor] = useState({
        current: 0,
        total: 0
    });

    const [progressPlace, setProgressPlace] = useState({
        current: 0,
        total: 0
    });

    
    const task_id = location.state.task_id;
    console.log(task_id)
    const labels = ["Successful", "Failed", "Warn"];
    const dic_step = {
        "CREATED" : 1,
        "MAPPING_MEDICAL_CARE" : 2,
        "FIND_DOCTOR" : 3,
        "FIND_PLACE" : 4,
        "MEASURE_DISTANCE" : 5,
        "FINISHED" : 6
    }

    // {
    //     "id": 1,
    //     "task_id": "Health_Automation_1726043120739",
    //     "step": "MEASURE_DISTANCE",
    //     "work_count_doctor": 1,
    //     "work_count_place": 1,
    //     "work_count_measture": 0,
    //     "total_count": 1,
    //     "failed_count_doctor": 0,
    //     "failed_count_place": 0,
    //     "failed_count_measure": 0,
    //     "status": "pending",
    //     "progress": 0
    // }

    // STEP = [
    //     "CREATED",
    //     "MAPPING_MEDICAL_CARE",
    //     "FIND_DOCTOR",
    //     "FIND_PLACE",
    //     "MEASURE_DISTANCE",
    //     "FINISHED"
    // ]

    const updateData = useCallback(async () => {
        try {
            const response = await axios.get(`http://localhost:8000/api/request-job-status/${task_id}/`);
            // setData({"Successful" : response.data["work_count_doctor"],
            //         "Failed" : response.data["failed_count_doctor"]
            // });
            setData([response.data["work_count_doctor"], response.data["failed_count_doctor"] + response.data["failed_count_place"], response.data["failed_count_measure"]])
            setStep(response.data["step"])
            
            setTotalProgress({current : response.data['work_count_doctor'] + response.data["work_count_measure"] + response.data["work_count_place"], total: (response.data['total_count'] *3)})
            setBarData([
                {
                    name : "의료인",
                    value : response.data["failed_count_doctor"],
                },
                {
                    name : "지출장소",
                    value : response.data["failed_count_place"],
                },
                {
                    name : "거리측정",
                    value : response.data["failed_count_measure"],
                },
            ]);
            console.log(response.data);

        } catch(error) {
            console.error("Error fetching data", error);  // 에러 처리
        }
    }, []);
    
    const updateTx = useCallback(async () => {
        try {
            const response = await axios.get(`http://localhost:8000/api/request-transactions/${task_id}/`);
            // setData({"Successful" : response.data["work_count_doctor"],
            //         "Failed" : response.data["failed_count_doctor"]
            // });
            console.log(response.data)

        } catch(error) {
            console.error("Error fetching data", error);  // 에러 처리
        }
    }, []);
    

    useEffect(() => {
        updateData();

        const intervalId = setInterval(() => {
            updateData();  // 5초마다 데이터 갱신
        }, 5000);

        return () => clearInterval(intervalId);

        }, [updateData]);



    return (
        <div className="h-auto border-t border-blackSecondary border-1 flex dark:bg-blackPrimary bg-whiteSecondary">
            <Sidebar />
            <div className="dark:bg-blackPrimary bg-whiteSecondary w-full ">
                <div className="dark:bg-blackPrimary bg-whiteSecondary py-10">
                    <div className="px-4 sm:px-6 lg:px-8 pb-8 border-b border-gray-800 flex justify-between items-center max-sm:flex-col max-sm:gap-5">
                        <div className="flex flex-col gap-3">
                            <h2 className="text-3xl font-bold leading-7 dark:text-whiteSecondary text-blackPrimary">
                                수행 경과
                            </h2>
                        </div>
                    </div>

                    {/* Contents */}
                    <div className="px-4 sm:px-6 lg:px-8 pb-8 pt-8 grid grid-cols-2 gap-x-10 max-xl:grid-cols-1 max-xl:gap-y-10">
                        {/* Left div*/}
                        <div>
                            <div>
                                <div className="mb-11">
                                    <Stepper currentStep={dic_step[step]} />
                                </div>
                                
                                <div className="mb-11">
                                <SingleProgressElementTotalSavings
                                    title="Progress"
                                    totalMoney={totalProgress.total}
                                    percentSaved={totalProgress.current}
                                />
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-x-10 max-xl:grid-cols-1 max-xl:gap-y-10">
                                <div style={{ width: '300px', height: '400px', margin: '0 auto' }}>
                                <h2 className="text-2xl font-bold leading-7 dark:text-whiteSecondary text-blackPrimary">
                                수행 결과
                                </h2>
                                    <PieChart_Task labels={labels}
                                                    data={data_1}  />
                                </div>
                                <div>
                                    <h2 className="text-center text-2xl font-bold leading-7 dark:text-whiteSecondary text-blackPrimary">수행이상</h2>
                                    <RechartsBarHealth data={bar_data} />
                                </div>
                            </div>

                            <div>
                                <h3 className="text-2xl font-bold leading-7 dark:text-whiteSecondary text-blackPrimary">
                                 </h3>
  
                            </div>

                        </div>

                        <div className="overflow-auto h-full">
                             <RealTimeTable taskId={task_id}/>
                        </div>

                    </div>


                </div>

            </div>
        </div>


    );

}

export default ViewJobStatus;