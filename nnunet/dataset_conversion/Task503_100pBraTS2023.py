from genericpath import isdir, isfile
import numpy as np
from collections import OrderedDict
from batchgenerators.utilities.file_and_folder_operations import *
from nnunet.paths import nnUNet_raw_data
import SimpleITK as sitk
import shutil
import os
from batchgenerators.utilities.file_and_folder_operations import subdirs, subfiles, join, maybe_mkdir_p

print("hello")
if __name__ == "__main__":
    """
    REMEMBER TO CONVERT LABELS BACK TO BRATS CONVENTION AFTER PREDICTION!
    """
    
    task_name = "Task503_100pBraTS2023"
    downloaded_data_dir = "/home/aiotlabws/SonDinh/nnUNet_raw_data/Task503_100pBraTS2023/imagesTr"

    target_base = join(nnUNet_raw_data, task_name)
    target_imagesTr = join(target_base, "imagesTr")
    target_labelsTs = join(target_base, "labelsTs")
    target_imagesTs = join(target_base, "imagesTs")
    target_labelsTr = join(target_base, "labelsTr")

    maybe_mkdir_p(target_imagesTr)
    maybe_mkdir_p(target_labelsTs)
    maybe_mkdir_p(target_imagesTs)
    maybe_mkdir_p(target_labelsTr)
    
    # Chuyen doi ten sang dung Form TRAIN
    patient_names = []
    cur = join(downloaded_data_dir)
    
    for p in subfiles(cur, join=False):
        filename = p
        base = filename.split('.')[0]  # Lấy phần trước dấu chấm đầu tiên ("BraTS-PED-00002-000")

        # Bước 2: Tách chuỗi bởi dấu gạch ngang
        parts = base.split('-')  # ["BraTS", "PED", "00002", "000"]

        # Bước 3: Ghép lại chỉ lấy "BraTS" và "00002"
        p = parts[0] + '_' + parts[2] 
        print(p)
        patdir = join(cur, p)
        patient_name = p
        patient_names.append(patient_name + "_0000")

        '''
        t1 = join(patdir, p + "_t1.nii.gz")
        t1c = join(patdir, p + "_t1ce.nii.gz")
        t2 = join(patdir, p + "_t2.nii.gz")
        flair = join(patdir, p + "_flair.nii.gz")
        seg = join(patdir, p + "_seg.nii.gz")

        assert all([
            isfile(t1),
            isfile(t1c),
            isfile(t2),
            isfile(flair),
            isfile(seg)
        ]), "%s" % patient_name'''
    
        shutil.copy(join(cur,filename), join(target_imagesTr, p + "_0000.nii.gz"))

        
        shutil.copy(join("/home/aiotlabws/SonDinh/nnUNet_raw_data/Task503_100pBraTS2023/labelsTr",filename), join(target_labelsTr, p + ".nii.gz"))
        
    
    # Chuyen doi ten sang dung Form TEST
    downloaded_data_dir_test = "/home/aiotlabws/SonDinh/nnUNet_raw_data/Task503_100pBraTS2023/imagesTs"
    patient_namesTs = []
    cur = join(downloaded_data_dir_test)
    if isdir(downloaded_data_dir_test):
        for p in subfiles(downloaded_data_dir_test, join=False):
            filename = p
            base = filename.split('.')[0]  # Lấy phần trước dấu chấm đầu tiên ("BraTS-PED-00002-000")

            # Bước 2: Tách chuỗi bởi dấu gạch ngang
            parts = base.split('-')  # ["BraTS", "PED", "00002", "000"]

            # Bước 3: Ghép lại chỉ lấy "BraTS" và "00002"
            p = parts[0] + '_' + parts[2] 
            print(p)
            patdir = join(downloaded_data_dir_test, p)
            patient_name = p
            patient_namesTs.append(patient_name + "_0000")

            '''
            t1 = join(patdir, p + "_t1.nii.gz")
            t1c = join(patdir, p + "_t1ce.nii.gz")
            t2 = join(patdir, p + "_t2.nii.gz")
            flair = join(patdir, p + "_flair.nii.gz")

            assert all([
                isfile(t1),
                isfile(t1c),
                isfile(t2),
                isfile(flair),
            ]), "%s" % patient_name
            print("hello2")
            shutil.copy(t1, join(target_imagesTs, patient_name + "_0000.nii.gz"))
            shutil.copy(t1c, join(target_imagesTs, patient_name + "_0001.nii.gz"))
            shutil.copy(t2, join(target_imagesTs, patient_name + "_0002.nii.gz"))
            shutil.copy(flair, join(target_imagesTs, patient_name + "_0003.nii.gz"))'''
            
            shutil.copy(join(cur,filename), join(target_imagesTs, p + "_0000.nii.gz"))

            
            shutil.copy(join("/home/aiotlabws/SonDinh/nnUNet_raw_data/Task503_100pBraTS2023/labelsTs",filename), join(target_labelsTs, p + ".nii.gz"))

    json_dict = OrderedDict()
    json_dict['name'] = "1pBraTS2023"
    json_dict['description'] = "Pediatric high-grade glioma segmentation"
    json_dict['tensorImageSize'] = "4D"
    json_dict['reference'] = "BraTS 2023 Challenge"
    json_dict['licence'] = "CC-BY-SA 4.0"
    json_dict['release'] = "1.0 2023"
    json_dict['modality'] = {
        "0": "FLAIR"
    }
    json_dict['labels'] = {
        "0": "background",
        "1": "ET",
        "2": "NC",
        "3": "ED"
    }
    json_dict['numTraining'] = len(patient_names)
    json_dict['numTest'] = len(patient_namesTs)
    json_dict['training'] = [{'image': "./imagesTr/%s.nii.gz" % i, "label": "./labelsTr/%s.nii.gz" % i.rsplit('_', 1)[0]} for i in patient_names]
    json_dict['test'] =  [{'image': "./imagesTs/%s.nii.gz" % i, "label": "./labelsTs/%s.nii.gz" % i.rsplit('_', 1)[0]} for i in patient_namesTs]
    #, "label": "./labelsTs/%s.nii.gz" % i
    
    save_json(json_dict, join(target_base, "dataset.json"))
