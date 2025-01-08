import { FunctionComponent } from "react";
import styles from "../styles/FrameComponent.module.css";

export type FrameComponentType = {
  className?: string;
};

const FrameComponent: FunctionComponent<FrameComponentType> = ({
  className = "",
}) => {
  return (
    <section className={[styles.welcomeParent, className].join(" ")}>
      <div className={styles.welcome}>
        <h2 className={styles.welcomeBack}>Welcome back</h2>
        <div className={styles.loginButtons}>
          <div className={styles.loginButtonsInner}>
            <div className={styles.adminLabelParent}>
              <input
                className={styles.adminLabel}
                placeholder="admin"
                type="text"
              />
              <input
                className={styles.adminLabel1}
                placeholder="******"
                type="text"
              />
            </div>
          </div>
          <div className={styles.loginButton}>
            <div className={styles.rectangleParent}>
              <div className={styles.frameChild} />
              <div className={styles.logIn}>Log In</div>
            </div>
          </div>
          <div className={styles.centerInfo}>
            <img className={styles.icon} alt="" src="/-1@2x.png" />
            <div className={styles.aiitSystemCenterContainer}>
              <span>AI</span>
              <span className={styles.span}>·</span>
              <span>IT SYSTEM CENTER</span>
            </div>
          </div>
        </div>
      </div>
      <div className={styles.signupInfo}>
        <div className={styles.signupBackground} />
        <input
          className={styles.input}
          placeholder="신규 회원가입을 희망하시는 경우 센터로 연락을 주시기 바랍니다:"
          type="text"
        />
      </div>
    </section>
  );
};

export default FrameComponent;
