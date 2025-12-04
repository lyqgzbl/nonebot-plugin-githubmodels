import datetime
from pathlib import Path


from nonebot.rule import Rule
from nonebot.log import logger
from nonebot import require, get_plugin_config
from azure.ai.inference.models import SystemMessage
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
require("nonebot_plugin_alconna")
require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import md_to_pic
from nonebot_plugin_alconna import UniMessage, on_alconna, Match
from arclet.alconna import Args, Option, Alconna, MultiVar, CommandMeta

from .config import Config
from .openai_handler import OPENAI_Handler
from .context_manager import ContextManager


__plugin_meta__ = PluginMetadata(
    name="GitHub Models",
    description="一个调用 GitHub Models 的 AI 对话插件",
    usage="/AI Hello",
    type="application",
    homepage="https://github.com/lyqgzbl/nonebot-plugin-githubmodels",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)


plugin_config = get_plugin_config(Config)
REPLY_IMAGE = plugin_config.ai_reply_image


if not plugin_config.github_token:
    logger.opt(colors=True).warning("<yellow>缺失必要配置项 'github_token'，" \
    "已禁用该插件</yellow>")
    Openai_Handler = None
else:
    Openai_Handler = OPENAI_Handler(
        api_key=plugin_config.github_token,
        endpoint="https://models.github.ai/inference",
        model_name=plugin_config.ai_model_name,
        max_context_length=plugin_config.max_context_length,
        temperature=plugin_config.ai_temperature,
        top_p=plugin_config.ai_top_p,
    )


def is_enable() -> Rule:
    def _rule() -> bool:
        return bool(plugin_config.github_token)
    return Rule(_rule)


Context_Manager = ContextManager(max_context_length=plugin_config.max_context_length)


ai = on_alconna(
    Alconna(
        "AI",
        Args["user_input?", MultiVar(str)],
        Option("-r|--reset", help_text="重置上下文记忆"),
        Option("-i|--image", help_text="临时启用图片回复"),
        meta=CommandMeta(
            description="AI 对话插件",
            usage=__plugin_meta__.usage,
            example="/AI Hello; /AI -i Hello; /AI -r",
            compact=True,
        ),
    ),
    rule=is_enable(),
    use_cmd_start=True,
    block=True,
    aliases={"ai"},
)


@ai.assign("reset")
async def ai_reset():
    Context_Manager.reset_context()
    await ai.finish("上下文已重置")


@ai.assign("image")
async def ai_image(user_input: Match[tuple[str]]):
    if user_input.available:
        global REPLY_IMAGE
        REPLY_IMAGE = True
        ai.set_path_arg("user_input", " ".join(user_input.result))


@ai.handle()
async def handle_function(user_input: Match[tuple[str]]):
    if user_input.available:
        ai.set_path_arg("user_input", " ".join(user_input.result))


@ai.got_path("user_input", prompt="请输入有效问题")
async def got_location(user_input: str):
    global REPLY_IMAGE
    try:
        messages = [SystemMessage(content="回答尽量简练,请始终用中文回答")]
        Context_Manager.add_message("user", user_input)
        messages += Context_Manager.get_context()
        if Openai_Handler is not None:
            reply = await Openai_Handler.get_response(messages)
        Context_Manager.add_message("assistant", reply)
        if REPLY_IMAGE:
            current_hour = datetime.datetime.now().hour
            is_dark_mode = 18 <= current_hour or current_hour < 6
            css_file = (
                Path(__file__).
                parent / "css" / ("dark.css" if is_dark_mode else "light.css")
            )
            pic = await md_to_pic(md=reply, css_path=str(css_file))
            await UniMessage.image(raw=pic).send(reply_to=True)
        else:
            await UniMessage.text(reply).send(reply_to=True)
    except Exception as e:
        logger.opt(colors=True).error(f"<red>API 请求失败: {e}</red>")
        await ai.send("问题触发了内容过滤策略,请修改问题后重试")
    finally:
        REPLY_IMAGE = plugin_config.ai_reply_image
