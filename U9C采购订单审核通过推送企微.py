import pyodbc
import requests

# =========================
# SQL Server 配置
# =========================
server = "192.168.92.133"
database = "U9C"
username = "sa"
password = "Aa123456"

# =========================
# 企业微信 Webhook
# =========================
webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=bca6e236-1b03-4a6e-a3d4-bca945121528"

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "TrustServerCertificate=yes;"
)

try:
    # 连接数据库
    conn = pyodbc.connect(conn_str, timeout=10)
    cursor = conn.cursor()

    # 查询最近一张已核准采购订单
    cursor.execute("""
        SELECT TOP 1
            ID,
            DocNo,
            Status,
            ApprovedBy,
            ApprovedOn,
            Supplier_shortName
        FROM PM_PurchaseOrder
        WHERE Status = 2
        ORDER BY ApprovedOn DESC
    """)

    row = cursor.fetchone()
    conn.close()

    if row:
        message = f"""【采购订单审核通知】

采购订单号：{row.DocNo}
审核状态：已核准
审核人：{row.ApprovedBy}
审核时间：{row.ApprovedOn}
供应商名称：{row.Supplier_shortName}
"""

        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }

        response = requests.post(
            webhook,
            json=data,
            timeout=10
        )

        print("企业微信返回：")
        print(response.text)

    else:
        print("没有找到已核准的采购订单")

except Exception as e:
    print("发生错误：")
    print(e)