// *********************
// Role of the component: SingleProgressElementTotalSavings component that displays the single progress element with the title, total money, and percentage saved
// Name of the component: SingleProgressElementTotalSavings.tsx
// Developer: Aleksandar Kuzmanovic
// Version: 1.0
// Component call: <SingleProgressElementTotalSavings title="Education" totalMoney={300} percentSaved={50} />
// Input parameters: roles: { title: string; totalMoney: number; percentSaved: number }
// Output: SingleProgressElementTotalSavings component that displays the single progress element with the title, total money, and percentage saved
// *********************

const getBackgroundColor = (percentAmount) => {
  if (percentAmount === 0) {
    return 'rgb(128, 128, 128)'; // 회색
  } else if (percentAmount > 0 && percentAmount < 50) {
    const greenValue = Math.floor((percentAmount / 50) * 255); // 노란색에서 주황색으로
    return `rgb(255, ${greenValue}, 0)`; // 노란색에서 주황색 그라데이션
  } else if (percentAmount >= 50 && percentAmount <= 100) {
    const redValue = Math.floor((100 - percentAmount) * 2.55); // 초록색 그라데이션
    return `rgb(${redValue}, 255, 0)`; // 초록색에서 연한 초록색으로
  }
  return 'rgb(255, 255, 255)'; // 기본값
};

const SingleProgressElementTotalSavings = ({
  title,
  totalMoney,
  percentSaved,
}: {
  title: string;
  totalMoney: number;
  percentSaved: number;
}) => {
    console.log(title, totalMoney, percentSaved);
    
    const percentAmount = (percentSaved / totalMoney) * 100;
  return (
    
    <div>
      <div className="flex justify-between my-3">
        <h4 className="text-2xl font-semibold dark:text-whiteSecondary text-blackPrimary max-sm:text-xl max-[450px]:text-lg">
          { title }
        </h4>
        {/* <p className="dark:text-whiteSecondary text-blackPrimary text-2xl font-semibold max-sm:text-lg  max-[450px]:text-base">
          {percentSaved} / {totalMoney}
        </p> */}
      </div>
      <div className="bg-white w-full h-5">
        <div>
          <div style={{ width: `${percentAmount}%`, backgroundColor: getBackgroundColor(percentAmount), transition: `background-color 0.5s ease`  }} className="dark:bg-green-600 bg-green-500 h-5"></div>
        </div>
      </div>
    </div>
  );
};
export default SingleProgressElementTotalSavings;
