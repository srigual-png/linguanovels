export const keyFor = unit => `linguanovels:progress:1:${unit.id}`;
export function grade(unit,answers) {
  if (!answers || Object.keys(answers).length!==unit.questions.length || unit.questions.some(q=>!q.options.some(o=>o.id===answers[q.id]))) throw new Error('Answer all six questions before submitting.');
  const feedback=unit.questions.map(q=>({id:q.id,correct:answers[q.id]===q.correctOptionId,correctOptionId:q.correctOptionId,explanation:q.explanation}));
  const score=feedback.filter(f=>f.correct).length;
  return {score,total:feedback.length,percentage:Math.round(100*score/feedback.length),feedback,transcriptUnlocked:true};
}
export function saveProgress(unit,answers,storage) {
  const result=grade(unit,answers);
  const progress={unitId:unit.id,contentHash:unit.contentHash,answers:{...answers},submittedAt:new Date().toISOString()};
  let persisted=false;try{storage.setItem(keyFor(unit),JSON.stringify(progress));persisted=true;}catch{}
  return {...result,persisted};
}
export function restoreProgress(unit,storage) {
  try {
    const p=JSON.parse(storage.getItem(keyFor(unit))||'null');
    if(!p || p.unitId!==unit.id || p.contentHash!==unit.contentHash || typeof p.submittedAt!=='string')return null;
    return {...p,...grade(unit,p.answers)};
  } catch {return null;}
}
