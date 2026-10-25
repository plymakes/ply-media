#!/usr/bin/env python3
"""Ply sound: original music + sound effects for Reels, baked into the MP4 (21 Oct 2026).

Why: Metricool can't attach Instagram's licensed music without a Facebook Page, and Ply has none, so every Reel
carries its own original audio. The music is composed here (MIDI -> FluidSynth with the MIT-licensed FluidR3 GM
soundfont), so it's ours to use. One family of calm, warm lo-fi beds (electric piano, warm pad, finger bass,
soft brushes) gives Ply a recognisable sound; small effects land on the cuts (a marimba "pop" when a card appears,
a soft swoosh on transitions, a chime on the end card, drips for Loom, a ting for Pleat, layer ticks for printing).

Needs: apt-get install fluidsynth fluid-soundfont-gm ; pip install pretty_midi
Usage:  python3 tools/ply_sound.py <reel-name> [...] [--keep-natural]   (names from REELS below, or "all";
        --keep-natural mixes the clip's own sound, e.g. the printer or the tray click, over the music: use it for real footage)
        -> reels/<file>-sound.mp4 next to the silent original, then run tools/ply_check_reel.py on it.
To add a new Reel: add an entry to REELS with its file, preset and cue times (seconds, from its animation code).
"""
import math, random, subprocess, sys, tempfile, wave
from pathlib import Path
import numpy as np
import pretty_midi as pm

ROOT = Path(__file__).resolve().parent.parent
SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
SR = 48000

# chord = (root midi note, intervals); voiced around C4..C5
PRESETS = {
    'warm':   dict(bpm=86, chords=[(65, [0, 4, 7, 11]), (64, [0, 3, 7, 10]), (62, [0, 3, 7, 10]), (60, [0, 4, 7, 11])], accent=12),   # Fmaj7 Em7 Dm7 Cmaj7, marimba
    'morning': dict(bpm=84, chords=[(60, [0, 4, 7, 11]), (57, [0, 3, 7, 10]), (65, [0, 4, 7, 11]), (67, [0, 4, 7, 9])], accent=11),   # Cmaj7 Am7 Fmaj7 G6, vibraphone
    'linen':  dict(bpm=88, chords=[(62, [0, 4, 7, 11]), (59, [0, 3, 7, 10]), (67, [0, 4, 7, 11]), (69, [0, 4, 7, 9])], accent=108),  # Dmaj7 Bm7 Gmaj7 A6, kalimba
    'clay':   dict(bpm=82, chords=[(63, [0, 4, 7, 11]), (60, [0, 3, 7, 10]), (68, [0, 4, 7, 11]), (70, [0, 4, 7, 9])], accent=8),    # Ebmaj7 Cm7 Abmaj7 Bb6, celesta
}

# name -> (source file, preset, duration s, cues [(t, kind)], loop?)
REELS = {
    'ep1':     ('reels/ply-reel-14-building-ply-ep1.mp4', 'warm', 11.0, [(1.4, 'pop'), (3.0, 'pop'), (3.45, 'pop'), (3.9, 'pop'), (4.35, 'pop'), (5.2, 'soft'), (8.0, 'swoosh'), (8.4, 'chime')], False),
    'zoomq':   ('reels/ply-reel-15-zoom-quilt.mp4', 'morning', 8.0, [(0.9, 'riser:4.7'), (5.4, 'chime')], True),
    'ten':     ('reels/ply-reel-16-ply-in-10-seconds.mp4', 'linen', 11.0, [(1.1, 'pop'), (2.4, 'pop'), (3.7, 'pop'), (5.0, 'pop'), (6.4, 'tick'), (6.55, 'tick'), (6.7, 'tick'), (6.85, 'tick'), (8.8, 'chime')], False),
    'three':   ('reels/ply-reel-17-three-things.mp4', 'clay', 12.0, [(1.2, 'pop'), (3.8, 'pop'), (6.4, 'pop'), (9.6, 'soft')], False),
    'ep2':     ('reels/ply-reel-18-building-ply-ep2.mp4', 'warm', 11.0, [(1.6, 'pop'), (2.8, 'swoosh'), (5.4, 'swoosh'), (8.0, 'swoosh'), (8.4, 'chime')], False),
    'loom':    ('reels/ply-reel-19-loom-puddle.mp4', 'linen', 10.0, [(1.4, 'swoosh'), (2.3, 'drip'), (2.75, 'drip'), (3.3, 'drip'), (5.2, 'soft'), (7.8, 'chime')], False),
    'pleat':   ('reels/ply-reel-20-pleat-rings.mp4', 'clay', 10.0, [(1.4, 'swoosh'), (2.0, 'ting'), (4.6, 'swoosh'), (5.1, 'soft'), (7.8, 'chime')], False),
    'zoomt':   ('reels/ply-reel-21-zoom-tile.mp4', 'linen', 8.0, [(0.9, 'riser:4.7'), (5.4, 'chime')], True),
    'ep3':     ('reels/ply-reel-22-building-ply-ep3.mp4', 'warm', 11.0, [(1.4, 'pop'), (2.0, 'swoosh'), (3.2, 'soft'), (8.0, 'swoosh'), (8.4, 'chime')], False),
    # reels made on 17-19 Oct
    'layers':  ('reels/ply-reel-09-hundreds-of-layers-v3.mp4', 'morning', 11.0, [(1.2, 'layers:5.0'), (6.6, 'soft'), (8.2, 'chime')], False),
    'quiltile': ('reels/ply-reel-10-quilt-or-tile-v3.mp4', 'warm', 10.5, [(1.0, 'swoosh'), (1.6, 'swoosh'), (2.3, 'pop'), (2.6, 'pop'), (3.6, 'tick'), (4.5, 'tick'), (5.4, 'tick'), (6.3, 'tick'), (7.4, 'chime')], False),
    'colours': ('reels/ply-reel-11-four-colours-v3.mp4', 'clay', 11.5, [(0.9, 'pop'), (2.05, 'pop'), (3.2, 'pop'), (4.35, 'pop'), (5.8, 'tick'), (5.95, 'tick'), (6.1, 'tick'), (6.25, 'tick'), (8.8, 'chime')], False),
    'tray':    ('reels/ply-reel-12-hidden-tray-v3.mp4', 'linen', 12.0, [(1.0, 'swoosh'), (2.2, 'pop'), (3.6, 'pop'), (5.0, 'drip'), (5.4, 'drip'), (8.6, 'chime')], False),
    'tiles':   ('reels/ply-reel-13-why-tiles-v3.mp4', 'morning', 11.5, [(1.0, 'cascade:2.1'), (3.6, 'swoosh'), (4.0, 'pop'), (5.0, 'soft'), (8.6, 'chime')], False),
    # weekly plan 25 Oct (tools/reels_growth_2026_10_25.py)
    'gift':    ('reels/ply-reel-23-friend-who-moved.mp4', 'clay', 11.0, [(3.3, 'pop'), (3.6, 'soft'), (5.3, 'pop'), (5.6, 'soft'), (7.9, 'swoosh'), (8.2, 'chime')], False),
    'howlong': ('reels/ply-reel-24-how-long.mp4', 'morning', 11.0, [(4.3, 'ting'), (5.6, 'pop'), (8.0, 'swoosh'), (8.4, 'chime')], False),
    'mint':    ('reels/ply-reel-25-mint-in-a-tin.mp4', 'linen', 11.0, [(2.4, 'soft'), (4.4, 'swoosh'), (4.7, 'pop'), (5.4, 'soft'), (8.0, 'swoosh'), (8.4, 'chime')], False),
    'ivch':    ('reels/ply-reel-26-ivory-or-charcoal.mp4', 'warm', 11.0, [(3.3, 'pop'), (3.5, 'pop'), (5.6, 'pop'), (5.8, 'pop'), (7.9, 'swoosh'), (8.3, 'chime')], False),
    'zoomp':   ('reels/ply-reel-27-zoom-pleat.mp4', 'morning', 8.0, [(0.9, 'riser:4.7'), (5.4, 'chime')], True),
}


def chord_at(preset, t):
    bar = 4 * 60 / preset['bpm']
    return preset['chords'][int(t // bar) % len(preset['chords'])]


def compose(name):
    src, pname, dur, cues, loop = REELS[name]
    p = PRESETS[pname]; rnd = random.Random(name)
    beat = 60 / p['bpm']; bars = math.ceil((dur + 1) / (4 * beat))
    midi = pm.PrettyMIDI(initial_tempo=p['bpm'])
    ep, pad, bass, acc = pm.Instrument(4), pm.Instrument(89), pm.Instrument(33), pm.Instrument(p['accent'])
    bell = pm.Instrument(9); wood = pm.Instrument(115); drums = pm.Instrument(0, is_drum=True)
    hum = lambda: rnd.uniform(-0.012, 0.012)
    def add(inst, pitch, start, length, vel):
        start = max(0.0, start)
        inst.notes.append(pm.Note(velocity=int(max(1, min(127, vel + rnd.randint(-5, 5)))), pitch=int(pitch), start=start, end=start + length))
    for b in range(bars):
        t0 = b * 4 * beat; root, iv = p['chords'][b % len(p['chords'])]
        for i in iv:                                   # electric piano: hit on 1, soft push on the "and" of 2
            add(ep, root + i, t0 + hum(), 3.4 * beat, 54)
            add(ep, root + i, t0 + 1.5 * beat + hum(), 1.2 * beat, 38)
        for i in iv[:3]:
            add(pad, root + i - 12, t0, 4 * beat, 34)  # warm pad underneath
        add(bass, root - 24, t0 + hum(), 1.6 * beat, 72)
        add(bass, root - 24 + 7, t0 + 2.5 * beat + hum(), 0.9 * beat, 60)
        for k in range(8):                             # brushed groove, light swing
            sw = 0.07 * beat if k % 2 else 0.0
            add(drums, 42, t0 + k * 0.5 * beat + sw + hum(), 0.1, 30 if k % 2 == 0 else 22)
        if b > 0 or dur < 9:
            add(drums, 36, t0 + hum(), 0.2, 52); add(drums, 36, t0 + 2.5 * beat + hum(), 0.2, 40)
        add(drums, 37, t0 + 1 * beat + hum(), 0.1, 40); add(drums, 37, t0 + 3 * beat + hum(), 0.1, 40)
    noise_events = []
    for t, kind in cues:
        root, iv = chord_at(p, t); tones = [root + i + 12 for i in iv]
        k, _, arg = kind.partition(':')
        if k == 'pop':
            add(acc, rnd.choice(tones), t, 0.6, 78)
        elif k == 'soft':
            add(acc, tones[0], t, 0.8, 54)
        elif k == 'tick':
            add(acc, tones[-1], t, 0.25, 48)
        elif k == 'chime':
            for j, n in enumerate([tones[0] + 12, tones[1] + 12, tones[2] + 12]):
                add(bell, n, t + j * 0.09, 1.6, 62)
        elif k == 'ting':
            add(bell, tones[1] + 12, t, 1.2, 70); add(bell, tones[2] + 12, t + 0.07, 1.2, 55)
        elif k == 'layers':                            # printer layer ticks, speeding up
            span = float(arg); x = 0.0; gap = 0.28
            while x < span:
                add(wood, 84, t + x, 0.05, 34 + int(14 * x / span)); x += gap; gap = max(0.07, gap * 0.93)
        elif k == 'cascade':                           # tiles landing, rising notes
            span = float(arg); n = 11
            for j in range(n):
                add(acc, tones[j % len(tones)] + 12 * min(1, j // len(tones)), t + j * span / n, 0.4, 50 + j * 2)
        elif k in ('swoosh', 'riser', 'drip'):
            noise_events.append((t, k, float(arg) if arg else None))
    for inst in (pad, ep, bass, drums, acc, bell, wood):
        if inst.notes:
            midi.instruments.append(inst)
    return midi, noise_events, dur, loop


def synth_fx(n_samples, events):
    out = np.zeros(n_samples); rng = np.random.default_rng(7)
    for t, kind, arg in events:
        i0 = int(t * SR)
        if kind in ('swoosh', 'riser'):
            d = 0.45 if kind == 'swoosh' else arg
            n = int(d * SR); x = rng.standard_normal(n)
            fc = np.geomspace(300, 4500, n) if kind == 'swoosh' else np.geomspace(120, 1600, n)
            y = np.zeros(n); s1 = s2 = 0.0
            for j in range(n):                         # two one-pole low-passes (12 dB/oct) with a sweeping cutoff
                a = 1 - math.exp(-2 * math.pi * fc[j] / SR); s1 += a * (x[j] - s1); s2 += a * (s1 - s2); y[j] = s2
            env = np.minimum(np.linspace(0, 1, n) / (0.7 if kind == 'swoosh' else 0.95), 1) * np.minimum(np.linspace(1, 0, n) / 0.3, 1)
            amp = 0.07 if kind == 'swoosh' else 0.035
            seg = y * env * amp / (np.abs(y).max() + 1e-9)
        else:                                          # drip: falling sine "plip"
            n = int(0.12 * SR); tt = np.arange(n) / SR
            f = 1900 * np.exp(-tt * 9); ph = 2 * np.pi * np.cumsum(f) / SR
            seg = np.sin(ph) * np.exp(-tt * 38) * 0.22
        i1 = min(n_samples, i0 + len(seg)); out[i0:i1] += seg[:i1 - i0]
    return out


def render(name, keep_natural=False):
    src, _, _, _, _ = REELS[name]
    midi, fx, dur, loop = compose(name)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td); mid, raw = td / 'm.mid', td / 'm.wav'
        midi.write(str(mid))
        subprocess.run(['fluidsynth', '-ni', '-q', '-g', '0.55', '-r', str(SR), '-F', str(raw), SF2, str(mid)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with wave.open(str(raw)) as w:
            ch = w.getnchannels(); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
        a = a.reshape(-1, ch)
        n = int((dur + 0.1) * SR)
        if len(a) < n: a = np.vstack([a, np.zeros((n - len(a), ch))])
        a = a[:n]; f = synth_fx(n, fx)
        a = a + f[:, None]
        mix = td / 'mix.wav'
        with wave.open(str(mix), 'wb') as w:
            w.setnchannels(ch); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())
        fade_out = 0.25 if loop else 0.7
        af = (f'highpass=f=45,lowpass=f=11500,aecho=0.8:0.6:60:0.18,acompressor=threshold=-20dB:ratio=2.5:attack=15:release=250,'
              f'loudnorm=I=-15:TP=-1.5:LRA=7,afade=t=in:d=0.04,afade=t=out:st={dur - fade_out:.2f}:d={fade_out}')
        out = ROOT / src.replace('.mp4', '-sound.mp4').replace('-v3-sound', '-sound')
        if keep_natural:  # real clips: their own sound (printer hum, tray click) stays on top, music sits under it
            fc = f'[1:a]volume=0.55[m];[0:a]aresample=48000,volume=1.0[n];[m][n]amix=inputs=2:duration=first:normalize=0,{af}[a]'
            amap = ['-filter_complex', fc, '-map', '0:v:0', '-map', '[a]']
        else:
            amap = ['-map', '0:v:0', '-map', '1:a:0', '-af', af]
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(ROOT / src), '-i', str(mix), *amap,
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', f'{dur:.2f}',
                        '-movflags', '+faststart', '-map_metadata', '-1', str(out)], check=True)
        print(out.relative_to(ROOT))
        return out


if __name__ == '__main__':
    args = [x for x in sys.argv[1:] if not x.startswith('--')]; keep = '--keep-natural' in sys.argv
    for nm in (list(REELS) if args in ([], ['all']) else args):
        render(nm, keep)
