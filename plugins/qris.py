from core.base import PaymentMethod
from core.registry import register_plugin
from core.utils import buat_id


@register_plugin("qris")
class QRIS(PaymentMethod):
    BATAS_TRANSAKSI = 5_000_000
    
    def __init__(self, merchant: str = "Kantin Kampus"):
        super().__init__(f"QRIS {merchant}")
        
    def validasi(self, jumlah: float) -> bool:
        ...  # TODO: terima jika jumlah tidak melebihi BATAS_TRANSAKSI
        return 0 < jumlah <= self.BATAS_TRANSAKSI
    
    def bayar(self, jumlah: float) -> str:
        ...  # TODO: kembalikan ID transaksi berawalan "QRS"
        return buat_id("QRS")