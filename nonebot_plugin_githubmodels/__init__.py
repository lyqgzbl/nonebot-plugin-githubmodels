import nonebot
from openai import AsyncOpenAI
from nonebot import on_command, get_plugin_config, require
require("nonebot_plugin_alconna")
require("nonebot_plugin_htmlrender")
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMessage, Image 
from nonebot_plugin_htmlrender import md_to_pic
from .config import Config

plugin_config = get_plugin_config(Config)
TOKEN = plugin_config.github_token 
MODEL_NAME = plugin_config.ai_model_name
MAX_CONTEXT_LENGTH = plugin_config.max_context_length

endpoint = "https://models.inference.ai.azure.com"
client = AsyncOpenAI(
    base_url=endpoint,
    api_key=TOKEN,
)
shared_context = []

AI = on_command("AI", priority=10, block=True)

@AI.handle()
async def handle_function(args: Message = CommandArg()):
    global shared_context
    user_input = args.extract_plain_text().strip()

    if user_input.lower() == "重置":
        shared_context = []
        await AI.finish("上下文已重置")
    
    if not user_input:
        await AI.finish("请输入有效的问题")
    
    shared_context.append({"role": "user", "content": user_input})
    
    if len(shared_context) > MAX_CONTEXT_LENGTH:
        shared_context = shared_context[-MAX_CONTEXT_LENGTH:]
    
    messages = [
        {
            "role": "system",
            "content": "回答尽量简练，请始终用中文回答。",
        }
    ] + shared_context
    
    response = await client.chat.completions.create(
        messages=messages,
        model=MODEL_NAME,
        temperature=1,
        max_tokens=500,
        top_p=1,
    )
    
    reply = response.choices[0].message.content
    shared_context.append({"role": "assistant", "content": reply})


    pic = await md_to_pic(md=reply)
    await UniMessage.image(raw=pic).send(reply_to=True)
		
__plugin_meta__ = PluginMetadata(
    name="githubmodels",
    description="API 调用 GitHub Models 的大语言模型",
    usage="AI",
    type="application",
    homepage="https://github.com/lyqgzbl/nonebot-plugin-githubmodels",
    supported_adapters=None,
)