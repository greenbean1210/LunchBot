'''

Made by:
[GREENBEAN]
    ___       ___       ___       ___       ___       ___       ___       ___       ___   
   /\  \     /\  \     /\  \     /\  \     /\__\     /\  \     /\  \     /\  \     /\__\  
  /::\  \   /::\  \   /::\  \   /::\  \   /:| _|_   /::\  \   /::\  \   /::\  \   /:| _|_ 
 /:/\:\__\ /::\:\__\ /::\:\__\ /::\:\__\ /::|/\__\ /::\:\__\ /::\:\__\ /::\:\__\ /::|/\__\
 \:\:\/__/ \;:::/  / \:\:\/  / \:\:\/  / \/|::/  / \:\::/  / \:\:\/  / \/\::/  / \/|::/  /
  \::/  /   |:\/__/   \:\/  /   \:\/  /    |:/  /   \::/  /   \:\/  /    /:/  /    |:/  / 
   \/__/     \|__|     \/__/     \/__/     \/__/     \/__/     \/__/     \/__/     \/__/  

   

성지고등학교 급식 메뉴 정보를 제공하고, 학생들이 직접 급식에 대한 의견을 제공할 수 있는
디스코드 봇 "급식이" 파이썬 코드.


'''


# Module 임포트
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from pytz import timezone
from version_manager import VersionManager
import os
import pickle
import sys

# 로그 모듈
import logging
import colorlog

# 
# from Lunch_info import get_menu_info
from Token_info import get_token
from Help import help
from Menu_info import get_menu_info


version_manager = VersionManager('version.txt', 'commit_hash.txt')


intents = discord.Intents.all()
intents.typing = False
intents.presences = False

app = commands.Bot(intents=intents, command_prefix='!') # 봇 커맨드 설정
app.remove_command("help")

token = get_token()

# 딕셔너리 선언
vote_dict = {}  # 투표 결과를 저장할 딕셔너리
user_votes = {}  # 각 사용자의 투표 상태. {user_id: {message_id: emoji}} 형태

today_menu = []
today_allergens = []
yesterday_menu_info = None


# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------**로그 설정**-----------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------

# 로그 레벨과 메시지를 출력하는 포맷터 생성
formatter = colorlog.ColoredFormatter("%(log_color)s[%(levelname)s] %(message)s")


# 스트림 핸들러 생성 및 포맷터 설정
stream = logging.StreamHandler()
stream.setFormatter(formatter)

# 로거 생성 및 핸들러 추가
logger = colorlog.getLogger('Logger')
logger.addHandler(stream)
logger.setLevel(logging.DEBUG)


# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------




# 정의되지 않은 명령어를 전송할 경우 오류 처리 코드
@app.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    



# 봇 시작 로그
logger.info(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
logger.info("봇을 시작합니다.")
logger.info("로딩 중...")




# 봇 시작
@app.event
async def on_ready():
    logger.info(f"다음 봇이 시작되었습니다: {app.user.name}")
    # logger.info(app.user.name)
    logger.info(f"ID: {app.user.id}") 
    # logger.info(app.user.id)
    logger.info("------------------------------------")
    game = discord.Game("오늘의 급식 정보를 알려 드립니다!")
    await app.change_presence(activity=game)
    scheduler.start()

@app.event
async def on_member_join(member):
    role_id = 1179309457914732564  # 역할의 고유 ID 입력
    role = discord.utils.get(member.guild.roles, id=role_id)
    if role is not None:
        await member.add_roles(role)
        print(f'{member}에게 역할 부여 완료')
    else:
        print('역할을 찾을 수 없습니다.')

@app.command()
async def versioncheck(ctx):
    version_manager.check_commit()  # 커밋 확인

# 급식 정보 보내기
async def menu_notice():
    # now = datetime.now()
    # next_run_time = now + timedelta(days=1)
    # scheduler.add_job(menu_notice, 'date', run_date=next_run_time)
    today_menu_list, today_allergens__list = get_menu_info()
    
    today_menu = '\n'.join(today_menu_list)
    today_allergens = '\n'.join(today_allergens__list)
    channel = app.get_channel(1144834533200498738)

    embed = discord.Embed(title="🍚 오늘의 급식", description=today_menu, color=0xFFFFFF)
    # embed.add_field(name=today_menu, value="", inline=False)
    
    await channel.send(embed=embed)


# 급식 정보 보내기
async def menu_allergies(ctx):
    today_menu_list, today_allergens__list = get_menu_info()
    
    today_menu = '\n'.join(today_menu_list)
    today_allergens = ', '.join(today_allergens__list)

    # channel = app.get_channel(1144834533200498738)
    channel = ctx
    embed = discord.Embed(title="알레르기 정보", description=today_allergens, color=0xFFFFFF)
    # embed.add_field(name=today_menu, value="", inline=False)
    
    await channel.send(embed=embed)





# 급식 의견 받기
async def menu_rating():
    global vote_dict  # 전역 변수 사용
    global yesterday_menu_info


    # 현재 날짜와 시간 가져오기
    now = datetime.now()
    date_str = datetime.now().strftime('%Y%m%d')

    try:
        # 현재 스크립트 파일의 절대 경로를 구하고, 그 경로에서 디렉토리 부분만 추출
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # 결과 저장 디렉토리 설정
        result_dir = os.path.join(script_dir, 'results')

        # 결과 저장 파일 경로 설정
        result_file_path = os.path.join(result_dir, f'results_{date_str}.txt')

    except Exception as e:
        logger.error(f"저장 디렉토리 설정 중 에러: {e}")

    

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    if now.strftime("%a").lower() != "sat": # 토요일이 아닐 경우 실행(토요일은 급식이 없음)
        channel = app.get_channel(1144834533200498738)
        logchannel = app.get_channel(1144838499472789604)
        today_menu_list, today_allergens__list = get_menu_info()
        today_menu = '\n'.join(today_menu_list)
        embed = discord.Embed(title="🤔 오늘의 급식은 어떠셨나요?", description="오늘의 급식에 대해 알려주세요.", color=0xFFFFFF)
        embed.add_field(name="오늘의 급식이 뭐였냐면...", value=today_menu, inline=False)
        embed.add_field(name="아래의 이모지를 눌러주세요.", value="하나만 누를 수 있습니다.", inline=False)


        msg = await channel.send(embed=embed)

        # 이모지 추가
        emojis = ['👍', '👎']  # 좋아요와 싫어요 이모지 사용
        for emoji in emojis:
            await msg.add_reaction(emoji)
    
    
    if now.strftime("%a").lower() != "mon" and now.strftime("%a").lower() == "sat": # 월요일이 아닐 경우, 토요일일 경우 실행(월요일은 전날의 결과가 없고 토요일은 전날인 금요일의 결과를 알려줘야 함)
        # 전날의 결과 저장
        try: 
            pkl_file_path = os.path.join(os.path.dirname(__file__), 'vote_result.pkl')

            logger.debug(f"다음 경로의 파일을 엽니다... {pkl_file_path}")
            results_text= "" #results_text 초기화

            with open(pkl_file_path, 'rb') as f:  
                data = pickle.load(f)
                results_text= "투표 결과:\n"

                # 오늘의 급식 메뉴 추가 
                results_text += f"메뉴: \n{yesterday_menu_info}"

                # 아무도 투표하지 않은 경우
                if not data:
                    results_text += "\n어제는 아무도 투표하지 않았습니다."

                # 누군가는 투표했을 경우
                else:
                    for message_id,result in data.items(): 
                        logger.info("메시지 객체를 얻습니다...")
                        # 메시지 객체 얻기
                        try:
                            message = await channel.fetch_message(message_id)

                        except discord.NotFound:
                            logger.error(f"ID {message_id}의 메시지를 찾을 수 없습니다.")

                        except discord.Forbidden:
                            logger.error(f"ID {message_id}의 메시지에 접근할 권한이 없습니다.")

                        except Exception as e:
                            logger.error(f"메시지 정보 가져오는 중 오류: {e}")
            
                        # 서울 시간대로 변경하기
                        seoul_time = message.created_at.astimezone(timezone('Asia/Seoul'))

                        # 원하는 형식의 문자열로 변환하기
                        formatted_time = seoul_time.strftime('%Y-%m-%dT%H:%M:%S')

                        results_text += f"\n날짜: {formatted_time}\n\n"
                    


                    try:
                        for emoji, count in result.items():
                            results_text += f"{emoji}: {count} 개\n"

                    except discord.errors.NotFound:
                        results_text= f"투표 결과를 찾을 수 없습니다. id: {message_id}"
                        await loggererror(f"투표 메시지를 찾을 수 없습니다. 메시지가 삭제되지 않았는지 확인해보세요. id: {message_id}", logchannel)

                    except Exception as e:
                        await loggererror(f"메시지 정보 가져오는 중 오류: {e}", logchannel)

                    
            # 특정 채널의 메시지 정보가 담긴 파일이 있다면 그 내용을 추가합니다.
            suggestions_file_path = os.path.join(os.path.dirname(__file__), 'suggestions.pkl')
            try:
                with open(suggestions_file_path, 'rb') as msg_file:
                    messages = pickle.load(msg_file)

                    results_text += "건의사항:\n"
                    for msg in messages:  # 각각의 메시지 정보를 추가합니다.
                        results_text += msg + "\n"

            except Exception as e:
                    logger.error(f"건의사항 불러오기 중 에러: {e}")


            try:
                with open(result_file_path, 'w', encoding='utf-8') as f:
                    logger.debug(results_text)
                    f.write(results_text)
                    logger.info("쓰기 완료")
            except Exception as e:
                logger.error(f"파일 쓰기 중 에러: {e}")

            
        
            try:
                await logchannel.send(file=discord.File(result_file_path))
                logger.info("logchannel 전송 완료")
                
            except discord.Forbidden:
                await logchannel.send("전날의 투표 결과를 보낼 수 없습니다.\n메시지 전송 권한을 확인해주세요.")

            except Exception as e:
                logger.error(f"파일 전송 중 에러: {e}")
                
        except Exception as e: 
            await embedwarning(e)

        # 'vote_result.pkl' 초기화하기 
        with open(os.path.join(os.path.dirname(__file__), 'vote_result.pkl'), 'wb') as f:
            pickle.dump({}, f)
            pickle.dump({}, f)
            logger.info("vote_result.pkl 초기화 성공.")
            vote_dict = {} # vote_dict 초기화

        with open(os.path.join(os.path.dirname(__file__), 'suggestions.pkl'), 'wb') as f:
            pickle.dump([], f)
            pickle.dump([], f)
            logger.info("suggestions.pkl 초기화 성공.")

        yesterday_menu_info = get_menu_info()

            





 

# 정기적으로 상태를 로깅하는 함수
def log_status():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{current_time}] 정상 작동 중")


# 스케줄러 설정
scheduler = AsyncIOScheduler(timezone='Asia/Seoul')

scheduler.add_job(menu_notice, 'cron', day_of_week='mon-fri', hour=8, minute=50, id="menu_notice") # 8시 50분 급식 메뉴 알림
scheduler.add_job(menu_rating, 'cron', day_of_week='mon-sat', hour=13, minute=50, id="menu_rating") # 1시 50분 급식 평가 알림
scheduler.add_job(log_status, 'cron', minute=0) # "생존신고"



# 테스트 코드
@app.command(pass_context=True)
async def 급식(ctx, *, args=None):
    await menu_notice()

@app.command(pass_context=True)
async def 알레르기(ctx, *, args=None):
    await menu_allergies(ctx)
    
@app.command(pass_context=True)
async def gr(ctx, *, args=None):
    logger.debug("VBBB")
    await menu_rating()
    logger.debug("dsdsadsds")

@app.command(pass_context=True)
async def vd(ctx, *, args=None):
    logger.debug(vote_dict)

@app.command()
async def delnotice(ctx):
    try:
        for job_id in ['menu_notice', 'menu_rating']:
            job = scheduler.get_job(job_id)
            if job and job.next_run_time.date() == datetime.now().date():
                scheduler.remove_job(job_id)

        embedinfo("오늘의 알림이 취소되었습니다.")
    except Exception as e:
        embedwarning("오류: " + e)
    
# 테스트 코드
@app.event
async def on_message(message):
    await app.process_commands(message)

    if message.author.bot:
        return None

    messages = []
    
    if message.channel.id == 1145255799040528506:
        logger.debug("건의사항 감지됨")
        content = message.content
        author = message.author.name
        timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")

        msg_info = f"{timestamp} - {author}: {content}"
    
        file_path = os.path.join(os.path.dirname(__file__), 'suggestions.pkl')

        try:
            
            # logger.debug(f"Current working directory: {cwd}")
            # logger.debug(f"Absolute file path: {abs_filename}")

            # 기존의 메시지가 담긴 리스트를 불러옵니다.
            if os.path.exists(file_path):
                with open(os.path.join(os.path.dirname(__file__), file_path), 'rb') as f:
                    messages = pickle.load(f)

            # 새로운 메시지 추가 전 후 상태 출력
            logger.debug(f"Messages before append: {messages}")
            messages.append(msg_info)
            logger.debug(f"Messages after append: {messages}")

            # 변경된 리스트를 다시 저장합니다.
            with open(os.path.join(os.path.dirname(__file__), file_path), 'wb') as f:
                pickle.dump(messages, f)
                
        except Exception as e:  # 모든 예외 타입을 잡기 위해 가장 상위의 Exception 클래스 사용
            logger.error(f"Error occurred: {e}")  # 오류 메시지 로깅





    if message.content == "급식 평가":
        # await message.channel.send(f"{message.author.mention}님, 안녕하세요!")
        channel = app.get_channel(1144834533200498738)
    
    
        embed = discord.Embed(title="🤔 오늘의 급식은 어떠셨나요?", description="오늘의 급식에 대해 알려주세요.", color=0x00ff00)
        embed.add_field(name="오늘의 급식이 뭐였냐면...", value=get_menu_info(timezone('Asia/Seoul')), inline=False)
        embed.add_field(name="아래의 이모지를 눌러 알려주세요.", value="한 번만 눌러 주세요.\n너무 빠르게 여러 번 누를 경우\n오류가 발생할 수 있습니다.", inline=False)


        embed.set_author(name="급식이#2677", icon_url="https://cdn.discordapp.com/attachments/816942503734542368/877543719132364850/web_hi_res_512.png")
        embed.set_footer(text="Bot Made by 완두콩#8795", icon_url="https://media.discordapp.net/attachments/876805711181516852/877558099983077386/Bean256p.png")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/816942503734542368/877543719132364850/web_hi_res_512.png")

        msg = await channel.send(embed=embed)

        # 이모지 추가
        emojis = ['👍', '👎']  # 예제로 좋아요와 싫어요 이모지 사용
        for emoji in emojis:
            await msg.add_reaction(emoji)














# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------**이벤트 처리**----------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------











# 급식 평가에 반응이 추가된 경우
@app.event
async def on_reaction_add(reaction, user):
    # logger.debug("on_reaction_add called")
    try:
        if user.bot:
            return None

        if user == app.user:
            return

        message = reaction.message

        # 현재 시각과 메시지 생성 시각 사이의 차이를 계산
        diff = datetime.now(timezone('UTC')) - message.created_at

        # 메세지가 만들어진지 24시간 이상 지났다면
        if diff.total_seconds() > 24 * 60 * 60:
            # 사용자의 이모지 반응을 제거합니다.
            await reaction.remove(user)
            return   # 아무것도 하지 않고 함수 반환

        emoji = str(reaction.emoji)

        # vote_dict 초기화
        if reaction.message.id not in vote_dict:
            vote_dict[reaction.message.id] = {}

        # 이미 해당 이모지에 투표한 경우 아무런 동작도 수행하지 않음
        if user.id in user_votes and reaction.message.id in user_votes[user.id] and emoji == user_votes[user.id][reaction.message.id]:
            return
        
        # 이미 다른 이모지에 투표한 경우 해당 반응을 제거한다.
        if user.id in user_votes and reaction.message.id in user_votes[user.id] and user_votes[user.id][reaction.message.id] != emoji:
            return await reaction.remove(user)

        # 사용자의 투표 상태 업데이트
        user_votes.setdefault(user.id, {})[reaction.message.id] = emoji

        # 투표 결과 업데이트 및 저장
        vote_dict[reaction.message.id][emoji] = vote_dict[reaction.message.id].get(emoji, 0) + 1

        with open(os.path.join(os.path.dirname(__file__), 'vote_result.pkl'), 'wb') as f:
            pickle.dump(vote_dict, f)
    except Exception as e:
        logger.error(f"on_reaction_add 실행 중 예외 발생: {e}")
    #logger.debug("on_reaction_add 성공")



# 반응이 삭제된 경우
@app.event
async def on_reaction_remove(reaction, user):
    if (user.bot or 
        not reaction.message.id in vote_dict or 
        not str(reaction) in vote_dict[reaction.message.id]):
        return None

    emoji = str(reaction.emoji)

    # 현재 제거된 반응이 사용자의 선택이었다면 결과 갱신.
    if user.id in user_votes and reaction.message.id in user_votes[user.id] and user_votes[user.id][reaction.message.id] == emoji:
        del vote_dict[reaction.message.id][emoji]
        
        # 여기서도 사용자의 투표 상태 업데이트
        del user_votes[user.id][reaction.message.id]

        if len(vote_dict[reaction.message.id]) == 0: 
            del vote_dict[reaction.message.id]
         
        with open(os.path.join(os.path.dirname(__file__), 'vote_result.pkl'), 'wb') as f:
            pickle.dump(vote_dict,f)




@app.command()
async def 도움말(ctx):
    try:
        embed = await help()
        ping = (round(app.latency * 1000))
        embed.add_field(name="Ping", value="`{}`ms".format(ping), inline=True)
        await ctx.channel.send (embed=embed)
    except Exception as e:
        print(e)



# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------**디버그 코드**----------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------


@app.command()
async def vwpk(ctx):
    await loggerwarning("vwpk 명령어가 사용되었습니다.", ctx)
    logger.debug("pickle 파일 내부 데이터를 출력합니다.")
    # 'vote_result.pkl' 파일 열기
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'vote_result.pkl')
        logger.debug(f"Trying to open file at {file_path}")  # Add this line
        with open(file_path, 'rb') as f:
            # pickle로 데이터 로드
            data = pickle.load(f)

    except FileNotFoundError:
        await loggerwarning("Pickle 파일을 찾을 수 없습니다.", ctx)
        logger.debug("현재 디렉토리:" + os.getcwd())
        return

    if not data:  # data가 비어있다면,
        await loggerwarning("Pickle 파일 내부에 데이터가 존재하지 않습니다.", ctx)
        return

    senddata = ''  # 빈 문자열로 초기화
    for key, value in data.items():
        
        logger.debug(f'{key}: {value}')

        new_data = f'{key}: {value}\n'
        
        if len(senddata + new_data) > 2000:   # Discord message length limit.
            await ctx.send(senddata)
            senddata = new_data   # Reset senddata with the current entry.
            
        else:
            senddata += new_data
        
    if senddata:   # Send any remaining data.
       await ctx.send(senddata)


       
@app.command()
async def vwspk(ctx):
    await loggerwarning("vwspk 명령어가 사용되었습니다.", ctx)
    logger.debug("pickle 파일 내부 데이터를 출력합니다.")
    file_path = os.path.join(os.path.dirname(__file__), 'suggestions.pkl')
    logger.debug(f"Trying to open file at {file_path}")  # Add this line
    try:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                messages = pickle.load(f)
                await ctx.send('\n'.join(messages))  # 메시지들을 줄바꿈으로 연결하여 출력합니다.
        else:
            await ctx.send("No suggestions found.")  # 파일이 없으면 해당 메시지를 출력합니다.
    except Exception as e:  
        await ctx.send(f"Error occurred: {e}")  # 오류 발생 시 오류 메시지를 출력합니다.



@app.command()
async def rmpk(ctx):
    logger.warning("rmpk 명령어가 사용되었습니다.")
    # 'vote_result.pkl' 파일 열기 및 데이터 로드
    with open('vote_result.pkl', 'rb') as f:
        data = pickle.load(f)

    try:

        pickle.dump({}, f)
        logger.info("pickle 초기화 성공.")

    except Exception as e:
        logger.error(e)


    # # 만약 메시지 ID가 데이터에 있다면, 해당 항목 삭제
    # if message_id in data or int(message_id) in data:
    #     if message_id in data:
    #         del data[message_id]
    #     else:
    #         del data[int(message_id)]

    #     await loggerwarning(f"메시지 ID {message_id}의 정보가 삭제되었습니다.", ctx)
        
        
    # else:
    #     await loggerwarning(f"메시지 ID {message_id}의 정보를 찾을 수 없습니다.", ctx)

    # 변경된 데이터를 다시 'vote_result.pkl' 파일에 저장
    with open('vote_result.pkl', 'wb') as f:
        pickle.dump(data, f)


@app.command()
async def ym(ctx):
    ctx.send(yesterday_menu_info)

@app.command()
async def addnote(ctx, *, note: str):
    if ctx.message.author.guild_permissions.administrator: # 관리자 권한 확인
        with open('patch_notes.txt', 'a') as file:
            file.write(note + '\n')
        await ctx.send(f'패치 노트에 추가됨: {note}')
    else:
        await ctx.send('관리자만 이 명령어를 사용할 수 있습니다.')
   
@app.command()
async def readnote(ctx):
    if ctx.message.author.guild_permissions.administrator: # 관리자 권한 확인
        with open('patch_notes.txt', 'r') as file:
            notes = file.read()
        await ctx.send(f'현재 패치 노트 내용:\n{notes}')
    else:
        await ctx.send('관리자만 이 명령어를 사용할 수 있습니다.')
    

@app.command()
async def delnote(ctx):
    if ctx.message.author.guild_permissions.administrator: # 관리자 권한 확인
        with open('patch_notes.txt', 'w') as file:
            file.write("")

        await ctx.send(f'내용 삭제됨')
    else:
        await ctx.send('관리자만 이 명령어를 사용할 수 있습니다.')

@app.command()
async def patchnote(ctx):
    if ctx.message.author.guild_permissions.administrator: # 관리자 권한 확인
        with open('patch_notes.txt', 'r') as file:
            notes = file.read()

        version_manager.check_commit()
        version = f'{version_manager.major_version}.{version_manager.minor_version}'


        # Create an embed message
        embed = discord.Embed(title=f"📝 {version}버전 업데이트 내용", description=notes, color=0x00ff00)
        channel = app.get_channel(1144839284617117736)
        await channel.send(embed=embed)
    else:
        await ctx.send('관리자만 이 명령어를 사용할 수 있습니다.')




@app.command()
async def send_result(ctx, date: str):
    if ctx.message.author.guild_permissions.administrator: # 관리자 권한 확인
        # 'YYYYMMDD' 형태의 문자열을 입력받아 파일명 생성
        filename = f'results_{date}.txt'
        
        # 해당 파일이 존재하는지 확인
        if not os.path.exists(filename):
            await embedwarning(f'{date}의 결과가 없습니다.', ctx)
            return
        
        # 존재한다면 파일 전송
        await ctx.send(file=discord.File(filename))
    else:
        await ctx.send('관리자만 이 명령어를 사용할 수 있습니다.')



@app.command()
async def list_results(ctx):
    if ctx.message.author.guild_permissions.administrator: # 관리자 권한 확인
        print(os.listdir())
        result_files = [filename for filename in os.listdir() if filename.startswith('results_')]
        
        if not result_files:
            await ctx.send('저장된 결과 파일이 없습니다.')
            return
        
        file_list = '\n'.join(result_files)
        await ctx.send(f'저장된 결과 파일 목록:\n`{file_list}`')
    else:
        await ctx.send('관리자만 이 명령어를 사용할 수 있습니다.')


@app.command()
async def stop(ctx):
    if ctx.message.author.guild_permissions.administrator: # 관리자 권한 확인
        await ctx.send('봇을 종료합니다.')
        await app.close() # 봇 작동 중지
        sys.exit()
    else:
        await ctx.send('관리자만 이 명령어를 사용할 수 있습니다.')

@app.command()
async def version(ctx):
    version_manager.check_commit()
    version = f'{version_manager.major_version}.{version_manager.minor_version}'
    await ctx.send(f"현재 버전은 {version}입니다.")


@app.command()
async def increment_minor(ctx):
    if ctx.message.author.guild_permissions.administrator: # 관리자 권한 확인
        version_manager.increment_minor()
    else:
        await ctx.send('관리자만 이 명령어를 사용할 수 있습니다.')

@app.command()
async def decrement_minor(ctx):
    if ctx.message.author.guild_permissions.administrator: # 관리자 권한 확인
        version_manager.decrement_minor()
    else:
        await ctx.send('관리자만 이 명령어를 사용할 수 있습니다.')


# -----------------------------------------------------------------------------

# 디버그 코드 함수
async def loggerwarning(str, ctx):
    await ctx.send(str)
    logger.warning(str)

async def loggererror(str, ctx):
    await ctx.send(str)
    logger.error(str)


async def embedwarning(str, ctx):
    embed = discord.Embed(title="경고", description=str, color=0xFF0000)
    await ctx.channel.send (embed=embed)
    logger.warning(str)
    
async def embedinfo(str, ctx):
    embed = discord.Embed(title="알림", description=str, color=0x5CA182)
    await ctx.channel.send (embed=embed)
    logger.info(str)
# ----------------------------------------------------------------------------------------------------------------------------------


# 실행

app.run(token)