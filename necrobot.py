import random
import discord
from discord.ext import commands
import datetime
import os
from userdata import UserDataManager
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GENCHAT_ID = int(os.getenv("GENCHAT_ID", 0))
GRAVEYARD_ID = int(os.getenv("GRAVEYARD_ID", 0))
NECROMANCER_ROLE_ID = int(os.getenv("NECROMANCER_ROLE_ID", 0))
DELAY_NEEDED_ROLE_STEAL = int(os.getenv("DELAY_NEEDED_ROLE_STEAL", 600))
DELAY_NEEDED_COINS = int(os.getenv("DELAY_NEEDED_COINS", 15))

if not TOKEN:
    raise ValueError("Missing DISCORD_BOT_TOKEN environment variable")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

last_message_time = None
messages_debounce = {}
last_bot_message = None
first_message_received = False

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}", flush=True)

@bot.event
async def on_message(message: discord.Message):
    global last_message_time, last_bot_message, first_message_received

    if message.author == bot.user:
        return

    if messages_debounce.get(message.author.id, 0) + DELAY_NEEDED_COINS < current_time.timestamp():
        userdata = UserDataManager(message.author.id)
        userdata["necrocoins"] += random.randint(10, 20)
        messages_debounce[message.author.id] = current_time.timestamp()

    if message.channel.id == GENCHAT_ID:
        current_time = message.created_at

        if not first_message_received:
            first_message_received = True
            await give_necromancer_role(message.author, message.channel)
        else:
            necromancer_role = message.guild.get_role(NECROMANCER_ROLE_ID)
            has_role = any(necromancer_role in member.roles for member in message.guild.members)

            if last_message_time is not None and has_role:
                elapsed = (current_time - last_message_time).total_seconds()
                if elapsed >= DELAY_NEEDED_ROLE_STEAL:
                    if necromancer_role not in message.author.roles:
                      await transfer_necromancer_role(message.author, message.channel)

        last_message_time = current_time

    await bot.process_commands(message)

async def give_necromancer_role(member: discord.Member, channel: discord.TextChannel):
    global last_bot_message, necromancer_role_holder

    userdata = UserDataManager(member.id)
    userdata["necrocoins"] += random.randint(100, 200)

    try:
        necromancer_role = channel.guild.get_role(NECROMANCER_ROLE_ID)
        await member.add_roles(necromancer_role, reason="Test")

        try:
            if last_bot_message:
                await last_bot_message.delete()
        except discord.NotFound:
            print("Previous bot message not found.", flush=True)
        except Exception as e:
            print(f"Error deleting previous bot message: {e}", flush=True)

        last_bot_message = await channel.send(
            f"Gave the Necromancer role to {member.mention}!"
        )

    except Exception as e:
        print(f"Error giving role to {member.name}: {e}", flush=True)

async def transfer_necromancer_role(
    new_owner: discord.Member, channel: discord.TextChannel
):
    global last_bot_message
    necromancer_role = channel.guild.get_role(NECROMANCER_ROLE_ID)

    previous_owner = None
    for member in channel.guild.members:
        if necromancer_role in member.roles:
            previous_owner = member
            break

    userdata = UserDataManager(new_owner.id)
    userdata["necrocoins"] += random.randint(100, 200)

    if previous_owner:
        try:
            await previous_owner.remove_roles(
                necromancer_role, reason="Necromancer role transferred"
            )
        except discord.Forbidden:
            print(
                f"Failed to remove role from {previous_owner.name}. Insufficient permissions.",
                flush=True,
            )
        except Exception as e:
            print(f"Error removing role from {previous_owner.name}: {e}", flush=True)

    try:
        await new_owner.add_roles(
            necromancer_role, reason="Stole the Necromancer role!"
        )
    except discord.Forbidden:
        print(
            f"Failed to add role to {new_owner.name}. Insufficient permissions.",
            flush=True,
        )
    except Exception as e:
        print(f"Error adding role to {new_owner.name}: {e}", flush=True)

    try:
        if last_bot_message:
            try:
                await last_bot_message.delete()
            except discord.NotFound:
                print("Previous bot message not found.", flush=True)
            except Exception as e:
                print(f"Error deleting previous bot message: {e}", flush=True)

        last_bot_message = await channel.send(
            f"{new_owner.mention} has stolen the {necromancer_role.mention} role!"
        )
    except discord.Forbidden:
        print("Failed to send message. Insufficient permissions.", flush=True)
    except Exception as e:
        print(f"Error sending message: {e}", flush=True)

@bot.command(name="color")
async def change_color(ctx, hex_color: str):
    necromancer_role = ctx.guild.get_role(NECROMANCER_ROLE_ID)

    if necromancer_role not in ctx.author.roles:
        await ctx.send("Only the Necromancer role holder can use this command.")
        return

    try:
        color = discord.Color(int(hex_color, 16))
        await necromancer_role.edit(color=color)
        await ctx.send(f"Changed {necromancer_role.name} color to {hex_color}")
    except ValueError:
        await ctx.send(
            "Invalid hex color code. Please use a valid 6-digit hex code (e.g., FFFFFF)."
        )
    except discord.Forbidden:
        await ctx.send("I don't have permission to change that role's color.")
    except Exception as e:
        await ctx.send(f"An error occurred while changing the color: {e}")

@bot.command(name="balance")
async def balance(ctx: commands.Context):
    userdata = UserDataManager(ctx.author.id)
    await ctx.send(f"You have {userdata["necrocoins"]} coins.")

bot.run(TOKEN)
