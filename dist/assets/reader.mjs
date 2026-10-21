import {initChapterPlayer} from './chapter-player.mjs';
import {saveProgress,restoreProgress} from './learning.mjs';
const dataElement=document.getElementById('unit-data');
const storage={getItem:key=>localStorage.getItem(key),setItem:(key,value)=>localStorage.setItem(key,value)};
if(dataElement){
 const unit=JSON.parse(dataElement.textContent),form=document.getElementById('questions'),result=document.getElementById('result'),transcript=document.getElementById('transcript'),audio=document.getElementById('audio');
 // On the final part, make the newly restored chapter player easy to find.
 if (unit.part === 3) {
  const nav = document.querySelector('.page-nav');
  if (nav) {
   const whole = document.createElement('a');
   whole.href = '/the-last-letter/' + unit.level.toLowerCase() + '/chapter-' + unit.chapter + '/';
   whole.textContent = '🎧 Listen to the full chapter →';
   nav.append(whole);
  }
 }
 const showResult=r=>{
  result.textContent=`You scored ${r.score} out of ${r.total} (${r.percentage}%). ${r.score===r.total?'Well done!':'Read the explanations, listen again and try once more.'}`+(r.persisted===false?' Progress could not be saved in this browser.':'');
  transcript.dataset.locked='false';document.getElementById('transcript-lock').hidden=true;
  for(const [i,q] of unit.questions.entries()){
   const field=form.querySelector(`[data-question="${q.id}"]`),f=r.feedback[i];
   for(const label of field.querySelectorAll('.answer')){
    const input=label.querySelector('input');label.classList.toggle('correct',input.value===f.correctOptionId);label.classList.toggle('incorrect',input.checked&&!f.correct);
   }
   field.querySelector('.question-feedback').textContent=`${f.correct?'Correct.':'Not quite.'} ${q.options.find(o=>o.id===q.correctOptionId).text}. ${f.explanation}`;
  }
  document.getElementById('retry').hidden=false;
 };
 const old=restoreProgress(unit,storage);
 if(old){for(const input of form.querySelectorAll('input')) input.checked=input.value===old.answers[input.name];showResult(old);}
 form.addEventListener('submit',event=>{event.preventDefault();try{showResult(saveProgress(unit,Object.fromEntries(new FormData(form)),storage));result.focus();}catch(error){result.textContent=error.message;}});
 document.getElementById('retry').addEventListener('click',()=>{
  form.reset();result.textContent='';for(const label of form.querySelectorAll('.answer'))label.classList.remove('correct','incorrect');for(const p of form.querySelectorAll('.question-feedback'))p.textContent='';form.querySelector('input').focus();
 });
 document.getElementById('speed').addEventListener('change',event=>{audio.playbackRate=Number(event.target.value);});
 audio.addEventListener('error',()=>{document.getElementById('audio-status').textContent='The audio could not be loaded. Check your connection, then reload this page.';});
 try{localStorage.setItem('linguanovels:last-unit',JSON.stringify({id:unit.id,url:location.pathname,title:`Chapter ${unit.chapter} · Part ${unit.part} · ${unit.level}`}));}catch{}
}
const clear=document.getElementById('clear-progress');
if(clear)clear.addEventListener('click',()=>{
 if(!confirm('Clear all LinguaNovels progress saved in this browser?'))return;
 try{for(const key of Object.keys(localStorage))if(key.startsWith('linguanovels:'))localStorage.removeItem(key);document.getElementById('clear-status').textContent='Your saved LinguaNovels progress has been cleared.';}catch{document.getElementById('clear-status').textContent='Your browser did not allow progress to be cleared.';}
});
for(const element of document.querySelectorAll('[data-progress-units]')){
 const units=JSON.parse(element.dataset.progressUnits);let completed=0;
 for(const u of units){const p=restoreProgress(u,storage);if(p){completed++;const marker=document.querySelector(`[data-completed="${u.id}"]`);if(marker)marker.textContent='Completed';}}
 element.textContent=`${completed} of ${units.length} parts completed in this browser`;
 const bar=document.getElementById('progress-fill');if(bar)bar.style.width=`${completed/units.length*100}%`;
}
const resume=document.getElementById('resume');
if(resume){try{const p=JSON.parse(localStorage.getItem('linguanovels:last-unit')||'null');if(p&&/^\/the-last-letter\/(b1|b2|c1)\/chapter-([1-9]|1[0-5])\/part-[1-3]\/$/.test(p.url)){resume.href=p.url;resume.textContent='Continue: '+p.title;resume.hidden=false;}}catch{}}

initChapterPlayer({restoreProgress,storage});
