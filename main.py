from src.Bot_Twic import GoogleBot
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
import shutil
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
            subprocess.check_call(
                [python, "-m", "pip", "install", lib], stdout=subprocess.DEVNULL
            )
            console.print(f"[green]{lib} It was installed successfully.[/green]")
    else:
        console.print("[green]All libraries are already installed.[/green]")


def write_check_status_to_file(status):
    filepath = os.path.join("data", "check_status.txt")
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
        "Script version": "First Edition Version",
    }

    console.print("[bold magenta]معلومات النظام:[/bold magenta]")
    for key, value in info.items():
        console.print(f"{key}: [bold cyan]{value}[/bold cyan]")


# تشغيل الفحوصات وطباعة الرسالة
def load_proxy_list():
    proxy_file_path = os.path.join("data", "Proxy.txt")
    with open(proxy_file_path, "r") as file:
        return [line.strip() for line in file]


# ... [بقية الكود الخاص بـ GoogleBot]


def check_proxy_and_account_file_length():
    proxy_list = load_proxy_list()
    auth_tokens = load_auth_tokens()

    if len(proxy_list) != len(auth_tokens):
        raise ValueError(
            f"The number of proxies ({len(proxy_list)}) does not match the number of auth tokens ({len(auth_tokens)})."
        )

    return proxy_list, auth_tokens


# ... [بقية الكود كما هو]


def load_auth_tokens():
    token_path = os.path.join("data", "twitchaccount.txt")
    with open(token_path, "r") as file:
        return [line.strip() for line in file]


def run_bot(profile_id, proxy, option, use_proxy, token):
    bot = GoogleBot(profile_id, proxy, option, use_proxy, token)
    bot.start()

def setup_and_run_profiles():
    auth_tokens = load_auth_tokens()
    token_groups = [auth_tokens[i:i + 4] for i in range(0, len(auth_tokens), 4)]

    for index, group in enumerate(token_groups):
        print(f"Group {index + 1} (Profiles {index * 4 + 1} to {index * 4 + len(group)})")

    group_choice = int(input("Choose a group by number: "))
    if 1 <= group_choice <= len(token_groups):
        selected_group = token_groups[group_choice - 1]
        threads = []
        for i in range(len(selected_group)):
            profile_id = f"Profile_{group_choice * 4 - 4 + i + 1}"
            bot = GoogleBot(profile_id, None, None, False, selected_group[i])
            thread = threading.Thread(target=bot.setup_profile)
            threads.append(thread)
            thread.start()

        # انتظار انتهاء جميع الخيوط
        for thread in threads:
            thread.join()
    else:
        print("Invalid group choice. Please try again.")
def delete_all_profiles(profiles_directory):
    """
    تحذف جميع البروفايلات الموجودة داخل مجلد البروفايلات المحدد.

    :param profiles_directory: مسار مجلد البروفايلات.
    """
    try:
        # تحقق مما إذا كان المجلد موجود
        if not os.path.exists(profiles_directory):
            console.print(f"لم يتم العثور على مجلد البروفايلات: {profiles_directory}", style="bold yellow")
            return

        # حذف محتويات المجلد
        for filename in os.listdir(profiles_directory):
            file_path = os.path.join(profiles_directory, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        
        console.print(f"تم حذف جميع البروفايلات بنجاح من {profiles_directory}.", style="bold green")

    except Exception as e:
        console.print(f"حدث خطأ أثناء حذف البروفايلات: {e}", style="bold red")

def main():
    print("Main Menu:")
    print("1. Start Multiple Bots")
    print("2. Exit")
    print("3. Delete All Profiles")  # إضافة خيار حذف البروفايلات
    print("4. Setup Profiles")  # إضافة الخيار الجديد

    choice = input("Enter your choice: ")

    if choice == "1":
        multiplayer = input("Multiplayer operation (yes/no): ")
        if multiplayer.lower() == "yes":
            auth_tokens = load_auth_tokens()
            # تقسيم الرموز إلى مجموعات مع تحديد عدد البروفايلات في كل مجموعة
            token_groups = [auth_tokens[i:i + 4] for i in range(0, len(auth_tokens), 4)]

            for index, group in enumerate(token_groups):
                # عرض المجموعات وعدد البروفايلات المستخدمة
                print(f"Group {index + 1} (Profiles {index * 4 + 1} to {index * 4 + len(group)}): {group}")

            group_choice = int(input("Choose a group by number: "))
            if 1 <= group_choice <= len(token_groups):
                selected_group = token_groups[group_choice - 1]
                threads = []
                for i, token in enumerate(selected_group):
                    profile_id = f"Profile_{group_choice * 4 - 4 + i + 1}"  # تحديد البروفايلات بناءً على المجموعة المختارة
                    thread = threading.Thread(target=run_bot, args=(profile_id, None, None, False, token))
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()
            else:
                print("Invalid group choice. Please try again.")

        # ... [الكود الحالي للخيار 'no' والخيارات الأخرى]
    elif choice == "2":
        print("Exiting the program. Goodbye!")
    elif choice == "3":
        delete_all_profiles()  # تشغيل دالة حذف البروفايلات
    elif choice == "4":
        setup_and_run_profiles()  # تشغيل دالة إعداد البروفايلات
    else:
        print("Invalid choice. Please try again.")


# ... [بقية الكود كما هو]

if __name__ == "__main__":
    # Printool()
    # install_and_check_libraries()
    # write_check_status_to_file("The scan was completed successfully.")
    # print_pretty_message("#The scan was completed successfully\nAll libraries are available.")
    print_system_info()
    main()
