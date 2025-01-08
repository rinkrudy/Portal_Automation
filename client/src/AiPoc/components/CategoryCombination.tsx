import { FunctionComponent, useMemo, type CSSProperties } from "react";
import styles from "../styles/CategoryCombination.module.css";

export type CategoryCombinationType = {
  className?: string;
  faithEval?: string;
  faithfulness?: string;
  salesforceAIResearch?: string;

  /** Style props */
  categoryCombinationFlex?: CSSProperties["flex"];
  categoryCombinationMinWidth?: CSSProperties["minWidth"];
  faithEvalDisplay?: CSSProperties["display"];
  faithEvalMinWidth?: CSSProperties["minWidth"];
  salesforceAIResearchDisplay?: CSSProperties["display"];
  salesforceAIResearchMinWidth?: CSSProperties["minWidth"];
};

const CategoryCombination: FunctionComponent<CategoryCombinationType> = ({
  className = "",
  faithEval,
  faithfulness,
  salesforceAIResearch,
  categoryCombinationFlex,
  categoryCombinationMinWidth,
  faithEvalDisplay,
  faithEvalMinWidth,
  salesforceAIResearchDisplay,
  salesforceAIResearchMinWidth,
}) => {
  const categoryCombinationStyle: CSSProperties = useMemo(() => {
    return {
      flex: categoryCombinationFlex,
      minWidth: categoryCombinationMinWidth,
    };
  }, [categoryCombinationFlex, categoryCombinationMinWidth]);

  const faithEvalStyle: CSSProperties = useMemo(() => {
    return {
      display: faithEvalDisplay,
      minWidth: faithEvalMinWidth,
    };
  }, [faithEvalDisplay, faithEvalMinWidth]);

  const salesforceAIResearchStyle: CSSProperties = useMemo(() => {
    return {
      display: salesforceAIResearchDisplay,
      minWidth: salesforceAIResearchMinWidth,
    };
  }, [salesforceAIResearchDisplay, salesforceAIResearchMinWidth]);

  return (
    <div
      className={[styles.categoryCombination, className].join(" ")}
      style={categoryCombinationStyle}
    >
      <div className={styles.categoryCombinationChild} />
      <div className={styles.faithEvalCategory}>
        <div className={styles.faitheval} style={faithEvalStyle}>
          {faithEval}
        </div>
        <div className={styles.categorySeparator}>?</div>
      </div>
      <div className={styles.faithfulnessCategory}>
        <h1 className={styles.faithfulness}>{faithfulness}</h1>
      </div>
      <div className={styles.salesforceCategory}>
        <div
          className={styles.salesforceAiResearch}
          style={salesforceAIResearchStyle}
        >
          {salesforceAIResearch}
        </div>
      </div>
    </div>
  );
};

export default CategoryCombination;
