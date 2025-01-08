
import { FunctionComponent } from "react";
import styles from '../styles/header.module.css';

export interface HeaderProps {
    className?: string;
}

const Header:FunctionComponent<HeaderProps> = ({ className = ""}) => {
    return (
            <header className={styles.analysisSteps}>
                <div className={styles.stepOne}>
                    <div className={styles.landingFrame}>{`K&C AI AUDIT`}</div>
                </div>
                <div className={styles.stepTwo}>
                    <div className={styles.generativeAnalysis}>
                        <div className={styles.generativeAiAnalysis}>
                            Generative AI Analysis
                        </div>
                    </div>
                    <div className={styles.redTeaming}>
                        <div className={styles.redTeamingChild} />
                        <div className={styles.multiTurnRedTeaming}>
                            <p className={styles.multiTurn}>Multi-Turn</p>
                            <p className={styles.redTeaming1}>Red-Teaming</p>
                        </div>
                    </div>
                </div>
            </header>
    )

}

export default Header;