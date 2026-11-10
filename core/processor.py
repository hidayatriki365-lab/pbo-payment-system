from core.base import PaymentMethod, PembayaranGagal
from core.protocols import Notifier
from core.utils import rupiah


class PaymentProcessor:
    """Memproses checkout tanpa peduli metode bayar dan kanal notifikasi."""
    
    def __init__(self, notifier: Notifier):
        if not isinstance(notifier, Notifier):
            raise TypeError(
                "notifier harus memiliki method kirim(penerima, pesan)"
            )
        self.notifier = notifier
        self.riwayat: list[tuple[str, str, float]] = []
        
    def checkout(
        self, metode: PaymentMethod, jumlah: float, pelanggan: str
    ) -> bool:
        try:
            biaya_admin = metode.biaya_admin(jumlah)
            total = jumlah + biaya_admin 
            trx_id = metode.proses(jumlah)
        except PembayaranGagal as err:
            self.notifier.kirim(pelanggan, f"Pembayaran gagal: {err}")
            return False
        
        self.riwayat.append((trx_id, metode.nama, jumlah, biaya_admin, total))
        self.notifier.kirim(
            pelanggan,
            f"Pembayaran {metode.nama} berhasil. "
            f"Jumlah: Rp{jumlah:,.0f}, "
            f"Biaya admin: Rp{biaya_admin:,.0f}, "
            f"Total: Rp{total:,.0f}"
        )
        return True