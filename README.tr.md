# KitapKontrol

KitapKontrol, EPUB 2/3 dosyalarının temel yapısını ve sık görülen paketleme hatalarını denetleyen açık kaynaklı bir komut satırı aracıdır.

**Amaç:** Bağımsız yazarların, yayınevlerinin ve e-kitap geliştiricilerinin EPUB dosyalarını yayımlamadan önce hızlıca kontrol edebilmesi.

## Kurulum

Python 3.10+ gerekir.

```bash
git clone https://github.com/USERNAME/kitapkontrol.git
cd kitapkontrol
python -m pip install -e .
```

## Kullanım

```bash
kitapkontrol kitap.epub
kitapkontrol kitap.epub --json
kitapkontrol kitap.epub --language en
```

Hata yoksa çıkış kodu `0`, hata varsa `1` olur.

## Neleri kontrol eder?

- EPUB dosyasının ZIP yapısını
- `mimetype` dosyasının varlığını ve ilk sırada olmasını
- `META-INF/container.xml` ve OPF paket dosyasını
- Başlık, dil ve benzersiz tanımlayıcı metadata alanlarını
- Manifestte listelenen dosyaların varlığını
- Spine referanslarının manifestte tanımlı olmasını

Bu araç EPUBCheck'in yerine geçmez; hızlı ön kontrol aracıdır.

## Test

```bash
python -m pip install -e ".[dev]"
pytest
```

Katkı için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bakın.
