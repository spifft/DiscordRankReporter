import os
import discord
from discord.ext import commands
import asyncio
from database import DatabaseManager
from rank_utils import validate_rank, format_rank_message, create_rank_embed
from config import VALID_RANKS, ROLES
import datetime

# Initialize bot with minimum required intents
intents = discord.Intents.default()
intents.message_content = True  # Required for commands to work
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize database manager
db = DatabaseManager()

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user.name}')
    # Connect to database
    if await db.connect():
        print("Successfully connected to database")
    else:
        print("Failed to connect to database")

@bot.command(name='rank')
async def set_rank(ctx, role: str = None, *, rank: str = None):
    """Command to set or update a specific Overwatch 2 rank"""
    if not role or not rank:
        return await ctx.send("Usage: !rank <role> <rank>\nExample: !rank Support Gold 3\nRoles: Support, DPS, Tank")
    
    # Convert role to title case for consistent comparison
    role = role.strip().title()
    rank = rank.strip().title()
    print(f"Debug: Updating {role} rank to {rank} for user {ctx.author.id}")
    
    # Case-insensitive role validation
    valid_role = next((r for r in ROLES if r.lower() == role.lower()), None)
    if not valid_role:
        return await ctx.send(f"Invalid role. Please choose from: {', '.join(ROLES)}")
    
    if not validate_rank(rank):
        return await ctx.send(f"Invalid rank. Valid ranks are: {', '.join(VALID_RANKS)}")
    
    try:
        # Get current ranks
        current_ranks = await db.get_ranks(ctx.author.id)
        if current_ranks is None:
            current_ranks = ["Unranked", "Unranked", "Unranked"]
        else:
            current_ranks = list(current_ranks)
            # Replace any None values with "Unranked"
            current_ranks = ["Unranked" if r is None else r for r in current_ranks]
            
        print(f"Debug: Current ranks before update: {current_ranks}")
        
        # Update the specific role's rank
        role_index = ROLES.index(valid_role)  # Use the matched valid role
        print(f"Debug: Role index for {role}: {role_index}")
        current_ranks[role_index] = rank
        print(f"Debug: New ranks after update: {current_ranks}")
        
        # Update database
        success = await db.update_ranks(
            ctx.author.id,
            current_ranks[0],
            current_ranks[1],
            current_ranks[2]
        )
        
        if success:
            embed = create_rank_embed(ctx, *current_ranks)
            await ctx.send(f"✅ {valid_role} rank updated successfully!", embed=embed)
        else:
            await ctx.send("❌ Failed to update rank. Please try again later.")
            
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        print(f"Error in rank command: {e}")

@bot.command(name='ranks')
async def show_ranks(ctx):
    """Command to display current Overwatch 2 ranks"""
    try:
        ranks = await db.get_ranks(ctx.author.id)
        if ranks:
            # Replace any None values with "Unranked"
            ranks = ["Unranked" if r is None else r for r in ranks]
            embed = create_rank_embed(ctx, *ranks)
            await ctx.send(embed=embed)
        else:
            await ctx.send("You haven't set any ranks yet. Use !rank <role> <rank> to set your ranks.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        print(f"Error in ranks command: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !rank to set ranks or !ranks to view them.")
    else:
        print(f"Debug: Command error occurred: {error}")
        await ctx.send(f"An error occurred: {str(error)}")

# Run the bot
if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("Error: DISCORD_TOKEN environment variable not set")
    else:
        try:
            bot.run(TOKEN)
        finally:
            db.close()
