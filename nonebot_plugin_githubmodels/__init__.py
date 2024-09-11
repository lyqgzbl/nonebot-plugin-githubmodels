import nonebot
from openai import OpenAI
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
# 获取配置
config = nonebot.get_driver().config
token = config.github_token
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

# 初始化 OpenAI 客户端
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# 上下文共享
shared_context = []
MAX_CONTEXT_LENGTH = 20  # 最大保留的上下文数量

# 定义 Nonebot 命令
AI = on_command("AI", priority=10, block=True)

@AI.handle()
async def handle_function(args: Message = CommandArg()):
    global shared_context
    user_input = args.extract_plain_text().strip()

    # 重置上下文
    if user_input.lower() == "重置":
        shared_context = []
        await AI.finish("上下文已重置。请开始新的对话。")

    # 检查用户输入是否有效
    if not user_input:
        await AI.finish("请输入有效的问题。")

    # 添加用户输入到上下文
    shared_context.append({"role": "user", "content": user_input})

    # 保留最新的 MAX_CONTEXT_LENGTH 条对话记录
    if len(shared_context) > MAX_CONTEXT_LENGTH:
        shared_context = shared_context[-MAX_CONTEXT_LENGTH:]

    # 准备发送给模型的消息
    messages = [
        {
            "role": "system",
            "content": "只使用中文回答。回答尽量简练。",
        }
    ] + shared_context

    # 调用 OpenAI 接口进行对话生成
    try:
        response = client.chat.completions.create(
            messages=messages,
            model=model_name,
            temperature=1,
            max_tokens=500,
            top_p=1,
        )
        # 获取助手的回复
        reply = response.choices[0].message.content

        # 将助手的回复添加到上下文
        shared_context.append({"role": "assistant", "content": reply})

        # 发送回复
        await AI.send(reply, reply_message=True)
    except Exception as e:
        # 错误处理
        await AI.finish(f"请求失败：{str(e)}")

__plugin_meta__ = PluginMetadata(
    name="githubmodels",
    description="API 调用 GitHub Models 的 GPT-4o 模型",
    usage="AI",
    type="application",
    homepage="https://github.com/lyqgzbl/nonebot-plugin-githubmodels",
    supported_adapters={"~onebot.v11"},
    )