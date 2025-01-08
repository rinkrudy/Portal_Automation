import React, { useEffect, useState } from 'react';
import './Stepper.css';

interface StepperProps {
  currentStep: number;
}

const Stepper: React.FC<StepperProps> = React.memo(({ currentStep }) => {
  const [activeStep, setActiveStep] = useState<number>(currentStep);
  const arrStep = [{label : "Start", description : "1"},
    {label : "기관번호매핑", description : "1"},
    {label : "의료인확인", description : "1"},
    {label : "지출장소확인", description : "1"},
    {label : "거리측정", description : "1"},
    {label :"End", description :"1"}, 
  ]

  useEffect(() => {
    // 현재 스텝이 변경되면 업데이트
    setActiveStep(currentStep);
  }, [currentStep]);

  return (
    <div className="stepper">
      {arrStep.map((step, index) => (
        <div key={index} className="step-container">
          <div
            className={`step ${
              activeStep === index + 1 ? 'active' : ''
            } ${activeStep > index + 1 ? 'completed' : ''}`}
          >
            {index + 1}
          </div>
          <p className="step-label">{step.label}</p>
          {index < arrStep.length - 1 && <div className="line"></div>}

        </div>
      ))}
    </div>
  );
});

export default Stepper;