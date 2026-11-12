from zipfile import ZipFile, ZIP_STORED
from kitapkontrol.checker import check_epub


def make_epub(path):
    container = """<?xml version="1.0"?>
    <container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
      <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
    </container>"""
    opf = """<?xml version="1.0"?>
    <package xmlns="http://www.idpf.org/2007/opf" version="3.0">
      <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>Örnek Kitap</dc:title><dc:language>tr</dc:language><dc:identifier>urn:test:1</dc:identifier>
      </metadata>
      <manifest><item id="chapter" href="chapter.xhtml" media-type="application/xhtml+xml"/></manifest>
      <spine><itemref idref="chapter"/></spine>
    </package>"""
    with ZipFile(path, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=ZIP_STORED)
        z.writestr("META-INF/container.xml", container)
        z.writestr("OEBPS/content.opf", opf)
        z.writestr("OEBPS/chapter.xhtml", "<html xmlns='http://www.w3.org/1999/xhtml'><body>Merhaba</body></html>")


def test_valid_minimal_epub_has_no_errors(tmp_path):
    path = tmp_path / "valid.epub"
    make_epub(path)
    report = check_epub(path)
    assert report.errors == 0


def test_missing_file_is_reported(tmp_path):
    report = check_epub(tmp_path / "missing.epub")
    assert report.errors == 1
    assert report.findings[0].code == "FILE_NOT_FOUND"


def test_invalid_zip_is_reported(tmp_path):
    path = tmp_path / "bad.epub"
    path.write_text("not a zip")
    report = check_epub(path)
    assert report.findings[0].code == "INVALID_ZIP"
