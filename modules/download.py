import os
import sys
import wget
import requests
import multiprocessing
from modules.FileManager import FileManager

def run_process(id, url, path):
    if 'ftp' in url:
        wget.download(url, path)
    else:        
        r = requests.get(url, allow_redirects=True)
        open('{}{}.fasta'.format(path, id), 'wb').write(r.content)
    

def parser_url(ncbi_id):
    url_list = []
    for filename in ncbi_id:
        if '_genomic.fna.gz' in filename: #download chromosome
            id = filename.split('_genomic.fna.gz')[0]
            gcf = id.split('_')[0]
            second = id.split('_')[1]
            number = second.split('.')[0]
            letter = '/'.join(number[i:i+3] for i in range(0, len(number), 3))                   
            url = "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/{gcf}/{letter}/{id}/{filename}".format(gcf=gcf, letter=letter, id=id, filename=filename) 
            url_list.append(url)
        else: #download plasmid                  
            url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={id}&rettype=fasta'.format(id=filename)
            url_list.append(url)
    return url_list


def download(path, ncbi_id, url_list): 

    db_dir = path + '/db/'
    db_dir = FileManager.handle_output_directory(db_dir)
    max_pool_size = 3 #API rate limit exceeded, can't go higher
    cpus = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cpus if cpus < max_pool_size else max_pool_size)
    for id, url in zip(ncbi_id, url_list):
        pool.apply_async(run_process, args=(id, url, db_dir))
    pool.close()    
    pool.join()  

    file_path = db_dir + '/*'
    db_path = path + '/db.fna.gz'
    os.system('cat {} > {}'.format(file_path, db_path)) 
    return db_path