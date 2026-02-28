"""Create a soft mapping from project data/sequences_jpg to external KITTI sequences path.

Usage (Windows PowerShell/CMD examples):
  python scripts/create_data_softlink.py --source "F:\\kitti_00_10\\dataset\\sequences"

Usage (Linux/macOS):
  python scripts/create_data_softlink.py --source /mnt/kitti_00_10/dataset/sequences
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


def ensure_link(target: Path, source: Path, force: bool = False) -> None:
    if target.exists() or target.is_symlink():
        if target.is_symlink() and target.resolve() == source.resolve():
            print(f"Already linked: {target} -> {source}")
            return
        if not force:
            raise FileExistsError(
                f"Target already exists: {target}. Use --force to remove and recreate."
            )
        if target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        else:
            target.unlink()

    target.parent.mkdir(parents=True, exist_ok=True)

    # Windows: directory symlink usually requires admin/dev mode;
    # junction is more robust for normal users.
    if os.name == "nt":
        cmd = f'mklink /J "{target}" "{source}"'
        status = os.system(f'cmd /c {cmd}')
        if status != 0:
            raise OSError("Failed to create junction with mklink /J")
    else:
        os.symlink(source, target, target_is_directory=True)

    print(f"Created link: {target} -> {source}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="External KITTI sequences directory")
    parser.add_argument(
        "--target",
        default="data/sequences_jpg",
        help="Project directory to map (default: data/sequences_jpg)",
    )
    parser.add_argument("--force", action="store_true", help="Replace existing target")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    target = Path(args.target).expanduser().resolve()

    if not source.exists() or not source.is_dir():
        print(f"Invalid source path: {source}", file=sys.stderr)
        return 1

    ensure_link(target=target, source=source, force=args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
