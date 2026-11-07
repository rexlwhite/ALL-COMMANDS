import os
import discord
from keep_alive import keep_alive
from discord.ext import commands

# ตั้งค่า Intents (ต้องเปิด Server Members Intent และ Message Content Intent ใน Discord Developer Portal ด้วย)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


# 1. คำสั่งส่งข้อความถึงทุกคนในช่อง (Announcement / Broadcast)
# ใช้งาน: !ty <ข้อความ> หรือใส่ @everyone
@bot.command(name='ty', help='ให้บอทส่งข้อความไปยังแชท')
@commands.has_permissions(administrator=True) # กำหนดให้ใช้ได้เฉพาะแอดมิน (เปลี่ยนได้ตามต้องการ)
async def ty(ctx, *, message: str):
    # ลบข้อความคำสั่งของคนที่พิมพ์ เพื่อความสะอาดของแชท (ถ้าต้องการ)
    await ctx.message.delete()
    # ส่งข้อความ
    await ctx.send(f">>> ** {message}**") # หากไม่อยากแท็ก @everyone ให้ลบคำว่า @everyone ออก


# 2. คำสั่งเคลียร์ข้อความ (Purge / Clear)
# ใช้งาน: !d <จำนวน> เช่น !clear 10
@bot.command(name='d', aliases=['purge'], help='ลบข้อความตามจำนวนที่กำหนด')
@commands.has_permissions(manage_messages=True) # ต้องมีสิทธิ์จัดการข้อความ
async def d(ctx, amount: int):
    # ลบข้อความคำสั่ง + จำนวนที่ระบุ
    deleted = await ctx.channel.purge(limit=amount + 1)
    # ส่งข้อความแจ้งเตือนแล้วลบอัตโนมัติใน 3 วินาที
    msg = await ctx.send(f'>>> **เรียลไวท์ลบแล้ว {len(deleted) - 1} ข้อความ**', delete_after=3)


# จัดการกรณีไม่มีสิทธิ์ใช้งานคำสั่ง
@ty.error
@d.error
async def command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(">>> **คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้!**", delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(">>> **กรุณากรอกข้อมูลให้ครบถ้วนด้วยครับ!**", delete_after=5)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  print(f"Logged in as {bot.user} (ID: {bot.user.id})")
  print("-----------------------------------------")


# คำสั่งแบน: !ban @user [เหตุผล]
@bot.command()
@commands.has_permissions(ban_members=True)
async def b(ctx, member: discord.Member, *, reason=None):
  if member == ctx.author:
    await ctx.send(">>> **คุณไม่สามารถแบนตัวเองได้!**")
    return

  await member.ban(reason=reason)
  await ctx.send(
      f">>> **แบน {member.mention} เรียบร้อยแล้ว (เหตุผล: {reason or 'ไม่ได้ระบุ'}**)"
  )


@b.error
async def ban_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(">>> **คุณไม่มีสิทธิ์ในการใช้คำสั่งแบน**)")
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(">>> **กรุณาแท็กผู้ใช้ที่ต้องการแบน เช่น !b @username**")


# คำสั่งปลดแบน: !unban UserID หรือ Username#0000
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user_identifier):
  # ดึงรายการคนที่โดนแบนทั้งหมดในเซิร์ฟเวอร์
  banned_users = await ctx.guild.bans()

  target_user = None

  for ban_entry in banned_users:
    user = ban_entry.user
    # ค้นหาจาก ID หรือ Username
    if str(user.id) == user_identifier or f"{user.name}#{user.discriminator}" == user_identifier or user.name == user_identifier:
      target_user = user
      break

  if target_user:
    await ctx.guild.unban(target_user)
    await ctx.send(f">>> **ปลดแบนให้แก่ {target_user.mention} เรียบร้อยแล้ว!**")
  else:
    await ctx.send(
    )


@unban.error
async def unban_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(">>> **คุณไม่มีสิทธิ์ในการใช้คำสั่งปลดแบน**")
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send()

keep_alive()

# ใส่ Token ของบอทคุณตรงนี้
bot.run(os.getenv('TOKEN'))