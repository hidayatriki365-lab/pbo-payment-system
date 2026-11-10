from core.base import PaymentMethod
from plugins.transfer_bank import TransferBank

# Eksperimen A: ABC tidak boleh diinstansiasi langsung
try:
    PaymentMethod("uji")
except TypeError as e:
    print("Error yang diharapkan:", e)
    
# Eksperimen B: subclass yang belum lengkap (bayar() belum ada)
class Setengah(PaymentMethod):
    def validasi(self, jumlah):
        return True
    
    
try:
    Setengah("uji")
except TypeError as e:
    print("Error yang diharapkan:", e)
    
# Eksperimen C: subclass lengkap berjalan normal
transfer = TransferBank(saldo=500_000, bank="BCA")
print("ID transaksi:", transfer.proses(150_000))
print("Saldo sisa  :", transfer.saldo)

from core.protocols import Notifier
from core.notifiers import ConsoleNotifier, EmailNotifier, WhatsAppNotifier, TelegramNotifier

class TanpaKirim:
    """Kelas ini sengaja tidak punya method kirim()."""
    
daftar = [
    ConsoleNotifier(),
    EmailNotifier(),
    WhatsAppNotifier(),
    TelegramNotifier(),
    TanpaKirim(),
]
for n in daftar:
    cocok = isinstance(n, Notifier)
    print(f"{type(n).__name__:<16} memenuhi Notifier? {cocok}")
    TelegramNotifier().kirim("08123456789", "Pengujian notifikasi Telegram")
    
from core.notifiers import ConsoleNotifier, EmailNotifier
from core.processor import PaymentProcessor
from plugins.ewallet import EWallet
from plugins.transfer_bank import TransferBank

email = "andi@utr.ac.id"
pemroses = PaymentProcessor(ConsoleNotifier())
pemroses.checkout(TransferBank(saldo=1_000_000), 250_000, email)
pemroses.checkout(EWallet(saldo=100_000), 150_000, email)

# Ganti kanal notifikasi tanpa mengubah PaymentProcessor
pemroses.notifier = EmailNotifier()
dana = EWallet(saldo=500_000, provider="DANA")
pemroses.checkout(dana, 300_000, email)

# Objek yang bukan Notifier harus ditolak
try:
    PaymentProcessor(notifier="bukan notifier")
except TypeError as e:
    print("Error:", e)    
    
from core.notifiers import ConsoleNotifier
from core.processor import PaymentProcessor
from core.registry import buat_metode, daftar_plugin
from core.utils import rupiah
from plugins import muat_semua_plugin

def main() -> None:
    muat_semua_plugin()
    print("Plugin terdaftar:", daftar_plugin())
    print("-" * 60)
    
    pemroses = PaymentProcessor(ConsoleNotifier())
    
    skenario = [
        ("transfer", {"saldo": 1_000_000, "bank": "BCA"}, 250_000),
        ("ewallet", {"saldo": 100_000}, 150_000),
        ("ewallet", {"saldo": 5_000_000}, 2_500_000),
        ("qris", {}, 50_000),
    ]
    for kode, parameter, jumlah in skenario:
        try:
            metode = buat_metode(kode, **parameter)
        except KeyError as err:
            print("[PERINGATAN]", err)
            continue
        pemroses.checkout(metode, jumlah, pelanggan="mahasiswa@utr.ac.id")
    print("-" * 60)
    print("Riwayat transaksi berhasil:")
    for trx_id, nama, jumlah, biaya_admin, total in pemroses.riwayat:
        print(f" {trx_id} | {nama} | "
              f" jumlah: {rupiah(jumlah)} | "
              f"Admin: {rupiah(biaya_admin)} | "
              f"Total: {rupiah(total)}")
if __name__ == "__main__":
    main()    