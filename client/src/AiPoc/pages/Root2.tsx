import { FunctionComponent } from "react";
import SafetyUpdates from "../components/SafetyUpdates";
import styles from "../styles/Root2.module.css";

const Root2: FunctionComponent = () => {
    return (
        <div className={styles.root}>
            <img className={styles.icon} alt="" src="/-20241024--93114-1@2x.png" />
            <div className={styles.aIAudit}>
                <h1 className={styles.aiAudit}>AI AUDIT</h1>
            </div>
            <section className={styles.koreaTrendsContainer}>
                <div className={styles.koreaTrends}>
                    <div className={styles.koreaTrendsTitle}>
                        <h1 className={styles.aiTrendsWithin}>AI TRENDS WITHIN KOREA</h1>
                        <div className={styles.koreaTrendsTitleInner}>
                            <div className={styles.frameChild} />
                        </div>
                    </div>
                </div>
                <div className={styles.newsletterHeader}>
                    <div className={styles.newsletterDescription}>
                        <div className={styles.newsletterBody}>
                            <div className={styles.newsletterBodyChild} />
                            <div className={styles.newsletterIntro}>
                                <h3 className={styles.h3}>뉴스레터</h3>
                                <h1
                                    className={styles.kcAiTechnical}
                                >{`K&C AI Technical Updates (2024 November)`}</h1>
                                <div className={styles.aiitSystemCenter}>
                                    김·장 AI·IT System Center에서 월별 발행하는 국문
                                    종합뉴스레터입니다. 국내외 주요 AI 기술 트렌드 동향을
                                    분석하고, 나아가 국내 AI 입법 동향 및 가이드라인 체계를...
                                </div>
                            </div>
                            <div className={styles.regulationUpdates}>2024.11.01</div>
                        </div>
                        <SafetyUpdates
                            aI="과학기술정보통신부, AI 안전연구소 출범"
                            eTRIAI="ETRI 산하 기관으로 AI 안전연구소 출범하였으며 이로써 세계 4번째 AISI..."
                            safetyDate="2024.11.01"
                        />
                    </div>
                    <div className={styles.newsletterDescription1}>
                        <SafetyUpdates
                            aI="국회, 인공지능 산업 진흥에 관한 법률안 발의"
                            eTRIAI="국내 12번째 AI 법안은 소관위심사 계류 중으로 상호대응되는 논문이 입법과 정책..."
                            safetyDate="2024.10.31"
                            safetyUpdatesWidth="unset"
                            safetyUpdatesFlex="1"
                            safetyUpdatesMinWidth="121px"
                            h3Width="29px"
                            h3Display="inline-block"
                        />
                        <SafetyUpdates
                            aI="네이버, AI 안전성 프레임워크 발표"
                            eTRIAI="네이버는 AI Safety Framework(ASF)를 통해AI 시스템의 개발 및 배포 프로세스의..."
                            safetyDate="2024.MM.DD"
                            safetyUpdatesWidth="unset"
                            safetyUpdatesFlex="1"
                            safetyUpdatesMinWidth="121px"
                            h3Width="29px"
                            h3Display="inline-block"
                        />
                        <SafetyUpdates
                            aI="개인정보보호위원회, 동의 관련 원칙 및 계획 공개"
                            eTRIAI="개인정보 처리에 대한 동의를 받는 방법을 규정한 개정 ‘개인정보 보호법’..."
                            safetyDate="2024.09.13"
                            safetyUpdatesWidth="unset"
                            safetyUpdatesFlex="1"
                            safetyUpdatesMinWidth="121px"
                            h3Width="29px"
                            h3Display="inline-block"
                        />
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Root2;
