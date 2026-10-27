import assert from 'node:assert/strict';
import {connectTranscriptPlayer} from '../dist/assets/transcript-player.mjs';
class Control extends EventTarget {
 constructor(){super();this.value='0';this.attrs={};}
 setAttribute(k,v){this.attrs[k]=v;}
}
class Audio extends EventTarget {
 constructor(){super();this.paused=true;this.ended=false;this.currentTime=0;this.duration=NaN;}
 async play(){if(this.fail)throw Error('offline');this.paused=false;this.dispatchEvent(new Event('play'));}
 pause(){this.paused=true;this.dispatchEvent(new Event('pause'));}
}
const controls=Object.fromEntries(['play','seek','time','audio-status'].map(k=>['#transcript-'+k,new Control()]));
const audio=new Audio();connectTranscriptPlayer(audio,{querySelector:s=>controls[s]});
const play=controls['#transcript-play'], seek=controls['#transcript-seek'];
assert.equal(seek.disabled,true);
audio.duration=110;audio.dispatchEvent(new Event('loadedmetadata'));
assert.equal(seek.max,'110');assert.equal(seek.disabled,false);
await audio.play();assert.equal(play.textContent,'Pause');
audio.currentTime=31;audio.dispatchEvent(new Event('timeupdate'));assert.equal(seek.value,'31');
play.dispatchEvent(new Event('click'));assert.equal(audio.paused,true);assert.equal(audio.currentTime,31);
play.dispatchEvent(new Event('click'));await Promise.resolve();assert.equal(audio.paused,false);assert.equal(audio.currentTime,31);
audio.pause();seek.value='62';seek.dispatchEvent(new Event('input'));assert.equal(audio.currentTime,62);assert.equal(audio.paused,true);
audio.currentTime=89;audio.dispatchEvent(new Event('seeked'));assert.equal(seek.value,'89');assert.equal(controls['#transcript-time'].textContent,'1:29 / 1:50');
audio.ended=true;audio.dispatchEvent(new Event('ended'));assert.equal(play.textContent,'Play');
audio.fail=true;play.dispatchEvent(new Event('click'));await Promise.resolve();assert.match(controls['#transcript-audio-status'].textContent,/Unable/);
console.log('Shared audio: play/pause/resume, seek both directions, metadata, ended and playback errors passed.');
