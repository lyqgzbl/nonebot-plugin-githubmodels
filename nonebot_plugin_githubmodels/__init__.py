import nonebot
from nonebot import require, get_plugin_config
require("nonebot_plugin_alconna")
require("nonebot_plugin_htmlrender")
from openai import AsyncOpenAI
from arclet.alconna import Args, Option, Alconna
from nonebot.plugin import PluginMetadata
from nonebot_plugin_htmlrender import md_to_pic
from nonebot_plugin_alconna import UniMessage, on_alconna, Match
from .config import Config

plugin_config = get_plugin_config(Config)
TOKEN = plugin_config.github_token
MODEL_NAME = plugin_config.ai_model_name
REPLY_IMAGE = plugin_config.ai_reply_image
MAX_CONTEXT_LENGTH = plugin_config.max_context_length

endpoint = "https://models.inference.ai.azure.com"
client = AsyncOpenAI(
    base_url=endpoint,
    api_key=TOKEN,
)
shared_context = []

ai = on_alconna(
    Alconna(
        "AI",
        Args["user_input?", str],
        Option("-r|--reset"),
        Option("-i|--image"),
    ),
    use_cmd_start=True,
    block=True,
    aliases={"ai"},
)

@ai.assign("reset")
async def ai_reset():
    global shared_context
    shared_context = []
    await ai.finish("上下文已重置")

@ai.assign("image")
async def ai_image(user_input: Match[str]):
    if user_input.available:
        global REPLY_IMAGE
        REPLY_IMAGE = True
        ai.set_path_arg("user_input", user_input.result)

@ai.handle()
async def handle_function(user_input: Match[str]):
    if user_input.available:
        ai.set_path_arg("user_input", user_input.result)

@ai.got_path("user_input", prompt="请输入有效问题")
async def got_location(user_input: str):
    if not user_input.strip():
        await ai.reject("你真的输入了有效问题吗?请输入有效问题")
    global shared_context
    shared_context.append({"role": "user", "content": user_input})
    if len(shared_context) > MAX_CONTEXT_LENGTH:
        shared_context = shared_context[-MAX_CONTEXT_LENGTH:]

    messages = [
        {
            "role": "system",
            "content": "回答尽量简练,请始终用中文回答",
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

    if REPLY_IMAGE:
        pic = await md_to_pic(md=reply)
        await UniMessage.image(raw=pic).send(reply_to=True)
    else:
        await UniMessage.text(reply).send(reply_to=True)

__plugin_meta__ = PluginMetadata(
    name="githubmodels",
    description="API 调用 GitHub Models 的大语言模型",
    usage="AI",
    type="application",
    homepage="https://github.com/lyqgzbl/nonebot-plugin-githubmodels",
    supported_adapters=None,
)
