import discord
from discord.ext import commands
from version_manager import VersionManager
from datetime import datetime, timedelta

version_manager = VersionManager('version.txt', 'commit_hash.txt')

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
app = commands.Bot(intents=intents, command_prefix='!') # 봇 커맨드 설정

async def help():
    version_manager.check_commit()
    version = f'{version_manager.major_version}.{version_manager.minor_version}'

    embed = discord.Embed(title="도움말", description="급식이#2677 도움말입니다.", timestamp=datetime.now(), color=0x5CA182)

    embed.add_field(name="테스트 도움말 메시지", value="value", inline=False)
    embed.add_field(name=
"명령어 목록", value="""
!gr : menu_rating()
!vd : logger.debug(vote_dict)
!급식 : menu_notice()
!vwpk : View vote_results.pkl
!vwspk : View suggestions.pkl
!send_result : Send results.txt
!list_results : Send results.txt list
!list_results : Reset vote_results.pkl
!stop : Stop Bot
!addnote: 패치 노트에 내용 추가
!readnote: 패치 노트 내용 읽기
!delnote: 패치 노트 내용 삭제"""
                    , inline=True)

    embed.set_author(name="급식이#2677", icon_url="https://cdn.discordapp.com/attachments/816942503734542368/877543719132364850/web_hi_res_512.png")
    embed.set_footer(text="Bot Made by 완두콩#8795", icon_url="https://media.discordapp.net/attachments/876805711181516852/877558099983077386/Bean256p.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/816942503734542368/877543719132364850/web_hi_res_512.png")

    embed.add_field(name="버전", value=version + " Beta", inline=False)
    return embed
