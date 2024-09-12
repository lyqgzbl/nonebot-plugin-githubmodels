import nonebot
from openai import OpenAI
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

config = nonebot.get_driver().config
token = config.github_token
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)
shared_context = []
MAX_CONTEXT_LENGTH = 20  # 设置上下文最大保留条数
AI = on_command("AI", priority=10, block=True)

@AI.handle()
async def handle_function(args: Message = CommandArg()):
    global shared_context
    user_input = args.extract_plain_text().strip()
    if user_input.lower() == "重置":
        shared_context = []
        await AI.finish("上下文已重置。请开始新的对话。")
    if not user_input:
        await AI.finish("请输入有效的问题。")
    
    shared_context.append({"role": "user", "content": user_input})
    
    # 保持上下文列表的最大长度
    if len(shared_context) > MAX_CONTEXT_LENGTH:
        shared_context = shared_context[-MAX_CONTEXT_LENGTH:]
    
    messages = [
        {
            "role": "system",
            "content": "回答尽量简练，请始终用中文回答。",
        }
    ] + shared_context
    response = client.chat.completions.create(
        messages=messages,
        model=model_name,
        temperature=1,
        max_tokens=500,
        top_p=1,
    )
    reply = response.choices[0].message.content
    shared_context.append({"role": "assistant", "content": reply})
    
    # 保持上下文列表的最大长度
    if len(shared_context) > MAX_CONTEXT_LENGTH:
        shared_context = shared_context[-MAX_CONTEXT_LENGTH:]
    
    await AI.send(reply, reply_message=True)

__plugin_meta__ = PluginMetadata(
    name="githubmodels",
    description="API 调用 GitHub Models 的 GPT-4o 模型",
    usage="AI",
    type="application",
    homepage="https://github.com/lyqgzbl/nonebot-plugin-githubmodels",
    supported_adapters={"~onebot.v11"},
)