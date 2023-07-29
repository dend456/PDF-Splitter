import pathlib
import sys
import PyPDF2 as pdf
import tqdm

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: pdfsplitter <file>')
        sys.exit(1)

    file = pathlib.Path(sys.argv[1])
    if not file.exists():
        print(f'Input file {file} does not exist.')
        sys.exit(1)

    if not file.is_file():
        print(f'Input file cannot be a folder.')
        sys.exit(1)

    try:
        reader = pdf.PdfReader(file)
    except pdf.errors.PdfReadError as e:
        print(f'Input file {file} is either not a PDF file or is corrupt.')
        sys.exit(1)

    folder = file.parent
    filename = file.stem

    new_path = folder / filename
    new_path.mkdir(exist_ok=True)

    with tqdm.tqdm(total=len(reader.pages)) as prog_bar:
        for i, page in enumerate(reader.pages):
            writer = pdf.PdfWriter()
            writer.add_page(page)
            with open(new_path / pathlib.Path(f'{i}.pdf'), 'wb') as out:
                writer.write(out)
            prog_bar.update(1)
