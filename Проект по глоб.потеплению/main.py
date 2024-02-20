import discord
from discord.ext import commands
import json 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

@bot.command()
async def start(ctx):
    await ctx.send('Привет! Я бот для работы с данными о климатических изменениях. '
                   'Используйте команду /help для получения списка доступных команд.')

@bot.command()
async def help(ctx):
    help_message = '''
    Вот список доступных команд:
    /start - Приветствие
    /help - Список доступных команд
    /visualize - Визуализация данных о климатических изменениях
    /analyze - Анализ данных о климатических изменениях
    /save - Сохранение графиков данных о климатических изменениях
    /send - Отправка данных во внешний инструмент визуализации
    '''
    await ctx.send(help_message)

def generate_climate_data():
    years = np.arange(1900, 2024)
    temperatures = np.random.uniform(low=-40.0, high=40.0, size=len(years))
    data = pd.DataFrame({'Год': years, 'Температура': temperatures})
    return data

def visualize_data():
    data = generate_climate_data()
    
    plt.figure(figsize=(10, 6))
    plt.plot(data['Год'], data['Температура'], marker='o')
    plt.title('Изменения температуры с годами')
    plt.xlabel('Год')
    plt.ylabel('Температура')
    plt.grid(True)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    return buf

@bot.command()
async def visualize(ctx):
    chart = visualize_data()
    await ctx.send(file=discord.File(chart, 'climate_data.png'))

@bot.command()
async def analyze(ctx):
    temperature = round(random.uniform(-30, +40), 2) 
    precipitation = round(random.uniform(0, 1500), 2)  
    
    await ctx.send(f'Средняя температура: {temperature}°C, Максимальные осадки: {precipitation} мм')

@bot.command()
async def save(ctx):
    plt.savefig('climate_data.png')
    await ctx.send('Графики данных сохранены в файле climate_data.png')

@bot.command()
async def send(ctx):
    await ctx.send('Данные отправлены во внешний инструмент визуализации данных')

bot.run('')
