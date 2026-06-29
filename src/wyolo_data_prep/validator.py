import os
import yaml
import cv2
import argparse
from pathlib import Path

def check_yolo_dataset(dataset_path: str, task_type: str = "detect") -> dict:
    """
    Validates a YOLO dataset based on the task type (detect, segment, classify).
    """
    path_obj = Path(dataset_path)
    
    if task_type == "classify":
        if not path_obj.is_dir():
            return {"valid": False, "error": f"For classification, dataset must be a directory: {dataset_path}"}
        
        train_dir = path_obj / 'train'
        val_dir = path_obj / 'val'
        
        if not train_dir.exists() or not train_dir.is_dir():
            return {"valid": False, "error": f"Missing 'train' directory in {dataset_path}"}
        if not val_dir.exists() or not val_dir.is_dir():
            return {"valid": False, "error": f"Missing 'val' directory in {dataset_path}"}
            
        classes = [d.name for d in train_dir.iterdir() if d.is_dir()]
        return {
            "valid": True,
            "task": "classify",
            "classes": len(classes),
            "names": classes,
            "train_path": str(train_dir)
        }
    else:
        # For detect and segment, dataset_path should be a YAML file
        if not path_obj.exists() or not path_obj.is_file():
            return {"valid": False, "error": f"YAML file not found or is not a file: {dataset_path}"}
            
        try:
            with open(dataset_path, 'r') as f:
                data = yaml.safe_load(f)
                
            base_dir = path_obj.parent
            
            # Check required fields
            for field in ['train', 'val', 'nc', 'names']:
                if field not in data:
                    return {"valid": False, "error": f"Missing required field in YAML: {field}"}
                    
            # Sample check: verify train path exists
            train_path_str = data['train']
            if isinstance(train_path_str, str):
                train_path = base_dir / train_path_str if not Path(train_path_str).is_absolute() else Path(train_path_str)
                if not train_path.exists():
                    return {"valid": False, "error": f"Train path does not exist: {train_path}"}
                
            return {
                "valid": True,
                "task": task_type,
                "classes": data['nc'],
                "names": data['names'],
                "train_path": str(train_path) if isinstance(train_path_str, str) else "multiple/complex paths"
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}

def augment_dataset(image_dir: str, output_dir: str):
    """
    Placeholder for albumentations dataset balancing.
    """
    pass

def main():
    parser = argparse.ArgumentParser(description="Validate YOLO dataset")
    parser.add_argument("--yaml", required=True, help="Path to dataset.yaml")
    args = parser.parse_args()
    result = check_yolo_dataset(args.yaml)
    print(result)

if __name__ == "__main__":
    main()
