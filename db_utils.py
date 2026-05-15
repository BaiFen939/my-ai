#注意！请确保你安装了pyodbc库，未安装请点击左上角四条杠打开视图，工具窗口，终端，输入pip install pyodbc进行下载。
import pyodbc
from datetime import datetime,date,timedelta
class MemoryCache:
#这是一个类，是封装好的工具箱，用于将对话暂存于内存中，加快查找
    def __init__(self):
        self._cache={}

    def get(self,user_id,limit=20):
        key=(user_id,limit)
        return self._cache.get(key)

    def set(self,user_id,value,limit=20):
        key=(user_id,limit)
        self._cache[key] = value

    def delete(self,user_id,limit=20):
        key=(user_id,limit)
        if key in self._cache:
            del self._cache[key]

    def update_after_limit(self,user_id,new_item,limit=20):
        key=(user_id,limit)
        if key in self._cache:
            old_item=self._cache[key]
            if len(old_item)>=limit:
                old_item=old_item[:1]
                #删除最早的一条信息
                old_item.append(new_item)
            return True
        return False
cache=MemoryCache()

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
    conn=None
    cursor=None
    try:
        #print(f"【DB插入】user_id={user_id}, speaker={speaker}, content={content[:20]}...")
        #类似上面的都是调试时打印有关数据情况
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO Conversation (User_id,Speaker,Content) VALUES (?,?,?)",(user_id,speaker,content))
        conn.commit()
        new_item=(speaker,content)
        update=cache.update_after_limit(user_id,new_item)
        '''if update!=None:
            print("缓存已更新")
        else:
            print("缓存不存在，下一次查询会加载。")'''
    except Exception as e:
        print("出现错误",e)
    finally:
        if cursor!=None:
            cursor.close()
        if conn!=None:
            conn.close()
'''if __name__=='__main__':
    insert_message('ShuHai','ShuHai','Hellow,Luoli!')
    print("插入完成，请去数据库查看")'''
#以上为数据库的插入(即写入)

def get_recent_conversation(user_id, limit=20):
    conn=None
    cursor=None
    try:
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT TOP(?) Conversation.Speaker,Conversation.Content FROM Conversation WHERE user_id=? ORDER BY TIME DESC",(limit,user_id))
        rows=cursor.fetchall()
        history=[]
        for row in rows:
            history.append((row.Speaker,row.Content))
        return history
    except Exception as e:
        print("出现错误: ",e)
        return []
    finally:
        if cursor!=None:
            cursor.close()
        if conn!=None:
            conn.close()
'''if __name__ == '__main__':
    user_id='ShuHai'
    history=get_recent_conversation(user_id)
    print(f"最近的20条对话：")
    for speaker,content in history:
        print(f"{speaker}:{content}")'''
# 以上为数据库的查询

def get_recent_conversation_cache(user_id, limit=20):
    cached=cache.get(user_id)
    #注意，不能用对一个对象操作的结果覆盖它本身，不然会导致下一次找不到这个对象，报错
    if cached!=None:
        return cached
    result=get_recent_conversation(user_id)
    cache.set(user_id,result)
    return result
#可以进行内存查询和缓存的对话查询

def get_conwersqation_by_date(user_id,target_date):
    conn=None
    cursor=None
    start=datetime.combine(target_date,datetime.min.time())
    end=start+timedelta(days=1)
    try:
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("select Speaker,Content from Conversation where user_id=? and Time>=? and Time<=? ORDER BY TIME ASC",(user_id,start,end))
        rows=cursor.fetchall()
        result=[]
        for row in rows:
            result.append((row.Speaker,row.Content))
        return result
    except Exception as e:
        print(f"查询失败{e}")
        return []
    finally:
        if cursor!=None:
            cursor.close()
        if conn!=None:
            conn.close()
'''if __name__ == '__main__':
    user_id='宿海'
    test_date=date(2026,5,5)
    convos=get_conwersqation_by_date(user_id,test_date)
    print(f"共{len(convos)}条")
    for speaker,content in convos:
        print(f"{speaker}:{content}")'''