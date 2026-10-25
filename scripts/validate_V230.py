#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter
import json,hashlib,subprocess,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist'
class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.refs=[];self.radios=[];self.lang=None;self.canonicals=[];self.descriptions=[];self.titles=[];self.in_title=False;self.jsons=[];self.capture=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if 'id' in a:self.ids.append(a['id'])
        for key in ('href','src'):
            if key in a:self.refs.append(a[key])
        if tag=='input' and a.get('type')=='radio':self.radios.append(a)
        if tag=='link' and a.get('rel')=='canonical':self.canonicals.append(a['href'])
        if tag=='meta' and a.get('name')=='description':self.descriptions.append(a['content'])
        if tag=='title':self.in_title=True
        if tag=='script' and a.get('type') in ('application/json','application/ld+json'):self.capture=''
    def handle_data(self,data):
        if self.in_title:self.titles.append(data)
        if self.capture is not None:self.capture+=data
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
        if tag=='script' and self.capture is not None:self.jsons.append(json.loads(self.capture));self.capture=None

def run():
    master=json.loads((ROOT/'content/master_V230.json').read_text());config=json.loads((ROOT/'site_config_V230.json').read_text())
    units=master['units'];assert len(units)==135
    paths={};titles=[];references=0;question_count=0
    for file in DIST.rglob('*.html'):
        if file.name.startswith('google') and file.read_text().strip()==f'google-site-verification: {file.name}':continue
        p=Page();p.feed(file.read_text());paths[file.resolve()]=p
        assert p.lang=='en-GB',file
        assert len(p.ids)==len(set(p.ids)),('duplicate HTML ids',file)
        assert len(p.descriptions)==len(p.canonicals)==1,file
        assert p.descriptions[0] and p.titles,file
        titles.append(''.join(p.titles))
        assert all(x['url'].startswith(config['site_url']) for x in p.jsons if '@context' in x),file
        if p.radios:
            assert len(p.radios)==18 and all('required' in x for x in p.radios),file
            assert set(Counter(x['name'] for x in p.radios).values())=={3},file
            question_count+=6
    assert len(titles)==len(set(titles))
    for file,p in paths.items():
        for ref in p.refs:
            s=urlsplit(ref)
            if s.scheme or s.netloc:continue
            target=(DIST/unquote(s.path).lstrip('/')) if s.path.startswith('/') else (file.parent/unquote(s.path))
            if not s.path:target=file
            if target.is_dir():target=target/'index.html'
            assert target.exists(),('broken link',file,ref)
            if s.fragment and target.suffix=='.html':assert unquote(s.fragment) in paths[target.resolve()].ids,(file,ref)
            references+=1
    hashes=[];durations=Counter();audio_count=0
    for u in units:
        p=DIST/u['audio']['src'].lstrip('/')
        digest=hashlib.sha256(p.read_bytes()).hexdigest();assert digest==u['audio']['sha256']
        assert hashlib.sha256(u['transcript'].encode()).hexdigest()==u['audio']['transcriptSha256']
        assert p.stat().st_size<25*1024*1024
        duration=float(json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(p)]))['format']['duration'])
        assert abs(duration-u['audio']['durationSeconds'])<.25
        durations[u['level']]+=duration;audio_count+=1
        hashes.append({'path':u['audio']['src'],'sha256':digest,'bytes':p.stat().st_size,'durationSeconds':duration})
        file=DIST/f'the-last-letter/{u["level"].lower()}/chapter-{u["chapter"]}/part-{u["part"]}/index.html'
        embedded=next(x for x in paths[file.resolve()].jsons if x.get('id')==u['id'])
        assert embedded['transcript']==u['transcript'] and embedded['questions']==u['questions']
    assert question_count==810
    assert audio_count==135 and len(list((DIST/'assets/audio').glob('*.mp3')))==135
    tree=ET.parse(DIST/'sitemap.xml');urls=[x.text for x in tree.findall('.//{*}loc')]
    assert len(urls)==189 and len(urls)==len(set(urls))
    for url in urls:assert (DIST/urlsplit(url).path.lstrip('/')/'index.html').exists()
    learning=json.loads(subprocess.check_output(['node',str(ROOT/'scripts/check_learning_V230.mjs')]))
    subprocess.run(['node','--check',str(DIST/'assets/reader.mjs')],check=True)
    source_bytes=sum(x.stat().st_size for x in DIST.rglob('*') if x.is_file())
    result={'version':'V230','status':'PASS','htmlPagesIncluding404':len(paths),'sitemapURLs':len(urls),'localReferencesChecked':references,'audioFiles':audio_count,'questions':question_count,'durationSecondsByLevel':dict(durations),'durationSecondsTotal':sum(durations.values()),'largestAssetBytes':max(x.stat().st_size for x in DIST.rglob('*') if x.is_file()),'staticTotalBytes':source_bytes,'staticFileCount':sum(1 for x in DIST.rglob('*') if x.is_file()),'learningChecks':learning,'audioDecodeValidation':'All 135 decoded successfully during input ZIP validation in this session; unchanged SHA-256 verified here.','browserVisualQA':'Not performed: browser QA capability unavailable in managed environment.','auditoryReview':'Pilot accepted; full production listening not completed.','deployment':'Not deployed; desired hostname availability unverified.','ads':'Inactive; template hooks only.'}
    (ROOT/'validation/validation_V230.json').write_text(json.dumps(result,indent=2))
    (ROOT/'validation/audio_manifest_V230.json').write_text(json.dumps(hashes,indent=2))
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
