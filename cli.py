"""Command-line interface."""
import argparse
import json
import sys

from .checker import check_epub


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="kitapkontrol",
        description="EPUB dosyaları için temel yapısal ön kontrol."
    )
    parser.add_argument("file", help="Kontrol edilecek .epub dosyası")
    parser.add_argument("--json", action="store_true", help="JSON raporu yazdır")
    parser.add_argument("--language", choices=("tr", "en"), default="tr",
                        help="Rapor dili (şimdilik kodlar ve rapor yapısı ortaktır)")
    args = parser.parse_args()

    report = check_epub(args.file)
    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print("KitapKontrol — report" if args.language == "en" else "KitapKontrol — rapor")
        print(f"Dosya: {report.file}")
        for finding in report.findings:
            label = {"ERROR": "HATA", "WARNING": "UYARI", "INFO": "BİLGİ"}.get(finding.level, finding.level)
            print(f"[{label}] {finding.message}")
        print(f"Sonuç: {report.errors} hata, {report.warnings} uyarı")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
