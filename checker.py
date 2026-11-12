"""Basic structural checks for EPUB archives."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile
import posixpath
import xml.etree.ElementTree as ET


@dataclass
class Finding:
    level: str
    code: str
    message: str


@dataclass
class Report:
    file: str
    findings: list[Finding]

    @property
    def errors(self) -> int:
        return sum(item.level == "ERROR" for item in self.findings)

    @property
    def warnings(self) -> int:
        return sum(item.level == "WARNING" for item in self.findings)

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "errors": self.errors,
            "warnings": self.warnings,
            "findings": [asdict(item) for item in self.findings],
        }


def _tag(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _find_child(parent: ET.Element, name: str):
    return next((child for child in parent.iter() if _tag(child) == name), None)


def _add(findings: list[Finding], level: str, code: str, message: str) -> None:
    findings.append(Finding(level, code, message))


def check_epub(path: str | Path) -> Report:
    path = Path(path)
    findings: list[Finding] = []

    if not path.exists() or not path.is_file():
        _add(findings, "ERROR", "FILE_NOT_FOUND", "EPUB dosyası bulunamadı.")
        return Report(str(path), findings)

    try:
        archive = ZipFile(path)
    except (BadZipFile, OSError):
        _add(findings, "ERROR", "INVALID_ZIP", "Dosya geçerli bir ZIP/EPUB arşivi değil.")
        return Report(str(path), findings)

    with archive:
        names = archive.namelist()
        name_set = set(names)

        if "mimetype" not in name_set:
            _add(findings, "ERROR", "MIMETYPE_MISSING", "mimetype dosyası eksik.")
        else:
            if names[0] != "mimetype":
                _add(findings, "WARNING", "MIMETYPE_ORDER", "mimetype arşivde ilk sırada değil.")
            try:
                if archive.read("mimetype").decode("utf-8").strip() != "application/epub+zip":
                    _add(findings, "ERROR", "MIMETYPE_VALUE", "mimetype içeriği beklenen değer değil.")
            except Exception:
                _add(findings, "ERROR", "MIMETYPE_READ", "mimetype dosyası okunamadı.")

        container_path = "META-INF/container.xml"
        if container_path not in name_set:
            _add(findings, "ERROR", "CONTAINER_MISSING", "META-INF/container.xml dosyası eksik.")
            return Report(str(path), findings)

        try:
            container = ET.fromstring(archive.read(container_path))
        except (ET.ParseError, KeyError):
            _add(findings, "ERROR", "CONTAINER_XML_INVALID", "container.xml okunamıyor veya XML biçimi hatalı.")
            return Report(str(path), findings)

        rootfile = next((e for e in container.iter() if _tag(e) == "rootfile"), None)
        opf_path = rootfile.attrib.get("full-path") if rootfile is not None else None
        if not opf_path:
            _add(findings, "ERROR", "OPF_PATH_MISSING", "container.xml içinde rootfile full-path bulunamadı.")
            return Report(str(path), findings)
        if opf_path not in name_set:
            _add(findings, "ERROR", "OPF_MISSING", f"Paket dosyası bulunamadı: {opf_path}")
            return Report(str(path), findings)

        try:
            package = ET.fromstring(archive.read(opf_path))
        except ET.ParseError:
            _add(findings, "ERROR", "OPF_XML_INVALID", "OPF paket dosyası geçerli XML değil.")
            return Report(str(path), findings)

        metadata = _find_child(package, "metadata")
        if metadata is None:
            _add(findings, "ERROR", "METADATA_MISSING", "OPF metadata bölümü eksik.")
        else:
            for field, code in (("title", "TITLE_MISSING"), ("language", "LANGUAGE_MISSING"), ("identifier", "IDENTIFIER_MISSING")):
                if _find_child(metadata, field) is None or not (_find_child(metadata, field).text or "").strip():
                    _add(findings, "WARNING", code, f"Metadata alanı eksik veya boş: {field}")

        manifest = _find_child(package, "manifest")
        manifest_ids: set[str] = set()
        if manifest is None:
            _add(findings, "ERROR", "MANIFEST_MISSING", "OPF manifest bölümü eksik.")
        else:
            opf_dir = posixpath.dirname(opf_path)
            for item in manifest:
                if _tag(item) != "item":
                    continue
                item_id = item.attrib.get("id")
                href = item.attrib.get("href")
                if item_id:
                    manifest_ids.add(item_id)
                if not href:
                    _add(findings, "ERROR", "MANIFEST_HREF_MISSING", "Manifest girdisinde href eksik.")
                    continue
                normalized = posixpath.normpath(posixpath.join(opf_dir, href))
                if normalized not in name_set:
                    _add(findings, "ERROR", "MANIFEST_FILE_MISSING", f"Manifest dosyası arşivde bulunamadı: {href}")

        spine = _find_child(package, "spine")
        if spine is None:
            _add(findings, "ERROR", "SPINE_MISSING", "OPF spine bölümü eksik.")
        else:
            for itemref in spine:
                if _tag(itemref) == "itemref":
                    idref = itemref.attrib.get("idref")
                    if not idref or idref not in manifest_ids:
                        _add(findings, "ERROR", "SPINE_REFERENCE_INVALID", f"Spine referansı manifestte yok: {idref or '(boş)'}")

    if not findings:
        _add(findings, "INFO", "NO_ISSUES", "Temel yapısal kontrollerde sorun bulunmadı.")
    return Report(str(path), findings)
