from abc import ABC, abstractmethod
from numpy.random import randint
import string

# KULLANICI İŞLEMLERİ

class KullaniciIslemleri:
    #hesap işlemlerinin yöneltildiği sınıf
    
    _kullanicilar = {}
    
    def __init__(self, kullanici_ad = "", kullanici_soyad ="", kullanici_sifre = "", kullanici_id = None, bakiye = 0):
        self._kullanici_ad = kullanici_ad
        self._kullanici_soyad = kullanici_soyad
        self._kullanici_sifre = kullanici_sifre
        self._kullanici_id = kullanici_id if kullanici_id is not None else self._generate_unique_id()
        self._bakiye = bakiye

    def _generate_unique_id(self):
        new_id = randint(35000,50000)
        while new_id in KullaniciIslemleri._kullanicilar:
            new_id = randint(35000,50000)
        return new_id
    
    @property
    def kullanici_id(self):
        return self._kullanici_id

    @property
    def bakiye(self):
        return self._bakiye
    @bakiye.setter
    def bakiye(self, value):
        self._bakiye = value
    @classmethod
    def kullanici_ekle(cls, kullanici_obj):
        cls._kullanicilar[kullanici_obj.kullanici_id] = {
            "kullanici_adi": kullanici_obj._kullanici_ad,
            "kullanici_soyadi": kullanici_obj._kullanici_soyad,
            "kullanici_sifre": kullanici_obj._kullanici_sifre,
            "bakiye": kullanici_obj._bakiye
        }
    
    @classmethod
    def kullanici_sil(cls, kullanici_id):
        if kullanici_id in cls._kullanicilar:
            del cls._kullanicilar[kullanici_id]
            print("Kullanici silindi")
        else: 
            print("Hesap bulunamadı")
    
    @classmethod
    def kullanicilari_getir(cls):
        return cls._kullanicilar
    
    def hesap_olustur(self):
        self._kullanici_ad = input("\nKullanıcı adını giriniz: ")
        self._kullanici_soyad = input("Kullanıcı soyadını giriniz: ")
        self._kullanici_sifre = input("Kullanıcı şifresini giriniz: ")
        self._kullanici_id = self._generate_unique_id()
        self._bakiye = 0  
        KullaniciIslemleri.kullanici_ekle(self)
        print("Kullanıcı eklendi")
        Menu.giris()
        
    def hesap_dogrula(self):
        ad = input("\nKullanıcı adınızı giriniz: ")
        for kullanici_id, bilgiler in KullaniciIslemleri._kullanicilar.items():
            if bilgiler["kullanici_adi"] == ad:
                sifre = input("Sifresinizi giriniz: ")
                if bilgiler["kullanici_sifre"] == sifre:
                    print("Giriş başarılı")
                    return bilgiler, kullanici_id
                else:
                    print("Şifre hatalı")
                    return None, None
        print("Kullanıcı adı hatalı")
        return None, None

class Islemler(ABC):
    """
    SOYUT SINIF HER İŞLEM İÇİN EXECUTE METHODU TANIMLANMAILIDIR
    """
    def __init__(self, account):
        self.account = account
        
    def execute(self):
        pass

class ParaCekme(Islemler):
    def execute(self):
        if self.account.bakiye <= 0:
            print("\nBakiyeniz yetersiz")
        else:
            try:
                tutar = int(input("Çekmek istediğiniz tutarı giriniz: ")) 
                if tutar > self.account.bakiye:
                    print("Bakiyeniz yetersiz")
                else:
                    self.account.bakiye -= tutar
                    KullaniciIslemleri._kullanicilar[self.account.kullanici_id]["bakiye"] = self.account.bakiye

                    print(f"Çekilen tutar: {tutar}\nGüncel bakiyeniz: {self.account.bakiye}")
            except ValueError:
                print("Lütfen geçerli bir sayı giriniz")              

class ParaYatir(Islemler):
    def execute(self):
        try:
            tutar = int(input("\nYatırmak istediğiniz tutarı yazınız: "))
            self.account.bakiye += tutar
            KullaniciIslemleri._kullanicilar[self.account.kullanici_id]["bakiye"] = self.account.bakiye
            print(f"Güncel bakiyeniz: {self.account.bakiye}")
        except ValueError:
            print("Lütfen geçerli bir sayı giriniz")

class BakiyeSorgu(Islemler):
    def execute(self):
        print(f"\nŞu an {self.account.bakiye} TL'niz bulunmakta")

class ParaTransferi(Islemler):
    def execute(self):
        while True:
            try:
                print("Sistemde kayıtlı kişiler: " + ", ".join(
                f"{user_id}:{user_info['kullanici_adi']}" 
                for user_id, user_info in KullaniciIslemleri._kullanicilar.items()
                ))
                target_id = int(input("\nLütfen para transferi yapmak istediğiniz kişinin ID'sini giriniz (Çıkmak için -1): "))
                if target_id == -1:
                    break
                elif target_id in KullaniciIslemleri.kullanicilari_getir():
                    tutar = int(input("\nLütfen göndermek istediğiniz miktarı yazınız: "))
                    if tutar > self.account.bakiye:
                        print("Bakiyeniz yetersiz") 
                        continue
                    KullaniciIslemleri._kullanicilar[target_id]["bakiye"] += tutar
                    self.account.bakiye -= tutar
                    KullaniciIslemleri._kullanicilar[self.account.kullanici_id]["bakiye"] = self.account.bakiye

                    print(f"Güncel bakiyeniz: {self.account.bakiye}")
                    break
                else: 
                    print("ID bulunamadı")    
            except ValueError:
                print("Lütfen geçerli bir sayı giriniz")

class HesapIslemleri(KullaniciIslemleri):
    def __init__(self, bilgiler, kullanici_id):
        super().__init__(
            kullanici_ad = bilgiler["kullanici_adi"],
            kullanici_soyad=bilgiler["kullanici_soyadi"],
            kullanici_sifre=bilgiler["kullanici_sifre"],
            kullanici_id=kullanici_id,
            bakiye=bilgiler["bakiye"]
        )
    def para_cek(self):
        islem = ParaCekme(self)
        islem.execute()
    def para_yatir(self):
        islem = ParaYatir(self)
        islem.execute()

    def para_transferi(self):
        islem = ParaTransferi(self)
        islem.execute()
    def bakiye_sorgu(self):
        islem = BakiyeSorgu(self)
        islem.execute()
class Menu:
    """
    Kullanıcı etkileşimi olan kısım.
    """
    @staticmethod
    def giris():
        try:
            secim = int(input("""
Lütfen yapmak istediğiniz işlemi seçiniz:

1. Yeni hesap oluştur 
2. Var olan hesaba giriş yap 
3. Çıkış yap

Seçiminiz: """))
            if secim == 1:
                kullanici.hesap_olustur()
            elif secim == 2:
                bilgiler, kullanici_id = kullanici.hesap_dogrula()
                if bilgiler:
                    hesap_islem = HesapIslemleri(bilgiler, kullanici_id)
                    Menu.hesap_menu(hesap_islem)
            elif secim == 3:
                exit()
            else:
                print("Geçersiz seçim!")
                Menu.giris()
        except ValueError:
            print("Geçersiz giriş, lütfen sayı giriniz!")
            Menu.giris()
    @staticmethod
    def hesap_menu(hesap_islem):
        while True:
            try:
                secim = int(input("""
Yapmak istediğiniz işlemi seçiniz:

1. Para çekme
2. Para yatırma
3. Para transferi
4. Bakiye sorgulama
5. Ana Menü
6. Çıkış

Seçiminiz: """))
                if secim == 1:
                    hesap_islem.para_cek()
                elif secim == 2:
                    hesap_islem.para_yatir()
                elif secim == 3:
                    hesap_islem.para_transferi()
                elif secim == 4:
                    hesap_islem.bakiye_sorgu()
                elif secim == 5:
                    print("Ana menüye dönülüyor...")
                    Menu.giris()
                elif secim == 6:
                    print("Çıkış yapılıyor...")
                    exit()
                else:
                    print("Hatalı işlem! \n")
            except ValueError:
                print("Lütfen geçerli bir sayı giriniz!")
                
    @classmethod
    def aktarım(cls, data):
        #ileride dosyadan veri aktarımı olursa diye yazdım
        return cls(data)          
            
kullanici = KullaniciIslemleri()

if __name__ == "__main__":
    Menu.giris()      
