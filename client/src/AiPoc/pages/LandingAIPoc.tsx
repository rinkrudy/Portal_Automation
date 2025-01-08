import { FunctionComponent } from "react";
import CategoryCombination from "../components/CategoryCombination";
import styles from "../styles/Landing.module.css";

export interface IFrame2Props {
    className?: string;
}

const LandingAIPoc: FunctionComponent<IFrame2Props> = ({ className = "" }) => {
    console.log("landing")
    return (
        <div className={[styles.root, className].join(" ")}>
            <section className={styles.landingFrame}>
                <div className={styles.projectDetails}>
                    <div className="container two-columns">
                        <h3 className={styles.projectName}>Project Name</h3>
                        <h3 className={styles.administrator}>Administrator</h3>
                    </div>
                    <div className={styles.frameParent}>
                        <div className={styles.combinedNamesWrapper}>
                            <div className={styles.combinedNames}>
                                <input
                                    className={styles.nameCombination}
                                    placeholder="Project Name"
                                    type="text"
                                />
                                <input
                                    className={styles.nameCombination1}
                                    placeholder="Adminstrator Name"
                                    type="text"
                                />
                            </div>
                        </div>
                        <div className={styles.datasetSelection}>
                            <div className={styles.benchmarkSelection}>
                                <div className={styles.datasetOptions}>
                                    <h3 className={styles.selectAiBenchmark}>
                                        Select AI Benchmark Dataset
                                    </h3>
                                </div>
                                <div className={styles.benchmarkList}>
                                    <div className={styles.benchmarkCategories}>
                                        <CategoryCombination
                                            faithEval="FaithEval"
                                            faithfulness="Faithfulness"
                                            salesforceAIResearch="Salesforce AI Research"
                                        />
                                        <div className={styles.categoryCombination}>
                                            <div className={styles.categoryCombinationChild} />
                                            <div className={styles.agentharmParent}>
                                                <div className={styles.agentharm}>AgentHarm</div>
                                                <div className={styles.div}>?</div>
                                            </div>
                                            <div className={styles.categoryCombinationInner}>
                                                <div className={styles.harmfulnessParent}>
                                                    <h1 className={styles.harmfulness}>Harmfulness</h1>
                                                    <div className={styles.redTeamingType}>
                                                        <div className={styles.withSingleTurnRedTeaming}>
                                                            with Single-Turn Red-Teaming
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className={styles.aiSafetyInstituteukWrapper}>
                                                <div className={styles.aiSafetyInstituteuk}>
                                                    AI Safety Institute(UK)
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <CategoryCombination
                                        categoryCombinationFlex="unset"
                                        categoryCombinationMinWidth="unset"
                                        faithEval="KC-Exclusive"
                                        faithEvalDisplay="inline-block"
                                        faithEvalMinWidth="80px"
                                        faithfulness="Custom"
                                        salesforceAIResearch={`K&C AI IT System Center`}
                                        salesforceAIResearchDisplay="unset"
                                        salesforceAIResearchMinWidth="unset"
                                    />
                                </div>
                            </div>
                            <div className={styles.aPIKeyInput}>
                                <div className={styles.aPIKeyFieldWrapper}>
                                    <div className={styles.aPIKeyField}>
                                        <h3 className={styles.enterYourModel}>
                                            Enter Your Model API Key
                                        </h3>
                                        <div className={styles.aPI}>?</div>
                                    </div>
                                </div>
                                <input
                                    className={styles.yourAPIKey}
                                    placeholder="Your API KEY"
                                    type="text"
                                />
                            </div>
                        </div>
                        <div className={styles.clearButton}>
                            <button className={styles.rectangleParent}>
                                <div className={styles.frameChild} />
                                <div className={styles.clear}>CLEAR</div>
                            </button>
                        </div>
                    </div>
                </div>
                <button className={styles.runButton}>
                    <div className={styles.runButtonChild} />
                    <div className={styles.run}>RUN</div>
                </button>
            </section>
        </div>
    );
};

export default LandingAIPoc;