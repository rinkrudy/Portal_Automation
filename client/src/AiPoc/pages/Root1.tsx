import { FunctionComponent } from "react";
import styles from "../styles/Root1.module.css";

export type Root1Type = {
    className?: string;
};

const Root1: FunctionComponent<Root1Type> = ({ className = "" }) => {
    return (
        <div className={[styles.root, className].join(" ")}>
            <div className={styles.generativeAnalysis}>
                <div className={styles.progressSteps}>
                    <div className={styles.stepThree}>
                        <div className={styles.stepFour}>
                            <div className={styles.stepFive}>
                                <div className={styles.kcAiAudit}>{`K&C AI AUDIT`}</div>
                            </div>
                            <div className={styles.generativeAiAnalysis}>
                                Generative AI Analysis
                            </div>
                        </div>
                    </div>
                    <h3 className={styles.aiAuditingInContainer}>
                        <p className={styles.aiAuditing}>AI AUDITING</p>
                        <p className={styles.inProgress}>IN PROGRESS...</p>
                    </h3>
                </div>
            </div>
            <section className={styles.rectangleParent}>
                <div className={styles.frameChild} />
                <div className={styles.spotlightContent}>
                    <div className={styles.spotlights}>
                        <div className={styles.kcAiAudit1}>{`K&C AI AUDIT SPOTLIGHTS`}</div>
                    </div>
                    <div className={styles.auditFactuality}>
                        <div className={styles.auditFactualityChild} />
                        <div className={styles.inTermsOfContainer}>
                            <p className={styles.inTermsOf}>
                                In terms of auditing generative AI,
                            </p>
                            <p className={styles.factualityIndicates}>
                                <span>‘</span>
                                <i className={styles.factuality}>factuality</i>
                                <span>’ indicates ...</span>
                            </p>
                            <p className={styles.faithfulnessIndicates}>
                                <span>‘</span>
                                <i className={styles.faithfulness}>faithfulness</i>
                                <span>’ indicates ...</span>
                            </p>
                            <p className={styles.harmfulnessIndicates}>
                                <span>‘</span>
                                <i className={styles.harmfulness}>harmfulness</i>
                                <span>’ indicates ...</span>
                            </p>
                            <p className={styles.performanceIndicates}>
                                <span>‘</span>
                                <i className={styles.performance}>performance</i>
                                <span className={styles.indicates}>’ indicates ...</span>
                            </p>
                        </div>
                    </div>
                </div>
                <div className={styles.mLModels}>
                    <div className={styles.modelTypes}>
                        <div className={styles.modelTypesChild} />
                        <div className={styles.discriminativeMl}>Discriminative ML</div>
                        <div className={styles.modelExamples}>
                            <div className={styles.modelsLinearRegressionContainer}>
                                <p
                                    className={styles.modelsLinearRegression}
                                >{`Models: Linear Regression, Logistic Regression, Decision Tree, Support Vector Machines, Naive Bayes, K-Means, KNN, Random Forest, Dimensionality Reduction Algorithms, Gradient Boost & Adaboost, ...`}</p>
                                <p className={styles.blankLine}>&nbsp;</p>
                                <p className={styles.evaluationFairnessExplaina}>
                                    Evaluation: Fairness, Explainability, Performance
                                </p>
                            </div>
                        </div>
                    </div>
                    <div className={styles.modelTypes1}>
                        <div className={styles.modelTypesItem} />
                        <div className={styles.generativeAi}>Generative AI</div>
                        <div className={styles.modelsOpenSourceegLlamaWrapper}>
                            <div className={styles.modelsOpenSourceegLlamaContainer}>
                                <p className={styles.modelsOpenSourceegLlama}>
                                    Models: Open-Source(e.g. Llama-3.2 by META)*, Proprietary(e.g.
                                    GPT-4o by OpenAI)*
                                </p>
                                <p className={styles.apiKeyFor}>
                                    *api key for your model to be audited is required
                                </p>
                                <p className={styles.blankLine1}>&nbsp;</p>
                                <p className={styles.evaluationFactualityFaithf}>
                                    Evaluation: Factuality, Faithfulness, Harmfulness, Performance
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Root1;
