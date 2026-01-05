import xgboost as xgb
import json
import numpy as np
import pandas as pd
from ..schemas.houses import HousePredictionInputSchema

class ModelService:
    def __init__(self, model_path: str, metadata_path: str):
        self.model = xgb.Booster()
        self.model.load_model(model_path)
        
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
        
        self.features = self.metadata['features']
        self.binary_map = self.metadata['binary_mapping']
        self.furnish_cats = self.metadata['expected_furnish_categories']
        # Safe access to stats
        self.stats = self.metadata.get('stats', {})

    def predict(self, input_data: HousePredictionInputSchema) -> float:
        # 1. Outlier check (Only if stats exist in metadata)
        if self.stats and 'area_max' in self.stats:
            if input_data.area > self.stats['area_max'] * 2:
                raise ValueError(f"Area {input_data.area} is too large for this model.")

        data_dict = input_data.model_dump()
        
        # 2. Transform Binary Fields
        binary_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
        for col in binary_cols:
            data_dict[col] = self.binary_map[data_dict[col]]
        
        # 3. Reconstruct One-Hot Columns
        status = data_dict.pop('furnishingstatus')
        for cat in self.furnish_cats:
            col_name = f"furnish_{cat}"
            data_dict[col_name] = 1 if status == cat else 0
            
        # 4. Ensure columns are in the EXACT order
        feature_values = [data_dict[feat] for feat in self.features]
        
        # 5. Inference
        final_input = xgb.DMatrix([feature_values], feature_names=self.features)
        log_prediction = self.model.predict(final_input)
        
        # DEBUG: Look at your terminal when you click 'Execute'
        print(f"---> Raw Model Output (Log Scale): {log_prediction[0]}")
        
        # 6. Inverse Log Transform
        actual_price = np.expm1(log_prediction[0])
        
        print(f"---> Converted Price: {actual_price}")
        
        return float(actual_price)

model_services = ModelService(
    model_path='models/house_model.json',
    metadata_path='models/model_metadata.json'
)