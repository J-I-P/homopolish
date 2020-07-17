import numpy as np
import pandas as pd
from Bio import SeqIO

def todf(draft, db_np, path):
    
    nuc_dict = {0:'A',1:'T',2:'C',3:'G'} 
    record = SeqIO.read(draft, "fasta")
    genome_size = len(record)
    np_arr = np.load(db_np)  

    arr, coverage, ins = np_arr['arr'], np_arr['coverage'], np_arr['ins']

    position = []
    draft = []
    A, T, C , G = [], [], [], []
    gap = []
    ins_A, ins_T, ins_C, ins_G = [], [], [], []
    homo = []
    cov = []
    
    insertion = np.where(ins != 0)[0]
    for i in np.unique(insertion):
        i = int(i)
        for j in range(4):
            count = 0
            if ins[i][j].any() != 0:
                position.append(i)
                draft.append('-')
                A.append(0)
                T.append(0)
                C.append(0)
                G.append(0)
                gap.append(0)
                ins_A.append(ins[i][j][0])
                ins_T.append(ins[i][j][1])
                ins_C.append(ins[i][j][2])
                ins_G.append(ins[i][j][3])
                cov.append(coverage[i])
                index = np.argmax(ins[i][j])
                temp = i
                while i + 1 < genome_size and record[i+1] == nuc_dict.get(index):
                    count += 1
                    i += 1
                i = temp
                while record[i] and record[i] == nuc_dict.get(index):
                    count += 1
                    i -= 1
                i = temp
                homo.append(count)
                
    deletion = np.where(arr[:,4]!=0)[0]
    for i in deletion:
        i = int(i)
        count = 0
        position.append(i)
        draft.append(record[i])
        A.append(arr[i][0])
        T.append(arr[i][1])
        C.append(arr[i][2])
        G.append(arr[i][3])
        gap.append(arr[i][4])
        ins_A.append(0)
        ins_T.append(0)
        ins_C.append(0)
        ins_G.append(0)
        cov.append(coverage[i])

        index = i
        nuc = record[i]
        while i + 1 < genome_size and record[i+1] == nuc:
            count += 1
            i += 1
        i = index
        while record[i] and record[i] == nuc:
            count += 1
            i -= 1
        i = index

        homo.append(count)
    
             
    dict = {"position": position,
            "draft": draft,
            "A": A,
            "T": T,
            "C": C,
            "G": G,
            "gap": gap,
            "Ins_A": ins_A,
            "Ins_T": ins_T,
            "Ins_C": ins_C,
            "Ins_G": ins_G,
            "coverage": cov,
            "homopolymer": homo
        }
    df_path = path + '/{}.feather'.format(record.id)
    df = pd.DataFrame(dict)
    df.to_feather(df_path)    
    return df_path