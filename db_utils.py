#注意！请确保你安装了pyodbc库，未安装请点击左上角四条杠打开视图，工具窗口，终端，输入pip install pyodbc进行下载。
import pyodbc
def get_connection():
    conn_str = (
        r'Driver={ODBC Driver 17 for SQL Server};'
        r'Server=(localdb)\MSSQLLocalDB;'                      #这是我的数据库名，看一下是否一致
        r'Database=LuoliMemory;'                               #这是我的数据库名，记得改
        r'Trusted_Connection=yes;'
    )
    conn=pyodbc.connect(conn_str)
    return conn
'''if __name__ == '__main__':                                  这是测试程序，把这行字和首尾各三个'删了就能测试了
    try:
        conn=get_connection()
        print("数据库连接成功！")
        conn.close()
    except Exception as e:
        print("连接失败：".e)'''
#以上为连接数据库

def insert_message(user_id,speaker,content):
        #print(f"【DB插入】user_id={user_id}, speaker={speaker}, content={content[:20]}...")
        #类似上面的都是调试时打印有关数据情况
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO Conversation (User_id,Speaker,Content) VALUES (?,?,?)",(user_id,speaker,content))
        conn.commit()
        cursor.close()
        conn.close()
'''if __name__=='__main__':                                    这是测试程序，把这行字和首尾各三个'删了就能测试了
    insert_message('ShuHai','ShuHai','Hellow,Luoli!')
    print("插入完成，请去数据库查看")'''
#以上为数据库的插入(即写入)

def get_recent_conversation(user_id, limit=15):                #limit是检索的对话条数，你可以自己改，但太多会很慢
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT TOP(?) Conversation.Speaker,Conversation.Content FROM Conversation WHERE user_id=? ORDER BY TIME DESC",(limit,user_id))
    rows=cursor.fetchall()
    history=[]
    for row in rows:
        history.append((row.Speaker,row.Content))
    return history
    cursor.close()
    conn.close()
'''if __name__ == '__main__':                                  这是测试程序，把这行字和首尾各三个'删了就能测试了
    user_id='ShuHai'
    history=get_recent_conversation(user_id)
    print(f"最近的20条对话：")
    for speaker,content in history:
        print(f"{speaker}:{content}")'''
# 以上为数据库的查询