import pathlib


vendor_dir = pathlib.Path(f'{__file__}').parent / 'vendor'


if __name__ == '__main__':
    print(vendor_dir)
