import discord
import datetime
from config import VALID_RANKS

def validate_rank(rank):
    """Validates if the provided rank is in the correct format and exists in valid ranks"""
    if not rank:
        return False
    # Convert input rank to title case for comparison
    normalized_rank = rank.strip().title()
    # Compare with valid ranks case-insensitively
    return normalized_rank in VALID_RANKS

def format_rank_message(support_rank, dps_rank, tank_rank):
    """Formats the rank message for display"""
    return (f"🏆 Your Overwatch 2 Ranks 🏆\n\n"
            f"🚑 Support: {support_rank}\n"
            f"⚔️ DPS: {dps_rank}\n"
            f"🛡️ Tank: {tank_rank}")

def create_rank_embed(ctx, support_rank, dps_rank, tank_rank):
    """Creates a Discord embed for displaying ranks"""
    # Use display_name which handles nicknames without requiring privileged intents
    display_name = ctx.author.display_name
    
    embed = discord.Embed(
        title=f"{display_name}'s Overwatch 2 Ranks",
        color=0xFF9900
    )
    embed.add_field(name="Support 🚑", value=support_rank or "Unranked", inline=False)
    embed.add_field(name="DPS ⚔️", value=dps_rank or "Unranked", inline=False)
    embed.add_field(name="Tank 🛡️", value=tank_rank or "Unranked", inline=False)
    embed.set_footer(text="Last updated")
    embed.timestamp = datetime.datetime.utcnow()
    return embed
