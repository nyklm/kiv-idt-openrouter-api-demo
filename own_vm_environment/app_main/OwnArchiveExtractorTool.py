
# Knihovna pro jednotnou extrakci ZIP, RAR a 7z archivu
# - reseni Zip-slip utoku a moznost vyberu pripon extrahovanych souboru.
# - POZOR: testovan pouze ZIP a neslo instalovat knihovnu pro 7z !!!

# ZIP by mel byt primo v Pythonu, pro RAR a 7z je potreba doinstalovat:
# pip install rarfile py7zr

from pathlib import Path
import zipfile
import rarfile # nyni netestovano, ale melo by fungovat
# import py7zr  # vyzaduje build, ktery mi na Windows neprochazi

class OwnArchiveExtractorTool:
    SUPPORTED = (".zip", ".rar", ".7z", ".7za")

    @staticmethod
    def extract(archive_path, out_dir=None, allowed_extensions=[]):
        '''
        Extrahuje archiv do urceneho adresare.
        :param archive_path: Cesta k archivu.
        :param out_dir: Cesta k vystupnimu adresari. Pokud neni zadano, vytvori se adresar se jmenem archivu bez pripony. (def.=None)
        :param allowed_extensions: Povolene pripony souboru pro extrakci (def.=[] - vsechny).
        '''
        # kontrola cesty k archivu a povolenych pripon extrahovanych souboru
        archive_path = Path(archive_path).resolve()
        if allowed_extensions:
            allowed_extensions = tuple(ext.lower() for ext in allowed_extensions)

        if not archive_path.exists():
            raise FileNotFoundError(archive_path)

        if archive_path.suffix.lower() not in OwnArchiveExtractorTool.SUPPORTED:
            raise ValueError(f"Nepodporovaný formát: {archive_path.suffix}")

        # vystupni adresar bud zadany, nebo dle nazvu archivu bez pripony
        out_dir = Path(out_dir) if out_dir else archive_path.with_suffix("")
        out_dir.mkdir(parents=True, exist_ok=True)

        # rozbaleni archivu dle typu
        suffix = archive_path.suffix.lower()
        if suffix == ".zip":
            OwnArchiveExtractorTool._extract_zip(archive_path, out_dir, allowed_extensions)
        elif suffix == ".rar":
            OwnArchiveExtractorTool._extract_rar(archive_path, out_dir, allowed_extensions)
        elif suffix == ".7z":
            OwnArchiveExtractorTool._extract_7z(archive_path, out_dir, allowed_extensions)

        # vraceni cesty k vystupnimu adresari
        return out_dir

    @staticmethod
    def _extract_zip(path, out_dir, allowed_extensions=[]):
        # pro ZIP extrahujeme pouze zvolene soubory a kontrolujeme Zip-Slip
        with zipfile.ZipFile(path) as z:
            # projdu obsah archivu
            for info in z.infolist():
                # pokud neni povolena pripona, preskocim
                if (allowed_extensions != []
                    and allowed_extensions is not None
                    and not info.filename.lower().endswith(allowed_extensions)
                ):
                    continue
                # kontrola Zip-Slip
                target = out_dir / info.filename
                try:
                    target.resolve().relative_to(out_dir.resolve())
                except ValueError:
                    raise Exception(f"ZIP Zip-Slip útok: {info.filename}")
                # extrahuji soubor do jeho adresare, pokud je uveden
                target.parent.mkdir(parents=True, exist_ok=True)
                with z.open(info) as src, open(target, "wb") as dst:
                    print(target)
                    dst.write(src.read())

    @staticmethod
    def _extract_rar(path, out_dir, allowed_extensions=[]):
        with rarfile.RarFile(path) as r:
            for info in r.infolist():
                # pokud neni povolena pripona, preskocim
                if (allowed_extensions != []
                    and allowed_extensions is not None
                    and not info.filename.lower().endswith(allowed_extensions)
                ):
                    continue
                # kontrola Zip-Slip
                target = out_dir / info.filename
                try:
                    target.resolve().relative_to(out_dir.resolve())
                except ValueError:
                    raise Exception(f"ZIP Zip-Slip útok: {info.filename}")
                # extrahuji soubor do jeho adresare, pokud je uveden
                target.parent.mkdir(parents=True, exist_ok=True)
                with r.open(info) as src, open(target, "wb") as dst:
                    print(target)
                    dst.write(src.read())

    @staticmethod
    def _extract_7z(path, out_dir, allowed_extensions=[]):
        with py7zr.SevenZipFile(path, mode="r") as z:
            for name, bio in z.readall().items():
                # pokud neni povolena pripona, preskocim
                if (allowed_extensions != []
                        and allowed_extensions is not None
                        and not name.lower().endswith(allowed_extensions)
                ):
                    continue
                # kontrola Zip-Slip
                target = out_dir / info.filename
                try:
                    target.resolve().relative_to(out_dir.resolve())
                except ValueError:
                    raise Exception(f"ZIP Zip-Slip útok: {info.filename}")
                # extrahuji soubor do jeho adresare, pokud je uveden
                target.parent.mkdir(parents=True, exist_ok=True)
                with open(target, "wb") as f:
                    print(target)
                    f.write(bio.read())

    #########################################

    @staticmethod
    def compress_directory_to_zip(compress_dir_path, output_zip_file_path):
        '''
        Komprimuje obsah adresare do ZIP archivu.
        :param compress_dir_path: Adresar, ktery bude komprimovan.
        :param output_zip_file_path: Cesta k vystupnimu ZIP souboru.
        '''
        compress_dir_path = Path(compress_dir_path).resolve()
        output_zip_file_path = Path(output_zip_file_path).resolve()

        if not compress_dir_path.is_dir():
            raise ValueError(f"{compress_dir_path} není adresář")

        root_name = compress_dir_path.name

        with zipfile.ZipFile(output_zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for path in compress_dir_path.rglob("*"):
                # relativne k adresari, ktery komprimujeme
                arcname = Path(root_name) / path.relative_to(compress_dir_path)
                zipf.write(path, arcname)


#################################################

# Priklad pouziti:
# OwnArchiveExtractorTool.extract("data.zip")
# OwnArchiveExtractorTool.extract("backup.rar", "out/backup")
# OwnArchiveExtractorTool.extract("logs.7z")
# OwnArchiveExtractorTool.compress_directory_to_zip("output_dir", "output_dir.zip")
