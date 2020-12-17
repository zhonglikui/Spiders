import configparser
from jqdatasdk import *
from pandas.core.frame import DataFrame
import pandas as pd

config = configparser.ConfigParser()
config.sections()
config.read("../config.ini")
name = config.get("jqdata", "name")
password = config.get("jqdata", "password")
# print("账号信息{}:{}".format(name,password))
auth(name, password)
print("登录状态{},剩余查询条数{}".format(is_auth(), get_query_count()))
df=get_concepts()
df.to_excel("股票概念.xls")
print(df)
# type = "股票型"
key = "医疗"
# df = finance.run_query(
#     query(finance.FUND_MAIN_INFO).filter(finance.FUND_MAIN_INFO.underlying_asset_type == type).limit(2100))
dfK = df["name"].str.contains(key)
dfAll = df.loc[dfK]
print(dfAll)
# dfAll.to_excel("基金.xls")
for row in dfAll.itertuples():
    code=getattr(row,"Index")
    name=getattr(row,"name")
    stock= get_concept_stocks(code, date=None)
    child=DataFrame(stock)
    print(child)
    fileName="{}-{}.xls".format(name,code)
    child.to_excel(fileName)
#     q = query(finance.FUND_PORTFOLIO_STOCK).filter(finance.FUND_PORTFOLIO_STOCK.code == getattr(row, "main_code")).order_by(
#         finance.FUND_PORTFOLIO_STOCK.pub_date.desc()).limit(500)
#     df = finance.run_query(q)
#     child = finance.run_query(q)
#     fileName="{}-{}.xls".format(getattr(row, "name"),getattr(row, "main_code"))
#     child.to_excel(fileName)
