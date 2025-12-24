# 1.Нам понадобятся стандартные модули времени и рандома, а также тяжелая артиллерия из rich.
# 2.Генератор предсказаний Какой Новый год без гаданий? Создадим список, который будет рандомно выдавать «пророчество» при каждом запуске. Это отличный способ поднять настроение коллегам.
# 3.Рисуем елку и считаем время Rich позволяет стилизовать текст тегами, похожими на BBCode. Мы сделаем функцию, которая возвращает красивый объект Text.
# 4. Собираем всё вместе (Main Loop) Самое интересное здесь — использование Layout. Мы делим экран на три части (Header, Body, Footer) и обновляем их внутри контекстного менеджера Live. Это позволяет избежать мерцания экрана, которое бывает при обычном cls / clear.
import time
import random
from datetime import datetime
import typer
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich.text import Text

app = typer.Typer()
console = Console()

PRIDICTIONS =[
    "🐍 В 2026 году твой код будет чистым без багов, не сгенерированный.",
    "☕ Твой сайт увидят многие и подпишутся на тебя в социальные сети",
    "☕ Ты наконец поймешь, зачем нужны сокеты(но это не точно)",
    "🚀Твой пет-проект заденет сердца работодателей и пригласят тебя на собеседование",
    "Телеграм бот будет работать, а ты нет.",
    "💰 Рекрутеры перестанут предлагать 'интересные проекты' за еду.",
    "🤖 Скайнет откладывается: нейросеть научится только писать калькулятор.",
]

def generate_tree():
    three_art = """
        🌟
       /  \\
      / 🎄 \\
     /  ✨  \\
    /  💾    \\
   / 🐍   🐛  \\
  /____________\\
       ||||
    """
    return Text(three_art, style="bold,green,justify_center")

def get_time_left():
    now = datetime.now()
    target = datetime(2026, 1, 1, 0, 0 , 0)
    diff = target - now
    
    if diff.total_seconds() <= 0:
        return "С новым 2026-м годом!🎉"
    
    days = diff.days
    hours, reminder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(reminder,60)
    
    return f"{days}д {hours:02} ч {minutes: 02} м {seconds: 02} с"


@app.command()
def start():
    console.clear()
    
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer",size=3)
    )
    
    prediction = random.choice(PRIDICTIONS)
    layout["header"].update(
        Panel(Align.center(f"[italic yellow]Oracle says: {prediction}[/]"), title="🔮Предсказание на 2026 год", style="red")
    )
    
    with Live(layout,refresh_per_second=4,screen=True):
        while True:
            time_left = get_time_left()
            if "С новым годом " in time_left:
                final_text = Text("\n\n" + time_left, style="bold red blink", justify="center")
                layout["body"].update(final_text)
                time.sleep(10)
                break
            
            content = Text()
            content.append(generate_tree())
            content.append("\n \n")
            content.append("До 2026 года осталось:\n", style="bold white justify_center")
            content.append(time_left, style="bold cyan justify_center")
            
            layout["body"].update(Align.center(content,vertical="middle"))
            time.sleep(0.1)
            
if __name__ == "__main__":
    app()