import sys
sys.path.append("C:/Users/User/Documents/Code/Projects/RPA/Portal/server/portal/api/module")


from test_workflow import Test_WorkFlow
import pandas as pd


df = pd.read_excel("C:/Users/User/Documents/Code/Python/RobotFramework/test_docs/Test_1st.xlsx")

df_result = Test_WorkFlow(df)

df_result.to_excel("C:/Users/User/Documents/Code/Python/RobotFramework/test_docs/Test_1st_result.xlsx")

