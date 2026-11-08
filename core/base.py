from abc import ABC, abstractmethod
from core.utils import rupiah

class PembayaranGagal(Exception):
    """Dilempar saat pembayaran ditolak atau tidak valid."""
    
class PaymentMethod(ABC):
    """Kontrak (abstract base class) untuk semua pembayaran."""
    
    def __init__(self, nama: str):
        self.nama = nama
        
    @abstractmethod
    def validasi(self, jumlah: float) -> bool:
        """Periksa apakah pembayaran dapat di proses."""
        
    @abstractmethod
    def bayar(self, jumlah: float) -> str:
        """Prosess pembayaran, lalu kembali ID transaksi."""
    
    def proses(self, jumlah: float) -> str:
        """Template method: urutan langkah di jaga oleh kelas induk."""
        if jumlah <= 0:
            raise PembayaranGagal("Jumlah pembayran harus lebih dari 0")
        if not self.validasi(jumlah):
            raise PembayaranGagal(
                f"{self.nama} menolak pembayaran {rupiah(jumlah)}"
            )  
        return self.bayar(jumlah)                   