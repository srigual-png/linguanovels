import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {grade,saveProgress,restoreProgress,keyFor} from '../dist/assets/learning.mjs';
const master=JSON.parse(readFileSync(new URL('../content/master_V230.json',import.meta.url),'utf8'));
let tested=0;
for(const u of master.units){
 const answers=Object.fromEntries(u.questions.map(q=>[q.id,q.correctOptionId]));
 const wrong=Object.fromEntries(u.questions.map(q=>[q.id,q.options.find(o=>o.id!==q.correctOptionId).id]));
 assert.equal(grade(u,answers).score,6);assert.equal(grade(u,wrong).score,0);
 assert.equal(grade(u,answers).transcriptUnlocked,true);
 assert.throws(()=>grade(u,{}));assert.throws(()=>grade(u,{...answers,extra:'A'}));
 assert.throws(()=>grade(u,{...answers,[u.questions[0].id]:'invalid'}));
 const values=new Map();const store={setItem:(k,v)=>values.set(k,v),getItem:k=>values.get(k)};
 assert.equal(restoreProgress(u,store),null);
 assert.equal(saveProgress(u,answers,store).persisted,true);
 assert.equal(restoreProgress(u,store).score,6);
 assert.equal(restoreProgress({...u,contentHash:'changed'},store),null);
 values.set(keyFor(u),'invalid JSON');assert.equal(restoreProgress(u,store),null);
 const blocked={getItem:()=>{throw Error('blocked')},setItem:()=>{throw Error('blocked')}};
 assert.equal(saveProgress(u,answers,blocked).persisted,false);
 assert.equal(restoreProgress(u,blocked),null);
 for(const q of u.questions){
  for(const o of q.options){const r=grade(u,{...answers,[q.id]:o.id});assert.equal(r.score,o.id===q.correctOptionId?6:5);}
  tested++;
 }
}
console.log(JSON.stringify({units:master.units.length,questions:tested,allCorrectAndWrong:true,allIndividualOptions:true,incompleteAndInvalidAnswersRejected:true,progressRestoreAndRevisionGuard:true,blockedStorageHandled:true}));
