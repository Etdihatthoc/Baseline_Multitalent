
**CHÚ Ý LABEL**
   Label: 

   1 - ET

   2 - NC

   3 - ED

   TC = ET + NC = 1 + 2
   
   WT = ET + NC + ED = 1 + 2 + 3

**Set up thí nghiệm**

1. Clone github [https://github.com/Etdihatthoc/Baseline\_Multitalent](https://github.com/Etdihatthoc/Baseline\_Multitalent)  
2. Tải dataset từ Drive [https://drive.google.com/drive/folders/1-BUUsbTUX\_XsZIBWgO-EuDt8jCp0hoCf?usp=sharing](https://drive.google.com/drive/folders/1-BUUsbTUX\_XsZIBWgO-EuDt8jCp0hoCf?usp=sharing)  lưu vào folder cùng cấp với MultiTalent  
3. Tạo môi trường ảo, install các package :   
   cd MultiTalent  
   pip install \-U .  
4. Tại tmux, active môi trường, setup bằng lệnh:  
     
   export nnUNet\_raw\_data\_base="/media/nnUNet\_raw\_data\_base"  
   export nnUNet\_preprocessed="/media/nnunet\_preprocessed"  
   export RESULTS\_FOLDER="/media/nnUNet\_trained\_models"  
   export MASTER_ADDR="222.252.4.232"                                             
   export MASTER_PORT="9000"
   export WORLD_SIZE=1
   export RANK=0
     
5. Xem laị file MultiTalent/nnunet/experiment_planning/experiment_planner_baseline_3DUNet_v21.py của package nnUNet xem self.unet_base_num_features = 30 chưa, nếu chưa sửa lại
1. Tái cấu trúc dữ liệu  
- python nnunet/dataset\_conversion/Task500\_1pBraTS2023.py  
- python nnunet/dataset\_conversion/Task501\_10pBraTS2023.py  
- python nnunet/dataset\_conversion/Task502\_50pBraTS2023.py  
- python nnunet/dataset\_conversion/Task503\_100pBraTS2023.py  
2. Preprocessing  
- nnUNet\_plan\_and\_preprocess \-t 500  
- nnUNet\_plan\_and\_preprocess \-t 501  
- nnUNet\_plan\_and\_preprocess \-t 502  
- nnUNet\_plan\_and\_preprocess \-t 503

**TRAINING**
   
CUDA_VISIBLE_DEVICES=1 python -m torch.distributed.launch --master_port=9000 ./nnunet/run/run_training_DDP.py 3d_fullres nnUNetTrainerV2_DDP 502 all -pretrained_weights media/nnUNet_trained_models/nnUNet/3d_fullres/Task100_MultiTalent/MultiTalent_trainer_ddp_2000ep__MultiTalent_bs4/all/model_final_checkpoint.model

Trong đó:

- CUDA\_VISIBLE\_DEVICES=1: chọn device nhưng mà hơi ngược nên check xem chạy đúng device chưa  
- 502 : task, anh có thể set là 502 (50%) hoặc 503 (100%)  
- all : ( ko cần thay đổi)
- --master_port: thay đổi tùy server

Nếu train tiếp với lastest checkpoint: CUDA_VISIBLE_DEVICES=1 python -m torch.distributed.launch ./nnunet/run/run_training_DDP.py 3d_fullres nnUNetTrainerV2_DDP 502 all -c

Xem tiến trình train ở: media/nnUNet\_trained\_models/nnUNet/3d\_fullres

**EVALUATION ON TEST SET**

1. Predict Test set

nnUNet_predict -i $nnUNet_raw_data_base/nnUNet_raw_data/Task500_1pBraTS2023/imagesTs -o test_evaluation/Task500_1pBraTS2023 -t 500 -m 3d_fullres -tr nnUNetTrainerV2_DDP -f all

- -i, -o : input, output dir nên chỉ cần thay đổi keyword "Task500_1pBraTS2023" => "Task502_50pBraTS2023" (50%) or "Task503_100pBraTS2023" (100%)
- -t 500 : task, anh có thể set là 502 (50%) hoặc 503 (100%)

2. Evaluation 

 nnUNet_evaluate_folder -pred test_evaluation/Task500_1pBraTS2023 -ref media/nnUNet_raw_data_base/nnUNet_raw_data/Task500_1pBraTS2023/labelsTs -l 0 1 2 3

- -pred, -ref : predict, label dir nên chỉ cần thay đổi keyword "Task500_1pBraTS2023" => "Task502_50pBraTS2023" (50%) or "Task503_100pBraTS2023" (100%)
- -l 0 1 2 3: các label dùng để predict không cần đổi

Xem kết quả tại: test_evaluation/Task500_1pBraTS2023/summary.json