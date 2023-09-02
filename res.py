import subprocess
import time

def run_bot():
    while True:
        try:
            # Botunuzu başlatan komutu buraya girin
            subprocess.run(["python", "bot.py"])

        except Exception as e:
            print(f"Hata oluştu: {e}")

        print("Kod durdu, 5 saniye sonra yeniden başlatılacak.")
        time.sleep(5)  # 5 saniye bekleyin ve yeniden başlatın

if __name__ == "__main__":
    run_bot()
