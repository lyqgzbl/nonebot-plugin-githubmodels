import nonebot
from openai import OpenAI
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
config = nonebot.get_driver().config
token = config.github_token
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)
shared_context = []
MAX_CONTEXT_LENGTH = 5
AI = on_command("AI", priority=10, block=True)
def summarize_context(context):
    summary = []
    for message in context:
        if len(message["content"]) > 100:
            summary.append({
                "role": message["role"],
                "content": message["content"][:100] + "... (内容简化)"
            })
        else:
            summary.append(message)
    return summary
def trim_context(context):
    user_messages = [msg for msg in context if msg['role'] == 'user']
    assistant_messages = [msg for msg in context if msg['role'] == 'assistant']
    return user_messages[-MAX_CONTEXT_LENGTH:] + assistant_messages[-1:] if assistant_messages else []
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
    trimmed_context = trim_context(shared_context)
    summarized_context = summarize_context(trimmed_context)
    messages = [
        {
            "role": "system",
            "content": "你是一个乐于助人的助手，请始终用中文回答。",
        }
    ] + summarized_context
    try:
        response = client.chat.completions.create(
            messages=messages,
            model=model_name,
            temperature=1,
            max_tokens=1000,
            top_p=1,
        )
        reply = response.choices[0].message.content
        shared_context.append({"role": "assistant", "content": reply})
        await AI.send(reply, reply_message=True)
    except Exception as e:
        await AI.finish(f"请求失败：{str(e)}")

__plugin_meta__ = PluginMetadata(
    name="githubmobile",
    description="API 调用 GitHub Mobile 的 GPT-4o 模型",
    type="application",
    homepage="https://github.com/lyqgzbl/nonebot-plugin-githubmobile",
    supported_adapters={"~onebot.v11"},
    )