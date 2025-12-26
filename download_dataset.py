from pathlib import Path
import shutil
import kagglehub

dataset_path = Path(kagglehub.dataset_download("vinothkannaece/sales-dataset"))
target_dir = Path(__file__).resolve().parent / "data"
target_dir.mkdir(parents=True, exist_ok=True)
shutil.copytree(dataset_path, target_dir, dirs_exist_ok=True)
print(f"Dataset available at {target_dir}")