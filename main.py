from src.Bot_Twic import  GoogleBot
import os
import subprocess
import sys
import pkg_resources
from rich.console import Console
from rich.markdown import Markdown
import platform
import threading
from src.Bot_Twic import GoogleBot
from rich.live import Live
from rich.text import Text
from time import sleep
# ... [استيراد المكتبات الأخرى كما هو]

REQUIRED_LIBS = ["selenium", "rich"]  # تحديد المكتبات المطلوبة هنا

console = Console()
def Printool():
    amazon_capsule_catcher_text = """
    Amazon capsule catcher
    """
    windows_logo = """

 ______  __    __  ____  ______   __  ____    ___   ______   __  __ __   ____  ______ 
|      ||  |__|  ||    ||      | /  ]|    \  /   \ |      | /  ]|  |  | /    ||      |
|      ||  |  |  | |  | |      |/  / |  o  )|     ||      |/  / |  |  ||  o  ||      |
|_|  |_||  |  |  | |  | |_|  |_/  /  |     ||  O  ||_|  |_/  /  |  _  ||     ||_|  |_|
  |  |  |  `  '  | |  |   |  |/   \_ |  O  ||     |  |  |/   \_ |  |  ||  _  |  |  |  
  |  |   \      /  |  |   |  |\     ||     ||     |  |  |\     ||  |  ||  |  |  |  |  
  |__|    \_/\_/  |____|  |__| \____||_____| \___/   |__| \____||__|__||__|__|  |__|  
                                                                                      

    """

    # طباعة النص
    console.print(amazon_capsule_catcher_text, style="bold green")
    console.print(windows_logo, style="bold blue")

def install_and_check_libraries():
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    missing_packages = [lib for lib in REQUIRED_LIBS if lib not in installed_packages]
    if missing_packages:
        console.print("[yellow]Installing missing libraries...[/yellow]")
        for lib in missing_packages:
            console.print(f"[blue]Install {lib}...[/blue]")
            python = sys.executable
            subprocess.check_call([python, '-m', 'pip', 'install', lib], stdout=subprocess.DEVNULL)
            console.print(f"[green]{lib} It was installed successfully.[/green]")
    else:
        console.print("[green]All libraries are already installed.[/green]")
def write_check_status_to_file(status):
    filepath = os.path.join("data","check_status.txt")
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(status)
def print_pretty_message(message):
    markdown = Markdown(message)
    console.print(markdown)
def print_system_info():
    info = {
        "OS": platform.system(),
        "OS version": platform.release(),
        "Python version": platform.python_version(),
        "System Architecture": platform.machine(),
        "Script version" : "First Edition Version"
    }

    console.print("[bold magenta]معلومات النظام:[/bold magenta]")
    for key, value in info.items():
        console.print(f"{key}: [bold cyan]{value}[/bold cyan]")
# تشغيل الفحوصات وطباعة الرسالة
def load_proxy_list():
        proxy_file_path = os.path.join("data", "Proxy.txt")
        with open(proxy_file_path, 'r') as file:
            return [line.strip() for line in file]

# ... [بقية الكود الخاص بـ GoogleBot]


def run_bot(profile, proxy, option, use_proxy):
    bot = GoogleBot(profile, proxy, option, use_proxy)
    bot.start()


def main():
    print("Main Menu:")
    print("1. Start Multiple Bots")
    print("2. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        use_proxy_option = input("Do you want to use proxy? (yes/no): ")
        use_proxy = use_proxy_option.lower() == "yes"
        proxy_list = load_proxy_list() if use_proxy else [None]
        hidden_option = input("Do you want all bots hidden? (yes/no): ")
        option = "--headless" if hidden_option.lower() == "yes" else "None"
        
        num_bots = len(proxy_list)  # إذا لم يتم استخدام بروكسي، سيكون هناك عنصر واحد فقط في القائمة
        threads = []
        for i in range(num_bots):  # تشغيل عدد المثيلات بناءً على طول proxy_list
            pathprofile = f"profile{i}"
            proxy = proxy_list[i % len(proxy_list)]
            t = threading.Thread(target=run_bot, args=(pathprofile, proxy, option, use_proxy))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()  # الانتظار حتى اكتمال كل الخيوط
    elif choice == '2':
        print("Exiting the program. Goodbye!")
    else:
        print("Invalid choice. Please try again.")
# ... [بقية الكود كما هو]

if __name__ == "__main__":
    Printool()
    install_and_check_libraries()
    write_check_status_to_file("The scan was completed successfully.")
    print_pretty_message("#The scan was completed successfully\nAll libraries are available.")
    print_system_info()
    main()