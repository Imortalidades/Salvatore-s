import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # ESSENCIAL para comandos prefixados

bot = commands.Bot(command_prefix="v!", intents=intents)
from flask import Flask
from threading import Thread
import discord
from discord.ext import commands

# Mantém o bot online
app = Flask('')


@app.route('/')
def home():
    return "Bot tá ON, bebê!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


# Intents CERTOS
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # ← ESSENCIAL PRA COMANDOS COM MEMBROS

bot = commands.Bot(command_prefix="v!", intents=intents)


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')


@bot.command()
async def oi(ctx):
    await ctx.message.delete()
    await ctx.send('E aí, vidoca! Tô on!')


@bot.command()
async def ajuda(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="`𖥔` 🕸️ • Central de Comandos",
        description=
        "ㅤ\n**⚰️ Meu prefixo:** `v!`\n**🌑 Use os comandos abaixo:**\nㅤ",
        color=0x000000)

    embed.set_thumbnail(
        url=ctx.guild.icon.url if ctx.guild.icon else discord.Embed.Empty)

    embed.add_field(name="`𖥔` 🩸 • **Utilitários**",
                    value=("`oi` • Testa se tô online\n"
                           "`ping` • Mostra meu ping\n"
                           "`avatar` • Mostra avatar de alguém\n"
                           "`serverinfo` • Info do servidor\n"
                           "`membros` • Contagem de membros\n"
                           "`boostinfo` • Benefícios do booster\n"
                           "`sugestao` • Envia uma sugestão\n"
                           "`painel` • Painel de tickets"),
                    inline=False)

    embed.add_field(name="`𖥔` ⚰️ • **Moderação & Staff**",
                    value=("`ban` • Banir um membro\n"
                           "`kick` • Expulsar um membro\n"
                           "`tempban` • Ban temporário\n"
                           "`warn / warnings` • Avisos\n"
                           "`limpar` • Limpar mensagens\n"
                           "`clearbots` • Limpar mensagens de bots\n"
                           "`nuke` • Explodir e recriar o canal 💣\n"
                           "`lock / unlock` • Trancar/Destrancar canal\n"
                           "`lockall / unlockall` • Todos os canais\n"
                           "`slow` • Ativar modo lento\n"
                           "`role / unrole` • Dar/Remover cargo\n"
                           "`anunciar` • Anunciar com embed\n"
                           "`dizer` • Falar por mim"),
                    inline=False)

    embed.add_field(name="`𖥔` 🕷️ • **Relacionamento**",
                    value=("`ship` • Mede o ship de dois 🖤\n"
                           "`namorar` • Pedir em namoro 💌\n"
                           "`casar` • Pedir em casamento 💍\n"
                           "`divorcio` • Separação 💔"),
                    inline=False)

    embed.add_field(name="`𖥔` 🕯️ • **Diversão & Extras**",
                    value=("`gay` • Mede o quanto é gay 🌈\n"
                           "`calc` • Calculadora rápida 🧠\n"
                           "`votar` • Criar uma enquete 🗳️\n"
                           "`lembrete` • Criar um lembrete ⏰"),
                    inline=False)

    embed.set_footer(text=f'Requisitado por {ctx.author.display_name}',
                     icon_url=ctx.author.avatar.url
                     if ctx.author.avatar else discord.Embed.Empty)

    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    await ctx.send("Mensagem que some em 5 segundos", delete_after=5)
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="⚫ Membro Banido",
            description=f"O membro **{member}** foi banido com sucesso.",
            color=0x000000)
        embed.add_field(name="Motivo:",
                        value=reason or "Não especificado",
                        inline=False)
        embed.set_footer(text=f"Solicitado por {ctx.author}",
                         icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f"❌ Não foi possível banir o membro: {e}")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.send("Mensagem que some em 5 segundos", delete_after=5)
    try:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="⚫ Membro Expulso",
            description=f"O membro **{member}** foi expulso do servidor.",
            color=0x1A1A1A)
        embed.add_field(name="Motivo:",
                        value=reason or "Não especificado",
                        inline=False)
        embed.set_footer(text=f"Solicitado por {ctx.author}",
                         icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f"❌ Não foi possível expulsar o membro: {e}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send(
            f'❌ {ctx.author.mention}, você não tem permissão pra isso.',
            delete_after=10)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        await ctx.send(
            f'⚠️ {ctx.author.mention}, comando inexistente. Usa `v!ajuda` pra ver meus comandos.',
            delete_after=10)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send(
            f'⚠️ {ctx.author.mention}, você esqueceu algum argumento no comando.',
            delete_after=10)
    elif isinstance(error, commands.BadArgument):
        await ctx.message.delete()
        await ctx.send(
            f'⚠️ {ctx.author.mention}, não encontrei esse membro ou cargo. Confere se escreveu certo.',
            delete_after=10)
    else:
        # Isso deixa o erro visível no console pra você identificar se for algo mais sério
        print(f"Erro não tratado: {error}")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, quantidade: int = 5):
    if quantidade < 1:
        await ctx.send(
            '❌ Por favor, informe uma quantidade válida maior que zero.',
            delete_after=10)
        return

    deleted = await ctx.channel.purge(limit=quantidade + 1
                                      )  # +1 para apagar o comando também
    embed = discord.Embed(
        title="⚫ Mensagens Apagadas",
        description=
        f"Foram apagadas **{len(deleted) - 1}** mensagens neste canal.",
        color=0x000000)
    embed.set_footer(text=f"Solicitado por {ctx.author}",
                     icon_url=ctx.author.avatar.url)
    mensagem = await ctx.send(embed=embed)
    await ctx.message.delete()
    await mensagem.delete(
        delay=5
    )  # Apaga o embed depois de 5 segundos para manter o canal limpo


@bot.command()
async def avatar(ctx, membro: discord.Member = None):
    await ctx.message.delete()
    membro = membro or ctx.author
    await ctx.send(f'🖼️ Avatar de {membro.display_name}: {membro.avatar.url}')


@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    await ctx.send(f'🏓 Pong! Meu ping tá {round(bot.latency * 1000)}ms!')


@bot.command()
async def membros(ctx):
    await ctx.message.delete()

    total = ctx.guild.member_count
    humanos = len([m for m in ctx.guild.members if not m.bot])
    bots = len([m for m in ctx.guild.members if m.bot])

    embed = discord.Embed(
        title="⚫ Contagem de Membros",
        description=
        f"👥 Total: **{total}**\n🧍 Humanos: **{humanos}**\n🤖 Bots: **{bots}**",
        color=0x000000)
    embed.set_footer(text=f"Solicitado por {ctx.author}",
                     icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed, delete_after=10)


@bot.command()
@commands.has_permissions(administrator=True)
async def anunciar(ctx, canal: discord.TextChannel, *, mensagem):
    await ctx.message.delete()

    embed = discord.Embed(
        title="<a:Siren_Purple:1051266560414720051> AVISO IMPORTANTE",
        description=mensagem,
        color=0x000000  # Sua cor maravilhosa lilás
    )

    embed.set_footer(text=f'Anunciado por {ctx.author.display_name}',
                     icon_url=ctx.author.avatar.url)

    await canal.send(embed=embed)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def dizer(ctx, canal: discord.TextChannel, *, mensagem):
    await ctx.message.delete()
    await canal.send(mensagem)


@bot.command()
async def ship(ctx, pessoa1: discord.Member, pessoa2: discord.Member):
    import random
    await ctx.message.delete()

    porcentagem = random.randint(0, 100)
    barra = "█" * (porcentagem // 10) + "░" * (10 - (porcentagem // 10))

    await ctx.send(f'💖 Ship de {pessoa1.mention} + {pessoa2.mention}\n'
                   f'❤️ Compatibilidade: `{porcentagem}%`\n'
                   f'[{barra}]')


@bot.command()
async def namorar(ctx, membro: commands.MemberConverter):
    await ctx.message.delete()
    if membro == ctx.author:
        await ctx.send(
            f'`𖥔` {ctx.author.mention} tentou se auto namorar... amor-próprio é essencial, né? 🤍'
        )
    else:
        await ctx.send(
            f'`𖥔` {ctx.author.mention} pediu {membro.mention} em namoro! aceita? 🕊️ ❞\n'
            f'↳ Responde com: `sim` ou `não`')

        def check(m):
            return m.author == membro and m.channel == ctx.channel and m.content.lower(
            ) in ['sim', 'não']

        try:
            resposta = await bot.wait_for('message', check=check, timeout=30)

            if resposta.content.lower() == 'sim':
                await ctx.send(
                    f'`𖥔` ♡ {ctx.author.mention} e {membro.mention} agora estão oficialmente namorando ♡\n'
                    f'☁️💌 Que coisa mais fofa ✨')
            else:
                await ctx.send(
                    f'`𖥔` {membro.mention} disse ❝ não ❞... 💔\n'
                    f'↳ Talvez o universo tenha outros planos, {ctx.author.mention}... 🕊️'
                )
        except:
            await ctx.send(
                f'`𖥔` ⏳ {membro.mention} não respondeu... destino ignorado 🥀')


@bot.command()
async def casar(ctx, membro: commands.MemberConverter):
    await ctx.message.delete()
    if membro == ctx.author:
        await ctx.send(
            f'`𖥔` {ctx.author.mention} tentou casar consigo mesmo... auto amor é arte. ✨'
        )
    else:
        await ctx.send(
            f'`𖥔` 💍 {ctx.author.mention} se ajoelhou... ❝ {membro.mention}, aceita casar comigo? ❞\n'
            f'↳ Responde com: `sim` ou `não`')

        def check(m):
            return m.author == membro and m.channel == ctx.channel and m.content.lower(
            ) in ['sim', 'não']

        try:
            resposta = await bot.wait_for('message', check=check, timeout=30)

            if resposta.content.lower() == 'sim':
                await ctx.send(
                    f'`𖥔` ♡ {ctx.author.mention} e {membro.mention} agora são oficialmente casados ♡\n'
                    f'💍✨ Felicidades aos pombinhos. Que o amor vença. ☁️')
            else:
                await ctx.send(
                    f'`𖥔` {membro.mention} disse ❝ não ❞... 💔\n'
                    f'↳ Nem sempre o destino sorri, {ctx.author.mention}... 🌫️'
                )
        except:
            await ctx.send(
                f'`𖥔` ⏳ {membro.mention} não respondeu... pedido perdido no vento 🥀'
            )


@bot.command()
async def divorcio(ctx, membro: commands.MemberConverter):
    await ctx.message.delete()
    if membro == ctx.author:
        await ctx.send(
            f'`𖥔` {ctx.author.mention} tentou se divorciar de si mesmo... reflexão profunda, né? 🪞'
        )
    else:
        await ctx.send(
            f'`𖥔` 💔 {ctx.author.mention} e {membro.mention} assinaram os papéis...\n'
            f'↳ O amor virou lembrança... 🌫️🥀')


@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.message.delete()
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      overwrite=overwrite)
    await ctx.send(
        f'`𖥔` 🔒 Este canal foi **trancado** por {ctx.author.mention} ☁️')


@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.message.delete()
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      overwrite=overwrite)
    await ctx.send(
        f'`𖥔` 🔓 Este canal foi **destrancado** por {ctx.author.mention} ☁️')


@bot.command()
@commands.has_permissions(manage_channels=True)
async def slow(ctx, tempo: int = 0):
    await ctx.message.delete()
    await ctx.channel.edit(slowmode_delay=tempo)
    if tempo == 0:
        await ctx.send(f'`𖥔` ⏳ Modo lento **desativado** neste canal ☁️')
    else:
        await ctx.send(
            f'`𖥔` ⏳ Modo lento ativado: **{tempo} segundos** neste canal ☁️')


@bot.command()
async def gay(ctx, membro: commands.MemberConverter = None):
    await ctx.message.delete()
    if membro is None:
        membro = ctx.author

    porcentagem = random.randint(0, 100)
    await ctx.send(f'`𖥔` 🌈 {membro.mention} é **{porcentagem}% gay** hoje... ✨'
                   )


@bot.command()
async def calc(ctx, *, conta):
    await ctx.message.delete()
    try:
        resultado = eval(conta)
        await ctx.send(f'`𖥔` 🧠 Resultado de `{conta}` é: **{resultado}**')
    except:
        await ctx.send(f'`𖥔` ⚠️ Não consegui calcular isso... Confere aí.')


@bot.event
async def on_message(message):
    # Se quem enviou foi o bot
    if message.author == bot.user:
        await message.delete(delay=60)  # Apaga depois de 60 segundos

    await bot.process_commands(
        message)  # Permite que os comandos continuem funcionando


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()  # Apaga a mensagem do usuário imediatamente
        await ctx.send(
            f'`𖥔` ⚠️ {ctx.author.mention} esse comando não existe, bebê...\n'
            f'↳ Confere se escreveu certo ou usa `v!ajuda` pra ver os comandos disponíveis. ☁️',
            delete_after=20)
    else:
        raise error


import discord
from discord.ext import commands


@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild

    total_membros = guild.member_count
    total_bots = sum(1 for member in guild.members if member.bot)
    total_humans = total_membros - total_bots
    total_canais = len(guild.channels)
    total_cargos = len(guild.roles)
    criacao = guild.created_at.strftime('%d/%m/%Y %H:%M')

    embed = discord.Embed(title=f'📊 Informações do Servidor: {guild.name}',
                          color=0x000000,
                          timestamp=ctx.message.created_at)
    embed.set_thumbnail(
        url=guild.icon.url if guild.icon else discord.Embed.Empty)
    embed.add_field(name='🆔 ID do Servidor', value=guild.id, inline=True)
    embed.add_field(name='👑 Dono', value=str(guild.owner), inline=True)
    embed.add_field(name='📅 Criado em', value=criacao, inline=True)
    embed.add_field(name='👥 Membros (humanos)',
                    value=total_humans,
                    inline=True)
    embed.add_field(name='🤖 Bots', value=total_bots, inline=True)
    embed.add_field(name='💬 Canais', value=total_canais, inline=True)
    embed.add_field(name='🎭 Cargos', value=total_cargos, inline=True)
    embed.add_field(
        name='🌍 Região',
        value=str(guild.region).title() if hasattr(guild, 'region') else 'N/D',
        inline=True)
    embed.add_field(name='🔧 Nível de Verificação',
                    value=str(guild.verification_level).title(),
                    inline=True)
    embed.set_footer(text=f'Solicitado por {ctx.author}',
                     icon_url=ctx.author.avatar.url
                     if ctx.author.avatar else discord.Embed.Empty)

    await ctx.send(embed=embed)


import asyncio
from discord.ext import commands


@bot.command()
@commands.has_permissions(ban_members=True)
async def tempban(ctx,
                  member: commands.MemberConverter,
                  tempo: int,
                  *,
                  motivo=None):
    await ctx.message.delete()
    await member.ban(reason=motivo)
    await ctx.send(
        f'`𖥔` 🚫 {member} foi banido por {tempo} segundos! Motivo: {motivo}',
        delete_after=30)
    await asyncio.sleep(tempo)
    await ctx.guild.unban(member)
    await ctx.send(
        f'`𖥔` ⏳ {member} foi desbanido automaticamente após o tempo!',
        delete_after=30)


warns = {}


@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    # Aqui você deve adicionar sua lógica para armazenar o aviso
    embed = discord.Embed(
        title="⚫ Aviso Registrado",
        description=f"O membro **{member}** recebeu um aviso.",
        color=0x000000)
    embed.add_field(name="Motivo:",
                    value=reason or "Não especificado",
                    inline=False)
    embed.set_footer(text=f"Solicitado por {ctx.author}",
                     icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(manage_messages=True)
async def warnings(ctx, member: commands.MemberConverter):
    user_warns = warns.get(member.id, [])
    if not user_warns:
        await ctx.send(f'`𖥔` ✅ {member.mention} não tem avisos.',
                       delete_after=15)
    else:
        avisos = '\n'.join(f'{i+1}. {motivo}'
                           for i, motivo in enumerate(user_warns))
        await ctx.send(f'`𖥔` ⚠️ Avisos de {member.mention}:\n{avisos}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()  # Apaga a mensagem do comando
        await ctx.send(
            f'`𖥔` ❌ {ctx.author.mention} você não tem permissão pra usar esse comando, bebê... 💔',
            delete_after=15)

    elif isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()  # Apaga a mensagem do comando errado
        await ctx.send(
            f'`𖥔` ⚠️ {ctx.author.mention} esse comando não existe...\n'
            f'↳ Usa `v!ajuda` pra ver meus comandos, tá? ☁️',
            delete_after=15)
    else:
        raise error  # Outros erros continuam aparecendo no console


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.dnd,  # ← Vermelhinho "Não Perturbe"
        activity=discord.Activity(type=discord.ActivityType.watching,
                                  name="v!ajuda"))
    print(f'Bot conectada como {bot.user}')


@bot.event
async def on_ready():
    await bot.user.edit(bio="⚙️ | Bot do [nome] • 🕸️ Moderação + diversão")
    print(f'Bot conectado como {bot.user}')


@bot.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    await ctx.message.delete()
    canal_antigo = ctx.channel
    novo = await canal_antigo.clone(reason="Nuke")
    await canal_antigo.delete()
    await novo.send(
        f'`𖥔` 💣 Este canal foi **NUKEADO** por {ctx.author.mention}')


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clearbots(ctx, quantidade: int = 100):
    await ctx.message.delete()
    deletadas = await ctx.channel.purge(limit=quantidade,
                                        check=lambda m: m.author.bot)
    await ctx.send(f'`𖥔` 🤖 Apaguei {len(deletadas)} mensagens de bots!',
                   delete_after=5)


@bot.command()
@commands.has_permissions(manage_channels=True)
async def lockall(ctx):
    await ctx.message.delete()
    for canal in ctx.guild.text_channels:
        await canal.set_permissions(ctx.guild.default_role,
                                    send_messages=False)
    await ctx.send(
        f'`𖥔` 🔒 Todos os canais foram **trancados** por {ctx.author.mention}!')


@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlockall(ctx):
    await ctx.message.delete()
    for canal in ctx.guild.text_channels:
        await canal.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(
        f'`𖥔` 🔓 Todos os canais foram **destrancados** por {ctx.author.mention}!'
    )


@bot.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx, membro: discord.Member, cargo: discord.Role):
    await ctx.message.delete()
    await membro.add_roles(cargo)
    await ctx.send(
        f'`𖥔` 🎭 {ctx.author.mention} deu o cargo {cargo.mention} para {membro.mention}!'
    )


@bot.command()
@commands.has_permissions(manage_roles=True)
async def unrole(ctx, membro: discord.Member, cargo: discord.Role):
    await ctx.message.delete()
    await membro.remove_roles(cargo)
    await ctx.send(
        f'`𖥔` 🎭 {ctx.author.mention} removeu o cargo {cargo.mention} de {membro.mention}!'
    )


@bot.command()
async def votar(ctx, *, texto):
    await ctx.message.delete()
    try:
        pergunta, op1, op2 = texto.split("|")
    except:
        await ctx.send(
            '`𖥔` ⚠️ Formato inválido. Use: `v!votar pergunta | opção1 | opção2`'
        )
        return

    embed = discord.Embed(title='🗳️ Enquete:',
                          description=f'**{pergunta}**\n\n🔴 {op1}\n🔵 {op2}',
                          color=0xd4b5ff)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('🔴')
    await msg.add_reaction('🔵')


import asyncio


@bot.command()
async def lembrete(ctx, tempo, *, motivo):
    await ctx.message.delete()

    unidade = tempo[-1]
    quant = int(tempo[:-1])

    if unidade == 's':
        segundos = quant
    elif unidade == 'm':
        segundos = quant * 60
    elif unidade == 'h':
        segundos = quant * 3600
    else:
        await ctx.send(
            '`𖥔` ⚠️ Unidade de tempo inválida. Use:\n`s` = segundos\n`m` = minutos\n`h` = horas'
        )
        return

    await ctx.send(
        f'`𖥔` ⏰ {ctx.author.mention}, lembrete criado! Te aviso em {tempo}.')
    await asyncio.sleep(segundos)
    await ctx.send(f'`𖥔` 🔔 {ctx.author.mention}, lembrete: {motivo}')


@bot.command()
async def boostinfo(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="🚀 Benefícios para Boosters",
        description=
        ("Seja um booster e desbloqueie benefícios exclusivos no servidor:\n\n"
         "🖤 Acesso a canais secretos\n"
         "🖤 Cargos exclusivos e destacados\n"
         "🖤 Prioridade em tickets e suporte\n"
         "🖤 Direito a 1 cargo personalizado com nome e cor\n"
         "🖤 E muito mais...\n\n"
         "🕸️ Obrigado por apoiar nosso servidor!"),
        color=0x0f0f13)
    embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.set_footer(text="Sistema de Boosters — Prometheus",
                     icon_url=ctx.guild.icon.url)
    await ctx.send(embed=embed)


@bot.command()
async def sugestao(ctx, *, mensagem):
    await ctx.message.delete()
    canal_sugestao = bot.get_channel(
        1385464860749463615)  # Coloque aqui o ID do canal de sugestões
    embed = discord.Embed(
        title="🗳️ Nova Sugestão",
        description=f"**Autor:** {ctx.author.mention}\n\n{mensagem}",
        color=0x0f0f13)
    embed.set_footer(text="Sistema de Sugestões — 🦇",
                     icon_url=ctx.guild.icon.url)
    msg = await canal_sugestao.send(embed=embed)
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")
    await ctx.message.delete()
    await ctx.send(f"🖤 {ctx.author.mention}, sua sugestão foi enviada!",
                   delete_after=5)


@bot.command()
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="🖤 Central de Tickets",
        description=("🕸️ Precisa de ajuda? Abra um ticket!\n\n"
                     "**Selecione abaixo o motivo do seu ticket:**\n"
                     "🔧 **Suporte**\n"
                     "📩 **Parcerias**\n"
                     "⚠️ **Denúncias**\n"
                     "💡 **Outros**"),
        color=0x0f0f13)
    embed.set_footer(text="Sistema de Tickets",
                     icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
    await ctx.send(embed=embed, view=TicketView())


class TicketView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Selecione uma opção...",
        options=[
            discord.SelectOption(label="Suporte",
                                 description="Abra um ticket para suporte",
                                 emoji="🔧"),
            discord.SelectOption(label="Parcerias",
                                 description="Ticket de parcerias",
                                 emoji="📩"),
            discord.SelectOption(label="Denúncias",
                                 description="Reportar usuários ou problemas",
                                 emoji="⚠️"),
            discord.SelectOption(label="Outros",
                                 description="Outros assuntos",
                                 emoji="💡"),
        ])
    async def select_callback(self, interaction: discord.Interaction,
                              select: discord.ui.Select):
        guild = interaction.guild
        category = None  # Se quiser, coloca ID da categoria aqui para organizar

        ticket_name = f"ticket-{interaction.user.name}".replace(" ",
                                                                "-").lower()

        overwrites = {
            guild.default_role:
            discord.PermissionOverwrite(view_channel=False),
            interaction.user:
            discord.PermissionOverwrite(view_channel=True,
                                        send_messages=True,
                                        attach_files=True),
            guild.me:
            discord.PermissionOverwrite(view_channel=True,
                                        send_messages=True,
                                        manage_channels=True),
        }

        canal = await guild.create_text_channel(
            name=ticket_name,
            overwrites=overwrites,
            category=category,
            topic=
            f"Ticket aberto por {interaction.user.display_name} • Motivo: {select.values[0]}"
        )

        embed = discord.Embed(
            title="🕸️ Ticket Aberto",
            description=
            (f"{interaction.user.mention} seu ticket foi criado com sucesso!\n\n"
             f"**Motivo:** {select.values[0]}\n"
             "Nossa equipe irá te atender em breve."),
            color=0x0f0f13)
        embed.set_footer(text="Sistema de Tickets",
                         icon_url=guild.icon.url if guild.icon else None)

        await canal.send(content=f"{interaction.user.mention}",
                         embed=embed,
                         view=FecharTicketView())

        await interaction.response.send_message(
            f"🖤 Ticket criado com sucesso: {canal.mention}", ephemeral=True)


class FecharTicketView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Fechar Ticket", style=discord.ButtonStyle.red)
    async def fechar(self, interaction: discord.Interaction,
                     button: discord.ui.Button):
        # Permite fechar só se for admin ou dono do ticket
        if interaction.user.guild_permissions.administrator or interaction.user == interaction.channel.members[
                0]:
            await interaction.channel.delete()
        else:
            await interaction.response.send_message(
                "❌ Você não pode fechar este ticket.", ephemeral=True)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(
            error, commands.BadArgument):
        await ctx.send(
            f"❌ **Você errou o comando!**\n"
            f"Tente usar assim: `{ctx.prefix}{ctx.command} {ctx.command.signature}`"
        )
    else:
        raise error

keep_alive()
bot.run(
    'MTM4NTM1MTM3NDI5NTkyNDc0Nw.GV-mPF.yZ_dXpo5ms2oySji4PpXPIDO_ndJFInTMI6POk')
