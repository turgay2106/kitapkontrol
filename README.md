# KitapKontrol

[![Tests](https://github.com/USERNAME/kitapkontrol/actions/workflows/tests.yml/badge.svg)](https://github.com/USERNAME/kitapkontrol/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**KitapKontrol**, EPUB 2/3 dosyalarının temel yapısını ve sık görülen paketleme hatalarını kontrol eden açık kaynaklı, hafif bir komut satırı aracıdır.

> Bu araç bir EPUB doğrulama standardının (ör. EPUBCheck) yerine geçmez. Hızlı ön kontrol ve geliştirici iş akışı için tasarlanmıştır.

## Özellikler

- EPUB ZIP yapısını ve `mimetype` dosyasını kontrol eder.
- `container.xml` üzerinden OPF paket dosyasını bulur.
- Başlık, dil ve benzersiz tanımlayıcı gibi temel metadata alanlarını denetler.
- Manifest dosyalarının gerçekten pakette bulunup bulunmadığını kontrol eder.
- Spine girdilerinin manifestte tanımlı olup olmadığını denetler.
- Makine tarafından okunabilir JSON çıktı verebilir.
- Türkçe ve İngilizce raporlar üretir.

## Kurulum

Python 3.10 veya üzeri gerekir.

```bash
git clone https://github.com/USERNAME/kitapkontrol.git
cd kitapkontrol
python -m pip install -e .
```

## Kullanım

```bash
kitapkontrol kitap.epub
kitapkontrol kitap.epub --language en
kitapkontrol kitap.epub --json
```

Sorun bulunursa komut `1`, temiz sonuçta `0` çıkış kodu verir.

## Örnek çıktı

```text
KitapKontrol — rapor
Dosya: ornek.epub
[OK] EPUB mimetype dosyası mevcut ve ilk sırada.
[OK] Paket dosyası bulundu.
[UYARI] OPF içinde dil metadata alanı eksik.
Sonuç: 1 hata, 1 uyarı
```

## Geliştirme

```bash
python -m pip install -e ".[dev]"
pytest
```

Katkı göndermeden önce [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını okuyun. Hata bildirimleri ve özellik önerileri için GitHub Issues kullanın.

## Yol haritası

- [ ] Daha kapsamlı EPUB 3 navigation kontrolleri
- [ ] Erişilebilirlik metadata kontrolleri
- [ ] HTML içindeki bozuk yerel bağlantıların tespiti
- [ ] GitHub Actions ile örnek EPUB dosyalarının sürekli kontrolü
- [ ] Türkçe hata mesajları ve dokümantasyon iyileştirmeleri

## Lisans

MIT. Ayrıntılar için [LICENSE](LICENSE) dosyasına bakın.
