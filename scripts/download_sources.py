"""Download official CMS sources and record an immutable acquisition manifest.
Run from any directory with Python 3: python3 scripts/download_sources.py
Existing snapshots are never overwritten.
"""
import csv, hashlib, io, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
IDS = ['xubh-q36u', 'yv7e-xc69']
API = 'https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items/'
def fetch(url):
    output = subprocess.check_output(['curl', '-sSL', '--fail', '--max-time', '90', '-w', '\n%{url_effective}', url])
    raw, effective_url = output.rsplit(b'\n', 1)
    return raw, effective_url.decode('utf-8')
def main():
    stamp = datetime.now(timezone.utc)
    folder = ROOT/'data/raw'/stamp.strftime('%Y%m%dT%H%M%S%fZ')
    folder.mkdir(parents=True, exist_ok=False)
    manifest = {'acquired_at_utc':stamp.isoformat(), 'datasets':[], 'dictionary':None}
    dictionaries = set()
    for identifier in IDS:
        meta_bytes, metadata_url = fetch(API+identifier)
        meta = json.loads(meta_bytes)
        (folder/f'{identifier}_metadata.json').write_bytes(meta_bytes)
        dist = next(d for d in meta['distribution'] if d.get('mediaType')=='text/csv')
        raw, resolved = fetch(dist['downloadURL'])
        name = dist['downloadURL'].rsplit('/',1)[1]
        (folder/name).write_bytes(raw)
        text = raw.decode('utf-8-sig')
        reader = csv.reader(io.StringIO(text, newline=''))
        headers = next(reader)
        count = sum(1 for _ in reader)
        manifest['datasets'].append({'identifier':identifier,'title':meta['title'],
            'source_page':meta['landingPage'],'metadata_url':metadata_url,
            'release_date':meta.get('released'),'modified_date':meta.get('modified'),
            'download_url':dist['downloadURL'],'resolved_download_url':resolved,
            'filename':name,'sha256':hashlib.sha256(raw).hexdigest(),
            'bytes':len(raw),'encoding':'utf-8-sig','row_count':count,'columns':headers})
        dictionaries.add(dist['describedBy'])
    if len(dictionaries)!=1:
        raise RuntimeError('Source datasets reference different dictionaries; inspect before proceeding.')
    dictionary_url = dictionaries.pop()
    pdf, resolved = fetch(dictionary_url)
    if not pdf.startswith(b'%PDF-'):
        raise RuntimeError('Dictionary download is not a PDF')
    (folder/'HOSPITAL_Data_Dictionary.pdf').write_bytes(pdf)
    manifest['dictionary']={'download_url':dictionary_url,'resolved_download_url':resolved,
        'filename':'HOSPITAL_Data_Dictionary.pdf','sha256':hashlib.sha256(pdf).hexdigest(),
        'bytes':len(pdf),'version':'Inspect PDF title; supplied by both dataset metadata records'}
    releases={d['release_date'] for d in manifest['datasets']}
    manifest['same_release_date']=len(releases)==1
    (folder/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    docs=ROOT/'docs'; docs.mkdir(exist_ok=True)
    (docs/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'snapshot_directory':str(folder),'manifest':manifest},indent=2))
if __name__=='__main__':
    main()
