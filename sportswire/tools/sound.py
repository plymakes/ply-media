#!/usr/bin/env python3
"""Original soundtrack for every SportsWire Reel. Every Reel has sound (Geoffry, 21 Oct 2026).

    python3 tools/sound.py out.wav --dur 10.6 --cuts 2.2,5.8,8.6 --seed my-slug [--mood drive|bright|calm]

Synthesised from scratch (drums, bass, chords, arpeggio, whooshes and impacts timed to the
slide changes), so there are no copyright or licensing questions and nothing to download.
The seed (use the post slug) picks tempo, key and progression, so Reels don't all sound
the same, and the same Reel always gets the same track.
Also importable: make(path, dur, cuts, seed, mood).
"""
from __future__ import annotations

import argparse
import hashlib

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100
MOODS = {
    # bpm choices, chord progressions as semitone offsets from the root (minor-key loops)
    'drive': {'bpm': [122, 124, 126, 128], 'prog': [[0, 8, 3, 10], [0, 5, 8, 7], [0, 10, 8, 7]], 'arp': 1.0, 'hat': 1.0},
    'bright': {'bpm': [118, 120, 124], 'prog': [[0, 7, 9, 5], [0, 5, 9, 7]], 'arp': 1.0, 'hat': 0.9},   # major-ish lift for wins and spotlights
    'calm': {'bpm': [96, 100, 104], 'prog': [[0, 8, 3, 10], [0, 5, 3, 7]], 'arp': 0.5, 'hat': 0.5},      # explainers, tables
}
ROOTS = [41.20, 43.65, 46.25, 49.00, 51.91, 55.00]  # E1, F1, F#1, G1, G#1, A1


def _rng(seed: str) -> np.random.Generator:
    return np.random.default_rng(int(hashlib.sha256(seed.encode()).hexdigest()[:12], 16))


def _bp(x, lo, hi, order=2):
    b, a = butter(order, [lo / (SR / 2), min(hi, SR / 2 - 100) / (SR / 2)], btype='band')
    return lfilter(b, a, x)


def _hp(x, f, order=2):
    b, a = butter(order, f / (SR / 2), btype='high')
    return lfilter(b, a, x)


def _lp(x, f, order=2):
    b, a = butter(order, f / (SR / 2), btype='low')
    return lfilter(b, a, x)


def _saw(freq, n, detune=0.0, phase=0.0):
    t = np.arange(n) / SR
    return 2 * ((t * freq * (1 + detune) + phase) % 1.0) - 1


def _add(buf, sig, start, gain=1.0):
    i = int(start * SR)
    if i >= len(buf) or i + len(sig) <= 0:
        return
    j = min(len(buf), i + len(sig))
    s0 = max(0, -i)
    buf[max(i, 0):j] += gain * sig[s0:s0 + (j - max(i, 0))]


def _kick(r):
    n = int(0.38 * SR); t = np.arange(n) / SR
    f = 46 + 120 * np.exp(-t * 32)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8.5)
    body += 0.25 * np.sin(2 * 2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)  # 2nd harmonic so phones hear the kick
    click = r.standard_normal(n) * np.exp(-t * 400) * 0.25
    return np.tanh(1.6 * (body + click))


def _snare(r):
    n = int(0.26 * SR); t = np.arange(n) / SR
    noise = _bp(r.standard_normal(n), 1200, 7000) * np.exp(-t * 17)
    tone = np.sin(2 * np.pi * 195 * t) * np.exp(-t * 28) * 0.5
    clap = sum(_bp(r.standard_normal(n), 900, 4000) * np.exp(-np.clip(t - d, 0, None) * 60) * (t >= d) for d in (0, 0.011, 0.023)) * 0.6
    return noise + tone + clap


def _hat(r, open_=False):
    n = int((0.22 if open_ else 0.06) * SR); t = np.arange(n) / SR
    return _hp(r.standard_normal(n), 7500) * np.exp(-t * (14 if open_ else 70))


def _whoosh(r, length=0.5):
    n = int(length * SR); t = np.arange(n) / SR
    noise = r.standard_normal(n)
    out = np.zeros(n); y = 0.0
    cut = 300 * (20 ** (t / length))  # rising filter 300 Hz -> 6 kHz
    a = np.exp(-2 * np.pi * cut / SR)
    for k in range(n):  # one-pole sweep
        y = (1 - a[k]) * noise[k] + a[k] * y
        out[k] = y
    return out * (t / length) ** 2 * 1.8


def _impact(r):
    n = int(0.9 * SR); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (38 + 40 * np.exp(-t * 10)) * t) * np.exp(-t * 4.5)
    crack = _bp(r.standard_normal(n), 400, 9000) * np.exp(-t * 22) * 0.5
    return boom + crack


def make(path: str, dur: float, cuts: list[float], seed: str, mood: str = 'drive') -> dict:
    r = _rng(seed)
    m = MOODS.get(mood, MOODS['drive'])
    bpm = float(r.choice(m['bpm'])); beat = 60.0 / bpm
    prog = m['prog'][int(r.integers(len(m['prog'])))]
    root = float(r.choice(ROOTS))
    n = int((dur + 1.0) * SR)
    drums, bass, pad, arp, fx = (np.zeros(n) for _ in range(5))
    padR = np.zeros(n)
    kick, snare = _kick(r), _snare(r)
    beats = int(dur / beat) + 2
    duck = np.ones(n)
    for b in range(beats):
        t0 = b * beat
        bar, pos = divmod(b, 4)
        _add(drums, kick, t0, 0.95)                                         # four on the floor
        k0 = int(t0 * SR); L = int(0.25 * SR)
        if k0 < n:
            seg = 1 - 0.65 * np.exp(-np.arange(min(L, n - k0)) / SR * 14)  # sidechain
            duck[k0:k0 + len(seg)] = np.minimum(duck[k0:k0 + len(seg)], seg)
        if pos in (1, 3):
            _add(drums, snare, t0, 0.5)
        for h in range(2):                                                  # 8th hats, open on the off-beat of 4
            _add(drums, _hat(r, open_=(pos == 3 and h == 1)), t0 + h * beat / 2, 0.16 * m['hat'])
        semis = prog[bar % len(prog)]
        f_b = root * 2 ** (semis / 12)
        for e in range(2):                                                  # 8th-note bass pluck
            L = int(beat / 2 * SR); t = np.arange(L) / SR
            note = _lp(_saw(f_b * 2, L) + 0.6 * np.sin(2 * np.pi * f_b * t) + 0.35 * _saw(f_b * 4, L, 0.003), 1500) * np.exp(-t * 7)
            _add(bass, note, t0 + e * beat / 2, 0.42)
        if pos == 0:                                                        # pad chord per bar
            L = int(4 * beat * SR); t = np.arange(L) / SR
            env = np.minimum(1, t / 0.25) * np.minimum(1, (4 * beat - t) / 0.3)
            third = 3 if mood != 'bright' else 4
            chord = sum(_saw(f_b * 4 * 2 ** (iv / 12), L, d) for iv in (0, third, 7, 12) for d in (-0.004, 0.004)) / 8
            sig = _lp(chord, 1600) * env
            _add(pad, sig, t0, 0.32)
            _add(padR, _lp(sum(_saw(f_b * 4 * 2 ** (iv / 12), L, d, 0.3) for iv in (0, third, 7, 12) for d in (-0.006, 0.006)) / 8, 1600) * env, t0, 0.32)
            if bar % 2 == 1 and m['arp'] > 0:                               # arpeggio every other bar
                tones = [0, third, 7, 12, 7, third, 12, 15]
                for s in range(16):
                    L2 = int(beat / 4 * SR); t2 = np.arange(L2) / SR
                    f = f_b * 8 * 2 ** (tones[s % len(tones)] / 12)
                    _add(arp, _lp(np.sign(np.sin(2 * np.pi * f * t2)), 2500) * np.exp(-t2 * 18), t0 + s * beat / 4, 0.12 * m['arp'])
    _add(fx, _impact(r), 0.0, 0.55)                                         # hit on the hook
    for c in cuts:
        _add(fx, _whoosh(r, 0.45), c - 0.45, 0.22)
        _add(fx, _impact(r), c, 0.38)
    music = drums + (bass + arp) * duck
    left = music + pad * duck + fx
    right = music + padR * duck + fx
    st = np.stack([left, right], axis=1)[: int(dur * SR)]
    st = _hp(st.T, 28).T
    fade = int(0.6 * SR)
    st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    st[: int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR))[:, None]
    rms = np.sqrt(np.mean(st ** 2)) + 1e-9
    st = np.tanh(st * (0.22 / rms) * 1.1) * 0.93                             # loud but clean
    wavfile.write(path, SR, (st * 32767).astype(np.int16))
    return {'bpm': bpm, 'root_hz': root, 'progression': prog, 'mood': mood}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--dur', type=float, required=True)
    ap.add_argument('--cuts', default='')
    ap.add_argument('--seed', default='sportswire')
    ap.add_argument('--mood', default='drive', choices=sorted(MOODS))
    a = ap.parse_args()
    cuts = [float(x) for x in a.cuts.split(',') if x]
    print(make(a.out, a.dur, cuts, a.seed, a.mood))
