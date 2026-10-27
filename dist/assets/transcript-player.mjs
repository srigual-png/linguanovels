// Both interfaces operate on the original HTMLAudioElement; no second media source.
export function connectTranscriptPlayer(audio, player) {
 const play=player.querySelector('#transcript-play');
 const seek=player.querySelector('#transcript-seek');
 const time=player.querySelector('#transcript-time');
 const status=player.querySelector('#transcript-audio-status');
 const format=value=>{
  const seconds=Math.max(0,Math.floor(Number.isFinite(value)?value:0));
  return `${Math.floor(seconds/60)}:${String(seconds%60).padStart(2,'0')}`;
 };
 const sync=()=>{
  const duration=Number.isFinite(audio.duration)?audio.duration:0;
  const playing=!audio.paused&&!audio.ended;
  play.textContent=playing?'Pause':'Play';
  play.setAttribute('aria-label',playing?'Pause narration':'Play narration');
  seek.max=String(duration);
  seek.disabled=duration<=0;
  seek.value=String(audio.currentTime||0);
  seek.setAttribute('aria-valuetext',`${format(audio.currentTime)} of ${format(duration)}`);
  time.textContent=`${format(audio.currentTime)} / ${format(duration)}`;
 };
 play.addEventListener('click',async()=>{
  if(!audio.paused&&!audio.ended){audio.pause();return;}
  status.textContent='';
  try{await audio.play();}catch{status.textContent='Unable to play audio. Try again or check your connection.';}
  sync();
 });
 seek.addEventListener('input',()=>{
  if(Number.isFinite(audio.duration)&&audio.duration>0){
   audio.currentTime=Math.min(audio.duration,Math.max(0,Number(seek.value)));
   sync();
  }
 });
 for(const event of ['play','playing','pause','ended','timeupdate','durationchange','loadedmetadata','seeking','seeked','emptied'])audio.addEventListener(event,sync);
 audio.addEventListener('error',()=>{status.textContent='The audio could not be loaded. Check your connection, then reload this page.';sync();});
 sync();
}
