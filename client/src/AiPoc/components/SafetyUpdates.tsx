import { FunctionComponent, useMemo, type CSSProperties } from "react";
import styles from "../styles/SafetyUpdates.module.css";

export type SafetyUpdatesType = {
  className?: string;
  aI?: string;
  eTRIAI?: string;
  safetyDate?: string;

  /** Style props */
  safetyUpdatesWidth?: CSSProperties["width"];
  safetyUpdatesFlex?: CSSProperties["flex"];
  safetyUpdatesMinWidth?: CSSProperties["minWidth"];
  h3Width?: CSSProperties["width"];
  h3Display?: CSSProperties["display"];
};

const SafetyUpdates: FunctionComponent<SafetyUpdatesType> = ({
  className = "",
  aI,
  eTRIAI,
  safetyDate,
  safetyUpdatesWidth,
  safetyUpdatesFlex,
  safetyUpdatesMinWidth,
  h3Width,
  h3Display,
}) => {
  const safetyUpdatesStyle: CSSProperties = useMemo(() => {
    return {
      width: safetyUpdatesWidth,
      flex: safetyUpdatesFlex,
      minWidth: safetyUpdatesMinWidth,
    };
  }, [safetyUpdatesWidth, safetyUpdatesFlex, safetyUpdatesMinWidth]);

  const h3Style: CSSProperties = useMemo(() => {
    return {
      width: h3Width,
      display: h3Display,
    };
  }, [h3Width, h3Display]);

  return (
    <div
      className={[styles.safetyUpdates, className].join(" ")}
      style={safetyUpdatesStyle}
    >
      <div className={styles.safetyUpdatesChild} />
      <h3 className={styles.h3} style={h3Style}>
        뉴스레터
      </h3>
      <div className={styles.safetyContent}>
        <h1 className={styles.ai}>{aI}</h1>
        <div className={styles.etri}>{eTRIAI}</div>
      </div>
      <div className={styles.safetyDate}>{safetyDate}</div>
    </div>
  );
};

export default SafetyUpdates;
