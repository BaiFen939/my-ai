#注意！请确保你安装了requests库，未安装请点击左上角四条杠打开视图，工具窗口，终端，输入pip install requests进行下载。
import requests
def ask_luoli(prompt):
    url = "http://localhost:11434/api/generate"                          #这是我的ai的地址，记得改
    payload = {
        "model": "luoli",                                                #模型名字，改成自己的模型名
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url,json=payload,timeout=45)
        if response.status_code == 200:
            result = response.json()
            return result.get("response"," ")
        else:
            return f"洛璃开小差去了，请求失败，状态码{resp.status_code}"
    except Exception as e:
        return f"调用出错：{e}"
'''if __name__=="__main__":                                             这是测试程序，把这行字和首尾各三个'删了就能测试了
    reply = ask_luoli("你好，洛璃！")
    print("洛璃说: ",reply)'''