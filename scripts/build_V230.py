#!/usr/bin/env python3
"""Build the static, dependency-free LinguaNovels website from reviewed content."""
from pathlib import Path
from html import escape as esc
import json, hashlib, re
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
CONFIG=json.loads((ROOT/'site_config_V230.json').read_text())
BASE=CONFIG['site_url'].rstrip('/')
assert urlparse(BASE).scheme=='https' and urlparse(BASE).netloc
MASTER=json.loads((ROOT/'content/master_V230.json').read_text())
UNITS=MASTER['units']
LEVELS={'B1':('Find your flow','Clear language and an engaging mystery for intermediate learners.'),'B2':('Go a little deeper','Richer language and more detail for upper-intermediate learners.'),'C1':('Read between the lines','Nuanced language and a demanding listening experience for advanced learners.')}
PAGES=[]

def unit_url(u):return f"/the-last-letter/{u['level'].lower()}/chapter-{u['chapter']}/part-{u['part']}/"
def chapter_url(level,c):return f'/the-last-letter/{level.lower()}/chapter-{c}/'
def level_url(level):return f'/the-last-letter/{level.lower()}/'
def safe_json(x):return json.dumps(x,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
def button(text,url,secondary=False):return f'<a class="button{" secondary" if secondary else ""}" href="{esc(url)}">{esc(text)} <span aria-hidden="true">↗</span></a>'
def badge(level):return f'<span class="badge {level.lower()}">{level}</span>'
def minutes(u):return max(1,round(u['audio']['durationSeconds']/60))
def progress(units):
    # Retain the existing progress schema, including the original content hash.
    compact=[{k:u[k] for k in ('id','contentHash','questions')} for u in units]
    return f'<p class="small" data-progress-units="{esc(safe_json(compact),quote=True)}">Progress is saved in this browser.</p><div class="progress-bar" aria-hidden="true"><span id="progress-fill"></span></div>'

def write_page(path,title,description,body,kind='WebPage',breadcrumb=None):
    PAGES.append(path)
    url=BASE+path
    schema={'@context':'https://schema.org','@type':kind,'name':title,'description':description,'url':url,'inLanguage':'en-GB','isAccessibleForFree':True}
    html=f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script>document.documentElement.classList.add('js')</script>
<title>{esc(title)}</title><meta name="description" content="{esc(description,quote=True)}">
<link rel="canonical" href="{esc(url)}"><meta property="og:type" content="website"><meta property="og:title" content="{esc(title,quote=True)}"><meta property="og:description" content="{esc(description,quote=True)}"><meta property="og:url" content="{esc(url)}"><meta property="og:site_name" content="LinguaNovels"><meta name="theme-color" content="#153d36">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"><script type="application/ld+json">{safe_json(schema)}</script><script type="module" src="/assets/reader.mjs"></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="/" aria-label="LinguaNovels home">Lingua<em>Novels</em></a><nav aria-label="Main navigation"><a href="/the-last-letter/">The story</a><a class="optional" href="/how-it-works/">How it works</a><a class="nav-link" href="/the-last-letter/#levels">Start listening</a></nav></div></header>
<main id="main" class="wrap">{body}</main>
<footer class="site-footer"><div class="wrap footer-inner"><div><a class="brand" href="/">Lingua<em>Novels</em></a><p class="footer-note">A good story. A little English. Every day.</p></div><div class="footer-links"><a href="/about/">About</a><a href="/how-it-works/">How it works</a><a href="/privacy/">Privacy &amp; saved progress</a></div></div></footer></body></html>'''
    out=DIST/('index.html' if path=='/' else path.strip('/')+'/index.html')
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(html)

def crumbs(items):
    return '<div class="breadcrumb" aria-label="Breadcrumb">'+' <span aria-hidden="true">/</span> '.join(f'<a href="{esc(url)}">{esc(text)}</a>' if url else esc(text) for text,url in items)+'</div>'

def level_cards():
    return '<div class="level-grid">'+''.join(f'<a class="level-card" href="{level_url(level)}">{badge(level)}<h3>{title}</h3><p>{desc}</p><span class="small">15 chapters · 45 listening parts</span><span class="card-link">Explore {level} <span aria-hidden="true">→</span></span></a>' for level,(title,desc) in LEVELS.items())+'</div>'

def build_home():
    art='<div class="story-art" role="img" aria-label="An illustrated green cover of The Last Letter with a cream envelope"><div class="book"><span class="book-kicker">A LinguaNovels mystery</span><div class="book-title">The<br>Last Letter</div><div class="envelope"></div><small>Some stories refuse to stay buried.</small></div><span class="art-tag">One mystery. Three English levels.</span></div>'
    body=f'''<section class="hero"><div class="hero-copy"><p class="eyebrow">English practice, one story at a time</p><h1>Get lost in a story.<br>Find your English.</h1><p>Listen to a mystery, follow the clues and build your English along the way. Free stories with audio, vocabulary and instant feedback.</p><div class="hero-actions">{button('Choose your level','/the-last-letter/#levels')}{button('How it works','/how-it-works/',True)}</div><a class="small" id="resume" hidden href="/the-last-letter/">Continue your story</a><p class="small">B1 · B2 · C1 &nbsp; / &nbsp; No account needed</p></div>{art}</section>
<div class="facts"><span><strong>15</strong> chapters</span><span><strong>3</strong> English levels</span><span><strong>135</strong> listening parts</span><span><strong>100%</strong> free to explore</span></div>
<section class="section" id="levels"><div class="section-head"><div><p class="eyebrow">Your story starts here</p><h2>Choose your English level.</h2></div><p>The same mystery, adapted to three levels. Start where you feel comfortable and change whenever you like.</p></div>{level_cards()}</section>
<section class="story-band"><div><p class="eyebrow" style="color:#ddbc91">The Last Letter</p><h2>A letter. A missing woman.<br>A story unfinished.</h2><p>When journalist Emma Fraser receives a letter in familiar handwriting, a disappearance from fifteen years ago returns to her life. Follow her investigation through Scotland.</p></div>{button('Discover the story','/the-last-letter/')}</section>
<section class="section"><p class="eyebrow">Make English part of your day</p><h2>Listen. Think. Discover.</h2><div class="steps"><div class="step"><span>01</span><h3>Press play.</h3><p>Meet the key words, then listen to a short part of the story at your own pace.</p></div><div class="step"><span>02</span><h3>Follow the clues.</h3><p>Answer six multiple-choice questions. Get your score and an explanation for every answer.</p></div><div class="step"><span>03</span><h3>Read and return.</h3><p>Unlock the transcript after submitting. Your results stay in this browser, ready for your next visit.</p></div></div></section><template data-ad-slot="home-end"></template>'''
    write_page('/','LinguaNovels | Free English Listening Stories for B1, B2 & C1','Practise English with The Last Letter: a free mystery in B1, B2 and C1, with British English audio, transcripts and comprehension quizzes.',body)

def build_indexes():
    body=crumbs([('Home','/'),('The Last Letter',None)])+'<div class="page-intro"><p class="eyebrow">A mystery in fifteen chapters</p><h1>The Last Letter</h1><p>An unexpected envelope brings journalist Emma Fraser back to a missing-person case she covered fifteen years ago. Listen, read and follow the investigation at your level.</p><p class="small">British English audio · 3 parts per chapter · 6 questions per part</p></div><section id="levels">'+level_cards()+'</section>'
    write_page('/the-last-letter/','The Last Letter | English Listening Story | LinguaNovels','Explore a fifteen-chapter mystery with British English audio, vocabulary, transcripts and quizzes. Choose B1, B2 or C1.',body)
    for level in LEVELS:
        units=[u for u in UNITS if u['level']==level]
        body=crumbs([('Home','/'),('The Last Letter','/the-last-letter/'),(level,None)])+f'<div class="page-intro">{badge(level)}<h1>The Last Letter: {level} English</h1><p>{LEVELS[level][1]} Follow the story in order, with three short parts in each chapter.</p>{progress(units)}</div><div class="chapter-list">'
        for c in range(1,16):
            parts=[u for u in units if u['chapter']==c]
            body+=f'<article class="chapter-card"><span class="chapter-num">Chapter {c:02}</span><h2><a href="{chapter_url(level,c)}">{esc(parts[0]["title"])}</a></h2><div class="part-links">'+''.join(f'<a href="{unit_url(u)}">Part {u["part"]}</a>' for u in parts)+'</div></article>'
        write_page(level_url(level),f'{level} English Listening Practice – The Last Letter | LinguaNovels',f'Practise {level} English with 45 mystery-story listening parts, full transcripts, vocabulary and six comprehension questions per part.',body+'</div>')
        for c in range(1,16):
            parts=[u for u in units if u['chapter']==c]
            body=crumbs([('Home','/'),(level,level_url(level)),(f'Chapter {c}',None)])+f'<div class="page-intro"><p class="eyebrow">The Last Letter · {level}</p><h1>Chapter {c}: {esc(parts[0]["title"])}</h1><p>Listen to the three parts in order. Each part includes vocabulary, six questions and a transcript to review after answering.</p></div><div class="chapter-parts">'
            for u in parts:
                body+=f'<article class="part-card"><div><span class="eyebrow">Part {u["part"]}</span><h2>{esc(u["title"])}</h2><p class="small">About {minutes(u)} minutes of audio · 6 questions</p><span class="completed-note" data-completed="{u["id"]}"></span></div>{button("Listen to part "+str(u["part"]),unit_url(u))}</article>'
            body+='</div>'+progress(parts)
            write_page(chapter_url(level,c),f'{level} English Listening – Chapter {c}: {parts[0]["title"]} | LinguaNovels',f'Chapter {c} of The Last Letter in {level} English. Three listening parts with vocabulary, transcripts and automatically marked comprehension activities.',body)

def build_unit(u):
    level=u['level']; c=u['chapter']; p=u['part']
    body=crumbs([('Home','/'),(level,level_url(level)),(f'Chapter {c}',chapter_url(level,c)),(f'Part {p}',None)])
    body+=f'<header class="reader-heading"><div class="reader-meta">{badge(level)}<span>The Last Letter · Chapter {c} · Part {p}</span><span>About {minutes(u)} min</span></div><h1>{esc(u["title"])}</h1><p class="small">Listen first. Answer six questions. Then explore the transcript.</p></header><div class="reader-layout"><div>'
    vocab=''.join(f'<div><dt>{esc(v["term"])}</dt><dd>{esc(v["definition"])}</dd></div>' for v in u['vocabulary'])
    body+=f'<section class="reader-panel"><p class="eyebrow">01 · Before you listen</p><h2>A few words to know</h2><details><summary>Explore the vocabulary</summary><dl class="vocabulary">{vocab}</dl></details></section>'
    body+=f'<section class="reader-panel"><p class="eyebrow">02 · Listen to the story</p><h2>Follow the clues.</h2><audio id="audio" controls preload="none" aria-label="Chapter {c}, Part {p}, {level} audio"><source src="{u["audio"]["src"]}" type="audio/mpeg">Your browser does not support audio. <a href="{u["audio"]["src"]}">Download the MP3</a>.</audio><p id="audio-status" role="status" class="small"></p><div class="speed-control"><label for="speed">Playback speed</label><select id="speed"><option value="0.75">0.75×</option><option value="0.85">0.85×</option><option value="1" selected>1×</option><option value="1.1">1.1×</option><option value="1.25">1.25×</option></select></div></section>'
    body+='<section class="reader-panel"><p class="eyebrow">03 · Check your understanding</p><h2>What did you discover?</h2><p class="small">Choose one answer for each question. Submit all six to see your score and unlock the transcript.</p><noscript><p class="noscript">Enable JavaScript to mark your answers and save progress. The audio and transcript are available without it.</p></noscript><form id="questions">'
    for i,q in enumerate(u['questions'],1):
        body+=f'<fieldset data-question="{q["id"]}"><legend>{i}. {esc(q["prompt"])}</legend>'
        for o in q['options']:
            body+=f'<label class="answer"><input type="radio" name="{q["id"]}" value="{o["id"]}" required><span>{esc(o["text"])}</span></label>'
        body+='<p class="question-feedback"></p></fieldset>'
    body+='<div class="form-actions"><button class="button" type="submit">Check my answers</button><button class="button secondary" id="retry" type="button" hidden>Try again</button></div></form><p class="score" id="result" role="status" aria-live="polite" tabindex="-1"></p></section>'
    transcript=''.join(f'<p>{esc(p)}</p>' for p in u['transcript'].split('\n\n'))
    body+=f'<section class="reader-panel transcript" id="transcript" data-locked="true"><p class="eyebrow">04 · Read &amp; review</p><h2>The transcript</h2><p class="transcript-lock" id="transcript-lock">Submit all six answers to unlock the transcript. You can then listen and read together.</p><div class="transcript-body">{transcript}</div></section><template data-ad-slot="reader-end"></template>'
    ordered=[x for x in UNITS if x['level']==level];index=next(i for i,x in enumerate(ordered) if x['id']==u['id'])
    body+='<nav class="page-nav" aria-label="Story navigation">'
    body+=f'<a href="{unit_url(ordered[index-1])}">← Previous part</a>' if index else f'<a href="{level_url(level)}">← All chapters</a>'
    body+=f'<a href="{unit_url(ordered[index+1])}">Next part →</a>' if index+1<len(ordered) else f'<a href="{level_url(level)}">Story complete · All chapters →</a>'
    body+='</nav></div><aside class="reader-aside"><h2>Your story</h2><p>Choose a level</p><div class="level-switch">'
    for l in LEVELS:
        other=next(x for x in UNITS if x['chapter']==c and x['part']==p and x['level']==l)
        body+=f'<a href="{unit_url(other)}"'+(' aria-current="page"' if l==level else '')+'>'+badge(l)+'</a>'
    body+=f'</div><p>Chapter {c}</p><div class="aside-parts">'
    for part in range(1,4):
        other=next(x for x in ordered if x['chapter']==c and x['part']==part)
        body+=f'<a href="{unit_url(other)}"'+(' aria-current="page"' if part==p else '')+f'>Part {part} · {esc(other["title"])}</a>'
    body+=f'</div><a href="{level_url(level)}">All 15 chapters →</a><p class="small">Your submitted results are saved only in this browser.</p></aside></div>'
    body+=f'<script type="application/json" id="unit-data">{safe_json(u)}</script>'
    write_page(unit_url(u),f'{level} English Listening – Chapter {c}, Part {p}: {u["title"]} | LinguaNovels',f'Listen to {u["title"]}, chapter {c} part {p} of The Last Letter in {level} English. Practise with British English audio, vocabulary, six questions and a transcript.',''.join(body))

def build_info():
    pages={
    '/about/':('About LinguaNovels','Learn about LinguaNovels and its story-based approach to free English listening practice.','''<h1>A story worth returning to.</h1><p>LinguaNovels is an independent English-learning project built around original fiction. Instead of unrelated listening clips, you follow characters, notice clues and discover what happens next.</p><h2>Meet The Last Letter</h2><p>Our first story is a mystery set in Scotland. It has fifteen chapters, each divided into three parts, with adaptations at B1, B2 and C1. The characters and events are fictional.</p><h2>Designed for independent practice</h2><p>Each part brings together a short listening activity, vocabulary and six multiple-choice comprehension questions. Explanations help you review your answers. The transcript becomes available after you submit.</p><h2>About the audio and levels</h2><p>The narration uses a synthetic British English voice. The level labels are learning guides, not an official assessment or a guarantee of exam equivalence. All audio files have been checked technically; listening review of the complete production is still in progress.</p><p><a href="/the-last-letter/">Choose your level and begin the story →</a></p>'''),
    '/how-it-works/':('How It Works | LinguaNovels','Find out how to practise English with audio stories, vocabulary, six-question quizzes, transcripts and saved progress.','''<h1>A little practice.<br>A story that stays with you.</h1><h2>1. Choose your level</h2><p>B1 uses clearer language, B2 adds detail, and C1 offers a more demanding version. You can switch levels from any listening part. Start with the first chapter: the story unfolds in order.</p><h2>2. Explore the words and listen</h2><p>Open the vocabulary if you need support. Press play and listen as often as you like. Change the playback speed if that helps. Audio starts only when you choose to play it.</p><h2>3. Answer six questions</h2><p>Choose one option for every question and select “Check my answers”. You will see your score, the correct options and an explanation. Select “Try again” for a fresh attempt; your last submitted result stays saved until you submit again.</p><h2>4. Unlock the transcript</h2><p>After submitting all six answers, read the transcript and listen again. The transcript remains available when you return to a part with a saved result.</p><h2>5. Come back for the next part</h2><p>Progress is saved in this browser when storage is available. It does not sync between devices. Clearing browser data or using private browsing can remove it. No account is required.</p><p><a href="/the-last-letter/">Start The Last Letter →</a></p>'''),
    '/privacy/':('Privacy & Saved Progress | LinguaNovels','How this version of LinguaNovels handles local progress, audio playback, hosting and advertising.','''<h1>Privacy &amp; saved progress</h1><p>This page describes the V230 website package, dated 19 October 2026.</p><h2>Progress on your device</h2><p>When you submit a quiz, the site stores your selected answers, the submission date and the content version in your browser’s local storage. It also remembers the last listening part you opened so you can return to it. This data is not sent to a LinguaNovels server and is not shared between devices.</p><h2>No account or tracking scripts</h2><p>This version has no registration, contact form, third-party analytics or active advertising scripts. It does not set application cookies. It uses local storage for progress and the last opened part.</p><h2>Audio and hosting</h2><p>The MP3 files were generated in advance. Playing an audio file does not send your text or answers to Google’s speech-generation service. When deployed on Cloudflare Pages, page and audio requests pass through Cloudflare, which may process connection information such as IP addresses and request logs under its own policies.</p><h2>Future advertising</h2><p>Advertising is not active in this version. Before adding advertising or analytics, the privacy information and any required consent controls must be updated.</p><h2>Clear your progress</h2><p>This removes only the LinguaNovels data stored by this website in this browser.</p><button class="button secondary" id="clear-progress" type="button">Clear my saved progress</button><p id="clear-status" role="status"></p><noscript><p>With JavaScript disabled, use your browser’s site-data settings to clear local storage.</p></noscript>''')}
    for path,(title,desc,content) in pages.items():write_page(path,title,desc,crumbs([('Home','/'),(title.split(' |')[0],None)])+'<article class="prose">'+content+'</article>')

def main():
    assert len(UNITS)==135 and sum(len(u['questions']) for u in UNITS)==810
    for u in UNITS:
        assert len(u['questions'])==6 and len({q['id'] for q in u['questions']})==6
        for q in u['questions']:
            assert len(q['options'])==3 and sum(o['id']==q['correctOptionId'] for o in q['options'])==1
        assert hashlib.sha256((DIST/u['audio']['src'].lstrip('/')).read_bytes()).hexdigest()==u['audio']['sha256']
    build_home();build_indexes()
    for u in UNITS:build_unit(u)
    build_info()
    write_page('/404/','Page Not Found | LinguaNovels','Return to LinguaNovels and continue your English listening story.','<article class="prose"><p class="eyebrow">Page not found</p><h1>This clue leads nowhere.</h1><p>The page may have moved. Return to the story to continue.</p>'+button('Back to the story','/the-last-letter/')+'</article>')
    (DIST/'404.html').write_bytes((DIST/'404/index.html').read_bytes());(DIST/'404/index.html').unlink();(DIST/'404').rmdir();PAGES.remove('/404/')
    sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{p}</loc></url>' for p in PAGES)+'</urlset>'
    (DIST/'sitemap.xml').write_text(sitemap)
    (DIST/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
    (DIST/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n/assets/audio/*\n  Cache-Control: public, max-age=31536000, immutable\n')
    (DIST/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#153d36"/><path d="M15 15h8v32h26v7H15z" fill="#f3ecdc"/><path d="m30 16 19 11-19 11z" fill="#d5ac76"/></svg>')
    print(f'Built {len(PAGES)} indexable pages + 404; 135 MP3; 810 questions. Canonical base: {BASE}')

if __name__=='__main__':main()
