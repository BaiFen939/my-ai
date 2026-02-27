#这是聊天主文件
from db_utils import get_recent_conversation,insert_message
from ai_utils import ask_luoli

USER_ID = '宿海'
#以下是ai人设，这里为了后续反应速度，简写了
SYSTEM_PROMPT = """
你是洛璃，我的聊天朋友，活泼友善并关心我。
"""

def main():
    print("开始聊天吧！")
    while True:
        user_input = input("\n你说: ").strip()                                    #这里的input相当于C中的scanf
        if user_input.lower() == "exit":                                         #input.lower()把输入转换为小写
            print("拜拜，下次在聊。")
            break
        if not user_input:                                                       #若输入为空，重新循环
            continue                                                             #以上为聊天的循环

        history = get_recent_conversation(USER_ID)
        #print(f"调试: 取到{len(history)}条历史")                                   #这里类似的都是调试时打印有关数据情况
        context = ""
        for speaker,content in history:
            context = context + f"{speaker}: {content}\n"
        prompt = f"{SYSTEM_PROMPT}\n{context}用户:{user_input}\n洛璃: "            #把ai的名字改掉，用你自己的
        #print(f"调试:prompt 长度{len(prompt)},前100字: {prompt[:100]}")
                                                                                 #到这里是调用历史，拼接成对话

        #print("调试:正在调用 ask_luoli...")
        reply = ask_luoli(prompt)                                                #到这里是调用回复
        #print(f"调试: ask_luoli返回了，repr(reply) = {repr(reply)}")

        print(f"洛璃: {reply}")                                                   #输出回复

        insert_message(USER_ID,'user',user_input)
        #print(f"【准备存储洛璃】reply={repr(reply)}")
        insert_message(USER_ID,'assistant',reply)
        #print("调试: 对话已储存")
if __name__ == "__main__":
    main()

